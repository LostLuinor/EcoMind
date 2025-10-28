<script>
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { user, setUser } from '../../stores';
	import Navbar from '$lib/widgets/Navbar.svelte';
	import Sidebar from '$lib/widgets/Sidebar.svelte';
	import { 
		Leaf, 
		Bell, 
		Settings, 
		User,
		Moon,
		Sun,
		BarChart3,
		TrendingUp,
		Zap,
		Recycle,
		Factory,
		Home as HomeIcon,
		Car,
		Plane,
		Lightbulb,
		Target,
		Award,
		ChevronRight,
		Download,
		Filter,
		RefreshCw
	} from 'lucide-svelte';

	let sidebarExpanded = false;
	let darkMode = false;
	let lastUpdated = "2 minutes ago";
	let currentUser = null;

	// Sample data for dashboard
	let totalEmissions = 2847;
	let emissionReduction = 12;
	let energyUsage = 1456;
	let offsetAchieved = 340;

	let emissionsData = [
		{ month: 'Jan', emissions: 2200 },
		{ month: 'Feb', emissions: 2400 },
		{ month: 'Mar', emissions: 2100 },
		{ month: 'Apr', emissions: 2600 },
		{ month: 'May', emissions: 2300 },
		{ month: 'Jun', emissions: 2847 }
	];

	let aiInsights = [
		{ text: "Transport emissions expected to increase by 4% next week.", type: "warning" },
		{ text: "Switching to renewable energy could reduce your footprint by 18%.", type: "suggestion" },
		{ text: "Your energy efficiency improved by 8% this month.", type: "success" }
	];

	let recommendations = [
		{ title: "Install Smart Plugs", impact: "Medium", co2Saved: "45 kg", icon: "plug" },
		{ title: "Switch to Carpooling", impact: "High", co2Saved: "120 kg", icon: "car" },
		{ title: "Use LED Lighting", impact: "Low", co2Saved: "25 kg", icon: "bulb" }
	];

	let leaderboard = [
		{ name: "EcoTech Corp", reduction: 28, badge: "🥇" },
		{ name: "Green Solutions", reduction: 24, badge: "🥈" },
		{ name: "You (CarbonTrack User)", reduction: 12, badge: "🥉" },
		{ name: "Sustainable Inc", reduction: 8, badge: "" },
	];

	onMount(() => {
		// Check if user is logged in
		const userData = sessionStorage.getItem('user');
		if (userData) {
			try {
				const parsedUser = JSON.parse(userData);
				setUser(parsedUser);
				currentUser = parsedUser;
			} catch (e) {
				console.error('Failed to parse user data:', e);
				goto('/');
			}
		} else {
			// Redirect to login if no user data
			goto('/');
		}
	});

	function toggleSidebar() {
		sidebarExpanded = !sidebarExpanded;
	}

	function toggleDarkMode() {
		darkMode = !darkMode;
	}
</script>

<svelte:head>
	<title>Dashboard - CarbonTrack</title>
</svelte:head>

<div class="min-h-screen bg-gray-50 {darkMode ? 'dark' : ''}">
	<!-- Top Navigation Bar -->
	<Navbar {toggleSidebar} />

	<!-- Layout Container -->
	<div class="flex pt-16">
		<!-- Left Sidebar -->
		<Sidebar {sidebarExpanded} currentPage="dashboard" />

		<!-- Main Content -->
		<main class="flex-1 ml-16 lg:ml-64 p-6 space-y-6">
			<!-- Header Info Cards -->
			<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
				<!-- Total Emissions Card -->
				<div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
					<div class="flex items-center justify-between mb-4">
						<div class="p-2 bg-red-100 rounded-lg">
							<Factory class="w-6 h-6 text-red-600" />
						</div>
					</div>
					<div class="space-y-1">
						<p class="text-2xl font-bold text-gray-900">{totalEmissions.toLocaleString()}</p>
						<p class="text-sm text-gray-500">Total Emissions (kg CO₂)</p>
						<p class="text-xs text-red-600">vs. last month +8%</p>
					</div>
				</div>

				<!-- Emission Reduction Card -->
				<div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
					<div class="flex items-center justify-between mb-4">
						<div class="p-2 bg-green-100 rounded-lg">
							<TrendingUp class="w-6 h-6 text-green-600" />
						</div>
					</div>
					<div class="space-y-1">
						<p class="text-2xl font-bold text-gray-900">{emissionReduction}%</p>
						<p class="text-sm text-gray-500">Emission Reduction This Month</p>
						<p class="text-xs text-green-600">vs. last month +4%</p>
					</div>
				</div>

				<!-- Energy Usage Card -->
				<div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
					<div class="flex items-center justify-between mb-4">
						<div class="p-2 bg-yellow-100 rounded-lg">
							<Zap class="w-6 h-6 text-yellow-600" />
						</div>
					</div>
					<div class="space-y-1">
						<p class="text-2xl font-bold text-gray-900">{energyUsage.toLocaleString()}</p>
						<p class="text-sm text-gray-500">Energy Usage (kWh)</p>
						<p class="text-xs text-yellow-600">vs. last month -2%</p>
					</div>
				</div>

				<!-- Offset Achieved Card -->
				<div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
					<div class="flex items-center justify-between mb-4">
						<div class="p-2 bg-teal-100 rounded-lg">
							<Recycle class="w-6 h-6 text-teal-600" />
						</div>
					</div>
					<div class="space-y-1">
						<p class="text-2xl font-bold text-gray-900">{offsetAchieved}</p>
						<p class="text-sm text-gray-500">Offset Achieved (kg CO₂)</p>
						<p class="text-xs text-teal-600">vs. last month +15%</p>
					</div>
				</div>
			</div>

			<!-- Main Analytics Section -->
			<div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
				<!-- Emissions Chart -->
				<div class="xl:col-span-2 bg-white rounded-xl p-6 shadow-sm border border-gray-100">
					<div class="flex items-center justify-between mb-6">
						<h3 class="text-lg font-semibold text-gray-900">Emissions Over Time</h3>
						<div class="flex items-center gap-2">
							<button class="px-3 py-1 text-sm bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors">
								<Filter class="w-4 h-4 inline mr-1" />
								Daily
							</button>
							<button class="px-3 py-1 text-sm text-gray-600 rounded-lg hover:bg-gray-100 transition-colors">Weekly</button>
							<button class="px-3 py-1 text-sm text-gray-600 rounded-lg hover:bg-gray-100 transition-colors">Monthly</button>
						</div>
					</div>
					
					<!-- Simple Chart Visualization -->
					<div class="h-64 flex items-end justify-between gap-2 mb-4">
						{#each emissionsData as data, i}
							<div class="flex-1 flex flex-col items-center gap-2">
								<div class="bg-green-500 rounded-t w-full transition-all duration-500 hover:bg-green-600" 
									 style="height: {(data.emissions / 3000) * 100}%"></div>
								<span class="text-xs text-gray-500">{data.month}</span>
							</div>
						{/each}
					</div>
					
					<div class="flex items-center justify-between text-sm text-gray-500">
						<span>0 kg</span>
						<span>3000 kg</span>
					</div>
				</div>

				<!-- AI Insights Panel -->
				<div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
					<h3 class="text-lg font-semibold text-gray-900 mb-4">AI Insights</h3>
					<div class="space-y-4">
						{#each aiInsights as insight}
							<div class="p-4 rounded-lg {insight.type === 'warning' ? 'bg-orange-50 border border-orange-200' : insight.type === 'success' ? 'bg-green-50 border border-green-200' : 'bg-blue-50 border border-blue-200'}">
								<p class="text-sm {insight.type === 'warning' ? 'text-orange-800' : insight.type === 'success' ? 'text-green-800' : 'text-blue-800'}">{insight.text}</p>
							</div>
						{/each}
					</div>
				</div>
			</div>

			<!-- Bottom Section -->
			<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
				<!-- Emission Breakdown -->
				<div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
					<h3 class="text-lg font-semibold text-gray-900 mb-4">Emission Breakdown</h3>
					<div class="space-y-4">
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-3">
								<div class="w-3 h-3 bg-red-500 rounded-full"></div>
								<span class="text-sm text-gray-600">Scope 1 (Direct)</span>
							</div>
							<span class="text-sm font-medium">45%</span>
						</div>
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-3">
								<div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
								<span class="text-sm text-gray-600">Scope 2 (Electricity)</span>
							</div>
							<span class="text-sm font-medium">35%</span>
						</div>
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-3">
								<div class="w-3 h-3 bg-green-500 rounded-full"></div>
								<span class="text-sm text-gray-600">Scope 3 (Indirect)</span>
							</div>
							<span class="text-sm font-medium">20%</span>
						</div>
					</div>
				</div>

				<!-- Recommendations -->
				<div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
					<h3 class="text-lg font-semibold text-gray-900 mb-4">Recommendations</h3>
					<div class="space-y-3">
						{#each recommendations as rec}
							<div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
								<div class="flex-1">
									<p class="text-sm font-medium text-gray-900">{rec.title}</p>
									<p class="text-xs text-gray-500">Impact: {rec.impact} • Saves {rec.co2Saved}</p>
								</div>
								<ChevronRight class="w-4 h-4 text-gray-400" />
							</div>
						{/each}
					</div>
				</div>

				<!-- Leaderboard -->
				<div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
					<h3 class="text-lg font-semibold text-gray-900 mb-4">Community Leaderboard</h3>
					<div class="space-y-3">
						{#each leaderboard as user, i}
							<div class="flex items-center justify-between {i === 2 ? 'bg-green-50 rounded-lg p-2' : ''}">
								<div class="flex items-center gap-3">
									<span class="text-lg">{user.badge || `${i + 1}.`}</span>
									<div>
										<p class="text-sm font-medium text-gray-900">{user.name}</p>
										<p class="text-xs text-gray-500">{user.reduction}% reduction</p>
									</div>
								</div>
							</div>
						{/each}
					</div>
				</div>
			</div>

			<!-- Export Actions -->
			<div class="flex items-center justify-between bg-white rounded-xl p-4 shadow-sm border border-gray-100">
				<p class="text-sm text-gray-600">Export your sustainability data</p>
				<div class="flex items-center gap-2">
					<button class="px-4 py-2 text-sm bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors">
						<Download class="w-4 h-4 inline mr-1" />
						CSV
					</button>
					<button class="px-4 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
						<Download class="w-4 h-4 inline mr-1" />
						PDF Report
					</button>
				</div>
			</div>
		</main>
	</div>
</div>