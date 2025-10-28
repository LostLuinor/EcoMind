<script>
	import { onMount } from 'svelte';
	import Navbar from '$lib/widgets/Navbar.svelte';
	import Sidebar from '$lib/widgets/Sidebar.svelte';
	import { 
		Brain,
		TrendingUp,
		TrendingDown,
		Zap,
		AlertTriangle,
		Target,
		Sparkles,
		BarChart3,
		Activity,
		Bot,
		RefreshCw,
		ArrowRight,
		Calendar,
		MapPin,
		Car,
		Home,
		Factory,
		Lightbulb,
		CheckCircle,
		Clock,
		ArrowUp,
		ArrowDown
	} from 'lucide-svelte';

	let sidebarExpanded = false;
	let isGeneratingInsight = false;
	
	function toggleSidebar() {
		sidebarExpanded = !sidebarExpanded;
	}

	// AI Insights data
	let keyPredictions = {
		nextMonthEmissions: { value: 2650, change: -8.2, trend: 'down' },
		aiConfidence: 94,
		topRiskSources: ['Transportation', 'Heating', 'Manufacturing']
	};

	let trendData = [
		{ month: 'Jan', actual: 2840, predicted: 2845 },
		{ month: 'Feb', actual: 2720, predicted: 2715 },
		{ month: 'Mar', actual: 2890, predicted: 2885 },
		{ month: 'Apr', actual: 2650, predicted: 2660 },
		{ month: 'May', actual: 2780, predicted: 2775 },
		{ month: 'Jun', actual: 2590, predicted: 2580 },
		{ month: 'Jul', actual: null, predicted: 2520 },
		{ month: 'Aug', actual: null, predicted: 2480 },
		{ month: 'Sep', actual: null, predicted: 2440 }
	];

	let aiInsights = [
		{
			id: 1,
			type: 'prediction',
			icon: TrendingUp,
			title: 'Transportation Emissions Rising',
			message: 'Your transportation emissions are expected to rise by 8% next week. Consider route optimization or carpooling to reduce impact.',
			confidence: 89,
			timestamp: '2 minutes ago',
			severity: 'medium'
		},
		{
			id: 2,
			type: 'opportunity',
			icon: Lightbulb,
			title: 'Energy Optimization Detected',
			message: 'AI detected 15% energy waste during off-peak hours. Implementing smart scheduling could save 180 kg CO₂ monthly.',
			confidence: 96,
			timestamp: '5 minutes ago',
			severity: 'high'
		},
		{
			id: 3,
			type: 'alert',
			icon: AlertTriangle,
			title: 'Seasonal Pattern Alert',
			message: 'Historical data shows 25% increase in heating emissions during this period. Pre-emptive action recommended.',
			confidence: 92,
			timestamp: '12 minutes ago',
			severity: 'medium'
		},
		{
			id: 4,
			type: 'success',
			icon: CheckCircle,
			title: 'Goal Achievement Likely',
			message: 'Based on current trends, you\'re 87% likely to achieve your monthly reduction target of 2,500 kg CO₂.',
			confidence: 87,
			timestamp: '18 minutes ago',
			severity: 'low'
		}
	];

	function getSeverityColor(severity) {
		switch(severity) {
			case 'high': return 'border-l-red-500 bg-red-50';
			case 'medium': return 'border-l-yellow-500 bg-yellow-50';
			case 'low': return 'border-l-green-500 bg-green-50';
			default: return 'border-l-gray-500 bg-gray-50';
		}
	}

	function getIconColor(severity) {
		switch(severity) {
			case 'high': return 'text-red-600';
			case 'medium': return 'text-yellow-600';
			case 'low': return 'text-green-600';
			default: return 'text-gray-600';
		}
	}

	async function generateNewInsight() {
		isGeneratingInsight = true;
		
		// Simulate AI generation delay
		await new Promise(resolve => setTimeout(resolve, 2000));
		
		const newInsight = {
			id: aiInsights.length + 1,
			type: 'prediction',
			icon: Brain,
			title: 'AI Analysis Complete',
			message: 'New pattern identified: Weekend emissions are 23% lower. Consider extending remote work policies to reduce weekday office energy consumption.',
			confidence: 91,
			timestamp: 'Just now',
			severity: 'medium'
		};
		
		aiInsights = [newInsight, ...aiInsights];
		isGeneratingInsight = false;
	}

	onMount(() => {
		// Add subtle animations and real-time updates here
	});
</script>

<svelte:head>
	<title>AI Insights - CarbonTrack</title>
</svelte:head>

<div class="min-h-screen bg-gray-50">
	<!-- Top Navigation -->
	<Navbar {toggleSidebar} />

	<!-- Sidebar -->
	<Sidebar {sidebarExpanded} currentPage="ai-insights" />

	<!-- Main Content -->
	<div class="lg:ml-64 pt-16">
		<div class="p-6 space-y-8">
			<!-- Header Section with AI Glow Effect -->
			<div class="text-center mb-8">
				<div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-full mb-6 relative">
					<div class="absolute inset-0 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-full animate-pulse opacity-75"></div>
					<Brain class="w-10 h-10 text-white relative z-10" />
				</div>
				<h1 class="text-4xl font-bold text-gray-900 mb-4">AI Insights</h1>
				<p class="text-xl text-gray-600 max-w-2xl mx-auto">Predictive analytics for a cleaner tomorrow</p>
			</div>

			<!-- Key Predictions Summary -->
			<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
				<div class="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-all duration-300">
					<div class="flex items-center justify-between mb-4">
						<div class="p-3 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-lg">
							<Calendar class="w-6 h-6 text-white" />
						</div>
						<div class="flex items-center space-x-1 text-sm">
							{#if keyPredictions.nextMonthEmissions.trend === 'down'}
								<ArrowDown class="w-4 h-4 text-green-500" />
								<span class="text-green-600 font-medium">{Math.abs(keyPredictions.nextMonthEmissions.change)}%</span>
							{:else}
								<ArrowUp class="w-4 h-4 text-red-500" />
								<span class="text-red-600 font-medium">{Math.abs(keyPredictions.nextMonthEmissions.change)}%</span>
							{/if}
						</div>
					</div>
					<h3 class="text-lg font-semibold text-gray-900 mb-2">Next Month's Projection</h3>
					<p class="text-3xl font-bold text-gray-900 mb-1">{keyPredictions.nextMonthEmissions.value}</p>
					<p class="text-sm text-gray-500">kg CO₂ estimated</p>
				</div>

				<div class="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-all duration-300">
					<div class="flex items-center justify-between mb-4">
						<div class="p-3 bg-gradient-to-r from-green-500 to-teal-600 rounded-lg">
							<Target class="w-6 h-6 text-white" />
						</div>
						<div class="flex items-center space-x-1 text-sm">
							<Sparkles class="w-4 h-4 text-green-500" />
							<span class="text-green-600 font-medium">High</span>
						</div>
					</div>
					<h3 class="text-lg font-semibold text-gray-900 mb-2">AI Confidence Level</h3>
					<p class="text-3xl font-bold text-gray-900 mb-1">{keyPredictions.aiConfidence}%</p>
					<div class="w-full bg-gray-200 rounded-full h-2 mt-2">
						<div 
							class="bg-gradient-to-r from-green-500 to-teal-600 h-2 rounded-full transition-all duration-500"
							style="width: {keyPredictions.aiConfidence}%"
						></div>
					</div>
				</div>

				<div class="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-all duration-300">
					<div class="flex items-center justify-between mb-4">
						<div class="p-3 bg-gradient-to-r from-orange-500 to-red-600 rounded-lg">
							<AlertTriangle class="w-6 h-6 text-white" />
						</div>
					</div>
					<h3 class="text-lg font-semibold text-gray-900 mb-2">Top Risk Sources</h3>
					<div class="space-y-2">
						{#each keyPredictions.topRiskSources as source, i}
							<div class="flex items-center justify-between">
								<span class="text-gray-700">{i + 1}. {source}</span>
								<div class="w-2 h-2 bg-gradient-to-r from-orange-500 to-red-500 rounded-full"></div>
							</div>
						{/each}
					</div>
				</div>
			</div>

			<!-- Trend Visualization -->
			<div class="grid grid-cols-1 xl:grid-cols-2 gap-8">
				<!-- Predictions Chart -->
				<div class="bg-white border border-gray-200 rounded-xl p-6">
					<div class="flex items-center justify-between mb-6">
						<h3 class="text-xl font-semibold text-gray-900">Emission Trends & Predictions</h3>
						<div class="flex items-center space-x-2 text-sm text-gray-500">
							<Activity class="w-4 h-4" />
							<span>AI Powered</span>
						</div>
					</div>
					
					<!-- Chart Area -->
					<div class="h-64 flex items-end justify-between space-x-3">
						{#each trendData as point, i}
							<div class="flex flex-col items-center space-y-2 flex-1">
								<!-- Predicted Values -->
								{#if point.predicted}
									<div 
										class="w-full bg-gradient-to-t from-cyan-400 to-cyan-200 rounded-t-lg opacity-70 border-2 border-dashed border-cyan-400 hover:opacity-90 transition-all cursor-pointer"
										style="height: {(point.predicted / Math.max(...trendData.map(p => Math.max(p.actual || 0, p.predicted)))) * 80}%"
										title="Predicted: {point.predicted} kg CO₂"
									></div>
								{/if}
								
								<!-- Actual Values -->
								{#if point.actual}
									<div 
										class="w-full bg-gradient-to-t from-green-500 to-green-300 rounded-t-lg hover:from-green-400 hover:to-green-200 transition-all cursor-pointer -mt-2"
										style="height: {(point.actual / Math.max(...trendData.map(p => Math.max(p.actual || 0, p.predicted)))) * 80}%"
										title="Actual: {point.actual} kg CO₂"
									></div>
								{/if}
								
								<span class="text-xs text-gray-500 font-medium">{point.month}</span>
							</div>
						{/each}
					</div>
					
					<!-- Legend -->
					<div class="flex items-center justify-center space-x-6 mt-4 text-sm">
						<div class="flex items-center space-x-2">
							<div class="w-3 h-3 bg-green-500 rounded"></div>
							<span class="text-gray-600">Actual</span>
						</div>
						<div class="flex items-center space-x-2">
							<div class="w-3 h-3 bg-cyan-400 rounded border-2 border-dashed border-cyan-500"></div>
							<span class="text-gray-600">AI Predicted</span>
						</div>
					</div>
				</div>

				<!-- Generate New Insight Panel -->
				<div class="bg-white border border-gray-200 rounded-xl p-6">
					<div class="text-center">
						<div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-600 rounded-full mb-4">
							<Bot class="w-8 h-8 text-white" />
						</div>
						<h3 class="text-xl font-semibold text-gray-900 mb-2">AI Analysis Engine</h3>
						<p class="text-gray-600 mb-6">Let our AI discover new patterns and optimization opportunities in your emission data.</p>
						
						<button 
							on:click={generateNewInsight}
							disabled={isGeneratingInsight}
							class="bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition-all duration-300 flex items-center justify-center space-x-2 mx-auto shadow-lg hover:shadow-xl"
						>
							{#if isGeneratingInsight}
								<RefreshCw class="w-5 h-5 animate-spin" />
								<span>Analyzing Data...</span>
							{:else}
								<Sparkles class="w-5 h-5" />
								<span>Generate New Insight</span>
							{/if}
						</button>

						<!-- AI Stats -->
						<div class="grid grid-cols-2 gap-4 mt-8">
							<div class="text-center p-3 bg-gray-50 rounded-lg">
								<p class="text-2xl font-bold text-purple-600">47</p>
								<p class="text-xs text-gray-500">Insights Generated</p>
							</div>
							<div class="text-center p-3 bg-gray-50 rounded-lg">
								<p class="text-2xl font-bold text-purple-600">92%</p>
								<p class="text-xs text-gray-500">Accuracy Rate</p>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- AI Insights Feed -->
			<div class="bg-white border border-gray-200 rounded-xl overflow-hidden">
				<div class="p-6 border-b border-gray-200">
					<div class="flex items-center justify-between">
						<div class="flex items-center space-x-3">
							<Bot class="w-6 h-6 text-purple-600" />
							<h3 class="text-xl font-semibold text-gray-900">AI Insights Feed</h3>
						</div>
						<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-purple-50 text-purple-700 border border-purple-200">
							Live Updates
						</span>
					</div>
				</div>

				<div class="divide-y divide-gray-100">
					{#each aiInsights as insight}
						<div class="p-6 hover:bg-gray-50 transition-colors border-l-4 {getSeverityColor(insight.severity)}">
							<div class="flex items-start space-x-4">
								<div class="p-2 bg-white rounded-lg shadow-sm border">
									<svelte:component this={insight.icon} class="w-5 h-5 {getIconColor(insight.severity)}" />
								</div>
								
								<div class="flex-1">
									<div class="flex items-start justify-between">
										<div>
											<h4 class="text-lg font-semibold text-gray-900 mb-1">{insight.title}</h4>
											<p class="text-gray-700 leading-relaxed mb-3">{insight.message}</p>
											
											<div class="flex items-center space-x-4 text-sm text-gray-500">
												<div class="flex items-center space-x-1">
													<Target class="w-4 h-4" />
													<span>{insight.confidence}% confidence</span>
												</div>
												<div class="flex items-center space-x-1">
													<Clock class="w-4 h-4" />
													<span>{insight.timestamp}</span>
												</div>
											</div>
										</div>
										
										<button class="p-2 text-gray-400 hover:text-gray-600 transition-colors">
											<ArrowRight class="w-5 h-5" />
										</button>
									</div>
								</div>
							</div>
						</div>
					{/each}
				</div>
			</div>
		</div>
	</div>
</div>

<style>
	@keyframes glow {
		0%, 100% { box-shadow: 0 0 20px rgba(34, 197, 94, 0.3); }
		50% { box-shadow: 0 0 30px rgba(34, 197, 94, 0.6); }
	}
	
	.animate-glow {
		animation: glow 2s ease-in-out infinite;
	}

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