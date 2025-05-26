/* eslint-disable @typescript-eslint/no-explicit-any */
import type { Message } from './store';
import { set, store, getActiveConversation, insertMessageToActive, getDocIdList, getPromptTemplate, resetPromptTemplate } from './store';
import { addError } from '$s/errors';
import { getErrorMessage } from '$api';

const _addMessage = (message: Message) => {
	insertMessageToActive(message);
};

interface metadatas {
	metaData:any[],
	image:any[],
	news:any[],
}

const _appendResponse = (id: number | undefined, text: string, metadatas: metadatas) => {
	store.update((state) => {
		const conv = state.conversations.find((c) => c.id === state.activeConversationId);
		if (!conv) {
			return;
		}
		conv.messages = conv.messages.map((message) => {
			if (message.id === id) {
				message.content += text;
				message.role = 'assistant';
				message.metaData = metadatas?.metaData.organic?.length > 0 ? metadatas?.metaData.organic : message.metaData;
				message.showLoading = text !=''? false : true;
			}
			return message;
		});
		state.showRelatedSearches = text !=''? true: false;
		state.images = metadatas?.image?.images?.length > 0 ? metadatas?.image.images : state.images;
		state.news = metadatas?.news?.images?.length > 0 ? metadatas?.news.images : state.news;
		state.relatedSearches = metadatas?.metaData.relatedSearches?.length > 0 ? metadatas?.metaData.relatedSearches : state.relatedSearches;			
		
	});
	
	
};

export const sendMessage = async (userMessage: Message, opts: MessageOptions)=> {
	const conversation = getActiveConversation();

	set({ loading: true });

	const responseMessage = {
		role: 'pending',
		content: '',
		id: Math.random(),
		showLoading: true
	} as Message;

	try {
		_addMessage(userMessage);
		_addMessage(responseMessage);
		let response = new Response();
		if(userMessage.isOpenChat){
			const data = await fetch(`/api/conversations/${conversation.id}/metadata`, {
				method: 'POST',
				body: JSON.stringify({
					input: userMessage.content,
					isConfluenceSearch: userMessage.isConfluenceSearch
				}),
				credentials: 'include',
				headers: {
					'Content-Type': 'application/json'
				}
			});
			const metadatas = await data.json();

			_appendResponse(responseMessage.id, '', metadatas);
			response = await fetch(`/api/conversations/${conversation.id}/open?stream=true`, {
				method: 'POST',
				body: JSON.stringify({
					input: userMessage.content,
					isConfluenceSearch: userMessage.isConfluenceSearch
				}),
				credentials: 'include',
				headers: {
					'Content-Type': 'application/json'
				}
			});
			


			const reader = response.body?.getReader();
			if (!reader) {
				return;
			}
			if (response.status >= 400) {
				await readError(response.status, reader);
			} else {
				await readResponse(reader, responseMessage);		
			}
		}
		else if(opts.docX){
			response = await fetch(`/api/conversations/${conversation.id}/graph`, {
				method: 'POST',
				body: JSON.stringify({
					input: userMessage.content
				}),
				credentials: 'include',
				headers: {
					'Content-Type': 'application/json'
				}
			});
		

			const reader = response.body?.getReader();
			if (!reader) {
				return;
			}
			if (response.status >= 400) {
				await readError(response.status, reader);
			} else {
				await readResponse(reader, responseMessage);		
			}
		}
		else{
			response = await fetch(`/api/conversations/${conversation.id}/messages?stream=true`, {
				method: 'POST',
				body: JSON.stringify({
					input: userMessage.content,
					template: getPromptTemplate(),
					docList: getDocIdList()
				}),
				credentials: 'include',
				headers: {
					'Content-Type': 'application/json'
				}
			});
		
			resetPromptTemplate();

			const reader = response.body?.getReader();
			if (!reader) {
				return;
			}
			if (response.status >= 400) {
				await readError(response.status, reader);
			} else {
				await readResponse(reader, responseMessage);		
			}
			set({ loading: false });
		}
	} catch (err) {
		set({ error: getErrorMessage(err), loading: false });
	} finally{
		set({ loading: false });
	}
};

const readResponse = async (
	reader: ReadableStreamDefaultReader<Uint8Array>,
	responseMessage: Message
) => {
	let inProgress = true;

	while (inProgress) {
		const { done, value } = await reader.read();
		if (done) {
			inProgress = false;
			break;
		}
		const text = new TextDecoder().decode(value);

		if (responseMessage.id) {
			_appendResponse(responseMessage.id, text);
		}
	}
};

const readError = async (statusCode: number, reader: ReadableStreamDefaultReader<Uint8Array>) => {
	let inProgress = true;
	let message = '';
	while (inProgress) {
		const { done, value } = await reader.read();
		if (done) {
			inProgress = false;
			break;
		}
		const text = new TextDecoder().decode(value);
		message += text;
	}

	if (statusCode >= 500) {
		addError({ message, contentType: message.includes('<!doctype html>') ? 'text/html' : '' });
	} else {
		try {
			set({ error: getErrorMessage(JSON.parse(message)) });
		} catch (err) {
			set({ error: getErrorMessage(message) });
		}
	}
};
