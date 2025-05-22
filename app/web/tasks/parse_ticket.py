
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import json

llm = ChatOpenAI(model="gpt-4o", temperature=0.6)

prompt = PromptTemplate(
    template="""You are an assistant for Jira ticket. 

    Analyze the Question text and parse the following information user story Title, Acceptance Criteria, Functional Test Cases.
     It will generate response in the below example format {{
                            "title": "title",
                            "description": "description",
                            "acceptance_criteria": "Acceptance Criteria",
                            "functional_test_cases": "Functional Test Cases"
                            }}. Generate description, Acceptance Criteria and Functional Test Cases as single string. Don't change the format or improvised the orginal text.
                              The json object without stingification and  no additional text.`
    Question: {question} 
    """,
    input_variables=["question"],
)

ticket_generation_chain = prompt | llm | StrOutputParser()

def parse_ticket(ticket_text):
    response = ticket_generation_chain.invoke({"question": ticket_text})
    print(response)
    ticket_response = json.loads(response)
    jira_issue = {
        "fields": {
            "project": {
                "key": "EP"
            },
            "summary": ticket_response["title"],
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": (
                                    "\n Description: \n"
                                    f"{ticket_response["description"]}\n"
                                    "\n Acceptance Criteria: \n"
                                    f"{ticket_response["acceptance_criteria"]}\n"
                                ),
                                "type": "text"
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": "Task"
            }
        }
    }
    return jira_issue
