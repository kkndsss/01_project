import streamlit as st
from google.cloud import vision

#기존 코드 함수화
def run_ocr():
    st.header("1.이미지 OCR 인식")
    st.write("원문 고서 이미지를 넣어주세요")
    uploaded_file = st.file_uploader("고서이미지 형식[png, jpg, jpeg 등등]", type=["png", "jpg", "jpeg", "bmp", "gif"])

    #업로드 파일이 등록되면 아래 if 문을 실행
    if uploaded_file is not None:
        #업로드 파일 읽어와서 content에 저장
        content = uploaded_file.read()
        #구글 ocr 문법 복사
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=content)
        #텍스트 파일 출력해서 response에 저장
        response = client.document_text_detection(image=image)

        #response에 이미지가 들어오면, 즉 True가 되면 d아래를 실행
        if response.full_text_annotation:
            #text 변수에 이미지 글자 저장
            text = response.full_text_annotation.text
            #session_state 해야 다른 모듈에서도 쓸 수 있단다...
            st.session_state['ocr_result'] = text
            #인식결과 출력
            st.text_area("OCR 인식 결과", text)
        #이미지 없으면?    
        else:
            st.write("텍스트 추출 불가")
    #이미지가 안들어오면 경고출력        
    else:
        st.write("이미지 넣으세요.")
