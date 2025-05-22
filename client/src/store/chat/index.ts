import type { Message, MessageOpts, Conversation } from './store';
import {
	store,
	set,
	resetAll,
	resetError,
	fetchConversations,
	createConversation,
	createOpenConversation,
	setActiveConversationId,
	getActiveConversation,
	setShowRelatedSearches,
	getShowRelatedSearches,
	scoreConversation,
	setSelectedText,
	getSelectedText,
	createJiraTicket,
	updateDocIdList,
	getDocIdList,
	resetComplete,
	updateBlogContent,
	getBlogContent,
	setPromptTemplate,
	getPromptTemplate,
	resetPromptTemplate,
	updateDiagramContent,
	getDiagramContent
} from './store.js';
import { sendMessage as sendStreamingMessage } from './stream';
import { sendMessage as sendSyncMessage } from './sync';

const sendMessage = (message: Message, opts: MessageOpts) => {
	return opts.useStreaming ? sendStreamingMessage(message, opts) : sendSyncMessage(message, opts);
};

export {
	store,
	set,
	sendMessage,
	resetAll,
	resetError,
	fetchConversations,
	createConversation,
	createOpenConversation,
	setActiveConversationId,
	getActiveConversation,
	setShowRelatedSearches,
	getShowRelatedSearches,
	Conversation,
	scoreConversation,
	setSelectedText,
	getSelectedText,
	createJiraTicket,
	updateDocIdList,
	getDocIdList,
	resetComplete,
	updateBlogContent,
	getBlogContent,
	setPromptTemplate,
	getPromptTemplate,
	resetPromptTemplate,
	updateDiagramContent,
	getDiagramContent
};
