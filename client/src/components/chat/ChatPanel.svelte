<script lang="ts">
	import { onMount } from 'svelte';
	import {
		store,
		resetError,
		fetchConversations,
		createConversation,
		getActiveConversation
	} from '$s/chat';
	import Alert from '$c/Alert.svelte';
	import ChatInput from '$c/chat/ChatInput.svelte';
	import ChatList from '$c/chat/ChatList.svelte';
	import ConversationSelect from '$c/chat/ConversationSelect.svelte';
	import PromptTemplate from './PromptTemplate.svelte';

	export let onSubmit: (text: string, useStreaming: boolean) => void;
	export let documentId: number;

	let useStreaming = !!localStorage.getItem('streaming');

	$: localStorage.setItem('streaming', useStreaming ? 'true' : '');
	$: activeConversation = $store.activeConversationId ? getActiveConversation() : null;
	let showPrompt = true

	function handleSubmit(event: CustomEvent<string>) {
		if (onSubmit) {
			onSubmit(event.detail, true);
			showPrompt = false
		}
	}

	function handleNewChat() {
		createConversation(documentId);
	}
	function resetPromptFlag(){
		showPrompt = true
	}
	onMount(() => {
		fetchConversations(documentId);
	});
</script>

<div
	style="height: calc(100vh - 80px);"
	class="flex flex-col h-full bg-slate-50 border shadow"
>
	<div class="chat-header">
		<div class="header-content">
			<div class="header-left m-6">
				<button class="new-chat-button" on:click={handleNewChat}>
					<svg class="button-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
					</svg>
					<span>New Chat</span>
				</button>
				<ConversationSelect conversations={$store.conversations} />
			</div>
			<PromptTemplate resetPromptFlag={resetPromptFlag}/>
		</div>
	</div>
	<div class="flex flex-col flex-1 px-3 py-2 overflow-y-scroll">
		<ChatList messages={activeConversation?.messages || []} />
		<div class="relative">
			{#if $store.error && $store.error.length < 200}
				<div class="p-4">
					<Alert type="error" onDismiss={resetError}>
						{$store.error}
					</Alert>
				</div>
			{/if}
			{#if $store.activePrompt && showPrompt}
			<div class="p-4 mb-2.5">
				<span class="sl-template">
					{$store.activePrompt}
				</span>
			</div>
			{/if}
			<ChatInput on:submit={handleSubmit} />
		</div>
	</div>
</div>

<style>
	.sl-template{
		padding:20px;
		border-radius: 15px;
		border: 1px solid #f4e6e6;
		margin-bottom: 10px;
	}
	.gap-1{
		gap: 1rem
	}
	.header-content {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 2rem;
	}

	.header-left {
		display: flex;
		align-items: center;
		gap: 1.25rem;
	}

	.new-chat-button {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.625rem 1.25rem;
		background-color: #e0edff;
		color: #1e40af;
		border: none;
		border-radius: 0.75rem;
		font-weight: 500;
		font-size: 0.9375rem;
		transition: all 0.2s ease;
		cursor: pointer;
		box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
		margin-right: 0.25rem;
	}

	.new-chat-button:hover {
		background-color: #d0e3ff;
		color: #174ea6;
		transform: translateY(-1px);
		box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
	}

	.new-chat-button:active {
		background-color: #b6d4fe;
		color: #174ea6;
		transform: translateY(0);
	}

	.new-chat-button .button-icon {
		width: 1.25rem;
		height: 1.25rem;
		transition: transform 0.2s ease;
		stroke: #1e40af;
	}

	.new-chat-button:hover .button-icon,
	.new-chat-button:active .button-icon {
		stroke: #174ea6;
	}

	:global(.conversation-select) {
		min-width: 200px;
		margin-left: 0;
	}
</style>

