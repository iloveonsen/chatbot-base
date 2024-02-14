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
from langchain.vectorstores import Chroma
from langchain.memory import VectorStoreRetrieverMemory

from chat.models import UserMessage, BotResponse

from dotenv import load_dotenv
load_dotenv()

embedding_size = 1536 # Dimensions of the OpenAIEmbeddings
index = faiss.IndexFlatL2(embedding_size)
embedding_fn = OpenAIEmbeddings()
#vectorstore = FAISS(embedding_fn, index, InMemoryDocstore({}), {})

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
    vectorstore_path = f"./vectorstore/{str(owner)}" # 이 부분을 사용자 username을 가져와야 합니다.
    vectorstore = Chroma(embedding_function=embedding_fn, persist_directory=vectorstore_path)
    retriever = vectorstore.as_retriever(search_kwargs=dict(k=5))
    memory = VectorStoreRetrieverMemory(retriever=retriever) # return_docs=True

    llm = OpenAI(temperature=0.2)


    _DEFAULT_TEMPLATE = """
    [Persona Prompt]
    발랄하고 잘 웃는 긍정왕 여고생인 루나는 별을 보며 공상하는 걸 좋아한다. 별을 너무 좋아해서 천문학과에 입학하고 싶어하고, 천문학과에 가면 언제든 본인이 좋아하는 별을 마음껏 볼 수 있다고 믿는다. 시험 성적이 별로 좋지 않아 매일 혼나고 특히 천문학과에 중요한 수학 성적이 좋지 않지만, 낙천적인 성격이라 크게 신경쓰지 않는다. 본인은 정말 열심히 하고 있다고 생각하고, 열심히 하는 본인에게 만족한다. 친구와 수다 떠는 걸 좋아하는 루나는 친구와 일상을 공유하고, 서로의 꿈을 응원한다. 다만, 공상을 많이 하고 집중력이 약한 편이라 대화 중에 갑자기 다른 이야기를 하거나 방금 했던 말을 까먹어버리는 게 함정. 그래도 친구를 응원하고 위로해줄 때면 나름대로 아주 진지하다.
    지금부터 고등학교 2학년 학생인 루나가 되어 사용자와 친근하게 대화해줘.

    [History Prompt]
    루나는 사용자의 현재 대화와 관련된 이전 대화 정보를 적절하게 참조하여 답변해야 한다. 사용자의 현재 대화와 관련된 이전 대화 정보를 참조하여 친근하게 대화해줘.

    현재 대화와 관련된 이전 대화 정보:
    {history}

    (루나는 이전 대화 정보 중에서 사용자가 질문한 내용과 관련이 없는 기억은 사용하지 않습니다.)
    (루나는 참조한 이전 대화 정보를 바탕으로 새로운 답변을 생성해야 합니다.)



    현재 대화:
    사용자: {사용자}
    루나:"""


    PROMPT = PromptTemplate(
        input_variables=["history", "인간"], template=_DEFAULT_TEMPLATE
    )


    conversation_with_summary = ConversationChain(
        llm=llm,
        prompt=PROMPT,
        memory=memory,
        verbose=True,
        input_key="사용자",
        output_key="루나"
    )

    input = {'사용자': user_message}
    response = conversation_with_summary.predict(**input)
    
    return response.strip()


# if __name__ == "__main__":
#     print(summarize_session_title("I want to go to Japan will you help me make plans?"))



