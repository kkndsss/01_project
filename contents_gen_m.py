import streamlit as st
import google.generativeai as genai
import os

def generate_contents():
    st.header("4.한자 원문을 현대 동화로 전환")
    # 직전 단계에서 보정된 텍스트 가져오기
    filled_text = st.session_state.get("filled_text", "")

    #마찬가지로 3단계를 먼저 거쳐야함.
    if not filled_text:
        st.warning("LLM 자동 보정 결과가 없습니다. 3단계를 먼저 실행하세요.")
        return
    
    #프롬프트 변수화. 3단계에서 완성된 문장 변수를 가져와서 포멧팅으로 삽입
    #제미나이 문법은 그냥 저렇게 하래서 참고함.
    prompt = f"""
다음의 한자 고문서를 모르는 일반인도 쉽게 이해할 수 있게, 현대적인 문장으로 소설이나 동화 형식으로 각색해줘.
고전적 표현 대신 쉽고 따뜻한 현대어를 사용하고, 아이들도 이해할 수 있도록 스토리텔링해줘. 너무 길어서 지루하지 않도록. 재밌고 흥미로운 내용이 담기도록. 그래서 아이들도 흥미를 가지고 볼 수 있도록.
한글로 출력해줘.

원문:
{filled_text}
"""

    # Gemini 키값은 main에 있다.
    gemini_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    #이건 모듈화 하기 이전의 독립 실행 조건문인데 그냥 넣어도 상관 없을 것 같아서 살려둠.
    if not gemini_api_key:
        st.warning("GEMINI_API_KEY 가 설정되지 않았습니다.")
        return

    # 실행 버튼을 눌러야지만 생성이 되도록. 역시 제미나이 세부 세팅은 다른 소스 참조함
    if st.button("컨텐츠 생성"):
        genai.configure(api_key=gemini_api_key)
        #pro 모델 말고 넉넉한 flash로
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        #결과 생성
        last_result = response.text.strip()
        #결과 출력
        st.text_area("동화 스타일 컨텐츠 생성 결과", value=last_result)
        # 필요하다면 세션에도 저장. 혹시 모르니까...
        st.session_state["contents_result"] = last_result
