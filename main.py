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

#1.run_ocr이미지를 넣으면 구글 ocr을 가동하여 안에 있는 한자를 가로쓰기 형태로 인식해서 추출하는 함수 
run_ocr()

#2.원문을 라벨링한 json 파일을 넣으면 정답지 한자를 가로쓰기 형태의 텍스트로 반환
run_compare()

#원래는 이 사이에 ocr과 json에서 추출한 글자의 오류율를 비교하는 모듈을 만드려고 했으나, 자료 형태를 리스트로 하나 더 뽑아야한다는 까다로움과 set 차집합 연산으로는 문장의 띄어쓰기와 순서가 훼손되는 문제를 해결 못하여 일단 보류.

#3.ocr 추출 문장과 json 정답지 추출 문장을 비교해서 ocr에서는 문장의 형태와 줄과 띄어쓰기를 참조하고 json에서는 정답 한자를 참조해서 두 개를 혼합하여 완성된 문장 생성
run_filling()

#4. run_filling()에서 반환된 완성된 문장을 LLM에 넣고 현대적인 컨텐츠(동화버젼)로 재창작
#추후 컨텐츠 형식은 늘려서 프롬프트별로 따로 저장
#추후 rag 기반으로 관련 유형 컨텐츠 형식과 문체를 백터db 기반으로 불러올 예정 
generate_contents()


st.write("끝")