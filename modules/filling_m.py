import streamlit as st
from openai import OpenAI
import os

def run_filling():
    st.header("3.Solar mini 활용 오인식 한자 자동 보정")
    #앞선 ocr 값과 json 정답지 모두 가지고 옴
    ocr_result = st.session_state.get("ocr_result", "")
    correct_text = st.session_state.get("correct_text", "")

    #둘다 넣어야지만 작동하게 함. return 쓰면 함수 강제 종료된단다. 경고문 띄우는 매소드래서 해봄
    if not ocr_result:
        st.warning("OCR 결과가 없습니다. 1단계에서 이미지를 먼저 넣어주세요")
        return
    if not correct_text:
        st.warning("정답지 결과가 없습니다. 2단계에서 JSON 파일을 넣어주세요.")
        return

    #프롬프트를 미리 작성해서 앞선 원문들을 가져온다. 그 아래는 solar 강의 코랩 형식 그냥 복붙했음...
    user_prompt = f"""
아래 두 한문을 비교해서 구글 ocr에서 누락되거나 잘못 인식된 한자를 찾아내고, 바로 잡아서 완성된 문장을 '한자'로 출력해줘. 한글로 출력하라는 것이 아니야.
------------
구글 ocr 인식 =[{ocr_result}]

정답지=[{correct_text}]
"""
    api_key = os.getenv("SOLAR_API_KEY")
    if st.button("OCR 오인식 자동수정"):
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
            #실질적 결과 텍스트들이 저장되는 공간
        filled_text = ""
        
        #아래는 그냥 코랩 코드 갖다 씀.
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                filling_text = chunk.choices[0].delta.content
                filled_text += filling_text
        #결과 출력        
        st.text_area("보정 결과", value=filled_text, height=300)
        #success매소드 쓰면 좀 더 세련된 페이지 만들 수 있다고 누가 블로그에 써놓음        
        st.success("보정 성공")
        #4단계 컨텐츠 생성을 위한 완전한 문장 스트림릿 공유형태로 저장
        st.session_state["filled_text"] = filled_text
          
