from re import sub
import streamlit as st
import pandas as pd
import datetime as dt
def load_data():
    try:
        data = pd.read_csv('./축의금.csv')
    except:
        data = pd.DataFrame(columns = ['이름','관계 측','관계','금액 (천원)', '인원','식권','기타','입력시간'])
    return data
def save_data(data):
    data.to_csv('./축의금.csv', index = False)



st.title('결혼식 축의금 관리')
name = st.text_input("이름 : ")
col1, col2 = st.columns(2)
with col1: 
    kind_item = st.radio('관계 측',('신부', '신랑', '부모님','기타'))
with col2: 
    relation_item = st.radio('관계',('가족', '직장', '친구', '기타'))

money = int(st.text_input('금액 (천원) : ',value="50"))
people = int(st.slider('인원 : ',0,10, 2))
tiket = int(st.slider('식권 : ',0,10, 2))
sub_ = st.text_input('기타 : ',value=" ")
c_time = st.text_input('입력시간 : ',value=str(dt.datetime.now().strftime('%m-%d %H시 %M분 %S초')))
button_pushed = st.button('저장')

data = load_data()
if button_pushed:
    # print([name, kind_item, relation_item, money, people, tiket,sub_,c_time])
    if name != '':
        data.loc[len(data)] = [name, kind_item, relation_item, money, people, tiket,sub_,c_time]
        save_data(data)
        st.text(str(sum(data['금액 (천원)']))+ ' 천원')

st.dataframe(data)


cam = st.camera_input(label='test_input',disabled=False)
if cam:
    st.image(cam)