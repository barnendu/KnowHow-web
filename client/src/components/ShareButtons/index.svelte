<script>
	import Jira from '$c/ShareButtons/Jira.svelte';
	import Blog from '$c/ShareButtons/Blog.svelte';
	import ShareIcon from '$c/Icons/Share.svelte';
	export let title;
	export let doclink;
	export let name;
	export let blogContent;

	$: webShareAPISupported = true;

	$: handleWebShare;
	const handleWebShare = async () => {
		webShareAPISupported = false;
	};
</script>

<aside class="container">
	<div class="wrapper">
		 <div class="buttons">
			{#if webShareAPISupported}
				<button on:click={handleWebShare}>
					<ShareIcon width={20} />
				</button>
			{:else}
				<Jira {title} />
			{/if} 
		</div>
	</div>
</aside>

<style>
	.container {
		display: flex;
		flex-direction: row;
		margin-top: 3rem;
		width: '100';
	}
	.wrapper {
		display: flex;
		flex-direction: row;
		font-weight: 700;
		font-size: 1.25rem;
	}
	.buttons {
		margin-left: 1rem;
	}

	button {
		background: transparent;
		border-style: none;
		transition: all 0.2s ease-in-out;
	}

	@media (prefers-reduced-motion: reduce) {
		button {
			transition: all 2s ease-in-out;
		}
	}

	button:focus,
	button:hover {
		transform: scale(1.1);
	}
</style>
