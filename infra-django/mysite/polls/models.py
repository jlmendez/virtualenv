import datetime
from django.db import models
from django.utils import timezone



class E1MS1(models.Model):
    fecha_sistema = models.DateTimeField(primary_key=True)
    infrasonido_1 = models.FloatField(default=0)
    infrasonido_2 = models.FloatField(default=0)
    infrasonido_3 = models.FloatField(default=0)
    infrasonido_4 = models.FloatField(default=0)
    audible_1 = models.FloatField(default=0)
    mpu_rotx = models.FloatField(default=0)
    mpu_roty = models.FloatField(default=0)
    mpu_rotz = models.FloatField(default=0)
    posicion = models.CharField(max_length=200)
    fecha_recepcion = models.DateTimeField()
    mpu_gxe = models.FloatField(default=0)
    mpu_gye = models.FloatField(default=0)
    mpu_gze = models.FloatField(default=0)
    mpu_axe = models.FloatField(default=0)
    mpu_aye = models.FloatField(default=0)
    mpu_aze = models.FloatField(default=0)

class ISE2_INFRA(models.Model):
    fecha_sistema = models.DateTimeField(primary_key=True)
    infrasonido_1 = models.FloatField(default=0)
    infrasonido_2 = models.FloatField(default=0)
    infrasonido_3 = models.FloatField(default=0)
    infrasonido_4 = models.FloatField(default=0)
    audible_1 = models.FloatField(default=0)
    mpu_rotx = models.FloatField(default=0)
    mpu_roty = models.FloatField(default=0)
    mpu_rotz = models.FloatField(default=0)
    posicion = models.CharField(max_length=200)
    fecha_recepcion = models.DateTimeField()
    mpu_gxe = models.FloatField(default=0)
    mpu_gye = models.FloatField(default=0)
    mpu_gze = models.FloatField(default=0)
    mpu_axe = models.FloatField(default=0)
    mpu_aye = models.FloatField(default=0)
    mpu_aze = models.FloatField(default=0)

class ISE1_INFRA(models.Model):
    fecha_sistema = models.DateTimeField(primary_key=True)
    infrasonido_1 = models.FloatField(default=0)
    infrasonido_2 = models.FloatField(default=0)
    infrasonido_3 = models.FloatField(default=0)
    infrasonido_4 = models.FloatField(default=0)
    audible_1 = models.FloatField(default=0)
    mpu_rotx = models.FloatField(default=0)
    mpu_roty = models.FloatField(default=0)
    mpu_rotz = models.FloatField(default=0)
    posicion = models.CharField(max_length=200)
    fecha_recepcion = models.DateTimeField()
    mpu_gxe = models.FloatField(default=0)
    mpu_gye = models.FloatField(default=0)
    mpu_gze = models.FloatField(default=0)
    mpu_axe = models.FloatField(default=0)
    mpu_aye = models.FloatField(default=0)
    mpu_aze = models.FloatField(default=0)



#class ISE2_INFRA(models.Model):
#	infrasonido_1 = models.FloatField(default=0)
#	infrasonido_2 = models.FloatField(default=0)
#	infrasonido_3 = models.FloatField(default=0)
#	infrasonido_4 = models.FloatField(default=0)
#	infrasonido_5 = models.FloatField(default=0)
#	fecha_recepcion = models.DateTimeField('fecha_captura')

#	def ultimos_datos(self):
#		from django.db import connection
#		result_list = []
#		with connection.cursor() as cursor:
#			cursor.execute("""select * from V_ISE2_INFRA_L2M""")
#			for row in cursor.fetchall():
#				p = self.model(id=row[0], infrasonido_1=row[1], infrasonido_2=row[2], infrasonido_3=row[3], infrasonido_4=row[4], fecha_recepcion=row[5])
#				result_list.append(p)
#		return result_list


#	def __str__(self):
#		return str(self.id)	
	
#	def published_recently(self):
#		return self.fecha_recepcion >= timezone.now() - datetime.timedelta(minutes=1)



