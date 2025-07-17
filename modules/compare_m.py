import streamlit as st
import json
from collections import Counter

def run_compare():
    #제목
    st.header("2.정답지(JSON 파일) 업로드 및 가공")
    #f라벨링된 json 파일 업로드
    upload_json = st.file_uploader("정답지 JSON 파일을 업로드하세요", type="json")

    #입력 확인을 위한 분기
    if upload_json is not None:
        data = json.load(upload_json)

        #꺼내야할 데이터는 리스트 안에 "Image_Text_Coord"라는 키값으로 존재. "Image_Text_Coord": [[{"bbox": [좌표, 좌표, 좌표, 좌표, 줄인덱스, 칸인덱스], "label": "한자"}, {~~}, {~~}], [{},{}~~~~]
        #겉 리스트가 한자 원문 한줄 -> 줄단위
        #그렇다면 키값으로 접근해서 리스트를 뽑아내고 다시 그 안에 bbox 키값의 리스트에서 줄/칸 인텍스를 가져와야 원문 이미지 순서대로 뽑아낼 수 있음.
        hanjas = []
        for x in data["Image_Text_Coord"]:
            for ch in x:
                row = ch["bbox"][-2]
                column = ch["bbox"][-1]
                hanja_1 = ch["label"]
                #순서가 꼬이면 원문 정답이 훼손되므로 튜플화 하여 추가
                hanjas.append((row, column, hanja_1))
        #0,0 부터 순서대로 정렬
        hanjas.sort()


        #자 이제 이거 가로형식으로 바꿔보자...
        #첫글자를 저장하고 같은 줄의 글자를 이어붙이다가, 줄 바꿈이 일어나면 그때 여태껏 이어붙인 문자를 lines 리스트에 텍스트원소로 저장

        lines = []
        #초기 줄 설정
        cur_row = -1
        #아래 변수에 줄단위로 계속 저장될거임.
        cur_line = ""
        #hanjas의 각 튜플 원소를 임시변수에 다시 나열
        for row, column, hanja_1 in hanjas:
            #첫 줄은 0이다. if 조건문 진입
            #줄이 1로 바뀐다? if문 진입
            if row != cur_row:
                #첫 실행은 -1 이므로 아래 if문 append 재끼고
                #현재 row=1, cur_row=0, 아래 if문 진입
                if cur_row != -1:
                    #당연히 -1일리가 없으니 여태껏 0번줄 hanja_1을 붙여넣은 모든 글자를 lines 리스트에 저장 
                    lines.append(cur_line)
                #첫글자 불러와서 변수에 저장
                #첫글자 초기화    
                cur_line = hanja_1
                #이제서야 row=0이 되므로 그 다음부터 아래 else 문으로 가서 계속 글자 추가
                cur_row = row
            #줄이 같을 때는 cur_line에 계속 글자 붙여넣기    
            else:
                cur_line += hanja_1
        #마지막 문자 처리용        
        lines.append(cur_line)
        #정답텍스트 가로 줄바꿈으로 저장
        correct_text = "\n".join(lines)

        #스트림릿 출력
        st.text_area("정답지 가로쓰기 결과 출력", value=correct_text, height=300)
        #모듈화를 위해 결과값을 변수에 저장
        st.session_state["correct_text"] = correct_text
    #json이 안들어오면 동작이 멈추는 것을 방지하고자 ocr 때처럼 문자경고    
    else:
        st.write("JSON 파일을 업로드하세요.")

#정확도 계산기 Counter로 구현
#ocr 모듈과 run_compare함수에서 출력된 텍스트들을 인자로 가져온다.
#가져와서 공백, 탭, 줄바꿈 등, 계산에 방해될 요소를 replace 매소드로 모두 삭제.
#정답지-ocr=틀린 글자
#중복 포함, 두 변수의 모든 글자의 갯수만 따와서 합침
#(정답지 총 글자갯수-틀린 글자/정답지 총 글자갯수)*100 = 정확도
#결과값 반환 
def cal_accuracy(ocr, labeled_json):
    ocr_clean = ocr.replace(' ', '').replace('\n', '')
    labeled_json_clean = labeled_json.replace(' ', '').replace('\n', '')
    count_ocr=Counter(ocr_clean)
    count_labeled_json= Counter(labeled_json_clean)
    missed_hanja= count_labeled_json-count_ocr
    correct_total= sum(count_labeled_json.values())
    wrong_total=sum(missed_hanja.values())
    return ((correct_total-wrong_total)/correct_total)*100



##코랩함수검증용
# ocr="나는이나라의대통령인김재명입니다."
# labeled_json="나는 이 나라의 대통령인 이재명입니다."

# def cal_accuracy(ocr, labeled_json):
#     ocr_clean = ocr.replace(' ', '').replace('\n', '')
#     labeled_json_clean = labeled_json.replace(' ', '').replace('\n', '')
#     count_ocr=Counter(ocr_clean)
#     count_labeled_json= Counter(labeled_json_clean)
#     missed_hanja= count_labeled_json-count_ocr
#     correct_total= sum(count_labeled_json.values())
#     wrong_total=sum(missed_hanja.values())
#     return ((correct_total-wrong_total)/correct_total)*100
# a=cal_accuracy(ocr, labeled_json)
#a
#print(f"정확도는 {a: .2f}%입니다.")

def run_accuracy():
    st.header("OCR 정확도 평가")
    st.write("json 정답지와 비교")
    ocr=st.session_state.get('ocr_result')
    labeled_json=st.session_state.get("correct_text")
    if ocr and labeled_json : 
        acc=cal_accuracy(ocr, labeled_json)
        st.success(f"인식된 OCR의 정확도는 {acc: .2f}%입니다.")
    else:
        st.warning("OCR 값과 정답지 값이 모두 필요합니다. 이전 단계로 돌아가주세요!")
