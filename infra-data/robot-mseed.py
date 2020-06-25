from __future__ import print_function
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
from obspy import UTCDateTime, read, Trace, Stream


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

    Q = '''select fecha_sistema, infrasonido_1, infrasonido_2, infrasonido_3, infrasonido_4, mpu_axe, mpu_aze, mpu_aye, to_char(fecha_recepcion,'ss.ms') tiempo, to_char(fecha_recepcion, 'ss.ms')||' '||infrasonido_1 || ' '|| infrasonido_2 || ' ' || infrasonido_3 || ' ' || infrasonido_4 infra_d, to_char(fecha_recepcion, 'ss.ms') || ' ' || mpu_axe || ' ' || mpu_aye || ' ' || mpu_aze xyz_d, to_char(fecha_recepcion,'YYYY-MM-DD HH24:MI:SS.MS') fecha_recepcion
     from polls_ise2_infra
where  fecha_recepcion > (select max(fecha_recepcion) from polls_ise2_infra) - interval '30 minutes'
order by fecha_recepcion
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
       
img_array = []
fecha_sistema = []
infrasonido_1 = []
infrasonido_2 = []
infrasonido_3 = []
infrasonido_4 = []
v_infra_1 = ''
mpu_axe = []
mpu_aye = []
mpu_aze = []
tiempo  = []
xyz_data = []
infra_data = []
fecha_recepcion = []
linea = 1
infra_string = ''

for r in df.iterrows():
 #   print('infrasonido_1 {0}'.format(r[1].values[1]))
 #   print('infrasonido_2 {0}'.format(r[1].values[2]))
 #   print('infrasonido_3 {0}'.format(r[1].values[3]))
 #   print('infrasonido_4 {0}'.format(r[1].values[4]))
 #   print('mpu_axe {0}'.format(r[1].values[5]))
 #   print('mpu_aye {0}'.format(r[1].values[6]))
 #   print('mpu_aze {0}'.format(r[1].values[7]))
 #   print('tiempo  {0}'.format(r[1].values[8]))
 #   print('infra_d {0}'.format(r[1].values[9]))
 #   print('xyz_d   {0}'.format(r[1].values[10]))
 #   print('fecha_recepcion {0}'.format(r[1].values[11]))
    fecha_sistema.append(r[1].values[0])
    infrasonido_1.append(r[1].values[1])
    infrasonido_2.append(r[1].values[2])
    infrasonido_3.append(r[1].values[3])
    infrasonido_4.append(r[1].values[4])
    mpu_axe.append(r[1].values[5])
    mpu_aye.append(r[1].values[6])
    mpu_aze.append(r[1].values[7])
    tiempo.append(r[1].values[8])
    infra_data.append(r[1].values[9])
    xyz_data.append(r[1].values[10])
    fecha_recepcion.append(r[1].values[11])
    infra_string = infra_string + str(r[1].values[1])+'\r\n'
#print(infra_string)
infra_npa = np.fromstring(infra_string, dtype='|S1')
#print(infra_npa)
stats = {'network': 'ov', 'station': 'ise2_infra', 'location': '',
         'channel': 'WLZ', 'npts': len(infra_data), 'sampling_rate': 0.018,
         'mseed': {'dataquality': 'D'}}

stats ={'TIMESERIES': 'GI_ISE2INFRA_01_BDF_D', 'sps': 55, 'Format': 'SLIST', 'Type':'INTEGER', 'Units':'Counts'}
# set current time
print(stats)
print(fecha_recepcion[0])
date_time_obj = datetime.strptime(fecha_recepcion[0],'%Y-%m-%d %H:%M:%S.%f')
print(date_time_obj)
stats['starttime'] = UTCDateTime(date_time_obj)
stats['samples'] = len(infra_data)
print(stats)
st = Stream([Trace(data=infra_npa, header=stats)])
print(st)
# write as ASCII file (encoding=0)
st.write("/home/incyt/Documents/infrasonido.mseed", format='MSEED', encoding=0, reclen=256)

con.close()

