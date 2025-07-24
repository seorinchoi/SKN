import chainlit as cl
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain #← ConversationChain을 사용해 메모리 관리 자동화


@cl.on_chat_start
async def on_chat_start():
    """
    채팅이 시작될 때 모델, 메모리, 체인을 초기화하여 사용자 세션에 저장합니다.
    """
    # 1. ChatOpenAI 모델 초기화
    # 최신 버전에서는 langchain_openai 라이브러리에서 가져옵니다.
    chat = ChatOpenAI(
        model="gpt-4.1"
    )


    # 2. 메모리 초기화
    memory = ConversationBufferMemory(
        return_messages=True
    )
   
    # 3. ConversationChain 초기화
    # 이 체인이 모델(llm)과 메모리(memory)를 연결하여 대화 흐름을 자동으로 관리합니다.
    chain = ConversationChain(
        llm=chat,
        memory=memory,
    )


    # # 4. 생성된 체인을 사용자 세션에 저장
    cl.user_session.set("chain", chain)
   
    await cl.Message(content="저는 대화의 맥락을 고려해 답변할 수 있는 채팅봇입니다. 메시지를 입력하세요.").send()


@cl.on_message
async def on_message(message: cl.Message):
    """
    사용자로부터 메시지가 오면 세션에 저장된 체인을 사용해 답변을 생성합니다.
    """
    # 1. 사용자 세션에서 체인 가져오기
    chain = cl.user_session.get("chain")


    # 2. 체인을 비동기적으로 실행(ainvoke)
    # 체인이 자동으로 메모리를 로드하고, 사용자 입력을 추가한 뒤, 모델을 호출하고,
    # 마지막으로 새로운 대화 내용을 메모리에 저장합니다.
    response = await chain.ainvoke({"input": message.content})


    # 3. 모델의 답변(response['response'])을 사용자에게 전송
    await cl.Message(content=response["response"]).send()
