from django import forms
import datetime
from python_hol.models import Cliente,ClienteServicio,Servicio,Telefono
from django.contrib.admin import widgets 
from django.contrib.admin.widgets import AdminTimeWidget,AdminDateWidget
import html5.forms.widgets as html5_widgets
from suit.widgets import SuitDateWidget, SuitTimeWidget, SuitSplitDateTimeWidget
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'dateinput', 'readonly':'true'})
#time_widget = forms.widgets.TimeInput(attrs={'class': 'timepicker', 'readonly':'true'})
#time_widget.format = '%I:%M %p'
import cx_Oracle


conn_str='skrillfer/SearsZemansky@localhost:1521/XE'
db_conn = cx_Oracle.connect(conn_str)
cursor = db_conn.cursor()



class clienteForm(forms.Form):
    Transaccion = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    nit = forms.CharField(max_length=50)
    nombre = forms.CharField(max_length=50)
    direccion = forms.CharField(max_length=50)
    fecha_nacimiento = forms.DateField(widget = html5_widgets.DateInput())
    hora_nacimiento = forms.TimeField(widget =  html5_widgets.TimeInput())

class updateClienteForm(forms.Form):
    idcliente = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    nit = forms.CharField()
    nombre = forms.CharField()
    direccion = forms.CharField()
    fecha_nacimiento = forms.CharField()


class InicioSesionForm(forms.Form):
    mensaje = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','style': 'width:250px'}))
    nickname = forms.CharField(max_length=50)
    contrasena = forms.CharField(max_length=50,widget=forms.PasswordInput())

class UsuarioForm(forms.Form):
    mensaje = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','style': 'width:250px'}))
    nickname = forms.CharField(max_length=50)
    contrasena = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    nit = forms.CharField(max_length=50)

class AdministradorForm(forms.Form):
    mensaje = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    nickname = forms.CharField(max_length=50)
    contrasena = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)


class UploadFileForm(forms.Form):
    mensaje = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    title = forms.CharField(label='Path Para Guardar',max_length=250,widget=forms.TextInput(attrs={'style': 'width:250px'}))
    file = forms.FileField()


class clserForm(forms.Form):
    Transaccion = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    cliente = forms.ModelMultipleChoiceField(queryset=Cliente.objects.order_by('idcliente'))
    cliente.help_text = 'Selecciona Un Cliente'
    servicio = forms.ModelMultipleChoiceField(queryset=Servicio.objects.all())
    servicio.help_text = 'Selecciona Un Servicio'
    fecha_contrato = forms.DateField(widget = html5_widgets.DateInput())
    hora_contrato = forms.TimeField(widget =  html5_widgets.TimeInput())


    
class updateClienteServicioForm(forms.Form):
    i_d = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    cliente = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','style': 'width:250px'}))
    servicio = forms.ModelMultipleChoiceField(queryset=Servicio.objects.all())
    servicio.help_text = ''
    fecha_contrato = forms.CharField(widget=forms.TextInput(attrs={'style': 'width:250px'}))


class PlanTelForm(forms.Form):
    NO_OF_HRS = [('1','A'),('2','B'),('3','C'),('4','D')]
    Transaccion = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    cliente = forms.ModelMultipleChoiceField(queryset=Cliente.objects.order_by('idcliente'))
    cliente.help_text = 'Selecciona Un Cliente'
    telefono = forms.ModelMultipleChoiceField(queryset=Telefono.objects.order_by('idtelefono'))
    telefono.help_text = 'Selecciona Un Telefono'
    clasificacion = forms.CharField(widget=forms.Select(choices=NO_OF_HRS), max_length=1)
    limite = forms.CharField(max_length=50)
    velocidad_internet = forms.CharField(max_length=50)



class updatePlanTelForm(forms.Form):
    mensaje = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','style': 'width:250px'}))
    idplan = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','style': 'width:250px'}))
    idcliente = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','style': 'width:250px'}))
    idtelefono = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','style': 'width:250px'}))
    limite = forms.CharField(widget=forms.TextInput(attrs={'style': 'width:250px'}))
    clasificacion = forms.CharField(widget=forms.TextInput(attrs={'style': 'width:250px'}))
    velocidad_internet = forms.CharField(widget=forms.TextInput(attrs={'style': 'width:250px'}))

class Reporte1Form(forms.Form):
    cursor.execute('select DISTINCT  to_char(trunc(FECHA_HORA_INICIO,\'MON\'), \'YYYY\') as anio from   LLAMADA order by to_char(trunc(FECHA_HORA_INICIO,\'MON\'), \'YYYY\')')
    arrayAnios=[]
    contador=1
    fetch= cursor.fetchall()
    for dato in fetch:
	arrayAnios.append((contador,dato[0]))
	contador=contador+1
    cursor.execute('select DISTINCT  to_char(trunc(FECHA_HORA_INICIO,\'MON\'), \'MM\') as anio from   LLAMADA order by to_char(trunc(FECHA_HORA_INICIO,\'MON\'), \'MM\')')
    arrayMeses=[]
    contador=1
    fetch= cursor.fetchall()
    for dato in fetch:
	arrayMeses.append((contador,dato[0]))
	contador=contador+1
    cursor.execute('SELECT DISTINCT  NUMERO FROM PLAN_TELEFONICO \n INNER JOIN TELEFONO \nON TELEFONO.IDTELEFONO=PLAN_TELEFONICO.IDTELEFONO \norder by TELEFONO.NUMERO')
    arrayTel=[]
    contador=1
    fetch= cursor.fetchall()
    for dato in fetch:
	arrayTel.append((contador,dato[0]))
	contador=contador+1
    mensaje = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','style': 'width:350px'}))
    telefono  = forms.ChoiceField(choices=arrayTel)
    telefono.help_text = ''
    meses  = forms.ChoiceField(choices=arrayMeses)
    meses.help_text = ''
    anios  = forms.ChoiceField(choices=arrayAnios)
    anios.help_text = ''


class Reporte2Form(forms.Form):
    mensaje = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','style': 'width:250px'}))
    cliente  = forms.ModelMultipleChoiceField(queryset=Cliente.objects.order_by('idcliente'))
    cliente.help_text = ''

class Reporte4Form(forms.Form):
    cursor.execute('select DISTINCT  to_char(trunc(FECHA_HORA_INICIO,\'MON\'), \'YYYY\') as anio from   LLAMADA order by to_char(trunc(FECHA_HORA_INICIO,\'MON\'), \'YYYY\')')
    arrayAnios=[]
    contador=1
    fetch= cursor.fetchall()
    for dato in fetch:
	arrayAnios.append((contador,dato[0]))
	contador=contador+1
    mensaje = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','style': 'width:250px'}))
    anios  = forms.ChoiceField(choices=arrayAnios)
    anios.help_text = ''



class reporte9Form(forms.Form):
    mensaje = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','style': 'width:250px'}))
    cliente = forms.ModelMultipleChoiceField(queryset=Cliente.objects.order_by('idcliente'))
    cliente.help_text = ''


    #NO_OF_HRS = [('1','A'),('2','B'),('3','C'),('4','D')]
    #arregloT = []
    #contador=1
    #query=Telefono.objects.all()
    #for entry in query:
#	arregloT.append((contador, entry))
#	contador=contador+1
#    queryC=Cliente.objects.all()
#    arregloC = []
#    contador=0
#    for dato in queryC:
#	arregloC.append((contador, dato))
#	contador=contador+1
#    clasificacion = forms.CharField(widget=forms.Select(choices=NO_OF_HRS), max_length=1)

    
