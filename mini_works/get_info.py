import requests
from xml.etree import ElementTree as ET
import pandas as pd
import pymysql
import csv
def get_info(name, startDate, endDate):
    code = get_stock_code(name)
    url = f'https://m.stock.naver.com/front-api/external/chart/domestic/notice?symbol={code}&startTime={startDate}&endTime={endDate}&requestType=0'
    data = requests.get(url=url).text
    data = ET.fromstring(data) #데이터를 파싱할 준비
    total_data =  [{'date': i.get('date'), 'information':x.text} for i in data.iter(tag='item') for x in i]
    
    return pd.DataFrame(total_data)

def get_stock_code(name):
    
    df = pd.read_csv("/home/seorin0224/workspace/dataset/data_3729_20250528.csv", encoding="cp949")

    row = df[df['한글 종목약명'] == name]
    if not row.empty:
        return row.iloc[0]['단축코드']
    else:
        return None
    
def set_stock_code(code, s_date, e_date):
    url = f'https://m.stock.naver.com/front-api/external/chart/domestic/info?symbol={code}&requestType=1&startTime={s_date}&endTime={e_date}&timeframe=day'
    conn = pymysql.connect(host="127.0.0.1", user='play', passwd='123', database='sk17', port=3306)
    cur = conn.cursor()
    
    data = requests.get(url=url).text.strip()
    data = eval(data)
    
    sql= "INSERT INTO naver_day_stock VALUES (%s, %s, %s, %s, %s, %s, %s)"
    
    for i in data:
        if i == data[0]:
            pass
        else:
            cur.execute(sql, [code, i[0], i[1], i[2], i[3], i[4], i[5]])
            conn.commit()
            
def get_stock_code():
        sql = "SELECT * FROM naver_day_stock"
        conn = pymysql.connect(host="127.0.0.1", user='play', passwd='123', database='sk17', port=3306)
        cur = conn.cursor()

        
        try:
            with conn.cursor() as cur:
                cur.execute(sql)
                result = cur.fetchall()  # 리스트 형태의 딕셔너리 반환
                df = pd.DataFrame(result)
        finally:
            conn.close()
        return df
    
    
        
    
if __name__=="__main__":
    get_info('000080','20140504','20150728','/home/seorin0224/workspace/')
