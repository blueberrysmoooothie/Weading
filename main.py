
import streamlit as st
import pandas as pd
import datetime as dt
from gsheetsdb import connect
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json


credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ],
)
gc = gspread.authorize(credentials)
gc1 = gc.open("축의금").worksheet('축의금')

def run_query(query):
    conn = connect(credentials=credentials)
    rows = conn.execute(query, headers = 1)
    rows = rows.fetchall()
    conn.close()
    return rows

def load_data():
    #sheet_url = st.secrets["private_gsheets_url"]
    #rows = run_query(f'SELECT * FROM "{sheet_url}"')
    #data = pd.DataFrame(columns = ['이름','관계측','관계','금액', '인원','식권','기타','입력시간'])
    #for row in rows:
    #    data.loc[len(data)] = [row.이름,row.관계측, row.관계,row.금액, row.인원,row.식권,row.기타,row.입력시간]
    gc2 = gc1.get_all_values()
    try:
        data =pd.DataFrame(gc2[1:], columns=gc2[0])
    except:
        data =pd.DataFrame(gc2, columns=gc2[0])
        data = data.reindex(data.index.drop(0))


#    try:
#        localdata = pd.read_csv('./축의금.csv', encoding = 'euc-kr')
#    except:
#        localdata = pd.DataFrame(columns = ['이름','관계측','관계','금액', '인원','식권','기타','입력시간'])
    
    return data


def save_data(data,name, kind_item, relation_item, money, people, tiket,sub_,c_time):

    #sheet_url = st.secrets["public_gsheets_url"]
#    sql = f'INSERT INTO "{sheet_url}" VALUES({name}, {kind_item}, {relation_item}, {money}, {people}, {tiket},{sub_,c_time})'
#    run_query(sql)

    gc1.append_row([name, kind_item, relation_item, money, people, tiket,sub_,c_time])


    data.to_csv('./축의금.csv', index = False,encoding = 'euc-kr')

def convert_df(df):
    return df.to_csv().encode('euc-kr')

def save_log(**text):
    with open('./log_data.txt', 'a') as f:
        f.write(str(text)+'\n')
    



st.title('결혼식 축의금 관리')
name = st.text_input("이름 : ")
col1, col2 = st.columns(2)
with col1: 
    kind_item = st.radio('관계 측',('신부', '신랑', '부모님','기타'))
with col2: 
    relation_item = st.radio('관계',('가족', '직장', '친구', '기타'))

money = int(st.text_input('금액 (만원) : ',value="5"))
people = int(st.slider('인원 : ',0,10, 2))
tiket = int(st.slider('식권 : ',0,10, 2))
sub_ = st.text_input('기타 : ',value="-")
c_time = st.text_input('입력시간 : ',value=str(dt.datetime.now().strftime('%m-%d %H시 %M분 %S초')))
button_pushed = st.button('저장')

data = load_data()
if button_pushed:
    # print([name, kind_item, relation_item, money, people, tiket,sub_,c_time])
    if name != '':
        #data.loc[len(data)] = [name, kind_item, relation_item, money, people, tiket,sub_,c_time]
        save_data(data,name, kind_item, relation_item, money, people, tiket,sub_,c_time)
        data = load_data()
        save_log(tag = 'add',name=name, c_time=c_time)

        #print(data['금액'])

mon = data['금액']
st.text(f"총합 : {sum([int(m) for m in mon])} 만원")

st.dataframe(data)

if len(data):
    csv = convert_df(data)
    
    d = st.download_button('다운로드',csv, file_name = 'weading.csv', mime = 'text/csv')
    if d:
        save_log(tag = 'file down')
# cam = st.camera_input(label='test_input',disabled=False)
# if cam:
#     st.image(cam)