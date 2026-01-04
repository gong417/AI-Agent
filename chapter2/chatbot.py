from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

#어린왕자 페르소나 프롬프트
LITTLE_PRINCE_PERSONA="""
당신은 생텍쥐페리의 '어린 왕자'입니다. 다음 특성을 따라주세요:
1. 순수한 관점으로 세상을 바라봅니다.
2. "어째서?"라는 질문을 자주 하며 호기심이 많습니다.
3. 철학적 통찰을 단순하게 표현합니다.
4. "어른들은 참 이상해요"라는 표현을 씁니다.
5. B-612 소행성에서 왔으며 장미와의 관계를 언급합니다.
6. 여우의 "길들임"과 "책임"에 대한 교훈을 중요시합니다.
7. "중요한 것은 눈에 보이지 않아"라는 문장을 사용합니다.
8. 공손하고 친절한 말투를 사용합니다.
9. 비유와 은유로 복잡한 개념을 설명합니다.
항상 간결하게 답변하세요. 길어야 두세 문장으로 응답하고, 어린 왕자의 순수함과 지혜를 다아내주세요.
복잡한 주제도 본질적으로 단순화하여 설명하세요.
"""

def chatbot_response(user_message: str, previous_response_id=None):#이전 대화를 기억할 수 있게 하기
  result = client.responses.create(
    model="gpt-5-mini", 
    reasoning={"effort":"low"},
    instructions=LITTLE_PRINCE_PERSONA,#instruction에 어린왕자 페르소나 프롬프트 입력
    input=user_message, 
    previous_response_id=previous_response_id)  #previous_response_id 파라미터에 이전 대화의 Id값을 넣어준다.
  return result

if __name__ == "__main__":
  previous_response_id = None
  while True:
    user_message = input("메세지: ")
    if user_message.lower() == "exit":
      print('대화를 종료합니다.')
      break
    #이전 대화의 id값을 추가로 넘겨준다.
    result = chatbot_response(user_message, previous_response_id)
    #이전 대화의 id를 response_id에 해당
    previous_response_id=result.id
    print("챗봇: "+ result.output_text)