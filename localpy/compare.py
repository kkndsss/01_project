import streamlit as st
import json

# 파일 업로드 스트림릿 버젼
upload_json=st.file_uploader("json 파일을 업로드하세요", type="json")

if upload_json is not None :
    data = json.load(upload_json)
   
#한자만 추출, 인덱싱 기반, 변수에 저장 후 줄바꿀 때마다 추가
    hanjas = []
    for col in data["Image_Text_Coord"]:
        for char_info in col:
            row = char_info["bbox"][-2]
            coln = char_info["bbox"][-1]
            label = char_info["label"]
            hanjas.append((row, coln, label))

    # 2. (줄번호, 칸번호) 순서로 정렬
    hanjas.sort()

    # 3. 줄별로 한자들을 이어붙인다
    lines = []
    cur_row = -1      # 현재 줄번호(초기값 -1)
    cur_line = ""     # 한 줄씩 이어붙일 문자열

    for row, coln, label in hanjas:
        if row != cur_row:
            if cur_row != -1:
                lines.append(cur_line)  # 이전 줄 결과 저장
            cur_line = label           # 새 줄 시작 (첫 글자부터)
            cur_row = row
        else:
            cur_line += label          # 같은 줄이면 이어붙임

    lines.append(cur_line)             # 마지막 줄 저장

    # 4. 줄바꿈(\n)으로 합치기
    correct_text = "\n".join(lines)
    st.subheader("현대 가로쓰기 결과 (심플버전)")
    st.text_area("가로쓰기", value=correct_text, height=500)
    st.session_state["correct_text"] = correct_text

else:
    st.warning("json 파일을 먼저 입력해주세요")