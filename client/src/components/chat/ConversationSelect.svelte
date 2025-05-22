<script lang="ts">
	import type { Conversation } from '$s/chat';
	import { onMount } from 'svelte';
	import { setActiveConversationId } from '$s/chat';

	export let conversations: Conversation[] = [];
	let isOpen = false;
	

	async function handleClick(conversation: Conversation) {
		isOpen = false;
		console.log(JSON.stringify(conversation));
		setActiveConversationId(conversation.id);
	}

	onMount(() => {
		window.addEventListener('click', (e: any) => {
			if (e.target && !e.target.closest('.relative')) {
				isOpen = false;
			}
		});
		console.log(JSON.stringify(conversations));
	});
</script>

<div class="relative inline-block text-left">
	<div>
		<button
			on:click={() => (isOpen = !isOpen)}
			type="button"
			class="inline-flex justify-center w-full px-4 py-2 text-sm font-medium text-white bg-gray border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
			id="options-menu"
			aria-haspopup="true"
			aria-expanded="true"
		>
			History
			<svg
				class="-mr-1 ml-2 h-5 w-5"
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 20 20"
				fill="currentColor"
				aria-hidden="true"
			>
				<path
					fill-rule="evenodd"
					d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
					clip-rule="evenodd"
				/>
			</svg>
		</button>
	</div>

	{#if isOpen}
		<div
			class="origin-top-right overflow-y-scroll absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5"
			style="max-width: 250px; max-height: 250px;"
		>
			<div class="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
				{#each conversations as conversation (conversation)}
					<div
						class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 ellipsis"
						on:click={() => handleClick(conversation)}
						on:keypress={() => {}}
					>
						{conversation.messages?.[0]?.content}
					</div>
				{/each}
			</div>
		</div>
	{/if}
</div>
<style>
	.bg-gray{
		background-color:#84817f
	}
	.ellipsis {
		width: 200px; /* Adjust this value as needed */
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
}
</style>