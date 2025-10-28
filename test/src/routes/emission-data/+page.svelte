<script>
	import { onMount } from 'svelte';
	import Navbar from '$lib/widgets/Navbar.svelte';
	import Sidebar from '$lib/widgets/Sidebar.svelte';
	import { 
		Calendar, 
		Filter, 
		TrendingUp, 
		TrendingDown, 
		BarChart3, 
		PieChart, 
		Download, 
		Search,
		ArrowUpRight,
		ArrowDownRight,
		Zap,
		Car,
		Factory,
		Home,
		Leaf,
		Bell,
		Settings,
		User,
		Menu,
		X
	} from 'lucide-svelte';

	let sidebarExpanded = false;
	
	function toggleSidebar() {
		sidebarExpanded = !sidebarExpanded;
	}
	let selectedPeriod = '7d';
	let selectedRegion = 'all';
	let selectedSource = 'all';

	// Sample emission data
	let summaryStats = {
		totalEmissions: 2847,
		averagePerDay: 95.6,
		changeFromLastWeek: -8.2
	};

	let emissionsOverTime = [
		{ date: '2024-10-01', value: 120 },
		{ date: '2024-10-02', value: 95 },
		{ date: '2024-10-03', value: 110 },
		{ date: '2024-10-04', value: 85 },
		{ date: '2024-10-05', value: 102 },
		{ date: '2024-10-06', value: 78 },
		{ date: '2024-10-07', value: 92 },
		{ date: '2024-10-08', value: 88 }
	];

	let categoryBreakdown = [
		{ category: 'Transport', value: 1248, color: '#10B981', icon: Car },
		{ category: 'Energy', value: 856, color: '#F59E0B', icon: Zap },
		{ category: 'Industry', value: 485, color: '#EF4444', icon: Factory },
		{ category: 'Residential', value: 258, color: '#8B5CF6', icon: Home }
	];

	let emissionRecords = [
		{ id: 1, date: '2024-10-08', source: 'Vehicle Fuel', category: 'Transport', value: 25.4, unit: 'kg CO2' },
		{ id: 2, date: '2024-10-08', source: 'Electricity', category: 'Energy', value: 18.2, unit: 'kg CO2' },
		{ id: 3, date: '2024-10-07', source: 'Manufacturing', category: 'Industry', value: 45.1, unit: 'kg CO2' },
		{ id: 4, date: '2024-10-07', source: 'Heating', category: 'Residential', value: 12.8, unit: 'kg CO2' },
		{ id: 5, date: '2024-10-06', source: 'Fleet Vehicle', category: 'Transport', value: 32.7, unit: 'kg CO2' }
	];

	let sortColumn = 'date';
	let sortDirection = 'desc';

	function sortData(column) {
		if (sortColumn === column) {
			sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
		} else {
			sortColumn = column;
			sortDirection = 'asc';
		}

		emissionRecords = [...emissionRecords].sort((a, b) => {
			let aVal = a[column];
			let bVal = b[column];

			if (column === 'value') {
				aVal = parseFloat(aVal);
				bVal = parseFloat(bVal);
			}

			if (sortDirection === 'asc') {
				return aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
			} else {
				return aVal > bVal ? -1 : aVal < bVal ? 1 : 0;
			}
		});
	}
</script>

<svelte:head>
	<title>Emission Data - CarbonTrack</title>
</svelte:head>

<div class="min-h-screen bg-gray-50">
	<!-- Top Navigation -->
	<Navbar {toggleSidebar} />

	<!-- Sidebar -->
	<Sidebar {sidebarExpanded} currentPage="emission-data" />

	<!-- Main Content -->
	<div class="lg:ml-64 pt-16">
		<div class="p-6 space-y-6">
			<!-- Header Section -->
			<div class="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
				<div>
					<h1 class="text-3xl font-bold text-gray-900 mb-2">Emission Data</h1>
					<p class="text-gray-600">Track and analyze your carbon footprint across all sources</p>
				</div>
				
				<!-- Filters -->
				<div class="flex flex-wrap items-center gap-4">
					<div class="flex items-center space-x-2">
						<Calendar class="w-5 h-5 text-gray-500" />
						<select bind:value={selectedPeriod} class="bg-white border border-gray-300 text-gray-900 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500">
							<option value="7d">Last 7 days</option>
							<option value="30d">Last 30 days</option>
							<option value="90d">Last 90 days</option>
							<option value="1y">Last year</option>
						</select>
					</div>
					
					<div class="flex items-center space-x-2">
						<Filter class="w-5 h-5 text-gray-500" />
						<select bind:value={selectedRegion} class="bg-white border border-gray-300 text-gray-900 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500">
							<option value="all">All Regions</option>
							<option value="north">North America</option>
							<option value="europe">Europe</option>
							<option value="asia">Asia Pacific</option>
						</select>
					</div>
					
					<select bind:value={selectedSource} class="bg-white border border-gray-300 text-gray-900 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500">
						<option value="all">All Sources</option>
						<option value="transport">Transport</option>
						<option value="energy">Energy</option>
						<option value="industry">Industry</option>
						<option value="residential">Residential</option>
					</select>
				</div>
			</div>

			<!-- Summary Cards -->
			<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
				<div class="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-md transition-all">
					<div class="flex items-center justify-between">
						<div>
							<p class="text-gray-500 text-sm">Total Emissions</p>
							<p class="text-3xl font-bold text-gray-900">{summaryStats.totalEmissions}</p>
							<p class="text-gray-500 text-sm">kg CO₂</p>
						</div>
						<div class="p-3 bg-green-50 rounded-lg">
							<TrendingUp class="w-8 h-8 text-green-600" />
						</div>
					</div>
				</div>

				<div class="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-md transition-all">
					<div class="flex items-center justify-between">
						<div>
							<p class="text-gray-500 text-sm">Average per Day</p>
							<p class="text-3xl font-bold text-gray-900">{summaryStats.averagePerDay}</p>
							<p class="text-gray-500 text-sm">kg CO₂/day</p>
						</div>
						<div class="p-3 bg-blue-50 rounded-lg">
							<BarChart3 class="w-8 h-8 text-blue-600" />
						</div>
					</div>
				</div>

				<div class="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-md transition-all">
					<div class="flex items-center justify-between">
						<div>
							<p class="text-gray-500 text-sm">Change from Last Week</p>
							<p class="text-3xl font-bold text-gray-900 flex items-center">
								{Math.abs(summaryStats.changeFromLastWeek)}%
								{#if summaryStats.changeFromLastWeek < 0}
									<ArrowDownRight class="w-6 h-6 text-green-500 ml-2" />
								{:else}
									<ArrowUpRight class="w-6 h-6 text-red-500 ml-2" />
								{/if}
							</p>
							<p class="text-gray-500 text-sm">
								{summaryStats.changeFromLastWeek < 0 ? 'Decrease' : 'Increase'}
			</p>
						</div>
						<div class="p-3 bg-{summaryStats.changeFromLastWeek < 0 ? 'green' : 'red'}-50 rounded-lg">
							{#if summaryStats.changeFromLastWeek < 0}
								<TrendingDown class="w-8 h-8 text-green-500" />
							{:else}
								<TrendingUp class="w-8 h-8 text-red-500" />
							{/if}
						</div>
					</div>
				</div>
			</div>

			<!-- Charts Section -->
			<div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
				<!-- Emissions Over Time Chart -->
				<div class="bg-white border border-gray-200 rounded-xl p-6">
					<div class="flex items-center justify-between mb-6">
						<h3 class="text-xl font-semibold text-gray-900">Emissions Over Time</h3>
						<button class="p-2 text-gray-500 hover:text-gray-700 transition-colors">
							<Download class="w-5 h-5" />
						</button>
					</div>
					
					<!-- Simple line chart representation -->
					<div class="h-64 flex items-end justify-between space-x-2">
						{#each emissionsOverTime as point, i}
							<div class="flex flex-col items-center space-y-2 flex-1">
								<div 
									class="w-full bg-gradient-to-t from-green-500 to-green-300 rounded-t-lg hover:from-green-400 hover:to-green-200 transition-all cursor-pointer"
									style="height: {(point.value / Math.max(...emissionsOverTime.map(p => p.value))) * 100}%"
								></div>
								<span class="text-xs text-gray-500 transform rotate-45 origin-left">
									{new Date(point.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
								</span>
							</div>
						{/each}
					</div>
				</div>

				<!-- Category Breakdown Chart -->
				<div class="bg-white border border-gray-200 rounded-xl p-6">
					<div class="flex items-center justify-between mb-6">
						<h3 class="text-xl font-semibold text-gray-900">Category Breakdown</h3>
						<PieChart class="w-5 h-5 text-gray-500" />
					</div>
					
					<div class="space-y-4">
						{#each categoryBreakdown as category}
							<div class="flex items-center justify-between">
								<div class="flex items-center space-x-3">
									<div class="p-2 rounded-lg" style="background-color: {category.color}20">
										<svelte:component this={category.icon} class="w-5 h-5" style="color: {category.color}" />
									</div>
									<span class="text-gray-900 font-medium">{category.category}</span>
								</div>
								<div class="text-right">
									<p class="text-gray-900 font-semibold">{category.value} kg</p>
									<div class="w-24 h-2 bg-gray-200 rounded-full mt-1">
										<div 
											class="h-full rounded-full transition-all duration-500"
											style="background-color: {category.color}; width: {(category.value / Math.max(...categoryBreakdown.map(c => c.value))) * 100}%"
										></div>
									</div>
								</div>
							</div>
						{/each}
					</div>
				</div>
			</div>

			<!-- Data Table -->
			<div class="bg-white border border-gray-200 rounded-xl overflow-hidden">
				<div class="p-6 border-b border-gray-200">
					<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
						<h3 class="text-xl font-semibold text-gray-900">Recent Emissions</h3>
						<div class="flex items-center space-x-4">
							<div class="relative">
								<Search class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
								<input 
									type="text" 
									placeholder="Search emissions..."
									class="bg-gray-50 border border-gray-300 text-gray-900 pl-10 pr-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
								/>
							</div>
							<button class="p-2 text-gray-500 hover:text-gray-700 transition-colors">
								<Download class="w-5 h-5" />
							</button>
						</div>
					</div>
				</div>

				<div class="overflow-x-auto">
					<table class="w-full">
						<thead class="bg-gray-50">
							<tr>
								<th class="px-6 py-4 text-left">
									<button on:click={() => sortData('date')} class="flex items-center space-x-1 text-gray-600 hover:text-gray-900 transition-colors">
										<span>Date</span>
										{#if sortColumn === 'date'}
											{#if sortDirection === 'asc'}
												<ArrowUpRight class="w-4 h-4" />
											{:else}
												<ArrowDownRight class="w-4 h-4" />
											{/if}
										{/if}
									</button>
								</th>
								<th class="px-6 py-4 text-left">
									<button on:click={() => sortData('source')} class="flex items-center space-x-1 text-gray-600 hover:text-gray-900 transition-colors">
										<span>Source</span>
										{#if sortColumn === 'source'}
											{#if sortDirection === 'asc'}
												<ArrowUpRight class="w-4 h-4" />
											{:else}
												<ArrowDownRight class="w-4 h-4" />
											{/if}
										{/if}
									</button>
								</th>
								<th class="px-6 py-4 text-left">
									<button on:click={() => sortData('category')} class="flex items-center space-x-1 text-gray-600 hover:text-gray-900 transition-colors">
										<span>Category</span>
										{#if sortColumn === 'category'}
											{#if sortDirection === 'asc'}
												<ArrowUpRight class="w-4 h-4" />
											{:else}
												<ArrowDownRight class="w-4 h-4" />
											{/if}
										{/if}
									</button>
								</th>
								<th class="px-6 py-4 text-right">
									<button on:click={() => sortData('value')} class="flex items-center justify-end space-x-1 text-gray-600 hover:text-gray-900 transition-colors">
										<span>Emissions</span>
										{#if sortColumn === 'value'}
											{#if sortDirection === 'asc'}
												<ArrowUpRight class="w-4 h-4" />
											{:else}
												<ArrowDownRight class="w-4 h-4" />
											{/if}
										{/if}
									</button>
								</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-gray-200">
							{#each emissionRecords as record}
								<tr class="hover:bg-gray-50 transition-colors">
									<td class="px-6 py-4 text-gray-600">
										{new Date(record.date).toLocaleDateString()}
									</td>
									<td class="px-6 py-4 text-gray-900 font-medium">
										{record.source}
									</td>
									<td class="px-6 py-4">
										<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-50 text-green-700 border border-green-200">
											{record.category}
										</span>
									</td>
									<td class="px-6 py-4 text-right text-gray-900 font-semibold">
										{record.value} {record.unit}
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>
		</div>
	</div>
</div>

<style>
	/* Custom scrollbar styling */
	:global(::-webkit-scrollbar) {
		width: 8px;
		height: 8px;
	}

	:global(::-webkit-scrollbar-track) {
		background: #f3f4f6;
		border-radius: 4px;
	}

	:global(::-webkit-scrollbar-thumb) {
		background: #d1d5db;
		border-radius: 4px;
	}

	:global(::-webkit-scrollbar-thumb:hover) {
		background: #9ca3af;
	}
</style>