from dotenv import load_dotenv
import os
from google.cloud import vision
import streamlit as st

load_dotenv()

#타이틀
st.title("구글 OCR")
#스트림릿 이미지 입력


# 업로드 경로및 api 설정
uploaded_file = st.file_uploader("이미지 파일을 선택하세요", type=["png", "jpg", "jpeg", "bmp", "gif"])
API_json_key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
# 인증
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = API_json_key_path

#이미지 파일을 메모리로 읽어오기
if uploaded_file is not None :
    content = uploaded_file.read()






    # OCR 실행
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

 

    # 결과 출력 분기. 완성된 문장과 리스트 동시 출력
    if response.full_text_annotation:
        text = response.full_text_annotation.text
        listtext=list(text)
        onlyhanja=[]
        for c in listtext:
            if c != "\n" and c != " ":
                onlyhanja.append(c)
        st.subheader("인식 결과 전체 문장:")
        st.text_area("인식 결과", text)
        st.text(str(onlyhanja))
        
    else:
        st.warning("텍스트 없음")

else : 
    st.warning("이미지를 먼저 입력해주세요")