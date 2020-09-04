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


def run():
    url_array = []
    f_orden = 9
    
    try:
        con = psycopg2.connect(user = "postgres",
                               password = "postgres2020!Incyt",
                               host = "172.17.250.12",
                               port = "5432",
                               database = "iotgis")
        cursor = con.cursor()
        #print("me conecté")
    except (Exception, psycopg2.Error) as error:
        print("Error while connection to PostgreSQL",error)

    
    try:
        now = datetime.now()
        past_time = now - timedelta(minutes = 720)
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        date_time2 = past_time.strftime("%Y-%m-%d %H:%M:%S")

        #print(date_time)
        #print(date_time2)

        Q = '''select * from polls_ise2_infra
               where  position ('f-' in mseed_text) =0  
                  and fecha_recepcion > (select max(fecha_recepcion) 
                                     from polls_ise2_infra) - interval '180 seconds'
                  order by fecha_recepcion
            '''

        #print("entre al select")       
        #print(Q)
        cursor.execute(Q)# where estado = 0
        columns = cursor.description
        df = pd.DataFrame(cursor.fetchall())
        #print ('datos DF y columns')
        #print (df)
        #print(df.std())
        df_std = df.std()
        df_mean = df.mean()
        #print(df_mean)
        #print(columns)

        lim_in = df_mean - df_std*2
        lim_su = df_mean + df_std*2
        df_std =   df_std / ((2**24)/(935*2))
        df_mean = df_mean / ((2**24)/(935*2))
        lim_in =   lim_in / ((2**24)/(935*2))
        lim_su =   lim_su / ((2**24)/(935*2))
        #print(' {0} {1} {2} {3}'.format(df_std[1],df_mean[1],lim_in[1],lim_su[1]))
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

    for x in range(f_orden):

        for i in range(1,len(infrasonido_1)-1):
            a = infra_1[i-1]
            c = infra_1[i]
            p = infra_1[i+1]
            if (c-a)!=0 and  (c-p)!=0:
                dif_pa = abs(max((p-a)/(c-a) ,(p-a)/(c-p) ))
            else:
                if (c-a) ==0 and (c-p)!=0:
                    dif_pa = abs((p-a)/(c-p))
                elif (c-a)!=0 and (c-p)==0:
                    dif_pa = abs((p-a)/(c-a))
                else:
                    dif_pa = 0
            if  (abs(c-a) < lim_in[1] or abs(c-a) > lim_su[1]) and (abs(c-p) < lim_in[1] or abs(c-p) > lim_su[1]) and  abs(dif_pa) <0.01:
                infrasonido_1[i] =   (infrasonido_1[i-1]+infrasonido_1[i+1])/2
                Q= ''' update polls_ise2_infra set infrasonido_1 = '{0}', mseed_text = 'f-1,'||mseed_text  where fecha_sistema = '{1}'
                '''.format(infrasonido_1[i],fecha_sistema[i])
                print(Q)
                cursor.execute(Q)

            a = infra_2[i-1]
            c = infra_2[i]
            p = infra_2[i+1]
            if (c-a)!=0 and  (c-p)!=0:
                dif_pa = abs(max((p-a)/(c-a) ,(p-a)/(c-p) ))
            else:
                if (c-a) ==0 and (c-p)!=0:
                    dif_pa = abs((p-a)/(c-p))
                elif (c-a)!=0 and (c-p)==0:
                    dif_pa = abs((p-a)/(c-a))
                else:
                    dif_pa = 0
            if  (abs(c-a) < lim_in[2] or abs(c-a) > lim_su[2]) and (abs(c-p) < lim_in[2] or abs(c-p) > lim_su[2]) and  abs(dif_pa) <0.01:
                infrasonido_2[i] =    (infrasonido_2[i-1]+infrasonido_2[i+1])/2
                Q= ''' update polls_ise2_infra set infrasonido_2 = '{0}', mseed_text = 'f-2,'||mseed_text where fecha_sistema = '{1}'
                '''.format(infrasonido_2[i],fecha_sistema[i])
                print(Q)
                cursor.execute(Q)

            a = infra_3[i-1]
            c = infra_3[i]
            p = infra_3[i+1]
            if (c-a)!=0 and  (c-p)!=0:
                dif_pa = abs(max((p-a)/(c-a) ,(p-a)/(c-p) ))
            else:
                if (c-a) ==0 and (c-p)!=0:
                    dif_pa = abs((p-a)/(c-p))
                elif (c-a)!=0 and (c-p)==0:
                    dif_pa = abs((p-a)/(c-a))
                else:
                    dif_pa = 0
            if  (abs(c-a) < lim_in[3] or abs(c-a) > lim_su[3]) and (abs(c-p) < lim_in[3] or abs(c-p) > lim_su[3]) and  abs(dif_pa) <0.01:
                infrasonido_3[i] =    (infrasonido_3[i-1]+infrasonido_3[i+1])/2
                Q= ''' update polls_ise2_infra set infrasonido_3 = '{0}', mseed_text = 'f-3,'||mseed_text  where fecha_sistema = '{1}'
                '''.format(infrasonido_3[i],fecha_sistema[i])
                print(Q)
                cursor.execute(Q)

            a = infra_4[i-1]
            c = infra_4[i]
            p = infra_4[i+1]
            if (c-a)!=0 and  (c-p)!=0:
                dif_pa = abs(max((p-a)/(c-a) ,(p-a)/(c-p) ))
            else:
                if (c-a) ==0 and (c-p)!=0:
                    dif_pa = abs((p-a)/(c-p))
                elif (c-a)!=0 and (c-p)==0:
                    dif_pa = abs((p-a)/(c-a))
                else:
                    dif_pa = 0
            if  (abs(c-a) < lim_in[4] or abs(c-a) > lim_su[4]) and (abs(c-p) < lim_in[4] or abs(c-p) > lim_su[4]) and  abs(dif_pa) <0.01:
                infrasonido_4[i] =   (infrasonido_4[i-1]+infrasonido_4[i+1])/2
                Q= ''' update polls_ise2_infra set infrasonido_4 = '{0}', mseed_text = 'f-4,'||mseed_text  where fecha_sistema = '{1}'
                '''.format(infrasonido_4[i],fecha_sistema[i])
                print(Q)
                cursor.execute(Q)

        Q= ''' update polls_ise2_infra set mseed_text = 'f-,'||mseed_text  where fecha_sistema = '{0}'
           '''.format(fecha_sistema[i])
        #print(Q)
        cursor.execute(Q)

    con.commit()
    con.close()

while True:
    run()
