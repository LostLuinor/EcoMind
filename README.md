# EcoMind

EcoMind is a full-stack web application designed to track, analyze, and visualize carbon emissions for organizations. It helps users monitor sustainability metrics, gain AI-driven insights, and make data-driven decisions to reduce their environmental impact.

## Features

- **User Authentication:** Secure login and signup for organizations and individuals.
- **Carbon Emission Tracking:** Record, view, and analyze emission data.
- **AI Insights:** Get recommendations for reducing emissions using AI models.
- **Audit Logs:** Track changes and activities for compliance.
- **Sustainability Dashboard:** Visualize key metrics and progress.
- **Admin Panel:** Manage users, organizations, and data.

## Tech Stack

- **Frontend:** SvelteKit, Tailwind CSS
- **Backend:** FastAPI (Python), MySQL
- **AI/ML:** Python (for insights and recommendations)
- **Database:** MySQL

## Project Structure

```
MiniProject/
├── backend/           # FastAPI backend, database models, API endpoints
│   ├── main.py        # Main FastAPI app
│   ├── .env           # Environment variables for DB connection
│   └── ...
├── test/              # SvelteKit frontend
│   ├── src/           # Frontend source code
│   ├── package.json   # Frontend dependencies
│   └── ...
```