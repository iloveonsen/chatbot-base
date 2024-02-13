from langchain_openai import OpenAI, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, ConversationChain
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.memory import ConversationBufferMemory
import faiss
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import OpenAI
from langchain.docstore import InMemoryDocstore
from langchain.vectorstores import FAISS
from langchain.memory import VectorStoreRetrieverMemory

from chat.models import UserMessage, BotResponse

from dotenv import load_dotenv

load_dotenv()

embedding_size = 1536 # Dimensions of the OpenAIEmbeddings
index = faiss.IndexFlatL2(embedding_size)

embedding_fn = OpenAIEmbeddings()
vectorstore = FAISS(embedding_fn, index, InMemoryDocstore({}), {})
retriever = vectorstore.as_retriever(search_kwargs=dict(k=5))

memory = VectorStoreRetrieverMemory(retriever=retriever,return_docs=True)

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

    llm = OpenAI(temperature=0) 


    _DEFAULT_TEMPLATE = """다음은 인간과 인공지능 간의 매우 친근한 대화입니다. AI는 맥락에서 많은 구체적인 세부 정보를 제공합니다. AI가 질문에 대답할 수 없으면 솔직하게 그렇다고 말합니다.

    현재 대화와 관련된 이전 대화 정보:
    {history}

    (관련이 없는 이전 대화 정보는 사용할 필요가 없습니다.)

    (AI는 이전 대화 정보 중에서 인간이 질문한 내용과 관련된 정보를 이해하여 친근하게 답변합니다.)
    현재 대화:
    인간: {input}
    AI:"""


    PROMPT = PromptTemplate(
        input_variables=["history", "input"], template=_DEFAULT_TEMPLATE
    )


    conversation_with_summary = ConversationChain(
        llm=llm,
        prompt=PROMPT,
        memory=memory,
        verbose=True
    )

    response = conversation_with_summary.predict(input=user_message)


    return response.strip()


# if __name__ == "__main__":
#     print(summarize_session_title("I want to go to Japan will you help me make plans?"))



