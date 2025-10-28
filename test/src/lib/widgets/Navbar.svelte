<script>
	import { Bell, Settings, User, Leaf } from 'lucide-svelte';
	
	export let toggleSidebar = () => {};
</script>

<!-- Top Navigation Bar -->
<nav class="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 z-50 shadow-sm">
	<div class="flex items-center justify-between px-6 py-4">
		<!-- Left: Logo and Menu -->
		<div class="flex items-center gap-4">
			<button on:click={toggleSidebar} class="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors">
				<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
				</svg>
			</button>
			
			<div class="flex items-center gap-3">
				<div class="w-8 h-8 bg-gradient-to-br from-green-600 to-teal-600 rounded-lg flex items-center justify-center">
					<Leaf class="w-5 h-5 text-white" />
				</div>
				<div class="flex items-center gap-2">
					<span class="font-bold text-xl bg-gradient-to-r from-green-700 to-teal-700 bg-clip-text text-transparent">EcoMind</span>
					<span class="text-green-600 text-lg">🌿</span>
				</div>
			</div>
		</div>

		<!-- Center: Quick Stats -->
		<!-- <div class="hidden md:flex items-center gap-6">
			<div class="text-center">
				<p class="text-sm text-gray-500">Today's Emissions</p>
				<p class="text-lg font-semibold text-green-600">-12.3%</p>
			</div>
			<div class="h-8 w-px bg-gray-200"></div>
			<div class="text-center">
				<p class="text-sm text-gray-500">Monthly Goal</p>
				<p class="text-lg font-semibold text-green-600">78%</p>
			</div>
		</div> -->

		<!-- Right: User Actions -->
		<div class="flex items-center gap-4">
			<Bell class="w-5 h-5 text-gray-500 hover:text-gray-700 cursor-pointer transition-colors" />
			<Settings class="w-5 h-5 text-gray-500 hover:text-gray-700 cursor-pointer transition-colors" />
			
			<div class="w-8 h-8 bg-gradient-to-br from-green-500 to-teal-500 rounded-full flex items-center justify-center">
				<User class="w-5 h-5 text-white" />
			</div>
		</div>
	</div>
</nav>