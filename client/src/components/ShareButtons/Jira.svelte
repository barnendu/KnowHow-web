<script>
	import Jira from '$c/Icons/Jira.svelte';
	import { createJiraTicket } from '$s/chat/index';

	/**
	 * @type {string}
	 */
	export let title;
	/**
	 * @param {string} text
	 */
	function extractUserStoryTitle(text) {
		const titleRegex = /\*\*Title\*\*:\s*(.*?)(?=\n|\*\*)/;
		const titleMatch = text.match(/^Title:\s*(.*)$/m);
		const userStoryTitle = text.match(/\*\*User Story\*\*:\s*(.*?)(?=\n|\*\*)/);
		const match = text.match(titleRegex);
		if (match) {
			let title = match[1].trim();
			if (title.length > 255) {
				title = title.substring(0, 252) + '...';
			}
			return title;
		} else if(titleMatch) {	
			if (titleMatch) {
				let title = titleMatch[1];
				if (title.length > 255) {
					title = title.substring(0, 252) + '...';
				}
				return title;
			}
		}
		else if(userStoryTitle) {	
			if (userStoryTitle) {
				let title = userStoryTitle[1];
				if (title.length > 255) {
					title = title.substring(0, 252) + '...';
				}
				return title;
			}
		}

		return null;
	}

	/**
	 * @param {string} text
	 */
	function extractSections(text) {
		const regex = {
			acceptanceCriteria: /\*\*Acceptance criteria\*\*:\s*([\s\S]*?)(?=\n\*\*|$)/i,
			functionalTestCases: /\*\*Functional Test Cases\*\*:\s*([\s\S]*?)(?=\n\*\*|$)/i
		};
		const regex2 = {
			acceptanceCriteria: /Acceptance Criteria:\n([\s\S]*?)\n\n/,
			functionalTestCases: /Functional Test Cases:\n([\s\S]*?)$/
		};

		const result = {};

		for (const [key, pattern] of Object.entries(regex)) {
			const match = text.match(pattern);
			result[key] = match ? match[1].trim().replace(/\*\*/g, '') : null;
		}
		if (Object.keys(result).length === 0) {
			for (const [key, pattern] of Object.entries(regex2)) {
				const match = text.match(pattern);
				result[key] = match ? match[1].trim().replace(/\*\*/g, '') : null;
			}
		}
		return result;
	}

	// Function to extract functional test cases
	/**
	 * @param {string} text
	 */
	function extractFunctionalTestCases(text) {
		const testCasesRegex = /Functional Test Cases:\s*([\s\S]*?)(?=\n\n\w+:|$)/;
		const match = text.match(testCasesRegex);

		if (match && match[1]) {
			const testCasesText = match[1].trim();
			return testCasesText.trim().replace(/\*\*/g, '');
		}
		return null;
	}

	function handleClick() {
		console.log(title);
		let userStory = extractUserStoryTitle(title);
		const sections = extractSections(title);

		const payload = {
			fields: {
				project: {
					key: 'EP'
				},
				summary: userStory,
				description: {
					type: 'doc',
					version: 1,
					content: [
						{
							type: 'paragraph',
							content: [
								{
									// @ts-ignore
									text:
										'\n Acceptance Criteria: \n' +
										sections.acceptanceCriteria +
										'\n Functional Test Cases: \n' +
										sections.functionalTestCases,
									type: 'text'
								}
							]
						}
					]
				},
				issuetype: {
					name: 'Task'
				}
			}
		};
		createJiraTicket({"ticket":title});
	}
</script>

<button on:click={handleClick}><Jira /></button>

<style>
	button {
		background: transparent;
		border-style: none;
		transition: all 0.2s ease-in-out;
		margin-right: 0.5rem;
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
