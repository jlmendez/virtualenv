import pandas as pd
from datetime import datetime, timedelta 

from math import pi
from django.shortcuts import render, render_to_response
from bokeh.plotting import gridplot, figure, output_file, show #, ColumnDataSource
from bokeh.models import ColumnDataSource, Legend
from bokeh.embed import components
from django.utils import timezone
from bokeh.models import DatetimeTickFormatter

from django.views.decorators.clickjacking import xframe_options_exempt

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import E1MS1, ISE1_INFRA, ISE2_INFRA
# Create your views here.



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

def homepage(request):

#Graph X & Y coordinates
    d= datetime.now() - timedelta(hours=1)

#	data_list = ultimos_datos()
#	frame = pd.DataFrame(data_list)
#	frame.columns= ['fecha_sistema','gxe','gye','gze','axe','aye','aze']
    df = pd.DataFrame(list(ISE2_INFRA.objects.filter(fecha_recepcion__range=(d,datetime.now())).values('fecha_recepcion','infrasonido_1','infrasonido_2','infrasonido_3','infrasonido_4').order_by('fecha_recepcion')))
#    df = pd.DataFrame(list(ISE2_INFRA.objects.all().values('fecha_recepcion','infrasonido_1','infrasonido_2','infrasonido_3','infrasonido_4')))
	
    source = ColumnDataSource(df)
    p1 = figure(title = 'Data Cruda del Sensor 1', x_axis_label = 'Tiempo', y_axis_label = 'Cuentas', x_axis_type='datetime', y_axis_type='log', plot_width = 500, plot_height = 300)
    l1 = p1.line('fecha_recepcion', 'infrasonido_1', source=source, line_width=2, line_alpha=1, line_color="blue")

    p2 = figure(title = 'Data Cruda del Sensor 2', x_axis_label = 'Tiempo', y_axis_label = 'Cuentas', x_axis_type='datetime', y_axis_type='log', plot_width = 500, plot_height = 300)
    l2 = p2.line('fecha_recepcion', 'infrasonido_2', source=source, line_width=2, line_alpha=1, line_color="red")

    p3 = figure(title = 'Data Cruda del Sensor 3', x_axis_label = 'Tiempo', y_axis_label = 'Cuentas', x_axis_type='datetime', y_axis_type='log', plot_width = 500, plot_height = 300)
    l3 = p3.line('fecha_recepcion', 'infrasonido_3', source=source, line_width=2, line_alpha=1, line_color="green")

    p4 = figure(title = 'Data Cruda del Sensor 4', x_axis_label = 'Tiempo', y_axis_label = 'Cuentas', x_axis_type='datetime', y_axis_type='log', plot_width = 500, plot_height = 300)
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
    plot = gridplot([[p1,p2],[p3,p4]])
    script, div = components(plot)
    
    return render_to_response('polls/dash.html', {'script': script, 'div': div})
        

