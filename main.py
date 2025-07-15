import streamlit as st
from dotenv import load_dotenv
import os
from ocr_m import run_ocr
from compare_m import run_compare
from filling_m import run_filling
from contents_gen_m import generate_contents

#일단 구글 클라우드 인증이 까다로우니까 이거부터
load_dotenv()
#.env에 api.json파일 경로 저장. 그 안에 인증키값 있음. 
API_json_key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = API_json_key_path


#페이지 표시내용.
st.title("한자 고문서 인식 컨텐츠 생성기 -한지락-")
#모듈 순서대로 배치
st.write("qksemtl ekdmatnstjeofh wlsgod")
run_ocr()

run_compare()

run_filling()

generate_contents()


st.write("끝")