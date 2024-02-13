from langchain_openai import OpenAI, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, ConversationChain
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.memory import ConversationBufferMemory

from chat.models import UserMessage, BotResponse

from dotenv import load_dotenv

load_dotenv()

def summarize_session_title(user_message):
    llm = OpenAI(temperature=0)
    
    prompt_template = PromptTemplate(
        input_variables=['message'],
        template="""Here is a message provided by a user. message: {message}. 
        Summarize the message into single noun"""
    )

    llm_chain = LLMChain(llm=llm, prompt=prompt_template)

    response = llm_chain.invoke({'message': user_message})
    return response['text'].strip()


def get_chatbot_response(user_message, session, owner):
    chat = ChatOpenAI(temperature=.2)


    messages = [
        SystemMessage(
            content="You are a helpful ai kindly reply to user."
        ),
        HumanMessage(
            content=user_message
        ),
    ]

    existing_user_messages = UserMessage.objects.filter(session=session, owner=owner)
    for existing_user_message in existing_user_messages:
        messages.append(HumanMessage(content=existing_user_message.message))
        try:
            existing_bot_response = BotResponse.objects.get(user_message=existing_user_message)
        except Exception as e:
            break
        messages.append(AIMessage(content=existing_bot_response.response))

    response = chat.invoke(messages)
    return response.content.strip()


# if __name__ == "__main__":
#     print(summarize_session_title("I want to go to Japan will you help me make plans?"))



