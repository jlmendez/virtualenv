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
                           database = "hashFiles")
    cursor = con.cursor()
    print("me conecté")
except (Exception, psycopg2.Error) as error :
    print("Error while connection to PostgreSQL",error)

    
try:
    now = datetime.now()
    past_time = now - timedelta(days = 1)
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    date_time2 = past_time.strftime("%Y-%m-%d %H:%M:%S")

    print(date_time)
    print(date_time2)

    Q = '''select path 
           from filecatalog  
           where originalname='final.jpg' 
           and to_char(fecha,'YYYY-MM-DD HH24:MI:SS') between '{0}' and '{1}'
           order by fecha '''.format(date_time2, date_time)
    print("entre al select")       
    print(Q)
    cursor.execute(Q)# where estado = 0
    columns = cursor.description
    df = pd.DataFrame(cursor.fetchall())
    print(df)
    con.close()
            
except:
    print('ha ocurrido una excepción Purge 1')
    print("Unexpected error:", sys.exc_info()[0])
    raise    
       
    
    
img_array = []
linea = 1
for r in df.iterrows():
    #print(r[1].values[0])
    urladdres = r[1].values[0]
    number_str = str(linea)
    urllib.request.urlretrieve(r[1].values[0], '/virtualenv/video-project/img_vf/foto{0}.jpg'.format(number_str.zfill(7))) 
    linea= linea +1

size = (640,480)
for filename in sorted(glob.glob('/virtualenv/video-project/img_vf/*.jpg')):
    img = cv2.imread(filename)
    #print(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
#    out = cv2.VideoWriter('/home/incyt/servicio/uploads/project.avi',cv2.VideoWriter_fourcc(*'XVID'), 5, size)
out = cv2.VideoWriter('/home/incyt/servicio/uploads/project.webm',cv2.VideoWriter_fourcc(*'vp80'), 5, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()    

os.system(' rm /virtualenv/video-project/img_vf/*')
