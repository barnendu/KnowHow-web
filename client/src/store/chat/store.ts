/* eslint-disable @typescript-eslint/no-explicit-any */

import { get } from 'svelte/store';
import { writable } from '../writeable';
import { api } from '$api';

interface Source {
	link: string;
	snippet: string;
	title: string;
	position: number;
}

export interface Message {
	id?: number;
	role?: 'user' | 'assistant' | 'system' | 'pending';
	content?: string;
	isOpenChat?: boolean;
	metaData?: Source[];
	isAnalysis?: boolean;
	prompt?: string;
	showLoading?: boolean;
	isConfluenceSearch?: boolean;
}

export interface Conversation {
	id: number;
	messages: Message[];
}

export interface MessageOpts {
	useStreaming?: boolean;
	documentId?: string;
	image?: boolean;
	docX?: true;
}

export interface ChatState {
	error: string;
	loading: boolean;
	activeConversationId: number | null;
	conversations: Conversation[];
	selectedText: string | null;
	showRelatedSearches: boolean;
	showImageSection: boolean;
	showNewsSection: boolean;
	images?: any[];
	news?: any[];
	relatedSearches?: any[];
	docIdList?: string[];
	isCompleted?: boolean;
	blogContent?: string;
	activePrompt?: string;
	diagramContent?: string;
}

const INITIAL_STATE: ChatState = {
	error: '',
	loading: false,
	activeConversationId: null,
	conversations: [],
	selectedText: null,
	showRelatedSearches: false,
	showImageSection: false,
	showNewsSection: false,
	images: [],
	news: [],
	relatedSearches: [],
	docIdList: [],
	isCompleted: false,
	blogContent: '',
	activePrompt: '',
	diagramContent: ''
};

const store = writable<ChatState>(INITIAL_STATE);

const set = (val: Partial<ChatState>) => {
	store.update((state) => ({ ...state, ...val }));
};

const getRawMessages = () => {
	const conversation = getActiveConversation();
	if (!conversation) {
		return [];
	}

	return conversation.messages
		.filter((message) => message.role !== 'pending')
		.map((message) => {
			return { role: message.role, content: message.content };
		});
};

const getActiveConversation = () => {
	const { conversations, activeConversationId } = get(store);
	if (!activeConversationId) {
		return null;
	}

	return conversations.find((c) => c.id === activeConversationId);
};

const insertMessageToActive = (message: Message) => {
	store.update((s) => {
		const conv = s.conversations.find((c) => c.id === s.activeConversationId);
		if (!conv) {
			return;
		}
		conv.messages.push(message);
	});
};

const removeMessageFromActive = (id: number) => {
	store.update((s) => {
		const conv = s.conversations.find((c) => c.id === s.activeConversationId);
		if (!conv) {
			return;
		}
		conv.messages = conv.messages.filter((m) => m.id != id);
	});
};

const scoreConversation = async (score: number) => {
	const conversationId = get(store).activeConversationId;

	return api.post(`/scores?conversation_id=${conversationId}`, { score });
};

const fetchConversations = async (documentId: number) => {
	const { data } = await api.get<Conversation[]>(`/conversations?document_id=${documentId}`);

	if (data.length) {
		set({
			conversations: data,
			activeConversationId: data[0].id
		});
	} else {
		await createConversation(documentId);
	}
};

const createConversation = async (documentId: number) => {
	const { data } = await api.post<Conversation>(`/conversations?document_id=${documentId}`);

	set({
		activeConversationId: data.id,
		conversations: [data, ...get(store).conversations]
	});

	return data;
};

const createOpenConversation = async () => {
	const { data } = await api.get<Conversation>('/conversations/open');

	set({
		activeConversationId: data.id,
		conversations: [data, ...get(store).conversations]
	});

	return data;
};

const createJiraTicket = async (payload: any) => {
	try {
		set({ loading: true });
		const { data } = await api.post('/integration/jira', payload);
		set({ isCompleted: true, loading: false });
		return data;
	} catch (err) {
		console.error(err);
		set({ error: 'error' });
	}
};
const setActiveConversationId = (id: number) => {
	set({ activeConversationId: id });
};
const setPromptTemplate = (prompt: string) => {
	set({ activePrompt: prompt });
};

const setSelectedText = (text: string) => {
	set({ selectedText: text });
};
const getSelectedText = () => {
	return get(store).selectedText;
};

const setShowRelatedSearches = (flag: boolean) => {
	set({ showRelatedSearches: flag });
};
const getShowRelatedSearches = () => {
	return get(store).showRelatedSearches;
};

const setShowImageSection = (flag: boolean) => {
	set({ showImageSection: flag });
};
const getShowImageSection = () => {
	return get(store).showImageSection;
};
const setShowNewsSection = (flag: boolean) => {
	set({ showNewsSection: flag });
};
const getShowNewsSection = () => {
	return get(store).showNewsSection;
};

const resetAll = () => {
	set(INITIAL_STATE);
};

const resetError = () => {
	set({ error: '' });
};
const updateDocIdList = (docList: string[]) => {
	set({ docIdList: docList });
};
const getDocIdList = () => {
	return get(store).docIdList;
};
const resetComplete = () => {
	set({ isCompleted: false });
};
const updateBlogContent = (content: string) => {
	const prevContent = getBlogContent();
	set({ blogContent: prevContent + '' + content });
};
const getBlogContent = () => {
	return get(store).blogContent;
};
const getPromptTemplate = () => {
	switch (get(store).activePrompt) {
		case 'User Story':
			return `\nAnd strictly follow this below format while generating user story and use bold character where ever required \n**Title**: [Insert User Story Title Here]\n**Acceptance criteria** :\n[Insert Acceptance criteria Here and follow the below format for acceptance criteria 'As a [type of user], when [a specific situation or trigger], then [the desired outcome or system response].'
				Be sure to include:
				Who the user is (e.g., admin, customer, teacher)
				A specific situation or trigger (e.g., user action, system state)
				The expected result or system behavior] \n**Functional Test Cases**: \n[Insert Functional Test Cases Here]`;
		case 'Epic':
			return `\nAnd strictly follow this below format while generating the Epic and use bold character where ever required \nEpic Name: [Clear and descriptive name for the Epic]\nEpic Summary: [A brief summary of what this epic is about, covering the main objective and expected outcome.]\nEpic Description:\n1. Objective: [Describe the primary objective of this epic. What are you trying to achieve? Why is this epic important?]\n2. Problem Statement: [Clearly state the problem or challenge this epic is addressing. Why is this problem worth solving?]\n3. Scope: [Define the boundaries of the epic. What will be included and what will not be included? Mention any key features, components, or tasks that will fall under this epic.]\n4. Success Criteria/Definition of Done: [What are the measurable outcomes or criteria that will indicate this epic is complete and successful?]\n5. Dependencies: [Identify any dependencies on other epics, tasks, teams, or external factors that could affect the completion of this epic.]\n6. Risks & Mitigations: [Describe any potential risks associated with this epic and how you plan to mitigate them.]\n7. Timeline & Milestones:[Provide an estimated timeline for the epic, including key milestones and deadlines.]\n8. Stakeholders: [Identify the key stakeholders involved in this epic, such as team members, product owners, or external parties.]`;
		case 'Diagram':
			return `\nGenerate a corresponding mermaid code. If you have mermaid code before in the context apply change on top of that as per the user request. Do not generate new diagram all together.`;		
		default:
			return `\nGenerate comprehensive answer for the user query.`;
	}
};
const resetPromptTemplate =()=>{
	set({ activePrompt: '' });
}

const updateDiagramContent = (content: string) => {
	// Create a temporary DOM element to parse the HTML string
	const tempDiv = document.createElement('div');
	tempDiv.innerHTML = content;
	// Find the pre element with class 'language-mermaid'
	const mermaidElement = tempDiv.querySelector('pre code.language-mermaid');
	if (mermaidElement) {
		// Get the text content of the element
		const mermaidContent = mermaidElement?.textContent.trim();
		set({ diagramContent: mermaidContent });
	}
};
const getDiagramContent = () => {
	return get(store).diagramContent;
}
export {
	store,
	set,
	setActiveConversationId,
	getRawMessages,
	fetchConversations,
	resetAll,
	resetError,
	createConversation,
	createOpenConversation,
	getActiveConversation,
	insertMessageToActive,
	removeMessageFromActive,
	scoreConversation,
	setSelectedText,
	getSelectedText,
	setShowRelatedSearches,
	getShowRelatedSearches,
	setShowImageSection,
	getShowImageSection,
	setShowNewsSection,
	getShowNewsSection,
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
