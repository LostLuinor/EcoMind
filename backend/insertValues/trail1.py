# uvicorn main:app --reload --host 0.0.0.0 --port 8000
from fastapi import FastAPI, Query, HTTPException, Request
import mysql.connector
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List, Optional
from pydantic import BaseModel
from datetime import date
import hashlib

load_dotenv()

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or set to your frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class LoginRequest(BaseModel):
    username: str  # Can be email or name
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    user_data: Optional[dict] = None

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = "user"
    org_id: Optional[int] = None

class RegisterResponse(BaseModel):
    success: bool
    message: str
    user_id: Optional[int] = None

# Database connection
def get_connection():
    # Check if all required environment variables are set
    required_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),  # Default to 3306 if not set
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
    except mysql.connector.Error as err:
        raise Exception(f"Failed to connect to database: {err}")

# Helper function to hash password with SHA-256
def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

# Login endpoint
@app.post("/api/login", response_model=LoginResponse)
def login(login_data: LoginRequest):
    """
    Authenticate user with username/email and password
    """
    try:
        # Establish database connection
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Hash the provided password
        hashed_password = hash_password(login_data.password)
        
        # Query to find user by email or name and verify password
        query = """
        SELECT user_id, name, email, org_id, 
               created_at, role, status 
        FROM Users 
        WHERE (email = %s OR name = %s) AND password_hash = %s
        """
        cursor.execute(query, (login_data.username, login_data.username, hashed_password))
        
        # Fetch user data
        user = cursor.fetchone()
        
        # Close connections
        cursor.close()
        connection.close()
        
        if user:
            # Login successful
            return LoginResponse(
                success=True,
                message="Login successful",
                user_data={
                    "user_id": user["user_id"],
                    "name": user["name"],
                    "email": user["email"],
                    "org_id": user["org_id"],
                    "created_at": str(user["created_at"]),
                    "role": user["role"],
                    "status": user["status"]
                }
            )
        else:
            # Login failed
            return LoginResponse(
                success=False,
                message="Invalid username or password"
            )
        
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

# Registration endpoint
@app.post("/api/register", response_model=RegisterResponse)
def register(register_data: RegisterRequest):
    """
    Register a new user in the database
    """
    try:
        # Establish database connection
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if email already exists
        check_query = "SELECT email FROM Users WHERE email = %s"
        cursor.execute(check_query, (register_data.email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            cursor.close()
            connection.close()
            return RegisterResponse(
                success=False,
                message="Email already registered"
            )
        
        # Hash the password
        hashed_password = hash_password(register_data.password)
        
        # Insert new user
        insert_query = """
        INSERT INTO Users (name, email, password_hash, role, org_id, status, created_at)
        VALUES (%s, %s, %s, %s, %s, 'pending', CURRENT_TIMESTAMP)
        """
        cursor.execute(insert_query, (
            register_data.name,
            register_data.email,
            hashed_password,
            register_data.role,
            register_data.org_id
        ))
        
        # Get the inserted user ID
        user_id = cursor.lastrowid
        
        # Commit the transaction
        connection.commit()
        
        # Close connections
        cursor.close()
        connection.close()
        
        return RegisterResponse(
            success=True,
            message="User registered successfully",
            user_id=user_id
        )
        
    except mysql.connector.Error as err:
        # Rollback in case of error
        if connection:
            connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as e:
        # Rollback in case of error
        if connection:
            connection.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


# Admin endpoints

class UserStatusUpdate(BaseModel):
    user_id: int
    status: str  # 'approved', 'rejected', 'pending'

class UserRoleUpdate(BaseModel):
    user_id: int
    role: str  # 'admin', 'user'

@app.get("/api/admin/users")
def get_all_users(admin_id: int = Query(...)):
    """
    Get all users from the same organization (admin only)
    """
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Verify admin role and get admin's org_id
        cursor.execute("SELECT role, org_id FROM Users WHERE user_id = %s", (admin_id,))
        admin = cursor.fetchone()
        
        if not admin or admin['role'] != 'admin':
            raise HTTPException(status_code=403, detail="Access denied. Admin privileges required.")
        
        admin_org_id = admin['org_id']
        
        # Get users from the same organization only
        # If admin has no org (org_id is NULL), show only users with NULL org_id
        if admin_org_id is None:
            query = """
            SELECT u.user_id, u.name, u.email, u.role, u.status, u.created_at, 
                   o.name as org_name, u.org_id
            FROM Users u
            LEFT JOIN Organizations o ON u.org_id = o.org_id
            WHERE u.org_id IS NULL
            ORDER BY u.created_at DESC
            """
            cursor.execute(query)
        else:
            query = """
            SELECT u.user_id, u.name, u.email, u.role, u.status, u.created_at, 
                   o.name as org_name, u.org_id
            FROM Users u
            LEFT JOIN Organizations o ON u.org_id = o.org_id
            WHERE u.org_id = %s
            ORDER BY u.created_at DESC
            """
            cursor.execute(query, (admin_org_id,))
        
        users = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        # Convert datetime to string
        for user in users:
            if user['created_at']:
                user['created_at'] = str(user['created_at'])
        
        return {"success": True, "users": users}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@app.put("/api/admin/users/status")
def update_user_status(status_data: UserStatusUpdate, admin_id: int = Query(...)):
    """
    Update user status (admin only, same organization)
    """
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Verify admin role and get admin's org_id
        cursor.execute("SELECT role, org_id FROM Users WHERE user_id = %s", (admin_id,))
        admin = cursor.fetchone()
        
        if not admin or admin['role'] != 'admin':
            raise HTTPException(status_code=403, detail="Access denied. Admin privileges required.")
        
        admin_org_id = admin['org_id']
        
        # Verify target user is in the same organization
        cursor.execute("SELECT org_id FROM Users WHERE user_id = %s", (status_data.user_id,))
        target_user = cursor.fetchone()
        
        if not target_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if both users are in the same org (including both being NULL)
        if admin_org_id != target_user['org_id']:
            raise HTTPException(status_code=403, detail="Access denied. Can only manage users from your organization.")
        
        # Update user status
        update_query = "UPDATE Users SET status = %s WHERE user_id = %s"
        cursor.execute(update_query, (status_data.status, status_data.user_id))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return {"success": True, "message": "User status updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        if connection:
            connection.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@app.put("/api/admin/users/role")
def update_user_role(role_data: UserRoleUpdate, admin_id: int = Query(...)):
    """
    Update user role (admin only, same organization)
    """
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Verify admin role and get admin's org_id
        cursor.execute("SELECT role, org_id FROM Users WHERE user_id = %s", (admin_id,))
        admin = cursor.fetchone()
        
        if not admin or admin['role'] != 'admin':
            raise HTTPException(status_code=403, detail="Access denied. Admin privileges required.")
        
        admin_org_id = admin['org_id']
        
        # Verify target user is in the same organization
        cursor.execute("SELECT org_id FROM Users WHERE user_id = %s", (role_data.user_id,))
        target_user = cursor.fetchone()
        
        if not target_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if both users are in the same org (including both being NULL)
        if admin_org_id != target_user['org_id']:
            raise HTTPException(status_code=403, detail="Access denied. Can only manage users from your organization.")
        
        # Update user role
        update_query = "UPDATE Users SET role = %s WHERE user_id = %s"
        cursor.execute(update_query, (role_data.role, role_data.user_id))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return {"success": True, "message": "User role updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        if connection:
            connection.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@app.delete("/api/admin/users/{user_id}")
def delete_user(user_id: int, admin_id: int = Query(...)):
    """
    Delete user (admin only, same organization)
    """
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Verify admin role and get admin's org_id
        cursor.execute("SELECT role, org_id FROM Users WHERE user_id = %s", (admin_id,))
        admin = cursor.fetchone()
        
        if not admin or admin['role'] != 'admin':
            raise HTTPException(status_code=403, detail="Access denied. Admin privileges required.")
        
        # Prevent admin from deleting themselves
        if user_id == admin_id:
            raise HTTPException(status_code=400, detail="Cannot delete your own account")
        
        admin_org_id = admin['org_id']
        
        # Verify target user is in the same organization
        cursor.execute("SELECT org_id FROM Users WHERE user_id = %s", (user_id,))
        target_user = cursor.fetchone()
        
        if not target_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if both users are in the same org (including both being NULL)
        if admin_org_id != target_user['org_id']:
            raise HTTPException(status_code=403, detail="Access denied. Can only manage users from your organization.")
        
        # Delete user
        delete_query = "DELETE FROM Users WHERE user_id = %s"
        cursor.execute(delete_query, (user_id,))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return {"success": True, "message": "User deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        if connection:
            connection.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")




