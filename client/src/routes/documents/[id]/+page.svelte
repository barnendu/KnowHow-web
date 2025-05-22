<script lang="ts">
	import { fly } from 'svelte/transition';
	import type { PageData } from './$types';
	import { onMount } from 'svelte';
	import { beforeNavigate, goto } from '$app/navigation';
	import { getBlogContent, resetAll, sendMessage, store, resetComplete, resetError } from '$s/chat';
	import PdfViewer from '$c/PdfViewer.svelte';
	import CsvViewer from '$c/CsvViewer.svelte';
	import XlsxViewer from '$c/XlsxViewer.svelte';
	import TxtViewer from '$c/TxtViewer.svelte';
	import DocxViewer from '$c/DocxViewer.svelte';
	import ChatPanel from '$c/chat/ChatPanel.svelte';
	import AudioPlayer from '$c/AudioPlayer.svelte';
	import { createEventDispatcher } from 'svelte';
	import Alert from '$c/Alert.svelte';
	import CkEditor from '$c/CkEditor.svelte';
	import Diagram from '$c/Diagram.svelte';
	import html2pdf from 'html2pdf.js';

	let showTooltip = false;
	let tooltipX = 0;
	let tooltipY = 0;

	const dispatch = createEventDispatcher();
	let selectedText = '';
	let isCampaign = false;
	let isDocumentVisible = false;

	$: blogContent = $store.blogContent;
	$: diagramContent = $store.diagramContent;

	onMount(async () => {
		const queryParams = new URLSearchParams(window.location.search);
		isCampaign = queryParams.get('campaign') === 'true';
	});

	export let data: PageData;

	const docs = data.document;
	const documentUrl = data.documentUrl;
	const documentExt = docs.document_ext;

	function handleSubmit(content: string, useStreaming: boolean) {
		sendMessage({ role: 'user', content }, { useStreaming, documentId: docs.id, image: false });
	}

	function handleSearch() {
		goto('/openChat');
	}
	beforeNavigate(resetAll);

	function exportDoc() {
		// Implementation remains the same as provided above
	}
</script>

<div class="app-container">
	<!-- Top Section - Only visible when there's an error -->
	{#if data.error}
		<div class="top-section">
			<div class="error-message">
				<svg class="error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
				</svg>
				{data.error}
			</div>
		</div>
	{/if}

	<!-- Main Content -->
	<div class="main-content">
		<!-- Chat Panel -->
		<div
			class="chat-section"
			class:expanded={!isDocumentVisible}
		>
			<div class="chat-header">
				<h2>Chat History</h2>
				<button
					class="clear-button"
					on:click={() => resetAll()}
				>
					<svg class="button-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
					</svg>
					Clear History
				</button>
			</div>
			<ChatPanel documentId={docs.id} onSubmit={handleSubmit} />
			<button
				class="toggle-button"
				on:click={() => (isDocumentVisible = !isDocumentVisible)}
			>
				{isDocumentVisible ? '→' : '←'}
			</button>
		</div>

		<!-- Document Display -->
		{#if isDocumentVisible}
			<div
				class="document-section"
				transition:fly={{ x: 100, duration: 300 }}
			>
				{#if isCampaign}
					{#key blogContent}
						<CkEditor {blogContent} />
					{/key}
				{:else if diagramContent}
					{#key diagramContent}
						<Diagram chartCode={diagramContent} />
					{/key}
				{:else if documentExt == 'pdf'}
					<PdfViewer url={documentUrl[0]} />
				{:else if documentExt == 'csv'}
					<CsvViewer url={documentUrl[0]} />
				{:else if documentExt == 'xlsx'}
					<XlsxViewer url={documentUrl[0]} />
				{:else if documentExt == 'txt'}
					<TxtViewer url={documentUrl[0]} />
				{:else if documentExt == 'docx'}
					<DocxViewer url={documentUrl[0]} />
				{:else if documentExt == 'wav' || documentExt == 'mp3'}
					<AudioPlayer url={documentUrl} name={docs.name} />
				{:else if documentExt == 'webp' || documentExt == 'jpeg' || documentExt == 'jpg' || documentExt == 'png'}
					<div class="image-container">
						<img src={documentUrl[0]} alt="source information" class="document-image" />
					</div>
				{:else}
					<div class="loading-state">
						<svg class="loading-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
						</svg>
						<p>Loading document...</p>
					</div>
				{/if}
			</div>
		{/if}
	</div>
</div>

<style>
	.app-container {
		height: 100vh;
		background-color: #f8fafc;
		padding: 1.5rem;
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		font-family: 'Inter', system-ui, -apple-system, sans-serif;
		overflow-x: hidden;
	}

	.top-section {
		background: white;
		padding: 1rem 1.5rem;
		border-radius: 1rem;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
	}

	.error-message {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		color: #dc2626;
		font-weight: 500;
		font-size: 0.9375rem;
	}

	.error-icon {
		width: 1.5rem;
		height: 1.5rem;
		flex-shrink: 0;
	}

	.main-content {
		flex: 1;
		display: grid;
		grid-template-columns: 1fr 1.5fr;
		gap: 1.5rem;
		height: calc(100vh - 140px);
		overflow-x: hidden;
	}

	.alerts-container {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.actions-container {
		display: flex;
		gap: 1rem;
	}

	.action-button {
		display: inline-flex;
		align-items: center;
		gap: 0.625rem;
		padding: 0.75rem 1.25rem;
		border-radius: 0.75rem;
		font-weight: 600;
		font-size: 0.9375rem;
		transition: all 0.2s ease;
		cursor: pointer;
		box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
	}

	.action-button.new-chat {
		background-color: white;
		color: #1e293b;
		border: 1px solid #e2e8f0;
	}

	.action-button.new-chat:hover {
		background-color: #f8fafc;
		border-color: #cbd5e1;
		transform: translateY(-1px);
	}

	.action-button.export {
		background-color: #1e40af;
		color: white;
		border: none;
	}

	.action-button.export:hover {
		background-color: #1e3a8a;
		transform: translateY(-1px);
	}

	.button-icon {
		width: 1.25rem;
		height: 1.25rem;
	}

	.chat-section {
		background-color: white;
		border-radius: 1rem;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
		position: relative;
		transition: all 0.3s ease;
		display: flex;
		flex-direction: column;
	}

	.chat-section.expanded {
		grid-column: 1 / -1;
	}

	.chat-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1.25rem;
		border-bottom: 1px solid #e2e8f0;
		background-color: #f8fafc;
		border-radius: 1rem 1rem 0 0;
	}

	.chat-header h2 {
		font-size: 1.25rem;
		font-weight: 600;
		color: #1e293b;
	}

	.clear-button {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 1rem;
		color: #3b82f6;
		font-size: 0.875rem;
		font-weight: 500;
		transition: all 0.2s ease;
		border-radius: 0.5rem;
	}

	.clear-button:hover {
		color: #2563eb;
		background-color: #eff6ff;
	}

	.toggle-button {
		position: absolute;
		right: 0rem;
		top: 50%;
		transform: translateY(-50%);
		background-color: #64748b;
		color: white;
		width: 2rem;
		height: 2rem;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 0.5rem;
		cursor: pointer;
		transition: all 0.2s ease;
		font-weight: 600;
		box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.toggle-button:hover {
		background-color: #475569;
		transform: translateY(-50%) scale(1.05);
	}

	.document-section {
		background-color: white;
		border-radius: 1rem;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
		overflow: auto;
		padding: 1.5rem;
	}

	.image-container {
		width: 100%;
		height: 100%;
		overflow: auto;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.document-image {
		max-width: 100%;
		height: auto;
		object-fit: contain;
		border-radius: 0.5rem;
	}

	.loading-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100%;
		color: #64748b;
		gap: 1rem;
	}

	.loading-icon {
		width: 3.5rem;
		height: 3.5rem;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		from {
			transform: rotate(0deg);
		}
		to {
			transform: rotate(360deg);
		}
	}

	:global(.tooltip) {
		background-color: #1e293b;
		color: white;
		padding: 1rem 1.25rem;
		border-radius: 0.75rem;
		font-size: 0.9375rem;
		box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
		z-index: 50;
		max-width: 24rem;
	}

	:global(.tooltip button) {
		background-color: white;
		color: #1e293b;
		padding: 0.5rem 1rem;
		border-radius: 0.5rem;
		font-size: 0.875rem;
		font-weight: 600;
		margin-left: 80%;
		transition: all 0.2s ease;
		box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
	}

	:global(.tooltip button:hover) {
		background-color: #f8fafc;
		transform: translateY(-1px);
	}
</style>
