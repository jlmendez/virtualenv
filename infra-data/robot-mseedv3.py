from __future__ import print_function
import cv2
import os
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

    Q = '''select fecha_sistema, 
                  cast(infrasonido_1 as int) infra_1, 
                  cast(infrasonido_2 as int) infra_2,
                  cast(infrasonido_3 as int) infra_3, 
                  cast(infrasonido_4 as int) infra_4, 
                  mpu_axe, mpu_aze, mpu_aye, 
                  to_char(fecha_recepcion,'ss.ms') tiempo,  
                  to_char(fecha_recepcion,'YYYY-MM-DD HH24:MI:SS.MS') fecha_recepcion
            from polls_ise2_infra
            where  fecha_recepcion > (select max(fecha_recepcion) 
                                      from polls_ise2_infra) - interval '1 hours'
            order by fecha_recepcion
        '''
    print("entre al select")       
    print(Q)
    cursor.execute(Q)# where estado = 0
    columns = cursor.description
    df = pd.DataFrame(cursor.fetchall())
#    print(df)
#    print(columns)

            
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
fecha_recepcion = []
linea = 1
infra_string1 = ''
infra_string2 = ''
infra_string3 = ''
infra_string4 = ''

for r in df.iterrows():
    if linea == 1 or linea % 6 ==1:
        v_tab = '      '
    else:
        v_tab = '        '

    fecha_sistema.append(r[1].values[0])
    infrasonido_1.append(r[1].values[1])
    infrasonido_2.append(r[1].values[2])
    infrasonido_3.append(r[1].values[3])
    infrasonido_4.append(r[1].values[4])
    mpu_axe.append(r[1].values[5])
    mpu_aye.append(r[1].values[6])
    mpu_aze.append(r[1].values[7])
    tiempo.append(r[1].values[8])
    fecha_recepcion.append(r[1].values[9])
    infra_string1 = infra_string1 + v_tab+ str(r[1].values[1])
    infra_string2 = infra_string2 + v_tab+ str(r[1].values[2])
    infra_string3 = infra_string3 + v_tab+ str(r[1].values[3])
    infra_string4 = infra_string4 + v_tab+ str(r[1].values[4])

    if linea % 6 == 0:
        infra_string1 = infra_string1 + '\r\n'
        infra_string2 = infra_string2 + '\r\n'
        infra_string3 = infra_string3 + '\r\n'
        infra_string4 = infra_string4 + '\r\n'
    linea = linea+1


f_fecha =  fecha_recepcion[0]

f_date = f_fecha[0:10]
f_time = f_fecha[11:23]
t_header1= 'TIMESERIES GI_ISE2I_01_BDF_D, '+str(len(infrasonido_1)) + ' samples, 55 sps, ' + f_date +'T'+f_time +', SLIST, INTEGER, Counts\r\n'
infra_string1 = t_header1 + infra_string1
# set current time
text_file = open("mseed1.txt","w")
n = text_file.write(infra_string1)
text_file.close()

t_header2= 'TIMESERIES GI_ISE2I_02_BDF_D, '+str(len(infrasonido_2)) + ' samples, 55 sps, ' + f_date +'T'+f_time +', SLIST, INTEGER, Counts\r\n'
infra_string2 = t_header2 + infra_string2
# set current time
text_file = open("mseed2.txt","w")
n = text_file.write(infra_string2)
text_file.close()

t_header3= 'TIMESERIES GI_ISE2I_03_BDF_D, '+str(len(infrasonido_3)) + ' samples, 55 sps, ' + f_date +'T'+f_time +', SLIST, INTEGER, Counts\r\n'
infra_string3 = t_header3 + infra_string3
# set current time
text_file = open("mseed3.txt","w")
n = text_file.write(infra_string3)
text_file.close()

t_header4= 'TIMESERIES GI_ISE2I_04_BDF_D, '+str(len(infrasonido_4)) + ' samples, 55 sps, ' + f_date +'T'+f_time +', SLIST, INTEGER, Counts\r\n'
infra_string4 = t_header4 + infra_string4
# set current time
text_file = open("mseed4.txt","w")
n = text_file.write(infra_string4)
text_file.close()



os.system('sudo /virtualenv/ascii2mseed/ascii2mseed /virtualenv/infra-data/mseed1.txt -o /home/incyt/servicio/uploads/GI_ISE2I_01_BDF_D_'+f_date +'T'+f_time +'.mseed')
print(t_header1)

os.system('sudo /virtualenv/ascii2mseed/ascii2mseed /virtualenv/infra-data/mseed2.txt -o /home/incyt/servicio/uploads/GI_ISE2I_02_BDF_D_'+f_date +'T'+f_time +'.mseed')

os.system('sudo /virtualenv/ascii2mseed/ascii2mseed /virtualenv/infra-data/msee3.txt -o /home/incyt/servicio/uploads/GI_ISE2I_03_BDF_D_'+f_date +'T'+f_time +'.mseed')

os.system('sudo /virtualenv/ascii2mseed/ascii2mseed /virtualenv/infra-data/mseed4.txt -o /home/incyt/servicio/uploads/GI_ISE2I_04_BDF_D_'+f_date +'T'+f_time +'.mseed')

con.close()

