import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
import cv2
import numpy as np
import datetime


def get_frame_from_url(url):
  cap = cv2.VideoCapture(url)
  img = None
  while True:
      ret, frame = cap.read()  
      if frame is not None:
        frame = cv2.resize(frame, (300, 200))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        img = frame
      break
        
  return img

# 파이어베이스 db에서 정보 가져오기
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)
collection = db.collection("user001")


st.title('저장된 영상 플레이')
date_input = st.date_input(
    "영상을 불러올 날짜를 선택하세요.",
    datetime.date(2023, 2, 1))

if st.button("가져오기"):
  started = False
  for doc in collection.stream():
    y, m, d, h, mi, se = doc.id.split('_')
    if str(date_input).split('-') != [y, m, d]: 
      if started: break
      else: continue
    
    started = True
    url = doc.to_dict()["URL"]
    video_img = get_frame_from_url(url)
    
    st.subheader(f'{h}시 {mi}분 {se}초')
    st.image(video_img)
  
  #if st.button('플레이', key=url):
  #  st.text('동영상 넣기')
    
