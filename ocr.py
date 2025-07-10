import os
from google.cloud import vision
import tkinter as tk
from tkinter import filedialog

#이미지 입력
root = tk.Tk()
root.withdraw()

# 설정
image_path = filedialog.askopenfilename(title="이미지 파일을 선택하세요", filetypes=[("이미지 파일", "*.png *.jpg *.jpeg *.bmp *.gif")])
json_key_path = r"C:\Users\kknd\Desktop\pymake\sesac\project1\api.json"

# 인증
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = json_key_path

# OCR 실행
client = vision.ImageAnnotatorClient()
with open(image_path, 'rb') as f:
    content = f.read()

image = vision.Image(content=content)
response = client.document_text_detection(image=image)

# 결과 출력
if response.full_text_annotation:
    text = response.full_text_annotation.text
    print("인식 결과:")
    print(text)
else:
    print("텍스트 없음")