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

    Q = '''select fecha_sistema, 
                  cast(infrasonido_1/8971.773262 as float) infra_1, 
                  cast(infrasonido_2/8971.773262 as float) infra_2,
                  cast(infrasonido_3/8971.773262 as float) infra_3, 
                  cast(infrasonido_4/8971.773262 as float) infra_4, 
                  mpu_axe, mpu_aze, mpu_aye, 
                  to_char(fecha_recepcion,'ss.ms') tiempo,  
                  to_char(fecha_recepcion,'YYYY-MM-DD HH24:MI:SS.MS') fecha_recepcion,
                  lag(fecha_recepcion) over delta_tiempo as  fecha_recepcion_previa,
                  fecha_recepcion - lag(fecha_recepcion) over delta_tiempo as delta
            from polls_ise2_infra
	    where  fecha_recepcion > (select max(fecha_recepcion) 
                                      from polls_ise2_infra) - interval '12 hours'
            window delta_tiempo as (partition by to_char(fecha_recepcion,'YYYY-MM-DD HH24') order by fecha_recepcion)
            order by fecha_recepcion asc
'''
    print("entre al select")       
    print(Q)
    cursor.execute(Q)# where estado = 0
    print("sali del select")
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
fecha_recepcion = []
fecha_previa = []
delta_fechas = []
linea = 1
linea_fecha = 0
infra_string = ''

print("inicio for")
for r in df.iterrows():

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
    fecha_previa.append(r[1].values[10])
    delta_fechas.append(r[1].values[11])

    if pd.isna(r[1].values[10]) and linea > 1:
        t_header= 'TIMESERIES GI_ISE2I_01_BDF_D, '+str(linea-1) + ' samples, 55 sps, ' + f_date +'T'+f_time +', SLIST, FLOAT, Counts\r\n'
        infra_string = t_header + infra_string
#        print(infra_string)
        # set current time
        text_file = open("mseed.txt","w")
        n = text_file.write(infra_string)
        text_file.close()

        os.system('sudo /virtualenv/ascii2mseed/ascii2mseed /virtualenv/infra-data/mseed.txt -o /home/incyt/servicio/uploads/GI_ISE2I_01_BDF_D_'+f_date +'T'+f_time +'.mseed')
        print(t_header)
        linea = 1
        infra_string = ''

    if pd.isna(r[1].values[10]):
        f_fecha =  fecha_recepcion[len(fecha_recepcion)-1]
        print(fecha_recepcion[len(fecha_recepcion)-1])
        f_date = f_fecha[0:10]
        f_time = f_fecha[11:23]

    if (linea) == 1 or (linea) % 6 ==1:
        v_tab = '      '
    else:
        v_tab = '        '

    infra_string = infra_string + v_tab+ str(r[1].values[1])
    if linea % 6 == 0:
        infra_string = infra_string + '\r\n'
#        print("linea {0}".format(linea))
    linea = linea+1

print("termina for")
#f_fecha =  fecha_recepcion[0]

#f_date = f_fecha[0:10]
#f_time = f_fecha[11:23]

t_header= 'TIMESERIES GI_ISE2I_01_BDF_D, '+str(linea-1) + ' samples, 55 sps, ' + f_date +'T'+f_time +', SLIST, FLOAT, Counts\r\n'
infra_string = t_header + infra_string
# set current time
text_file = open("mseed.txt","w")
n = text_file.write(infra_string)
text_file.close()

os.system('sudo /virtualenv/ascii2mseed/ascii2mseed /virtualenv/infra-data/mseed.txt -o /home/incyt/servicio/uploads/GI_ISE2I_01_BDF_D_'+f_date +'T'+f_time +'.mseed')
print(t_header)
con.close()

