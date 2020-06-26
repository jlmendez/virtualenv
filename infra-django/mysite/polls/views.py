import pandas as pd
import psycopg2
from datetime import datetime, timedelta 

from math import pi
from django.shortcuts import render, render_to_response
from bokeh.plotting import gridplot, figure, output_file, show #, ColumnDataSource
from bokeh.models import ColumnDataSource, Legend, Range1d
from bokeh.embed import components
from django.utils import timezone
from bokeh.models import DatetimeTickFormatter
from bokeh.io import export_png
from django.views.decorators.clickjacking import xframe_options_exempt

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import E1MS1, ISE1_INFRA, ISE2_INFRA
# Create your views here.

def ultima_foto():
    try:
        con1 = psycopg2.connect(user = "postgres",
                               password = "postgres2020!Incyt",
                               host = "172.17.250.12",
                               port = "5432",
                               database = "hashFiles")
        cursor2 = con1.cursor()
    except:
        print('error de conexión')

    cursor2.execute ("""select path 
                       from filecatalog  
                       where originalname = 'final.jpg'
                       and fecha = (select max(fecha) from filecatalog 
                       where originalname = 'final.jpg')""")
 
    for row in cursor2.fetchone():
            v_datos = row
    v_tag = '<img src="{0}" alt="Imagen IR Volcán de Fuego" width="640" height="480">'.format(v_datos)
    con1.close()
    return v_tag

def ultimos_datos():
    from django.db import connection
    result_list = []
    row_list = []
    with connection.cursor() as cursor:
        cursor.execute("""select  fecha_sistema,  mpu_gxe, mpu_gye, mpu_gze, mpu_axe, mpu_aye, mpu_aze from e1ms1 where fecha_sistema > (current_timestamp - (1 * interval '1 minute')) """)
        for row in cursor.fetchall():
                row_list = [row[0], row[1], row[2], row[3], row[4], row[5], row[6]]
                result_list.append(row_list)
        return result_list

def ultima_fecha(estacion):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("select max(fecha_recepcion) from polls_{0}".format(estacion))
        for DATOS in cursor.fetchone():
            columna =DATOS
            print(columna)
    return columna

def get_data():
    xmax= ultima_fecha('ise1_infra')
    xmax_ise1_infra = xmax
    xmin= xmax - timedelta(seconds=60)
    xmin_ise1_infra = xmin
    df1 = pd.DataFrame(list(ISE1_INFRA.objects.filter(fecha_recepcion__range=(xmin,xmax)).values('fecha_recepcion','infrasonido_1','infrasonido_2','infrasonido_3','infrasonido_4').order_by('fecha_recepcion')))
    df1.infrasonido_1 = df1.infrasonido_1/89771.77326
    df1.infrasonido_2 = df1.infrasonido_2/89771.77326
    df1.infrasonido_3 = df1.infrasonido_3/89771.77326
    df1.infrasonido_4 = df1.infrasonido_4/89771.77326
    
    dfa = df1.infrasonido_1
    df1.infrasonido_1 = dfa.diff()
    dfa = df1.infrasonido_2
    df1.infrasonido_2 = dfa.diff()
    dfa = df1.infrasonido_3
    df1.infrasonido_3 = dfa.diff()
    dfa = df1.infrasonido_4
    df1.infrasonido_4 = dfa.diff()
#------------

    xmax= ultima_fecha('ise2_infra')
    xmax_ise2_infra = xmax
    xmin= xmax - timedelta(seconds=60)
    xmin_ise2_infra = xmin
    df2 = pd.DataFrame(list(ISE2_INFRA.objects.filter(fecha_recepcion__range=(xmin,xmax)).values('fecha_recepcion','infrasonido_1','infrasonido_2','infrasonido_3','infrasonido_4').order_by('fecha_recepcion')))
    print(df2)
    df2.infrasonido_1 = df2.infrasonido_1/89771.77326
    df2.infrasonido_2 = df2.infrasonido_2/89771.77326
    df2.infrasonido_3 = df2.infrasonido_3/89771.77326
    df2.infrasonido_4 = df2.infrasonido_4/89771.77326

    dfa = df2.infrasonido_1
    df2.infrasonido_1 = dfa.diff()
    dfa = df2.infrasonido_2
    df2.infrasonido_2 = dfa.diff()
    dfa = df2.infrasonido_3
    df2.infrasonido_3 = dfa.diff()
    dfa = df2.infrasonido_4
    df2.infrasonido_4 = dfa.diff()
#------------
    xmax= ultima_fecha('e1ms1')
    xmax_e1ms1 = xmax
    xmin= xmax - timedelta(seconds=60)
    xmin_e1ms1 = xmin
    df3 = pd.DataFrame(list(E1MS1.objects.filter(fecha_recepcion__range=(xmin,xmax)).values('fecha_recepcion','infrasonido_1','infrasonido_2','infrasonido_3','infrasonido_4').order_by('fecha_recepcion')))

    df3.infrasonido_1 = df3.infrasonido_1/89771.77326
    df3.infrasonido_2 = df3.infrasonido_2/89771.77326
    df3.infrasonido_3 = df3.infrasonido_3/89771.77326
    df3.infrasonido_4 = df3.infrasonido_4/89771.77326

    dfa = df3.infrasonido_1
    df3.infrasonido_1 = dfa.diff()
    dfa = df3.infrasonido_2
    df3.infrasonido_2 = dfa.diff()
    dfa = df3.infrasonido_3
    df3.infrasonido_3 = dfa.diff()
    dfa = df3.infrasonido_4
    df3.infrasonido_4 = dfa.diff()

    
#------------
    return df1, df2, df3, xmin_ise1_infra, xmax_ise1_infra, xmin_ise2_infra, xmax_ise2_infra, xmin_e1ms1, xmax_e1ms1

def get_plot(df, estacion, xmin, xmax):
    source = ColumnDataSource(df)
    p1 = figure(title = 'Data Sensor 1  al {0}'.format(xmax), x_axis_label = 'Tiempo', y_axis_label = 'Pascales', x_axis_type='datetime', y_axis_type='linear', plot_width = 800, plot_height = 150)
    p1.x_range=Range1d(xmin, xmax)

    l1 = p1.line('fecha_recepcion', 'infrasonido_1', source=source, line_width=2, line_alpha=1, line_color="blue")

    if estacion != 'e1ms1':

        p2 = figure(title = 'Data Sensor 2  al {0}'.format(xmax), x_axis_label = 'Tiempo', y_axis_label = 'Pascales', x_axis_type='datetime', y_axis_type='linear', plot_width = 800, plot_height = 150)
        p2.x_range=Range1d(xmin, xmax)
        l2 = p2.line('fecha_recepcion', 'infrasonido_2', source=source, line_width=2, line_alpha=1, line_color="red")

        p3 = figure(title = 'Data Sensor 3 al {0}'.format(xmax), x_axis_label = 'Tiempo', y_axis_label = 'Pascales', x_axis_type='datetime', y_axis_type='linear', plot_width = 800, plot_height = 150)

        p3.x_range=Range1d(xmin, xmax)

        l3 = p3.line('fecha_recepcion', 'infrasonido_3', source=source, line_width=2, line_alpha=1, line_color="green")

        p4 = figure(title = 'Data Sensor 4  al {0}'.format(xmax), x_axis_label = 'Tiempo', y_axis_label = 'Pascales', x_axis_type='datetime', y_axis_type='linear', plot_width = 800, plot_height = 150)

        p4.x_range=Range1d(xmin, xmax)

        l4 = p4.line('fecha_recepcion', 'infrasonido_4', source=source, line_width=2, line_alpha=1, line_color="orange")

    if estacion != 'e1ms1':
        plot = gridplot([[p1],[p2],[p3],[p4]])
        script, div = components(plot)
        return plot,script,div
    else:
        script, div = components(p1)
        return p1, script,div
        
def homepage(request):
    xmax = ultima_fecha('ise2_infra')
    df1, df2, df3, xmin_ise1_infra, xmax_ise1_infra, xmin_ise2_infra, xmax_ise2_infra, xmin_e1ms1, xmax_e1ms1 = get_data()

    d = xmax - timedelta(seconds=30)
    #d= datetime.now() - timedelta(hours=48)
    #xmax =datetime.now()

    plot1,script1,div1 = get_plot(df1, 'ise1_infra',xmin_ise1_infra, xmax_ise1_infra)
    plot2,script2,div2 = get_plot(df2, 'ise2_infra',xmin_ise2_infra, xmax_ise2_infra)
    plot3,script3,div3 = get_plot(df3, 'e1ms1',     xmin_e1ms1,      xmax_e1ms1)
    xmin =xmax-timedelta(seconds=30)
#	data_list = ultimos_datos()
#	frame = pd.DataFrame(data_list)
#	frame.columns= ['fecha_sistema','gxe','gye','gze','axe','aye','aze']
    df = pd.DataFrame(list(ISE2_INFRA.objects.filter(fecha_recepcion__range=(d,xmax)).values('fecha_recepcion','infrasonido_1','infrasonido_2','infrasonido_3','infrasonido_4').order_by('fecha_recepcion')))

#    df = pd.DataFrame(list(ISE2_INFRA.objects.filter(fecha_recepcion__range=(d,datetime.now())).values('fecha_recepcion','infrasonido_1','infrasonido_2','infrasonido_3','infrasonido_4').order_by('fecha_recepcion')))
#    df = pd.DataFrame(list(ISE2_INFRA.objects.all().values('fecha_recepcion','infrasonido_1','infrasonido_2','infrasonido_3','infrasonido_4')))
	
    source = ColumnDataSource(df)
    p1 = figure(title = 'Data Cruda del Sensor 1  al {0}'.format(xmax), x_axis_label = 'Tiempo', y_axis_label = 'Cuentas', x_axis_type='datetime', y_axis_type='log', plot_width = 500, plot_height = 300)

    p1.x_range=Range1d(xmin, xmax)

    l1 = p1.line('fecha_recepcion', 'infrasonido_1', source=source, line_width=2, line_alpha=1, line_color="blue")
   
    p2 = figure(title = 'Data Cruda del Sensor 2  al {0}'.format(xmax), x_axis_label = 'Tiempo', y_axis_label = 'Cuentas', x_axis_type='datetime', y_axis_type='log', plot_width = 500, plot_height = 300)

    p2.x_range=Range1d(xmin, xmax)

    l2 = p2.line('fecha_recepcion', 'infrasonido_2', source=source, line_width=2, line_alpha=1, line_color="red")

    p3 = figure(title = 'Data Cruda del Sensor 3 al {0}'.format(xmax), x_axis_label = 'Tiempo', y_axis_label = 'Cuentas', x_axis_type='datetime', y_axis_type='log', plot_width = 500, plot_height = 300)

    p3.x_range=Range1d(xmin, xmax)

    l3 = p3.line('fecha_recepcion', 'infrasonido_3', source=source, line_width=2, line_alpha=1, line_color="green")

    p4 = figure(title = 'Data Cruda del Sensor 4  al {0}'.format(xmax), x_axis_label = 'Tiempo', y_axis_label = 'Cuentas', x_axis_type='datetime', y_axis_type='log', plot_width = 500, plot_height = 300)

    p4.x_range=Range1d(xmin, xmax)

    l4 = p4.line('fecha_recepcion', 'infrasonido_4', source=source, line_width=2, line_alpha=1, line_color="orange")


    #plot.xaxis.formatter=DatetimeTickFormatter(
    #hours=["%d %B %Y"],
    #minutes=["%d %B %Y"],
    #days=["%d %B %Y"],
    #months=["%d %B %Y"],
    #years=["%d %B %Y"],
    #)
    #plot.xaxis.major_label_orientation = pi/4
    
    #legend = Legend(items=[
    #("Infrasonido 1", [l1]),
    #("Infrasonido 2", [l2]),
    #("Infrasonido 3", [l3]),
    #("Infrasonido 4", [l4])
    #], location=(0, -30))

    #plot.add_layout(legend, 'right')
    plot = gridplot([[p1],[p2],[p3],[p4]])
    script, div = components(plot)
    img1 = ultima_foto()
    return render_to_response('polls/dash.html', {'script1': script1, 'div1': div1,'script2': script2, 'div2': div2, 'script3': script3, 'div3': div3, 'img1': img1 })
        

