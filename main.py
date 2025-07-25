import streamlit as st
import os
import tempfile
import json
from dotenv import load_dotenv

# --- 인증 함수 정의 ---

def setup_google_credentials():
    # st.write("[디버깅] setup_google_credentials 함수 실행됨")
    try:
        default_dict = st.secrets["default"]
        # st.write("[디버깅] st.secrets[default]=", default_dict)
        cred_json_str = default_dict["GOOGLE_APPLICATION_CREDENTIALS"]
        cred_json_dict = json.loads(cred_json_str)   # 꼭 dict로 변환!
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            json.dump(cred_json_dict, f)
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f.name
            # st.write("[디버깅] 구글 인증 임시파일:", f.name)
            # st.write("[디버깅] 환경변수 값:", os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
    except Exception as e:
        st.warning(f"[경고] st.secrets 인증 실패, .env로 대체")
        load_dotenv()  # <- 이 부분만 except 블록에!
        api_json_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if api_json_path and os.path.exists(api_json_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = api_json_path
        else:
            st.error("구글 인증 정보가 없습니다! st.secrets 또는 .env 설정을 확인하세요.")

# **반드시 모듈 import 전에 실행!**
setup_google_credentials()

# --- 이후는 기존 main.py 내용대로 쭉 이어가기 ---
from modules.ocr_m import run_ocr
from modules.compare_m import run_compare, run_accuracy
from modules.filling_m import run_filling
from modules.contents_gen_m import generate_contents


#과거 인증
# API_json_key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = API_json_key_path

#페이지 표시내용.
st.title("한자 고문서 인식 컨텐츠 생성기")
st.title("-한지락-")
#모듈 순서대로 배치
#모드 분류
st.write("정확도 평가-보정모드/간편 모드 선택")
st.write("간편 모드는 인식률 및 보정을 희생하는 대신, 정답지 json을 넣지 않아도 됩니다. 준비된 사진 이외에 어떤 고문서 이미지도 입력할 수 있습니다!")

#모드 선택버튼 생성
mode = st.radio("작업 방식을 선택하세요", ["정확도 평가 모드(보정o)", "간편 모드(보정x)"])

#모델분기
if mode == "정확도 평가 모드(보정o)":
    st.header("정확도 평가-보정 모드")
    #타입 힌팅은 나중에...
    #1.run_ocr이미지를 넣으면 구글 ocr을 가동하여 안에 있는 한자를 가로쓰기 형태로 인식해서 추출하는 함수 
    run_ocr()
    #2.원문을 라벨링한 json 파일을 넣으면 정답지 한자를 가로쓰기 형태의 텍스트로 반환
    run_compare()
    #3.정답지와의 정확도를 보여주는 함수 호출
    run_accuracy()
    #4.ocr 추출 문장과 json 정답지 추출 문장을 비교해서 ocr에서는 문장의 형태와 줄과 띄어쓰기를 참조하고 json에서는 정답 한자를 참조해서 두 개를 혼합하여 완성된 문장 생성
    run_filling()
    #5. run_filling()에서 반환된 완성된 문장을 LLM에 넣고 현대적인 컨텐츠(동화버젼)로 재창작
    #추후 컨텐츠 형식은 늘려서 프롬프트별로 따로 저장
    #추후 rag 기반으로 관련 유형 컨텐츠 형식과 문체를 백터db 기반으로 불러올 예정 
    generate_contents()
else:
    st.header("간편 모드-정확도 평가 및 보정 x")
    #딱 두개만 가지고 할 예정
    #대신 아무 이미지나 넣어도 가능.
    run_ocr()
    generate_contents()

st.write("재밌으셨나요? 사용해주셔서 감사합니다^^")
st.write("끝!")