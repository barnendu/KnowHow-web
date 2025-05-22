<script lang="ts">
	import AuthLinks from '$c/auth/AuthLinks.svelte';
	import { auth } from '$s/auth';
	import CtsLogo from './Icons/CtsLogo.svelte';

	$: user = $auth.user;
</script>

<header class="sticky top-0 z-50 w-full bg-blue-100 border-b border-gray-100">
	<nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
		<div class="flex h-16 items-center justify-between">
			<!-- Logo Section -->
			<div class="flex items-center">
				<div class="flex-shrink-0">
					<CtsLogo />
				</div>
			</div>

			<!-- Right Section -->
			<div class="flex items-center">
				<div class="flex items-center space-x-4">
					{#if user}
						<div class="hidden sm:flex items-center space-x-6">
							<a
								href="/documents"
								class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 border-b-2 border-blue-500"
							>
								<svg
									class="w-5 h-5 mr-2"
									fill="none"
									stroke="currentColor"
									viewBox="0 0 24 24"
									xmlns="http://www.w3.org/2000/svg"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
									/>
								</svg>
								Dashboard
							</a>
							<div class="flex items-center space-x-2 text-sm text-gray-500">
								<svg
									class="w-5 h-5"
									fill="none"
									stroke="currentColor"
									viewBox="0 0 24 24"
									xmlns="http://www.w3.org/2000/svg"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
									/>
								</svg>
								<span class="font-medium text-gray-900">{user.email?.split(".")[0]}</span>
							</div>
						</div>
					{/if}
					<div class="ml-4 flex items-center md:ml-6">
						<AuthLinks />
					</div>
				</div>
			</div>
		</div>
	</nav>
</header>

<style lang="postcss">
	:global(.auth-link) {
		@apply inline-flex items-center px-4 py-2 text-sm font-medium rounded-md transition-all duration-200;
	}

	:global(.auth-link-primary) {
		@apply bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500;
	}

	:global(.auth-link-secondary) {
		@apply text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500;
	}
</style>
