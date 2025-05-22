import type { Message, MessageOpts } from './store';
import { store, set, insertMessageToActive, removeMessageFromActive } from './store';
import { api, getErrorMessage } from '$api';

const _addPendingMessage = (message: Message, pendingId: number) => {
	insertMessageToActive(message);
	insertMessageToActive({
		id: pendingId,
		role: 'pending',
		content: '...'
	});
};

export const sendMessage = async (message: Message,  opts: MessageOpts) => {
	set({ loading: true });
	const pendingId = Math.random();
	const conversationId = store.get().activeConversationId;
	_addPendingMessage(message, pendingId);
	try {
		if (opts.image) { 
			const { data } = await api.post<Message>(`/conversations/${conversationId}/image`, {
				input: message.content
			});
			insertMessageToActive(data);

		} else if(opts.docX){
			const { data } = await api.post<Message>(`/conversations/${conversationId}/graph`, {
					input: message.content
				});
			insertMessageToActive(data);

		}else {
			const { data } = await api.post<Message>(`/conversations/${conversationId}/messages`, {
				input: message.content
			});
			insertMessageToActive(data);
		}

		removeMessageFromActive(pendingId);
	
		set({ error: '', loading: false });
	} catch (err) {
		set({ error: getErrorMessage(err), loading: false });
	}
};
