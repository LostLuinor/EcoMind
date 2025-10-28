<script>
	import { goto } from '$app/navigation';
	import { Leaf, Eye, EyeOff, User, Mail, Building2, Shield, Sparkles } from 'lucide-svelte';

	let name = '';
	let email = '';
	let password = '';
	let confirmPassword = '';
	let userType = 'Individual'; // Default user type
	let organizationName = '';
	let errorMessage = '';
	let successMessage = '';
	let isLoading = false;
	let showPassword = false;
	let showConfirmPassword = false;

	async function handleSubmit() {
		// Validation
		if (!name || !email || !password || !confirmPassword) {
			errorMessage = 'Please fill in all required fields';
			return;
		}

		if (userType === 'Organization' && !organizationName) {
			errorMessage = 'Please enter your organization name';
			return;
		}

		if (password !== confirmPassword) {
			errorMessage = 'Passwords do not match';
			return;
		}

		if (password.length < 8) {
			errorMessage = 'Password must be at least 8 characters long';
			return;
		}

		// Email validation
		const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
		if (!emailRegex.test(email)) {
			errorMessage = 'Please enter a valid email address';
			return;
		}

		isLoading = true;
		errorMessage = '';
		successMessage = '';

		try {
			const response = await fetch('http://localhost:8000/api/register', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					name: name,
					email: email,
					password: password,
					userType: userType,
					organizationName: organizationName || null,
					role: 'user'
				})
			});

			const data = await response.json();

			if (data.success) {
				successMessage = 'Welcome to EcoMind! Redirecting to login...';
				// Clear form
				name = '';
				email = '';
				password = '';
				confirmPassword = '';
				userType = 'Individual';
				organizationName = '';
				
				// Redirect to login after 2 seconds
				setTimeout(() => {
					goto('/login');
				}, 2000);
			} else {
				errorMessage = data.message || 'Registration failed';
			}
		} catch (error) {
			console.error('Registration error:', error);
			errorMessage = 'Unable to connect to server. Please try again.';
		} finally {
			isLoading = false;
		}
	}

	function togglePasswordVisibility() {
		showPassword = !showPassword;
	}

	function toggleConfirmPasswordVisibility() {
		showConfirmPassword = !showConfirmPassword;
	}

	function goToOverview() {
		goto('/');
	}
</script>

<svelte:head>
	<title>Sign Up - EcoMind</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-white via-green-50 to-teal-50 relative overflow-hidden">
	<!-- Navigation Bar -->
	<nav class="relative z-20 w-full h-16 bg-white/80 backdrop-blur-md border-b border-gray-200/50 flex items-center justify-between px-6 lg:px-8 shadow-sm">
		<!-- Logo - Clickable to go home -->
		<button 
			on:click={goToOverview}
			class="flex items-center gap-3 hover:opacity-80 transition-opacity"
		>
			<div class="w-10 h-10 bg-gradient-to-br from-green-600 to-teal-600 rounded-xl flex items-center justify-center shadow-md">
				<Leaf class="w-6 h-6 text-white" />
			</div>
			<span class="text-xl font-bold bg-gradient-to-r from-green-700 to-teal-700 bg-clip-text text-transparent">EcoMind</span>
		</button>
		
		<!-- Right side placeholder for future nav items if needed -->
		<div></div>
	</nav>

	<!-- Floating Background Elements -->
	<div class="absolute inset-0 overflow-hidden pointer-events-none">
		<div class="absolute top-20 left-10 w-32 h-32 bg-green-100 rounded-full opacity-30 animate-pulse"></div>
		<div class="absolute top-40 right-20 w-20 h-20 bg-teal-100 rounded-full opacity-40 animate-pulse delay-1000"></div>
		<div class="absolute bottom-20 left-20 w-24 h-24 bg-green-200 rounded-full opacity-20 animate-pulse delay-2000"></div>
		<div class="absolute bottom-40 right-10 w-16 h-16 bg-teal-200 rounded-full opacity-30 animate-pulse delay-3000"></div>
	</div>

	<div class="relative z-10 grid grid-cols-1 lg:grid-cols-2" style="min-height: calc(100vh - 4rem);">
		<!-- Left Side - Illustration -->
		<div class="hidden lg:flex flex-col justify-center items-center p-12 bg-gradient-to-br from-green-100 to-teal-100">
			<div class="max-w-md text-center space-y-6">
				<!-- Logo -->
				<div class="flex items-center justify-center gap-3 mb-8">
					<div class="w-12 h-12 bg-gradient-to-br from-green-600 to-teal-600 rounded-2xl flex items-center justify-center shadow-lg">
						<Leaf class="w-7 h-7 text-white" />
					</div>
					<span class="text-2xl font-bold bg-gradient-to-r from-green-700 to-teal-700 bg-clip-text text-transparent">EcoMind</span>
				</div>

				<!-- Illustration Area -->
				<div class="relative">
					<div class="w-80 h-80 bg-gradient-to-br from-green-200 to-teal-200 rounded-full flex items-center justify-center shadow-2xl">
						<div class="w-64 h-64 bg-white rounded-full flex items-center justify-center shadow-inner">
							<div class="text-center space-y-4">
								<Sparkles class="w-16 h-16 text-green-600 mx-auto animate-pulse" />
								<div class="space-y-2">
									<div class="w-12 h-2 bg-green-300 rounded mx-auto"></div>
									<div class="w-16 h-2 bg-teal-300 rounded mx-auto"></div>
									<div class="w-10 h-2 bg-green-400 rounded mx-auto"></div>
								</div>
							</div>
						</div>
					</div>
				</div>

				<div class="space-y-3">
					<h2 class="text-2xl font-bold text-green-800">Join the Green Revolution</h2>
					<p class="text-green-700 leading-relaxed">
						Empower your sustainability journey with AI-driven insights and make every action count towards a greener future.
					</p>
				</div>
			</div>
		</div>

		<!-- Right Side - Sign Up Form -->
		<div class="flex flex-col justify-center items-center p-8 lg:p-12">

			<div class="w-full max-w-md">
				<div class="text-center mb-8">
					<h1 class="text-3xl font-bold text-gray-900 mb-3">Create Your Account</h1>
					<p class="text-gray-600">Start your sustainable future today</p>
				</div>

				<form on:submit|preventDefault={handleSubmit} class="space-y-5">
					{#if errorMessage}
						<div class="bg-red-50 border-l-4 border-red-400 text-red-700 px-4 py-3 rounded-r-lg text-sm">
							<div class="flex">
								<div class="ml-3">
									<p>{errorMessage}</p>
								</div>
							</div>
						</div>
					{/if}

					{#if successMessage}
						<div class="bg-green-50 border-l-4 border-green-400 text-green-700 px-4 py-3 rounded-r-lg text-sm">
							<div class="flex">
								<div class="ml-3">
									<p>{successMessage}</p>
								</div>
							</div>
						</div>
					{/if}
					
					<!-- Full Name Field -->
					<div>
						<label for="name" class="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
							<User class="w-4 h-4 text-green-600" />
							Full Name
						</label>
						<input 
							type="text" 
							id="name" 
							bind:value={name} 
							placeholder="Enter your full name"
							required
							disabled={isLoading}
							class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-200 disabled:bg-gray-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md"
						/>
					</div>

					<!-- Email Field -->
					<div>
						<label for="email" class="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
							<Mail class="w-4 h-4 text-teal-600" />
							Email Address
						</label>
						<input 
							type="email" 
							id="email" 
							bind:value={email} 
							placeholder="Enter your email address"
							required
							disabled={isLoading}
							class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-200 disabled:bg-gray-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md"
						/>
					</div>

					<!-- User Type Field -->
					<div>
						<label for="userType" class="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
							<Shield class="w-4 h-4 text-green-600" />
							Account Type
						</label>
						<select 
							id="userType" 
							bind:value={userType}
							disabled={isLoading}
							class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-200 disabled:bg-gray-50 disabled:cursor-not-allowed appearance-none bg-white shadow-sm hover:shadow-md"
						>
							<option value="Individual">Individual</option>
							<option value="Organization">Organization</option>
							<option value="Community">Community</option>
						</select>
					</div>

					<!-- Organization Name Field (Conditional) -->
					{#if userType === 'Organization'}
						<div class="animate-fadeIn">
							<label for="organizationName" class="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
								<Building2 class="w-4 h-4 text-teal-600" />
								Organization Name
							</label>
							<input 
								type="text" 
								id="organizationName" 
								bind:value={organizationName} 
								placeholder="Enter your organization name"
								required
								disabled={isLoading}
								class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-200 disabled:bg-gray-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md"
							/>
						</div>
					{/if}
					
					<!-- Password Field -->
					<div>
						<label for="password" class="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
							<Shield class="w-4 h-4 text-green-600" />
							Password
						</label>
						<div class="relative">
							<input 
								type={showPassword ? "text" : "password"}
								id="password" 
								bind:value={password} 
								placeholder="Create a strong password (min 8 characters)"
								required
								disabled={isLoading}
								class="w-full px-4 py-3 pr-12 border border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-200 disabled:bg-gray-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md"
							/>
							<button
								type="button"
								on:click={togglePasswordVisibility}
								class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-green-600 transition-colors"
								disabled={isLoading}
							>
								{#if showPassword}
									<EyeOff class="w-5 h-5" />
								{:else}
									<Eye class="w-5 h-5" />
								{/if}
							</button>
						</div>
					</div>

					<!-- Confirm Password Field -->
					<div>
						<label for="confirmPassword" class="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
							<Shield class="w-4 h-4 text-teal-600" />
							Confirm Password
						</label>
						<div class="relative">
							<input 
								type={showConfirmPassword ? "text" : "password"}
								id="confirmPassword" 
								bind:value={confirmPassword} 
								placeholder="Confirm your password"
								required
								disabled={isLoading}
								class="w-full px-4 py-3 pr-12 border border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-200 disabled:bg-gray-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md"
							/>
							<button
								type="button"
								on:click={toggleConfirmPasswordVisibility}
								class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-green-600 transition-colors"
								disabled={isLoading}
							>
								{#if showConfirmPassword}
									<EyeOff class="w-5 h-5" />
								{:else}
									<Eye class="w-5 h-5" />
								{/if}
							</button>
						</div>
					</div>
					
					<button 
						type="submit" 
						disabled={isLoading}
						class="w-full bg-gradient-to-r from-green-600 to-teal-600 text-white py-3.5 px-6 rounded-xl font-semibold hover:from-green-700 hover:to-teal-700 focus:ring-4 focus:ring-green-200 transition-all duration-200 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
					>
						{#if isLoading}
							<div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
							Creating Account...
						{:else}
							<Sparkles class="w-5 h-5" />
							Create Account
						{/if}
					</button>
				</form>

				<div class="mt-8 text-center">
					<p class="text-gray-600">
						Already have an account? 
						<a href="/login" class="text-green-600 hover:text-teal-600 font-semibold hover:underline transition-colors">
							Login here
						</a>
					</p>
				</div>
			</div>
		</div>
	</div>
</div>


<style>
	@keyframes fadeIn {
		from { opacity: 0; transform: translateY(10px); }
		to { opacity: 1; transform: translateY(0); }
	}
	
	.animate-fadeIn {
		animation: fadeIn 0.3s ease-out;
	}
</style>