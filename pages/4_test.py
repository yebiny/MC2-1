import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
import cv2
import numpy as np
import datetime


def get_frame_from_url(url):
  cap = cv2.VideoCapture(url)
  loadedImage = None
  while True:
      ret, frame = cap.read()  
      if frame is not None:
        frame = cv2.resize(frame, (300, 200))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        loadedImage = frame
      break
        
  return loadedImage

# 파이어베이스 db에서 정보 가져오기
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)
collection = db.collection("user001")

st.title('저장된 영상 플레이')
date_input = st.date_input(
    "영상을 불러올 날짜를 선택하세요.",
    datetime.date(2023, 1, 1))
st.text(date_input)

for doc in collection.stream():
  doc_id = doc.id
  st.text(f'date input: {date_input.split("-")}')
  st.text(f'doc id: {doc_id.split("_")[:3]}')
  if date_input.split('-') == doc_id.split('_')[:3]:
    st.text('SAME')    
