from openai import OpenAI # openai==1.93.1
from dotenv import load_dotenv
import os
import streamlit as st

# 실행하면 .env file 내의 환경변수 컴퓨터에 저장
load_dotenv()
api_key = os.getenv("SOLAR_API_KEY")

#모듈변수 가져와야함.
ocr_result = st.session_state.get("ocr_result", "")
correct_text = st.session_state.get("correct_text", "")

user_prompt = f"""
아래 두 한문을 비교해서 구글 ocr에서 누락되거나 잘못 인식된 한자를 찾아내고, 바로 잡아서 완성된 문장을 '한자'로 출력해줘. 한글로 출력하라는 것이 아니야.
------------
구글 ocr 인식 =[{ocr_result}]

정답지=[{correct_text}]
"""

client = OpenAI(
    api_key=api_key,
    base_url="https://api.upstage.ai/v1",
)

stream = client.chat.completions.create(
    model="solar-mini",
    messages=[
      {
        "role": "system",
        "content": "너는 한자 고문서 전문가로서 구글 클라우드 비전이 ocr 해서 인식한 수기 고문서 한자 인식 결과물과 사람이 직접 라벨링한 해당 이미지의 정답지를 받게 될거야. 구글 클라우드 비전은 대략 훌륭하지만, 완벽하지 않아. 너가 구글 ocr과 정답지를 비교해주는 선생님이 될거야. 출력은 반드시 한자로만 해줘. 한글 번역을 의뢰하는 것이 아니야. 구글 ocr로 인식된 문장의 줄바꿈을 참조해"
      },
      {
        "role": "user",
        "content": user_prompt
      }


    ],
    stream=True,
)

filled_text =""

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
      filling_text= chunk.choices[0].delta.content
      print(filling_text, end="")
      filled_text+=filling_text