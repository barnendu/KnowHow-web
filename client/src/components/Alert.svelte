<script lang="ts">
	import classNames from 'classnames';

	export let onDismiss: (() => void) | null = null;
	export let type: 'error' | 'success' | 'info' | 'warning' = 'error';

	const klasses = {
		error: 'bg-red-50 border-l-4 border-red-500 text-red-700',
		success: 'bg-green-50 border-l-4 border-green-500 text-green-700',
		info: 'bg-blue-50 border-l-4 border-blue-500 text-blue-700',
		warning: 'bg-yellow-50 border-l-4 border-yellow-500 text-yellow-700'
	};

	const klass = classNames(
		klasses[type],
		'relative rounded-md p-4 shadow-sm',
		'flex items-start gap-3',
		'transition-all duration-200 ease-in-out'
	);

	function handleDismiss() {
		if (onDismiss) {
			onDismiss();
		}
	}
</script>

<div class={klass} role="alert">
	<div class="flex-shrink-0">
	</div>
	<div class="flex-1">
		<slot />
	</div>
	{#if onDismiss}
		<button
			on:click={handleDismiss}
			class="flex-shrink-0 p-1 rounded-full hover:bg-opacity-10 transition-colors duration-200
				{type === 'error' ? 'hover:bg-red-500' : 
				type === 'success' ? 'hover:bg-green-500' :
				type === 'info' ? 'hover:bg-blue-500' :
				'hover:bg-yellow-500'}"
			aria-label="Dismiss"
		>
			<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
			</svg>
		</button>
	{/if}
</div>

<style>
	/* Add smooth animation for alert appearance */
	div {
		animation: slideIn 0.3s ease-out;
	}

	@keyframes slideIn {
		from {
			transform: translateY(-10px);
			opacity: 0;
		}
		to {
			transform: translateY(0);
			opacity: 1;
		}
	}
</style>
