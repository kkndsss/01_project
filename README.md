# 01_project

# 프로젝트 '한지락' 소개

## 1.프로젝트 개요
본 프로젝트 '한지락'은 수기로 쓰여진 고문서를 디지털화하며 어렵게 느껴지는 한문 컨텐츠에 접근을 좀 더 용이하도록 사용자를 돕습니다. 나아가 OCR로 추출된 한문 컨텐츠를 현대적인 컨텐츠로 재창작하여 고문서에 대한 배경지식이 없는 사용자도 해당 문서를 쉽게 이해하도록 돕는 목적으로 제작되었습니다. 

사용자는 제공된 고문서 sample_data 폴더에 준비된 이미지, 그리고 라벨링된 json 파일을 순차적으로 함께 입력합니다. 구글 비전 OCR은 무료사용이 가능하고 다른 로컬 라이브러리에 비해 비교적 정확하나, 아직까지 손글씨 한자의 OCR은 100%의 정확도를 가지기 어렵습니다. 

이를 보완하기 위해 Solar LLM은 두 소스를 비교, 라벨링 데이터의 참조를 받아 더욱 정확하게 원문을 추출/보정합니다. Solar 모델은 OCR에서 추출된 실제 문장 구조와 라벨링된 개별 텍스트를 보완하여 완성된 문장을 반환합니다. 이는 필요한만큼만의 리소스를 사용하려는 의도입니다. 컨텐츠 창작에는 더욱 고급 모델을 사용해야하나 구글 Gemini 2.0 flash가 무료 사용이 가능합니다. 사용자의 비용을 고려, 최대한 무료로 이용할 수 있는 툴들을 사용하기 위해 구동 환경이 복잡해졌습니다. Gemini 2.0 flash는 Soalr-mini가 보정한 컨텐츠를 기반으로 동화, 단편소설, 웹툰 대사 등의 현대적인 컨텐츠로 쉽게 풀이하여 직역에서 느껴지는 거부감을 낮추고 사용자가 해당 한자 컨텐츠를 현대적으로 이해하고 활용할 수 있는 보조도구로 이용되기를 바라는 마음에서 코드를 공개하게 되었습니다. 언어의 장벽, 암호 같은 고문서를 쉽고 재밌게 즐길 수 있는 <한지락>을 소개합니다!

## 2.주요 기능

**OCR:** Google cloud vision ocr을 사용하여 고서 이미지 한자를 가로쓰기 형태로 추출

**정답지 비교:** 각 한자가 정확히 라벨링된 json 파일에서 가로쓰기 형태로 한자 추출

**오인식/누락 보정:** 두 소스를 경량화된 LLM을 이용하여 완성된 문장으로 보정

**현대적 컨텐츠로 변환:** 완성된 문장을 LLM 프롬프트를 이용하여 어린이들도 이해하기 쉬운 동화 형태로 변환


## 3.작동 순서

**main.py:** 스트림릿 프레임워크, 모듈 함수 차례대로 진행

1)run_ocr()

2)run_compare()

3)run_filling()

4)generate_contents()

**ocr_m.py:** run_ocr() 모듈. 이미지 입력 안되면 진행 불가

**compare_m.py:** run_compare() 모듈. json 입력 안되면 진행 불가

**filling_m.py:** run_filling() 모듈. 자동 보완 기능 버튼

**contents_gen_m.py:** generate_contents() 모듈. 컨텐츠 생성 버튼. 최종 결과


## 4.필요 도구

**Python**

**Git**

**Streamlit**

**Upstage Solar:** api키 발급 필요

**Google cloud vision ocr:** json 인증키 발급 필요. 공식 사이트(https://cloud.google.com/vision?hl=ko), 발급 참조글(https://bkyungkeem.tistory.com/40)

**Google Gemini:** Google AI studio에서 발급 필요.


## 5.실행 방법

### 1) 클론

git clone https://github.com/kkndsss/01_project.git

cd 01_project

### 2) 패키지

pip install -r requirements.txt

### 3) 환경변수 .env

GOOGLE_APPLICATION_CREDENTIALS= 구글 클라우드 비전 인증 json 파일 경로

SOLAR_API_KEY=api키

GOOGLE_GEMINI_API_KEY=api키


### 4) 실행

streamlit run main.py

## 6.사용 방법

1)고문서 이미지 입력(sample_data 폴더에 이미지-json 세트 20개 구비)

2)고문서 json 입력

3)'자동수정 실행 버튼' 클릭

4)'컨텐츠 생성' 버튼 클릭 ->결과 출력

## 7.폴더 구조

project_root/
│
├─ main.py                # 실행 코드
├─ README.md              # 프로젝트 설명서
├─ requirements.txt       # 필요한 파이썬 패키지 목록
│
├─ prompts/               # 프롬프트(txt) 파일 폴더
│    └─ 동화.txt
│    └─ 현대시.txt
│    └─ ...
│
├─ modules/               # 기능별 파이썬 모듈 폴더
│    ├─ __init__.py
│    ├─ ocr_m.py
│    ├─ compare_m.py
│    ├─ filling_m.py
│    └─ contents_gen_m.py
│
├─ data/                  # 데이터(샘플, 실험 등)
│    ├─ sample_data/
│    │    └─ ...         # 표준 실습 데이터(정답, 이미지 등)
│    └─ simplemode_data/
│         └─ ...         # 간편모드 테스트 데이터
│
└─ localpy/               # 실험/테스트용 개별 코드 모음
     └─ ...



## 8.최종결과 출력 예시

1)보정 문장


熙周善友蓮

善友堂次金侯韻

亭一號

鳴琴餘暇日城市一閒窩古砌蓮香襲新簷桂影多

鴻遵淸沼上鳥喚暮山阿已結金蘭社應嫌俗士過

鄕飮席上次金侯韻

同人于野秩西東是禮於今博古通豈爲桐鄕多耆

老第緣蜀郡有文翁豆邊迭薦主賓介工祝高颺雅

頌風盡日威儀元不侮九秋佳色映樽中

奉送金侯以修撰還朝

才兼文武廟廊身毛檄曾供匪爲貧紫海幾優鳧泛

舃彤庭忽報鳳含綸名留燕飮承宣地惠遠莊修


2)생성 문장


옛날 옛날 아주 먼 옛날, 희주라는 마을에 연이라는 예쁜 연꽃 정원이 있었어. 그곳은 정말 특별한 곳이었지.

**연꽃 정원 이야기**

연꽃 정원 '정일호'에는 늘 아름다운 거문고 소리가 울려 퍼졌어. 도시에 있지만 마치 숨겨진 보물처럼 조용하고 아늑한 곳이었지. 낡은 돌담 아래 연꽃 향기가 은은하게 퍼지고, 새 지붕 위로는 계수나무 그림자가 드리워져 정말 멋진 풍경을 자랑했어.

어느 날, 맑은 연못 위로 기러기들이 날아오르고, 저녁 해가 질 무렵에는 산골짜기에서 새들이 지저귀는 소리가 들려왔어. 이곳에 사는 사람들은 서로를 아끼고 사랑하는 마음으로 '금란사'라는 모임을 만들어 함께 지냈어. 속세의 시끄러움과는 거리가 먼, 순수하고 아름다운 사람들이었지.

금란사 모임에는 항상 맛있는 음식이 가득했고, 흥겨운 시를 짓는 시간도 가졌어. 특히 김후라는 친구는 시를 정말 잘 지었지. 김후는 넓은 들판을 누비며 세상을 배우고, 옛날 책을 읽으며 지혜를 쌓는 것을 좋아했어. 사람들은 김후를 보며 "역시 김후는 훌륭해!"라고 칭찬했지.

가을이 깊어가는 어느 날, 김후가 임금님을 모시는 중요한 일을 하게 되어 궁궐로 돌아가게 되었어. 사람들은 아쉬운 마음을 담아 김후를 위한 특별한 잔치를 열었어.

"김후! 당신은 글도 잘 쓰고, 무예도 뛰어나 정말 훌륭한 사람이오! 어려운 백성을 위해 힘쓰고, 나라를 위해 큰 일을 해낼 것이오!"

사람들은 김후의 앞날을 축복하며 맛있는 음식을 나누고, 아름다운 노래를 불렀어. 김후 또한 친구들의 따뜻한 마음에 감동하여 눈물을 글썽거렸지.

"친구들, 정말 고맙소! 여러분의 사랑과 응원을 잊지 않고, 언제나 정의롭고 훌륭한 사람이 되도록 노력하겠소!"

김후는 씩씩하게 궁궐로 떠났고, 사람들은 김후가 돌아오기를 기다리며 연꽃 정원에서 변함없이 아름다운 우정을 이어갔다고 해.



<끝>
