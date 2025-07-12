import os
from google.cloud import vision
import streamlit as st



#타이틀
st.title("구글 OCR")
#스트림릿 이미지 입력


# 업로드 경로및 api 설정
uploaded_file = st.file_uploader("이미지 파일을 선택하세요", type=["png", "jpg", "jpeg", "bmp", "gif"])
json_key_path = r"C:\Users\kknd\Desktop\pymake\sesac\project1\01_project\api.json"
# 인증
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = json_key_path

#이미지 파일을 메모리로 읽어오기
if uploaded_file is not None :
    content = uploaded_file.read()
else : 
    st.warning("이미지를 먼저 입력해주세요")





# OCR 실행
client = vision.ImageAnnotatorClient()
image = vision.Image(content=content)
response = client.document_text_detection(image=image)

# 결과 출력
if response.full_text_annotation:
    text = response.full_text_annotation.text
    st.subheader("인식 결과:")
    st.text_area("인식 문자 결과", text)
    
else:
    st.warning("텍스트 없음")