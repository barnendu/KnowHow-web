<script>
	import { onMount } from 'svelte';
	import mermaid from 'mermaid';
	export let chartCode = '';
	onMount(() => {
		mermaid.initialize({ startOnLoad: true });
		mermaid.contentLoaded(); // Ensures Mermaid processes the diagram
	});
</script>
<div class="diagram-content" style="height:calc(-80px + 100vh)">
{#if chartCode}
	<div class="mermaid">
		{@html chartCode}
	</div>
{/if}
</div>
<style>
	.diagram-content {
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Light shadow */
		border: 1px solid #ddd;
		overflow: auto;
		padding: 5%;
	}
</style>
