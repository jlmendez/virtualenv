import cv2
import numpy as np
import glob
import urllib.request
import pandas as pd
import webbrowser
import psycopg2
import pandas as pd
import sys
from datetime import datetime, timedelta
import os
#api_key = AIzaSyC6LBIi02y4Vq4aB5NiNsknuymsAAXGPFs
#oauth_id = 919362666395-viqenj9icetsq79iud7ct4ejv3j83g96.apps.googleusercontent.com
#secret_client = XKpLLKabM_ZL8f8f4Jggk-4N
url_array = []
    
    #d= datetime.now() - timedelta(hours=48)
    #xmax =datetime.now()


try:
    con = psycopg2.connect(user = "postgres",
                           password = "postgres2020!Incyt",
                           host = "172.17.250.12",
                           port = "5432",
                           database = "iotgis")
    cursor = con.cursor()
    print("me conecté")
except (Exception, psycopg2.Error) as error :
    print("Error while connection to PostgreSQL",error)

    
try:
    now = datetime.now()
    past_time = now - timedelta(seconds = 60)
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    date_time2 = past_time.strftime("%Y-%m-%d %H:%M:%S")

    print(date_time)
    print(date_time2)

    Q = '''select * from polls_ise2_infra
where  fecha_recepcion > (select max(fecha_recepcion) from polls_ise2_infra) - interval '60 seconds' '''
    print("entre al select")       
    print(Q)
    cursor.execute(Q)# where estado = 0
    columns = cursor.description
    df = pd.DataFrame(cursor.fetchall())
    df.to_csv(r'/home/incyt/servicio/uploads/ise2_infra.csv')
    print(df)
    print(columns)

    Q = '''select * from polls_ise1_infra
where  fecha_recepcion > (select max(fecha_recepcion) from polls_ise2_infra) - interval '60 seconds' '''
    print("entre al select")
    print(Q)
    cursor.execute(Q)# where estado = 0
    columns = cursor.description
    df = pd.DataFrame(cursor.fetchall())
    df.to_csv(r'/home/incyt/servicio/uploads/ise1_infra.csv')
    print(df)
    print(columns)
            
except:
    print('ha ocurrido una excepción Purge 1')
    print("Unexpected error:", sys.exc_info()[0])
    raise    
       
    
    
