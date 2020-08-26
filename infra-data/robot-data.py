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
           where  fecha_recepcion > (select max(fecha_recepcion) 
                                     from polls_ise2_infra) - interval '60 seconds'
           '''
    print("entre al select")       
    print(Q)
    cursor.execute(Q)# where estado = 0
    columns = cursor.description
    df = pd.DataFrame(cursor.fetchall())
    print(df)
    print(columns)

except:
    print('ha ocurrido una excepción Purge 1')
    print("Unexpected error:", sys.exc_info()[0])
    raise    
    
fecha_sistema = []
infrasonido_1 = []
infrasonido_2 = []
infrasonido_3 = []
infrasonido_4 = []
infra_1 = []
infra_2 = []
infra_3 = []
infra_4 = []
linea = 1
for r in df.iterrows():
    fecha_sistema.append(r[1].values[0])
    infrasonido_1.append(r[1].values[1])
    infrasonido_2.append(r[1].values[2])
    infrasonido_3.append(r[1].values[3])
    infrasonido_4.append(r[1].values[4])
    infra_1.append(r[1].values[1]/8971.77326203209)
    infra_2.append(r[1].values[2]/8971.77326203209)
    infra_3.append(r[1].values[3]/8971.77326203209)
    infra_4.append(r[1].values[4]/8971.77326203209)
    number_str = str(linea)
    linea= linea +1

for i in range(1,len(infrasonido_1)-1):
    a = infra_1[i-1]
    c = infra_1[i]
    p = infra_1[i+1]
    if abs(c-a) > 300 and abs(c-p) > 300 and abs(p-a) <25:
        infrasonido_1[i] =   (infrasonido_1[i-1]+infrasonido_1[i+1])/2
        Q= ''' update polls_ise2_infra set infrasonido_1 = '{0}' where fecha_sistema = '{1}'
           '''.format(infrasonido_1[i],fecha_sistema[i])
        print(Q)
        cursor.execute(Q)

    a = infra_2[i-1]
    c = infra_2[i]
    p = infra_2[i+1]
    if abs(c-a) > 300 and abs(c-p) > 300 and abs(p-a) <25:
        infrasonido_2[i] =    (infrasonido_2[i-1]+infrasonido_2[i+1])/2
        Q= ''' update polls_ise2_infra set infrasonido_2 = '{0}' where fecha_sistema = '{1}'
           '''.format(infrasonido_2[i],fecha_sistema[i])
        print(Q)
        cursor.execute(Q)

    a = infra_3[i-1]
    c = infra_3[i]
    p = infra_3[i+1]
    if abs(c-a) > 300 and abs(c-p) > 300 and abs(p-a) <25:
        infrasonido_3[i] =    (infrasonido_3[i-1]+infrasonido_3[i+1])/2
        Q= ''' update polls_ise2_infra set infrasonido_3 = '{0}' where fecha_sistema = '{1}'
           '''.format(infrasonido_3[i],fecha_sistema[i])
        print(Q)
        cursor.execute(Q)

    a = infra_4[i-1]
    c = infra_4[i]
    p = infra_4[i+1]
    if abs(c-a) > 300 and abs(c-p) > 300 and abs(p-a) <25:
        infrasonido_4[i] =   (infrasonido_4[i-1]+infrasonido_4[i+1])/2
        Q= ''' update polls_ise2_infra set infrasonido_4 = '{0}' where fecha_sistema = '{1}'
           '''.format(infrasonido_4[i],fecha_sistema[i])
        print(Q)
        cursor.execute(Q)

con.commit()
con.close()

