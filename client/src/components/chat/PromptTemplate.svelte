<script lang="ts">
	import type { Conversation } from '$s/chat';
	import { onMount } from 'svelte';
	import { setPromptTemplate } from '$s/chat';
	import Hamburger from '$c/Icons/Hamburger.svelte';

    let prompts: string[] = ["User Story", "Epic", "Diagram"];
	let isOpen = false;
	export let resetPromptFlag: Function;

	async function handleClick(prompt: string) {
		isOpen = false;
		setPromptTemplate(prompt);
        resetPromptFlag()
	}

	onMount(() => {
		window.addEventListener('click', (e: any) => {
			if (e.target && !e.target.closest('.relative')) {
				isOpen = false;
			}
		});
	});
</script>

<div class="relative inline-block text-left">
	<div>
        
		<button
			on:click={() => (isOpen = !isOpen)}
			type="button"
			class="inline-flex justify-center w-full px-4 py-2"
			id="options-menu"
			aria-haspopup="true"
			aria-expanded="true"
		>
            <Hamburger/>
		</button>
	</div>

	{#if isOpen}
		<div
			class="origin-top-right overflow-y-scroll absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5"
			style="max-width: 250px; max-height: 250px;"
		>
			<div class="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
				{#each prompts as prompt}
					<div
						class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 ellipsis"
						on:click={() => handleClick(prompt)}
						on:keypress={() => {}}
					>
						{prompt}
					</div>
				{/each}
			</div>
		</div>
	{/if}
</div>
<style>
	.bg-gray{
		background-color:#fff
	}
	.ellipsis {
		width: 200px; /* Adjust this value as needed */
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
}
</style>