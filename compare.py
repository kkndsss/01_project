import streamlit as st
import json

# 파일 경로는 네 환경에 맞게 수정!
upload_json=st.file_uploader("json 파일을 업로드하세요", type="json")

if upload_json is not None :
    data = json.load(upload_json)



# 라벨(한자)만 순서대로 리스트로 추출
    correct_hanja_list = []
    for col in data["Image_Text_Coord"]:
        for char_info in col:
            correct_hanja_list.append(char_info["label"])

    st.subheader("추출 결과:")
    st.text_area("추출 문장", correct_hanja_list)

else : 
    st.warning("json 파일을 먼저 입력해주세요")