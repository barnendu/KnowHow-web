<script lang="ts">
	import { marked } from 'marked';
	import ShareButtons from '$c/ShareButtons/index.svelte'

	export let content = '';
    let doclink = '';
	let name = '';
	let childComponent:any;
	let childContent = '';
	function createImageTagFromUrl(text:string) {
		// Regular expression to match a URL
		const urlRegex = /(https?:\/\/[^\s]+(?:jpg|jpeg|png|gif))/gi;

		// Search for the URL in the input text
		const match = text.match(urlRegex);

		if (match) {
			// If a match is found, return an img tag with the URL as the source
			return `<img src="${text}" alt="Image" />`;
		} else {
			// If no match is found, return an empty string or a default message
			return text;
		}
	}
</script>

<div class="flex flex-row items-center justify-between">
	<div bind:this={childComponent} 
		class="message border rounded-md py-1.5 px-2.5 my-0.25 break-words self-start bg-white text-black-100"
	>
		{@html marked(createImageTagFromUrl(content), { breaks: true, gfm: true })}
	</div>
	<div class="flex flex-row flex-1 items-start gap-1 flex-wrap justify-center">
		<ShareButtons title={content} {doclink} {name} blogContent={ marked(createImageTagFromUrl(content), { breaks: true, gfm: true })}/>
	</div>
</div>

<style>
	.message {
		max-width: 80%;
		overflow-x: visible !important;
	}
	.bg-white{
      background-color: #fff;
	}
	pre {
		overflow-y: scroll !important;
	}
	.message table {
		width: 100%;
		border-collapse: collapse;
	}

	.message th, .message td {
		border: 1px solid black;
		padding: 8px;
		text-align: left;
	}

	.message th {
		background-color: #f2f2f2;
	}

	/* Optional: Add some hover effects */
	.message tr:hover {
		background-color: #f5f5f5;
	}
</style>
