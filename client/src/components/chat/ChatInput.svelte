<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	let value = '';

	const dispatch = createEventDispatcher();
	function handleKeyDown(event: KeyboardEvent) {
		const isCombo = event.shiftKey || event.ctrlKey || event.altKey || event.metaKey;
		if (event.key !== 'Enter' || isCombo) {
			return;
		}

		if (event.key === 'Enter' && !isCombo && value === '') {
			event.preventDefault();
			return;
		}

		event.preventDefault();
		dispatch('submit', value);
		value = '';
	}

	function handleSubmit() {
		if (value.trim() === '') return;
		dispatch('submit', value);
		value = '';
	}

	$: height = (value.match(/\n/g)?.length || 0) * 25 + 72;
</script>

<div class="relative w-full">
	<textarea
		class="w-full mx-auto py-3 px-4 pr-12 resize-none border rounded-lg max-h-40 bg-white shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
		style:height={height + 'px'}
		bind:value
		on:keydown={handleKeyDown}
		placeholder="Type your message..."
	/>
	<button
		class="absolute right-3 bottom-3 p-2 text-gray-500 hover:text-blue-500 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
		on:click={handleSubmit}
		disabled={value.trim() === ''}
		aria-label="Send message"
	>
		<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 transform rotate-45" viewBox="0 0 20 20" fill="currentColor">
			<path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
		</svg>
	</button>
</div>
