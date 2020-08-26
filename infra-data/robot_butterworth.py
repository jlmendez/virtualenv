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
from scipy.signal import butter, lfilter
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
                                     from polls_ise2_infra) - interval '180 seconds'
           order by fecha_recepcion
           '''
    print("entre al select")       
    print(Q)
    cursor.execute(Q)# where estado = 0
    columns = cursor.description
    df = pd.DataFrame(cursor.fetchall())
    print ('datos DF y columns')
    print (df)
    print(df.std())
    df_std = df.std()
    df_mean = df.mean()
    print(df_mean)
    print(columns)

    lim_in = df_mean - df_std*2
    lim_su = df_mean + df_std*2
    df_std =   df_std / ((2**24)/(935*2))
    df_mean = df_mean / ((2**24)/(935*2))
    lim_in =   lim_in / ((2**24)/(935*2))
    lim_su =   lim_su / ((2**24)/(935*2))
    print(' {0} {1} {2} {3}'.format(df_std[1],df_mean[1],lim_in[1],lim_su[1]))
except:
    print('ha ocurrido una excepción Purge 1')
    print("Unexpected error:", sys.exc_info()[0])
    raise    
 
#------------------------------------------------------------
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
#------------------------------------------------------------


fecha_sistema = []
infrasonido_1 = []
infrasonido_2 = []
infrasonido_3 = []
infrasonido_4 = []
infra_1 = []
infra_2 = []
infra_3 = []
infra_4 = []
linea = 0
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
    
np_infrasonido_1 = np.array(infrasonido_1)
np_infrasonido_2 = np.array(infrasonido_2)
np_infrasonido_3 = np.array(infrasonido_3)
np_infrasonido_4 = np.array(infrasonido_4)

np_fecha_sis = np.array(fecha_sistema)

np_infra_1 = np.array(infra_1)
np_infra_2 = np.array(infra_2)
np_infra_3 = np.array(infra_3)
np_infra_4 = np.array(infra_4)


def run():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.signal import freqz

    # Sample rate and desired cutoff frequencies (in Hz).
    fs = 55.0
    lowcut = 0.5
    highcut = 25.0

    # Plot the frequency response for a few different orders.
    plt.figure(1)
    plt.clf()
    for order in [3, 6, 9]:
        b, a = butter_bandpass(lowcut, highcut, fs, order=order)
        w, h = freqz(b, a, worN=2000)
        plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)

    plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)],
             '--', label='sqrt(0.5)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid(True)
    plt.legend(loc='best')

    # Filter a noisy signal.
    t = np.linspace(0,linea-1,linea,endpoint=True)
    #t = np_fecha_sis
    x = np_infrasonido_1
    plt.figure(2)
    plt.clf()
    plt.plot(t, np_infrasonido_1, label='Noisy signal')

    y = butter_bandpass_filter(np_infrasonido_1, lowcut, highcut, fs, order=9)
    plt.plot(t, y, label='Filtered signal (%g Hz)' % highcut)
    plt.xlabel('time (seconds)')
    plt.hlines([-a, a], 0, linea-1, linestyles='--')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc='upper left')
    print(x)
    plt.show()

run()
con.close()

