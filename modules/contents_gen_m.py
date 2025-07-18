import streamlit as st
import google.generativeai as genai
import os
import time

#filling에서 처리된 텍스트를 삽입 = Ready단계
#LLM 입력전 처리 단계 : 사용자가 컨텐츠 유형을 선택하면, 미리 정의된 프롬프트가 저장된 txt를 prompt 폴더에서 불러온다.
#프롬프트 유지보수 및, 추후 컨텐츠 유형 추가를 위해 외부 입력 방식을 선택
#LLM에는 현재 filling 처리된 완성문장 + 사용자가 선택한 프로프트가 입력된 상태
#제대로된 vectordb 기반의 RAG는 구현을 못했습니다. 이 방식으로 일단 대체하겠습니다.
#LLM은 두 입력 소스를 기반으로 현대적 컨텐츠를 아웃풋하는 처리과정

def generate_contents():
    st.header("4.고문서 원문을 현대적 컨텐츠로 재창작")
    # 직전 단계에서 보정된 텍스트 가져오기
    filled_text = st.session_state.get("filled_text", "")

    #마찬가지로 3단계를 먼저 거쳐야함.
    #아 근데... 간편모드 하려니까 여기도 분기를 하나 더 해줘야겠네. ocr에서 ocr_result를 바로 받아오도록.
    if not filled_text :
        filled_text = st.session_state.get("ocr_result", "")
        if not filled_text:
            st.warning("간편모드시 : OCR 먼저 진행해주세요!/정확도 모드시 : LLM보정 먼저 진행해주세요!")
            return
    
    #컨텐츠 유형 메뉴 선택
    contents_menu=["동화", "현대시", "뉴스기사", "영화시나리오", "유튜브대본", "4컷웹툰", "광고"]
    menu_dropbox=st.selectbox("생성을 원하시는 컨텐츠 유형을 선택해주세요!", contents_menu)

    #메뉴가 선택되면 해당 유형에 맞게 미리 정의된 프롬프트 파일을 읽어온다.

    #프롬프트.txt가 저장된 폴더 접근
    prompt_folder = "./prompts"
    #os 유형에 따라 경로 오류를 최소화하고자 join함수 사용.
    prompt_path=os.path.join(prompt_folder, f"{menu_dropbox}.txt")
    #파일이 있는지 없는지 확인해주는 함수래... 그렇데...
    if not os.path.isfile(prompt_path) :
        st.warning(f"{menu_dropbox}.txt 파일이 없네요. 다시 확인해보세요.")
        return
    
    with open(prompt_path, encoding= "utf-8") as f:
        prompt_txt = f.read()
    #이 부분은 f-string 으로 편하게 하려고 했으나, 파일 읽어오는데에는 힘들다 하여 .format으로 바꿔봄.    
    prompt=prompt_txt.format(completed_text=filled_text)

    #프롬프트 변수화. 3단계에서 완성된 문장 변수를 가져와서 포멧팅으로 삽입
    #f""포멧팅 쓰려니까 외부 파일 동적 템플릿은 사용이 어렵단다... .famat으로 변경
    #제미나이 문법은 그냥 저렇게 하래서 참고함.

    # 구글 비젼 키값은 main에 있다. 이 키값은 gemini 용
    gemini_api_key = st.secrets["default"]["GOOGLE_GEMINI_API_KEY"]
    #이건 모듈화 하기 이전의 독립 실행 조건문인데 그냥 넣어도 상관 없을 것 같아서 살려둠.
    if not gemini_api_key:
        st.warning("GEMINI_API_KEY 가 설정되지 않았습니다.")
        return

    # 실행 버튼을 눌러야지만 생성이 되도록. 역시 제미나이 세부 세팅은 다른 소스 참조함
    if st.button("컨텐츠 생성"):
        with st.spinner("컨텐츠 생성 중입니다... 잠시만 기다려주세요!"):
            genai.configure(api_key=gemini_api_key)
            #pro 모델 말고 넉넉한 flash로
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)

            #아쉽게도 제미나이 문법에는 openai문법에서 쓰던 stream이 지원이 안된단다...
            #스트림 형식으로 뿌려보자.

            #결과값 담을 임시변수 설정
            steam_result = response.text.strip()
            #빈공간에 계속 갱신해야하니까... empty 없으니까 글자 생길때마다 아래 계속 생김.
            ph=st.empty()
            #최종 결과값 변수 선언(서빙그릇)
            last_result =""
            for chunk in steam_result:
                #글자가 생성되는대로 서빙그릇에 바로 담기
                last_result += chunk
                #st.empty()는 같은 자리에 다른 함수를 쓸 수 있다고 하니....
                #그리고 key 값 안넣으면 반복문 안에서 에러가 발생하더라... 지금 강제로 llm 처럼 보이게 하는 것이 공간을 계속 갱신하기 때문에 에어리어별로 고유 번호가 필요함. 안그럼 인지 못함.
                #창 높이도 좀 늘려보고
                #실시간 결과 출력
                ph.text_area( f"{menu_dropbox} 스타일 컨텐츠 생성 결과", value=last_result, height=1000)
                #애니메이션용 지연.
                time.sleep(0.05)
                                                           
            # 필요하다면 세션에도 저장. 혹시 모르니까...
            st.session_state["contents_result"] = last_result
        st.success("컨텐츠 생성 완료!")
