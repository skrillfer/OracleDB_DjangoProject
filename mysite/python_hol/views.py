from django.shortcuts import render
import os
from django.conf.urls import  patterns, include, url
#from django.conf.urls.defaults import *
from django.views.generic.list import ListView
from django.shortcuts import render_to_response, render
from django.template import  RequestContext
from forms import *
from django.http import HttpResponse
from python_hol.models import *
from django.utils import timezone
import cx_Oracle
import matplotlib.pyplot as plt

conn_str='skrillfer/SearsZemansky@localhost:1521/XE'
db_conn = cx_Oracle.connect(conn_str)
cursor = db_conn.cursor()

userActual='2'
claveActual='s'

# _____________________________________________________LISTA DE CLIENTES
class ListContactView(ListView):
    model = Cliente	
    template_name='clientes/cliente_list.html'

# _____________________________________________________LISTA DE PLANES TELEFONICOS
class ListaClienteServicioView(ListView):
    model = ClienteServicio	
    template_name='clientes/cliente_servicio_list.html'

# ___________________________________________________CREAR GUARDAR CLIENTES
def create_save_cliente(request):
    if request.method=='GET':
        form=clienteForm(request.GET)
        if form.is_valid():
            nit= request.GET['nit']
	    nombre= request.GET['nombre']
	    direccion= request.GET['direccion']
	    fecha_nacimiento = request.GET['fecha_nacimiento']
	    hora_nacimiento = request.GET['hora_nacimiento']
            fecha_hora= fecha_nacimiento
	    fecha_hora += hora_nacimiento
	    cursor.execute('SELECT * FROM CLIENTE where nit=\''+nit+'\' and nombre=\''+nombre+'\'')
            fecth= cursor.fetchone()
            if cursor.rowcount == 0:	
	    	cursor.execute('insert into CLIENTE values(0,\''+nit+'\',\''+nombre+'\',\''+direccion+'\',TO_TIMESTAMP(\''+fecha_hora+'\',\'YYYY-MM-DD HH24:MI:SS.FF3\'))')
            	db_conn.commit()
	        return render(request, 'PaginaInicio.html')
	    else:
		texto='CLIENTE EXISTENTE'
	        form = clienteForm(initial={'Transaccion': texto})
                return render(request,"clientes/cliente_form.html",{'form':form})

        else:
   	    texto='ingrese los campos'
            form = clienteForm(initial={'Transaccion': texto})
            return render(request,"clientes/cliente_form.html",{'form':form})

#_________________________________________________ ACTUALIZAR GUARDAR CLIENTE
def update_save_cliente(request,numcliente):
    if request.method=='GET':
        form=updateClienteForm(request.GET)
        if form.is_valid():
   	    idcliente = request.GET['idcliente']
            nit = request.GET['nit']
            nombre = request.GET['nombre']
            direccion = request.GET['direccion']
	    fecha_nacimiento = request.GET['fecha_nacimiento']
	    cursor.execute('update CLIENTE set nit= \''+nit+'\', nombre=\''+nombre+'\',direccion=\''+direccion+'\',fecha_nacimiento=TO_TIMESTAMP(\''+fecha_nacimiento+'\',\'YYYY-MM-DD HH24:MI:SS.FF3\') WHERE idcliente ='+idcliente+'')
	    db_conn.commit()  	
	    return render(request, 'PaginaInicio.html')
	else:
	    cursor.execute('SELECT *FROM CLIENTE WHERE idcliente='+numcliente+'')
	    fetch= cursor.fetchone()
	    form= updateClienteForm(initial={'idcliente': fetch[0],'nit': fetch[1],'nombre': fetch[2],'direccion': fetch[3],'fecha_nacimiento': fetch[4]})
	    return render(request,"clientes/cliente_form_update.html",{'form':form})
            
#_________________________________________________ ELIMINAR  CLIENTE
def delete_save_cliente(request, numc):
    if request.method=='GET':
	cursor.execute('DELETE FROM CLIENTE WHERE idcliente='+numc+'')
	db_conn.commit()
	return render(request,'PaginaInicio.html')

#_________________________________________________ ABC TABLAS DE LA BASE DE DATOS
def abc_tablas(request):
    if request.method=='GET':
	return render(request, 'PaginaInicio.html')
#_________________________________________________ LISTAR REPORTES ADMINISTRADOR
def listarReportes(request):
    if request.method=='GET':
	return render(request,'ListaReportes.html')

#_________________________________________________ LISTAR REPORTES cliente
def listarReportesU(request):
    if request.method=='GET':
	return render(request,'ReportesUsuario.html')

#_________________________________________________ LOGIN-REGISTRO USUARIO
def loginUsuario(request):
    if request.method =='GET':
	form=InicioSesionForm(request.GET)
	if form.is_valid():
	    nickname = request.GET['nickname']
	    contrasena = request.GET['contrasena']
	    cursor.execute('SELECT * FROM USUARIO where nickname=\''+nickname+'\' and contrasena=\''+contrasena+'\'' )
	    fecth= cursor.fetchone()
            if cursor.rowcount > 0:
	       global userActual
	       userActual = nickname
	       global claveActual
	       claveActual = contrasena	
	       return render(request,'ReportesUsuario.html')
            else:
		texto='USUARIO/CONTRASENA INCORRECTOS'
	        form = InicioSesionForm(initial={'mensaje': texto})
                return render(request,"Login.html",{'form':form}) 
	else:
	    texto='INGRESE USUARIO/CONTRASENA'
	    form = InicioSesionForm(initial={'mensaje': texto})
            return render(request,"Login.html",{'form':form}) 

def registroUsuario(request):
    if request.method =='GET':
	form=UsuarioForm(request.GET)
	if form.is_valid():
	    nickname = request.GET['nickname']
	    contrasena = request.GET['contrasena']
	    email = request.GET['email']
	    nit = request.GET['nit']
            cursor.execute('SELECT * FROM USUARIO where nickname=\''+nickname+'\'' )
            fecth= cursor.fetchone()
            if cursor.rowcount == 0:
		cursor.execute('insert into USUARIO values(0,\''+nickname+'\',\''+contrasena+'\',\''+email+'\',\''+nit+'\')')
            	db_conn.commit()
		texto='INGRESE USUARIO/CONTRASENA'
	        form = InicioSesionForm(initial={'mensaje': texto})
                return render(request,"Login.html",{'form':form}) 
	    else:
		texto='NICKNAME EXISTENTE INGRESE OTRO'
	        form = UsuarioForm(initial={'mensaje': texto})
                return render(request,"RegistroUsuario.html",{'form':form})
        else:
	    texto='INGRESE SUS DATOS'
	    form = UsuarioForm(initial={'mensaje': texto})
            return render(request,"RegistroUsuario.html",{'form':form}) 

#_________________________________________________ LOGIN-REGISTRO ADMINISTRADOR
def loginAdmin(request):
    if request.method =='GET':
	form=InicioSesionForm(request.GET)
	if form.is_valid():
	    nickname = request.GET['nickname']
	    contrasena = request.GET['contrasena']
	    cursor.execute('SELECT * FROM ADMINISTRADOR where nickname=\''+nickname+'\' and contrasena=\''+contrasena+'\'' )
	    fecth= cursor.fetchone()
            if cursor.rowcount > 0:
	       global userActual
	       userActual = nickname
	       global claveActual
	       claveActual = contrasena	
	       bienvenido='Bienvenido '
	       bienvenido += nickname
	       path='ingrese el path'
	       form=UploadFileForm(initial={'mensaje': bienvenido,'title': path}) 
               return  render(request,'PaginaInicio.html',{'form':form})
            else:
		texto='USUARIO/CONTRASENA INCORRECTOS'
	        form = InicioSesionForm(initial={'mensaje': texto})
                return render(request,"LoginAdmin.html",{'form':form}) 
	else:
	    texto='INGRESE USUARIO/CONTRASENA'
	    form = InicioSesionForm(initial={'mensaje': texto})
            return render(request,"LoginAdmin.html",{'form':form}) 


def registroAdmin(request):
    if request.method =='GET':
	form=AdministradorForm(request.GET)
	if form.is_valid():
	    nickname = request.GET['nickname']
	    contrasena = request.GET['contrasena']
	    email = request.GET['email']
            cursor.execute('SELECT * FROM ADMINISTRADOR where nickname=\''+nickname+'\'' )
            fecth= cursor.fetchone()
            if cursor.rowcount == 0:
		cursor.execute('insert into ADMINISTRADOR values(0,\''+nickname+'\',\''+contrasena+'\',\''+email+'\')')
            	db_conn.commit()
		texto='INGRESE USUARIO/CONTRASENA'
	        form = InicioSesionForm(initial={'mensaje': texto})
                return render(request,"LoginAdmin.html",{'form':form}) 
	    else:
		texto='NICKNAME EXISTENTE INGRESE OTRO'
	        form = AdministradorForm(initial={'mensaje': texto})
                return render(request,"RegistroAdmin.html",{'form':form})
        else:
	    texto='INGRESE SUS DATOS'
	    form = AdministradorForm(initial={'mensaje': texto})
            return render(request,"RegistroAdmin.html",{'form':form}) 

#_________________________________________________ UPLOAD FILE
def upload_file(request): 
    if request.method=='POST': 
        form  = UploadFileForm(request.POST,request.FILES) 
	docfile = request.POST['title']
	handle_uploaded_file(request.FILES['file'],docfile)
	creando_borrandoMetadata()
	llenandoMetadata()
	llenandoTablasCompletas()
        texto= 'cargado exitosamente'
	path='ingrese el path'
        form=UploadFileForm(initial={'mensaje': texto,'title': path}) 
        return  render(request,'PaginaInicio.html',{'form':form})

#enctype="multipart/form-data"
def handle_uploaded_file(f,nombre):
    modificando_ctl(nombre)	
    with open(nombre, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
#----------------------------------------------------------MODIFICANDO CTL
def modificando_ctl(path):
	contenido='OPTIONS (SKIP=1)\n'
	contenido+='load data\n'
	contenido+='  infile \''+path+'\' \n'
        contenido+='  into table metadata \n'
        contenido+='  fields terminated by \',\' optionally enclosed by \'\"\'\n'
        contenido+='(nit CHAR(50),nombre CHAR(50),direccion CHAR(50),fecha_Nacimiento CHAR(50),Mensaje_No_Envio CHAR(50),Mensaje_FechaHoraMandado CHAR(50),Servicio_FechaContrato CHAR(50),Tipo_Servicio CHAR(50),Telefono_Clasificacion CHAR(10),Telefono_Limite CHAR(50),Numero CHAR(50),Operadora CHAR(50),Llamada_Duracion CHAR(50),Llamada_Hora_Inicio CHAR(50),Llamada_No_Llamada CHAR(50),Internet_Velocidad CHAR(50))'
	file = open("/home/fernando/Escritorio/Metadata.ctl", "w")
	file.write(contenido)
	file.close()
#----------------------------------------------------------CREANDO_BORRANDO METADATA CTL
def creando_borrandoMetadata():
	cursor.execute('DROP TABLE METADATA')
        db_conn.commit()
	query='create table METADATA(\n'
	query+='        nit VARCHAR(50),\n'
	query+='	nombre VARCHAR(50),\n'
	query+='	direccion VARCHAR(50),\n'
	query+='	fecha_nacimiento VARCHAR(50),\n'
	query+='	mensaje_no_envio VARCHAR(50),\n'
	query+='	mensaje_fechahoramandado VARCHAR(50),\n'
	query+='	servicio_fechacontrato VARCHAR(50),\n'
	query+='	tipo_servicio VARCHAR(50),\n'
	query+='	telefono_clasificacion VARCHAR(10),\n'
	query+='	telefono_limite VARCHAR(50),\n'	
	query+='	numero VARCHAR(50),\n'
	query+='	operadora VARCHAR(50),\n'
	query+='	llamada_duracion VARCHAR(50),\n'
	query+='	llamada_hora_inicio VARCHAR(50),\n'
	query+='	llamada_no_llamada VARCHAR(50),\n'
	query+='	internet_velocidad VARCHAR(50)\n)'
	cursor.execute(query)
        db_conn.commit()	

def llenandoMetadata():
	os.system("cd /home/fernando/Escritorio \n ./ejecutable.sh")

	
def llenandoTablasCompletas():
	cursor.execute('DELETE FROM CLIENTE_SERVICIO')
	cursor.execute('DELETE FROM PLAN_TELEFONICO')
	cursor.execute('DELETE FROM TELEFONO')
	cursor.execute('DELETE FROM LLAMADA')
	cursor.execute('DELETE FROM MENSAJE')
	cursor.execute('DELETE FROM HISTORIAL_LLAMADA')
	cursor.execute('DELETE FROM HISTORIAL_MENSAJE')
	cursor.execute('DELETE FROM CLIENTE')
        db_conn.commit()
	cursor.callproc('CARGARCLIENTES')
	cursor.callproc('CARGARTELEFONOS')
	cursor.callproc('CARGAR_MENSAJES')
	cursor.callproc('CARGAR_LLAMADASFINAL')
	cursor.callproc('CARGARCLIENTESERVICIOS')
	cursor.callproc('CARGARPLANESTELEFONICOS')
        db_conn.commit()
#------------------------------------------------LISTA DE CLIENTE_SERVICIO	    
def listacliente_servicio(request):
	if request.method =='GET':
	    htmlI="<html>\n"
	    htmlI+="<head>\n"
	    htmlI+="<link rel=\"stylesheet\" href=\"{{ STATIC_URL }}style.css\">\n"
	    htmlI+="</head>\n"
	    htmlI+="<body bgcolor=\"#3CB371\">\n"
	    htmlI+="<div id=\"content\" style=\"text-align:center;\">\n"
            htmlI+="<h1><a href=\"/create_save_cliente_servicio/\" class=\"addlink\">Agregar Un Nuevo Servicio A Cliente</a></h1>\n"
	    htmlI+="<table id=\"cliente_list_table\" style=\"margin: 0 auto;\" style=\"width:100%\" frame=\"hsides\""
	    htmlI+="rules=\"cols\">\n"		
	    htmlI+="<tr bgcolor=\"#0000FF\">\n"
	    htmlI+="<th>Id</th>\n"
	    htmlI+="<th>Cliente</th>\n"
 	    htmlI+="<th>Servicio</th>\n"
            htmlI+="<th>Fecha Contrato</th>\n"
            htmlI+="<th>Action</th>\n"
            htmlI+="</tr>\n"
	    cursor.execute('SELECT IDCLIENTESERVICIO as a,IDCLIENTE as b,IDSERVICIO as c,FECHA_CONTRATO as d  from CLIENTE_SERVICIO ORDER BY IDCLIENTESERVICIO ')
            fetch= cursor.fetchall()
            for dato in fetch:
		cursor.execute('SELECT nombre,nit FROM CLIENTE WHERE idcliente='+str(dato[1])+'')
	        fetch1= cursor.fetchone()
		cursor.execute('SELECT nombre FROM SERVICIO WHERE idservicio='+str(dato[2])+'')
	        fetch2= cursor.fetchone()
		htmlI+="<tr bgcolor=\"#CDBE70\" align=\"center\">\n"
		htmlI+="<td><a href=\"/update_save_cliente_servicio/"+str(dato[0])+"\" name =\""+str(dato[0])+"\""
		htmlI+=" method=\"get\">"+str(dato[0])+"</a></td>\n"
		htmlI+="<td><a href=\"/vercliente/"+str(dato[1])+"\" name = \""+str(dato[1])+"\""
		htmlI+="method=\"get\">"+fetch1[0]+"-"+fetch1[1]+"</a></td>\n"
		htmlI+="<td><a href=\"/verservicio/"+str(dato[2])+"\" name = \""+str(dato[2])+"\""
		htmlI+=" method=\"get\">"+fetch2[0]+"</a></td>\n"
		htmlI+="<td>"+str(dato[3])+"</td>"
		htmlI+="<td><a href=\"/delete_save_cliente_servicio/"+str(dato[0])+"\">Eliminar</a></td>\n"
		htmlI+="</tr>\n"	
            htmlI +="</table>\n </div> \n</body> \n</html>"
            return HttpResponse(htmlI)

#------------------------------------------------LISTA DE PLAN_TELEFONICO	    
def listacliente_plan(request):
	if request.method =='GET':
	    htmlI="<html>\n"
	    htmlI+="<head>\n"
	    htmlI+="<link rel=\"stylesheet\" href=\"{{ STATIC_URL }}style.css\">\n"
	    htmlI+="</head>\n"
	    htmlI+="<body bgcolor=\"#3CB371\">\n"
	    htmlI+="<div id=\"content\" style=\"text-align:center;\">\n"
            htmlI+="<h1><a href=\"/create_save_plan_telefonico/\" class=\"addlink\">Agregar Un Nuevo Plan Telefonico A Cliente</a></h1>\n"
	    htmlI+="<table id=\"cliente_list_table\" style=\"margin: 0 auto;\" style=\"width:100%\" frame=\"hsides\""
	    htmlI+="rules=\"cols\">\n"		
	    htmlI+="<tr bgcolor=\"#0000FF\">\n"
	    htmlI+="<th>Id</th>\n"
	    htmlI+="<th>Cliente</th>\n"
 	    htmlI+="<th>Telefono</th>\n"
            htmlI+="<th>Limite</th>\n"
            htmlI+="<th>Clasificacion</th>\n"
            htmlI+="<th>VelocidadInternet</th>\n"
            htmlI+="<th>Action</th>\n"
            htmlI+="</tr>\n"
	    cursor.execute('SELECT IDPLAN,IDCLIENTE,IDTELEFONO,LIMITE,CLASIFICACION,VELOCIDADINTERNET  from PLAN_TELEFONICO ORDER BY IDPLAN')
            fetch= cursor.fetchall()
            for dato in fetch:
		cursor.execute('SELECT nombre,nit FROM CLIENTE WHERE idcliente='+str(dato[1])+'')
	        fetch1= cursor.fetchone()
		cursor.execute('SELECT numero FROM TELEFONO WHERE idtelefono='+str(dato[2])+'')
	        fetch2= cursor.fetchone()
		htmlI+="<tr bgcolor=\"#CDBE70\" align=\"center\">\n"
		htmlI+="<td><a href=\"/update_save_plan_telefonico/"+str(dato[0])+"\" name =\""+str(dato[0])+"\""
		htmlI+=" method=\"get\">"+str(dato[0])+"</a></td>\n"
		htmlI+="<td><a href=\"/vercliente/"+str(dato[1])+"\" name = \""+str(dato[1])+"\""
		htmlI+="method=\"get\">"+fetch1[0]+"-"+fetch1[1]+"</a></td>\n"
		htmlI+="<td>"+str(fetch2[0])+"</td>\n"
		htmlI+="<td>"+str(dato[3])+"</td>"
		htmlI+="<td>"+str(dato[4])+"</td>"
		htmlI+="<td>"+str(dato[5])+"</td>"
		htmlI+="<td><a href=\"/delete_save_plan_telefonico/"+str(dato[0])+"\">Eliminar</a></td>\n"
		htmlI+="</tr>\n"	
            htmlI +="</table>\n </div> \n</body> \n</html>"
            return HttpResponse(htmlI)

#________________________________________________________________ABC DE CLIENTE SERVICIO
# ___________________________________________________CREAR GUARDAR CLIENTE SERVICIO
def create_save_cliente_servicio(request):
    if request.method=='GET':
        form=clserForm(request.GET)
        if form.is_valid():
            cliente= request.GET['cliente']
	    servicio= request.GET['servicio']
	    fecha_contrato = request.GET['fecha_contrato']
	    hora_contrato = request.GET['hora_contrato']
	    fechaC=fecha_contrato
	    fechaC+=hora_contrato
	    cursor.execute('SELECT * FROM CLIENTE_SERVICIO where idcliente='+cliente+' and idservicio='+servicio+'  and fecha_contrato=TO_TIMESTAMP(\''+fechaC+'\',\'YYYY-MM-DD HH24:MI:SS.FF3\')')
            fecth= cursor.fetchone()
            if cursor.rowcount == 0:	
	    	cursor.execute('insert into CLIENTE_SERVICIO values(0,'+cliente+','+servicio+',TO_TIMESTAMP(\''+fechaC+'\',\'YYYY-MM-DD HH24:MI:SS.FF3\'))')
                db_conn.commit()
		print('llego hasta aca')
	        return render(request, 'PaginaInicio.html')
	    else:
	        texto='CLIENTE_SERVICIO EXISTENTE'
	        form = clserForm(initial={'Transaccion': texto})
                return render(request,"clientes/cliente_form_servicio.html",{'form':form})
        else:
   	    texto='ingrese los campos'
            form = clserForm(initial={'Transaccion': texto})
            return render(request,"clientes/cliente_form_servicio.html",{'form':form})

#_________________________________________________ ACTUALIZAR GUARDAR CLIENTE SERVICIO
def update_save_cliente_servicio(request,numcliente):
    if request.method=='GET':
        form=updateClienteServicioForm(request.GET)
        if form.is_valid():
            idS     = request.GET['i_d']
   	    cliente = request.GET['cliente']
            servicio = request.GET['servicio']
            cursor.execute('SELECT  *FROM CLIENTE WHERE nombre=\''+cliente+'\'')
	    fetch1=cursor.fetchone()
	    fecha_contrato = request.GET['fecha_contrato']
	    cursor.execute('update CLIENTE_SERVICIO set idservicio='+str(servicio)+',fecha_contrato=TO_TIMESTAMP(\''+fecha_contrato+'\',\'YYYY-MM-DD HH24:MI:SS.FF3\') WHERE idclienteservicio ='+idS+'')
	    db_conn.commit()  	
	    return render(request, 'PaginaInicio.html')
	else:
	    cursor.execute('SELECT *FROM CLIENTE_SERVICIO WHERE idclienteservicio='+numcliente+'')
	    fetch= cursor.fetchone()
            cursor.execute('SELECT nombre FROM CLIENTE WHERE idcliente='+str(fetch[1])+'')
	    fetch1=cursor.fetchone()
	    cursor.execute('SELECT nombre FROM SERVICIO WHERE idservicio='+str(fetch[2])+'')
	    fetch2=cursor.fetchone()
	    form= updateClienteServicioForm(initial={'i_d': fetch[0],'cliente': fetch1[0],'servicio': fetch2[0],'fecha_contrato': fetch[3]})
	    return render(request,"clientes/cliente_form_update_servicio.html",{'form':form})



#_________________________________________________ ELIMINAR  SERVICIO A CLIENTE
def delete_save_cliente_servicio(request, numc):
    if request.method=='GET':
	cursor.execute('DELETE FROM CLIENTE_SERVICIO WHERE idclienteservicio='+numc+'')
	db_conn.commit()
	return render(request,'PaginaInicio.html')


#_______________________________________________________________________________________________________
# ___________________________________________________CREAR GUARDAR PLAN TELEFONICO
def create_save_plan_telefonico(request):
    if request.method=='GET':
        form=PlanTelForm(request.GET)
        if form.is_valid():
            cliente= request.GET['cliente']
	    telefono= request.GET['telefono']
	    clasificacion = request.GET['clasificacion']
	    limite = request.GET['limite']
	    velocidad_internet = request.GET['velocidad_internet']
	    cl=""
	    if clasificacion =="1":
	        cl="A"
	    elif clasificacion=="2":
	        cl="B"
	    elif clasificacion=="3":
	        cl="C"
	    elif clasificacion=="4":
	        cl="D"
	    cursor.execute('SELECT * FROM PLAN_TELEFONICO where idtelefono='+telefono+'')
            fecth= cursor.fetchone()
            if cursor.rowcount == 0:
	    	cursor.execute('insert into PLAN_TELEFONICO values(0,'+cliente+','+telefono+','+limite+',\''+cl+'\','+velocidad_internet+')')
                db_conn.commit()
	        return render(request, 'PaginaInicio.html')
	    else:
	        texto='NUMERO EN PLAN ELIJA OTRO'
	        form = PlanTelForm(initial={'Transaccion': texto})
                return render(request,"planes/plan_form.html",{'form':form})
        else:
   	    texto='ingrese los campos'
            form = PlanTelForm(initial={'Transaccion': texto})
            return render(request,"planes/plan_form.html",{'form':form})


#_________________________________________________ ACTUALIZAR GUARDAR PLAN TELEFONICO
def update_save_plan_telefonico(request,numplan):
    if request.method=='GET':
        form=updatePlanTelForm(request.GET)
        if form.is_valid():
   	    idplan = request.GET['idplan']
   	    limite = request.GET['limite']
   	    clasificacion = request.GET['clasificacion']
            velocidad_internet = request.GET['velocidad_internet']
	    cursor.execute('update PLAN_TELEFONICO set limite='+str(limite)+', clasificacion=\''+clasificacion+'\',VELOCIDADINTERNET=\''+str(velocidad_internet)+'\' WHERE idplan ='+idplan+'')
	    db_conn.commit()  	
	    return render(request, 'PaginaInicio.html')
	else:
            texto='modifique los datos'
	    cursor.execute('SELECT *FROM PLAN_TELEFONICO WHERE idplan='+numplan+'')
	    fetch= cursor.fetchone()
            form= updatePlanTelForm(initial={'mensaje':texto,'idplan': fetch[0],'idcliente': fetch[1],'idtelefono': fetch[2],'limite': fetch[3],'clasificacion': fetch[4],'velocidad_internet': fetch[5]})
	    return render(request,"planes/plan_form_update.html",{'form':form})


#_________________________________________________ ELIMINAR  PLAN TELEFONICO
def delete_save_plan_telefonico(request, numc):
    if request.method=='GET':
	cursor.execute('DELETE FROM PLAN_TELEFONICO WHERE idplan='+numc+'')
	db_conn.commit()
	return render(request,'PaginaInicio.html')



#__________________________________________________METODOS DE LOS REPORTES DE USUARIO_____________________________
def reporte1(request):
    if request.method=='GET':
	form=Reporte1Form(request.GET)
        if form.is_valid():
            telefono = request.GET['telefono']
            meses = request.GET['meses']
            anios = request.GET['anios']

	    cursor.execute('select DISTINCT  to_char(trunc(FECHA_HORA_INICIO,\'MON\'), \'YYYY\') as anio from   LLAMADA order by to_char(trunc(FECHA_HORA_INICIO,\'MON\'), \'YYYY\')')
            arrayAnios=[]
    	    contador=0	
            variable1=''
    	    fetch=cursor.fetchall()
    	    for dato in fetch:
                contador=contador+1	    
		if contador==int(anios):
		   variable1=dato[0]
		   break
 	    cursor.execute('select DISTINCT  to_char(trunc(FECHA_HORA_INICIO,\'MON\'), \'MM\') as anio from   LLAMADA order by to_char(trunc(FECHA_HORA_INICIO,\'MON\'), \'MM\')')
            arrayMeses=[]
    	    contador=0	
            variable2=''
    	    fetch=cursor.fetchall()
    	    for dato in fetch:
                contador=contador+1	    
		if contador==int(meses):
		   variable2=dato[0]
		   break
            cursor.execute('SELECT DISTINCT  NUMERO FROM PLAN_TELEFONICO \n INNER JOIN TELEFONO \nON TELEFONO.IDTELEFONO=PLAN_TELEFONICO.IDTELEFONO \norder by TELEFONO.NUMERO')
            arrayMeses=[]
    	    contador=0	
            variable3=''
    	    fetch=cursor.fetchall()
    	    for dato in fetch:
                contador=contador+1	    
		if contador==int(telefono):
		   variable3=dato[0]
		   break
            cursor.execute('SELECT   IDCLIENTE FROM PLAN_TELEFONICO \nINNER JOIN TELEFONO \nON TELEFONO.IDTELEFONO=PLAN_TELEFONICO.IDTELEFONO\nwhere NUMERO='+str(variable3)+'')
	    idCliente=cursor.fetchone()
            cursor.execute('delete from historial_llamada')
            cursor.execute('drop sequence llamadahistorial_seq')
            db_conn.commit()
            cursor.execute('CREATE SEQUENCE llamadahistorial_seq')
            cursor.callproc("CARGARHISTORIALLLAMADAS", [idCliente[0]])
            cursor.callproc('SETCOSTOMENSUAL')
            cursor.callproc('SETCOSTOANUAL')
            htmlI="<html> \n <head><title>HISTORIAL DE LLAMADAS</title></head>\n"
	    htmlI+="<body  bgcolor=\"#E6E6FA\">\n"
            cursor.execute('select NUMERO,NUMERODESTINO,to_char(trunc(DIA_LLAMADA,\'MON\'),\'YYYY/MM/DD\') as FechaLlamada,COSTOLLAMADA,COSTOMENSUAL  from historial_llamada where  to_char(trunc(DIA_LLAMADA,\'MON\'), \'MM/YYYY\')=\''+variable2+'/'+variable1+'\' and NUMERO='+str(variable3)+' \ngroup by NUMERO,NUMERODESTINO,trunc(DIA_LLAMADA,\'MON\'),COSTOLLAMADA,COSTOMENSUAL')
            fetch= cursor.fetchall()
	    htmlI+="<h1 align=\"center\"><font color=\"#8B4500\"> FACTURA  DE TELEFONO </font></h1>"
	    htmlI+="<h2 align=\"center\"><font color=\"#8B4500\"> FECHA:"+variable2+"/"+variable1+" </font></h1>"
	    htmlI+="<h2 align=\"center\"><font color=\"#8B4500\"> TELEFONO:"+str(variable3)+" </font></h1>"
	    htmlI+="<h1 align=\"center\"><font color=\"#8B4500\"> HISTORIAL  DE LLAMADAS </font></h1>"
            htmlI+="<table align=\"center\" bgcolor=\"#32CD32\">"
	    htmlI+="<tr bgcolor=\"#EEDD82\"> \n<th>NUMERO</th> \n<th>NUMERODESTINO</th> \n<th>FECHA_LLAMADA</th>"
	    htmlI+="\n<th>COSTO_LLAMADA</th>\n"
    	    htmlI+="</tr>\n"
            totalCall=0
	    for dato in fetch:
	    	htmlI+="<tr>\n<td>"+str(dato[0])+"</td> \n<td>"+str(dato[1])+"</td> \n<td>"+str(dato[2])+"</td> \n<td>"+str(dato[3])+"</td> \n"
		htmlI+="</tr> \n"
		totalCall=totalCall+float(dato[3])
	    htmlI+="</table>\n"
            cursor.execute('delete from historial_mensaje')
            cursor.execute('drop sequence mensajehistorial_seq')
            db_conn.commit()
            cursor.execute('CREATE SEQUENCE mensajehistorial_seq')
            cursor.callproc("CARGARHISTORIALMENSAJES", [idCliente[0]])
            cursor.callproc('SETCOSTOMENSUAL_MENSAJE')
            cursor.callproc('SETCOSTOANUAL_MENSAJE')

            htmlI+="<h1 align=\"center\"><font color=\"#8B4500\"> HISTORIAL DE MENSAJES </font></h1>"
            htmlI+="<table align=\"center\" bgcolor=\"#32CD32\">"
	    htmlI+="<tr bgcolor=\"#EEDD82\"> \n<th>NUMERO</th> \n<th>NUMERO_DESTINO</th> \n<th>FECHA_MENSAJE</th>"
	    htmlI+="\n<th>COSTO_MENSAJE</th> \n"
    	    htmlI+="</tr>\n"
            cursor.execute('select Numero,NUMERODESTINO,to_char(trunc(DIA_MENSAJE,\'MON\'),\'YYYY/MM/DD\') as FechaMensaje,COSTOMENSAJE,COSTOMENSUAL from historial_mensaje  where  to_char(trunc(DIA_MENSAJE,\'MON\'), \'MM/YYYY\')=\''+variable2+'/'+variable1+'\' and NUMERO='+str(variable3)+' \ngroup by NUMERO,NUMERODESTINO,trunc(DIA_MENSAJE,\'MON\'),COSTOMENSAJE,COSTOMENSUAL')
            fetch= cursor.fetchall()
            totalMsg=0
            for dato in fetch:
	    	htmlI+="<tr>\n<td>"+str(dato[0])+"</td> \n<td>"+str(dato[1])+"</td> \n<td>"+str(dato[2])+"</td> \n<td>"+str(dato[3])+"</td> \n"
		htmlI+="</tr> \n"
		totalMsg=totalMsg+float(dato[3])
	    htmlI+="</table>\n</body>\n</html>"
	    htmlI+="<h2 align=\"center\"><font color=\"#8B4500\"> TOTAL:"+str(totalCall+totalMsg)+" </font></h1>"
            htmlI+="</body>\n</html>"
            return HttpResponse(htmlI)
	else:
	    texto='Debes Seleccionar El Mes Y Anio y Telefono'
            form = Reporte1Form(initial={'mensaje': texto})
            return render(request,"Reportes/reporte1_form.html",{'form':form})



def metodo_Reporte2(request):
    if request.method=='GET':
	form=Reporte2Form(request.GET)
        if form.is_valid():
            cliente = request.GET['cliente']
            cursor.execute('select nombre from cliente where idcliente='+cliente+'')
	    nombreCliente=cursor.fetchone()
            cursor.execute('delete from historial_llamada')
            cursor.execute('drop sequence llamadahistorial_seq')
            db_conn.commit()
            cursor.execute('CREATE SEQUENCE llamadahistorial_seq')
            cursor.callproc("CARGARHISTORIALLLAMADAS", [cliente])
            cursor.callproc('SETCOSTOMENSUAL')
            cursor.callproc('SETCOSTOANUAL')
            htmlI="<html> \n <head><title>HISTORIAL DE LLAMADAS</title></head>\n"
	    htmlI+="<body  bgcolor=\"#E6E6FA\">\n"
	    htmlI+="<h1 align=\"center\"><font color=\"#8B4500\"> HISTORIAL DE LLAMADAS DE "+nombreCliente[0]+" </font></h1>"
            htmlI+="<table align=\"center\" bgcolor=\"#32CD32\">"
	    htmlI+="<tr bgcolor=\"#EEDD82\"> \n<th>NUMERO</th> \n<th>NUMERODESTINO</th> \n<th>FECHA_LLAMADA</th>"
	    htmlI+="\n<th>COSTO_LLAMADA</th> \n<th>COSTO_MENSUAL</th> \n<th>COSTO_ANUAL</th>\n"
    	    htmlI+="</tr>\n"
            cursor.execute('select NUMERO,NUMERODESTINO,to_char(trunc(DIA_LLAMADA,\'MON\'),\'YYYY/MM/DD\') as FechaLlamada,COSTOLLAMADA,COSTOMENSUAL,COSTOANUAL from historial_llamada group by NUMERO,NUMERODESTINO,trunc(DIA_LLAMADA,\'MON\'),COSTOLLAMADA,COSTOMENSUAL,COSTOANUAL')
            fetch= cursor.fetchall()
            for dato in fetch:
	    	htmlI+="<tr>\n<td>"+str(dato[0])+"</td> \n<td>"+str(dato[1])+"</td> \n<td>"+str(dato[2])+"</td> \n<td>"+str(dato[3])+"</td> \n"
		htmlI+="<td>"+str(dato[4])+"</td> \n <td>"+str(dato[5])+"</td></tr> \n"
	    htmlI+="</table>\n</body>\n</html>"
            return HttpResponse(htmlI)
	else:
	    texto='Debes Seleccionar un Cliente'
            form = Reporte2Form(initial={'mensaje': texto})
            return render(request,"Reportes/reporte2_form.html",{'form':form})
	

def metodo_Reporte3(request):
    if request.method=='GET':
	form=Reporte2Form(request.GET)
        if form.is_valid():
            cliente = request.GET['cliente']
            cursor.execute('select nombre from cliente where idcliente='+cliente+'')
	    nombreCliente=cursor.fetchone()
            cursor.execute('delete from historial_mensaje')
            cursor.execute('drop sequence mensajehistorial_seq')
            db_conn.commit()
            cursor.execute('CREATE SEQUENCE mensajehistorial_seq')
            cursor.callproc("CARGARHISTORIALMENSAJES", [cliente])
            cursor.callproc('SETCOSTOMENSUAL_MENSAJE')
            cursor.callproc('SETCOSTOANUAL_MENSAJE')
            htmlI="<html> \n <head><title>HISTORIAL DE MENSAJE</title></head>\n"
	    htmlI+="<body  bgcolor=\"#E6E6FA\">\n"
	    htmlI+="<h1 align=\"center\"><font color=\"#8B4500\"> HISTORIAL DE MENSAJES DE "+nombreCliente[0]+" </font></h1>"
            htmlI+="<table align=\"center\" bgcolor=\"#32CD32\">"
	    htmlI+="<tr bgcolor=\"#EEDD82\"> \n<th>NUMERO</th> \n<th>NUMERO_DESTINO</th> \n<th>FECHA_MENSAJE</th>"
	    htmlI+="\n<th>COSTO_MENSAJE</th> \n<th>COSTO_MENSUAL</th> \n<th>COSTO_ANUAL</th>\n"
    	    htmlI+="</tr>\n"
            cursor.execute('select Numero,NUMERODESTINO,to_char(trunc(DIA_MENSAJE,\'MON\'),\'YYYY/MM/DD\') as FechaMensaje,COSTOMENSAJE,COSTOMENSUAL,COSTOANUAL from historial_mensaje group by NUMERO,NUMERODESTINO,trunc(DIA_MENSAJE,\'MON\'),COSTOMENSAJE,COSTOMENSUAL,COSTOANUAL')
            fetch= cursor.fetchall()
            for dato in fetch:
	    	htmlI+="<tr>\n<td>"+str(dato[0])+"</td> \n<td>"+str(dato[1])+"</td> \n<td>"+str(dato[2])+"</td> \n<td>"+str(dato[3])+"</td> \n"
		htmlI+="<td>"+str(dato[4])+"</td> \n <td>"+str(dato[5])+"</td></tr> \n"
	    htmlI+="</table>\n</body>\n</html>"
            return HttpResponse(htmlI)
	else:
	    texto='Debes Seleccionar un Cliente'
            form = Reporte2Form(initial={'mensaje': texto})
            return render(request,"Reportes/reporte3_form.html",{'form':form})
	

def metodo_Reporte4(request):
    if request.method=='GET':
	form=Reporte4Form(request.GET)
        if form.is_valid():
            anios = request.GET['anios']
            texto="Anio Seleccionado"
	    cursor.execute('select DISTINCT  to_char(trunc(FECHA_HORA_INICIO,\'MON\'), \'YYYY\') as anio from   LLAMADA order by to_char(trunc(FECHA_HORA_INICIO,\'MON\'), \'YYYY\')')
            arrayAnios=[]
    	    contador=0	
            variable=''
    	    fetch=cursor.fetchall()
    	    for dato in fetch:
                contador=contador+1	    
		if contador==int(anios):
		   variable=dato[0]
		   break
            htmlI="<html> \n <head><title>LLAMADAS EN SISTEMA</title></head>\n"
	    htmlI+="<body  bgcolor=\"#E6E6FA\">\n"
	    htmlI+="<h1 align=\"center\"><font color=\"#8B4500\">LLAMADAS EN SISTEMA DEL "+str(variable)+" </font></h1>"
            htmlI+="<table align=\"center\" bgcolor=\"#32CD32\">"
	    htmlI+="<tr bgcolor=\"#EEDD82\"> \n<th>MES</th> \n<th>DIA</th> \n<th>NUMERO</th>"
	    htmlI+="\n<th>NUMERO_DESTINO</th> \n<th>DURACION</th>\n"
    	    htmlI+="</tr>\n"
            cursor.execute('select to_char(trunc(FECHA_HORA_INICIO,\'MON\'),\'MONTH\') as Mes,to_char(trunc(FECHA_HORA_INICIO,\'MON\'),\'DAY\') as Dia, IDTELEFONOR as Numero, IDTELEFONOD as NumeroDestino, DURACION as Duracion from LLAMADA where to_char(trunc(FECHA_HORA_INICIO,\'MON\'), \'YYYY\')='+variable+'\ngroup by trunc(FECHA_HORA_INICIO,\'MON\'),IDTELEFONOR,IDTELEFONOD,DURACION \norder by trunc(FECHA_HORA_INICIO,\'MON\')')
	    fetch= cursor.fetchall()
            for dato in fetch:
		htmlI+="<tr>\n<td>"+str(dato[0])+"</td> \n<td>"+str(dato[1])+"</td> \n<td>"+str(dato[2])+"</td> \n<td>"+str(dato[3])+"</td> \n"
		htmlI+="<td>"+str(dato[4])+"</td> \n</tr> \n"
	    htmlI+="</table>\n</body>\n</html>"
            return HttpResponse(htmlI)
	else:
	    texto='Debes Seleccionar un Anio'
            form = Reporte4Form(initial={'mensaje': texto})
            return render(request,"Reportes/reporte4_form.html",{'form':form})

def metodo_Reporte5(request):
    if request.method=='GET':
	form=Reporte4Form(request.GET)
        if form.is_valid():
            anios = request.GET['anios']
            texto="Anio Seleccionado"
	    cursor.execute('select DISTINCT  to_char(trunc(FECHA_HORA_INICIO,\'MON\'), \'YYYY\') as anio from   LLAMADA order by to_char(trunc(FECHA_HORA_INICIO,\'MON\'), \'YYYY\')')
            arrayAnios=[]
    	    contador=0	
            variable=''
    	    fetch=cursor.fetchall()
    	    for dato in fetch:
                contador=contador+1	    
		if contador==int(anios):
		   variable=dato[0]
		   break
            htmlI="<html> \n <head><title>LLAMADAS EN SISTEMA</title></head>\n"
	    htmlI+="<body  bgcolor=\"#E6E6FA\">\n"
	    htmlI+="<h1 align=\"center\"><font color=\"#8B4500\">LLAMADAS EN SISTEMA DEL "+str(variable)+" </font></h1>"
            htmlI+="<table align=\"center\" bgcolor=\"#32CD32\">"
	    htmlI+="<tr bgcolor=\"#EEDD82\"> \n<th>MES</th> \n<th>DIA</th> \n<th>NUMERO</th>"
	    htmlI+="\n<th>NUMERO_DESTINO</th>\n"
    	    htmlI+="</tr>\n"
            cursor.execute('select to_char(trunc(DIA_MENSAJE,\'MON\'),\'MONTH\') as Mes,to_char(trunc(DIA_MENSAJE,\'MON\'),\'DAY\') as Dia, NUMRMENSAJE as Numero, NUMDMENSAJE as NumeroDestino \n from MENSAJE where to_char(trunc(DIA_MENSAJE,\'MON\'), \'YYYY\')=\''+str(variable)+'\'\ngroup by trunc(DIA_MENSAJE,\'MON\'),NUMRMENSAJE,NUMDMENSAJE \norder by trunc(DIA_MENSAJE,\'MON\')')
	    fetch= cursor.fetchall()
            for dato in fetch:
		htmlI+="<tr>\n<td>"+str(dato[0])+"</td> \n<td>"+str(dato[1])+"</td> \n<td>"+str(dato[2])+"</td> \n<td>"+str(dato[3])+"</td> \n"
		htmlI+="</tr> \n"
	    htmlI+="</table>\n</body>\n</html>"
            return HttpResponse(htmlI)
	else:
	    texto='Debes Seleccionar un Anio'
            form = Reporte4Form(initial={'mensaje': texto})
            return render(request,"Reportes/reporte5_form.html",{'form':form})



def reporte10(request):
    if request.method=='GET':
            htmlI="<html> \n <head><title>TOP 3 CLIENTES</title></head>\n"
	    htmlI+="<body  bgcolor=\"#E6E6FA\">\n"
	    htmlI+="<h1 align=\"center\"><font color=\"#8B4500\">TOP 3 CLIENTES CON MAS CONTRATOS</font></h1>"
            htmlI+="<table align=\"center\" bgcolor=\"#32CD32\">"
	    htmlI+="<tr bgcolor=\"#EEDD82\"> \n<th>ID_CLIENTE</th> \n<th>NOMBRE</th> \n<th>CANTIDAD</th>"
    	    htmlI+="</tr>\n"
	    cursor.execute('select idCliente,Nombr_e,cantidad from (select CLIENTE_SERVICIO.idCliente, count(CLIENTE_SERVICIO.idCliente) as cantidad, CLIENTE.NOMBRE as Nombr_e \nfrom CLIENTE_SERVICIO \ninner join CLIENTE \n on CLIENTE.idcliente=CLIENTE_SERVICIO.idcliente \n group by CLIENTE_SERVICIO.idCliente,CLIENTE.NOMBRE  \norder by cantidad desc) where rownum < 4')
            fetch= cursor.fetchall()
            for dato in fetch:
		htmlI+="<tr>\n<td>"+str(dato[0])+"</td> \n<td>"+str(dato[1])+"</td> \n<td>"+str(dato[2])+"</td> \n"
		htmlI+="</tr> \n"
	    htmlI+="</table>\n</body>\n</html>"
            return HttpResponse(htmlI)

def reporte11(request):
    if request.method=='GET':
            htmlI="<html> \n <head><title>TOP 3 CLIENTES</title></head>\n"
	    htmlI+="<body  bgcolor=\"#E6E6FA\">\n"
	    htmlI+="<h1 align=\"center\"><font color=\"#8B4500\">TOP 3 CLIENTES CON MAS CONTRATOS AGRUPADO POR ANIO</font></h1>"
            htmlI+="<table align=\"center\" bgcolor=\"#32CD32\">"
	    htmlI+="<tr bgcolor=\"#EEDD82\"> \n<th>ANIO</th> \n<th>ID_CLIENTE</th> \n<th>NOMBRE_CLIENTE</th>  \n<th>NOMBRE_SERVICIO</th>\n<th>CANTIDAD</th>"
    	    htmlI+="</tr>\n"
	    cursor.execute('Select to_char(trunc(CLIENTE_SERVICIO.fecha_contrato,\'MON\'),\'YYYY\') as Anio,CLIENTE_SERVICIO.idcliente,CLIENTE.nombre As NameCliente,SERVICIO.Nombre as ServiceName,count(CLIENTE_SERVICIO.idCliente) as cantidad \nfrom CLIENTE_SERVICIO\ninner join SERVICIO\non SERVICIO.idservicio=CLIENTE_SERVICIO.idservicio\ninner join CLIENTE\non CLIENTE.idcliente=CLIENTE_SERVICIO.idcliente\nwhere CLIENTE_SERVICIO.idcliente IN(select idC from (select CLIENTE_SERVICIO.idCliente as idC, count(CLIENTE_SERVICIO.idCliente) as cantidad, CLIENTE.NOMBRE as Nombr_e\nfrom CLIENTE_SERVICIO\ninner join CLIENTE\non CLIENTE.idcliente=CLIENTE_SERVICIO.idcliente\ngroup by CLIENTE_SERVICIO.idCliente,CLIENTE.NOMBRE\norder by cantidad desc)where rownum < 11)\ngroup by trunc(CLIENTE_SERVICIO.fecha_contrato,\'MON\'),CLIENTE_SERVICIO.idcliente,CLIENTE.nombre,SERVICIO.Nombre\norder by CLIENTE_SERVICIO.idcliente DESC')
            fetch= cursor.fetchall()
            for dato in fetch:
		htmlI+="<tr>\n<td>"+str(dato[0])+"</td> \n<td>"+str(dato[1])+"</td> \n<td>"+str(dato[2])+"</td> \n<td>"+str(dato[3])+"</td> \n<td>"+str(dato[4])+"</td> \n"
		htmlI+="</tr> \n"
	    htmlI+="</table>\n</body>\n</html>"
            return HttpResponse(htmlI)



def reporte9(request):
    if request.method=='GET':
	form=reporte9Form(request.GET)
        if form.is_valid():
		cliente=request.GET['cliente']
            	htmlI="<html> \n <head><title>TOP 3 CLIENTES</title></head>\n"
	    	htmlI+="<body  bgcolor=\"#E6E6FA\">\n"
	    	htmlI+="<h1 align=\"center\"><font color=\"#8B4500\">CONTRATOS DEL CLIENTE</font></h1>"
            	htmlI+="<table align=\"center\" bgcolor=\"#32CD32\">"
	    	htmlI+="<tr bgcolor=\"#EEDD82\"> \n<th>NOMBRE_CLIENTE</th> \n<th>NOMBRE_SERVICIO</th> \n<th>FECHA_CONTRATO</th>"
    	    	htmlI+="</tr>\n"
	    	cursor.execute('SELECT  CLIENTE.NOMBRE, SERVICIO.NOMBRE,CAST(FECHA_CONTRATO AS DATE) FROM CLIENTE_SERVICIO\ninner join SERVICIO \nON SERVICIO.IDSERVICIO=CLIENTE_SERVICIO.IDSERVICIO\ninner join CLIENTE\nON CLIENTE.IDCLIENTE=CLIENTE_SERVICIO.IDCLIENTE\nWHERE CLIENTE.IDCLIENTE='+cliente+'')
            	fetch= cursor.fetchall()
            	for dato in fetch:
			htmlI+="<tr>\n<td>"+str(dato[0])+"</td> \n<td>"+str(dato[1])+"</td> \n<td>"+str(dato[2])+"</td> \n"
			htmlI+="</tr> \n"
	    	htmlI+="</table>\n</body>\n</html>"
            	return HttpResponse(htmlI)
	else:
	        texto='Debes Seleccionar un Cliente'
                form = reporte9Form(initial={'mensaje': texto})
                return render(request,"Reportes/reporte9_form.html",{'form':form})
		


def reporte6(request):
    if request.method=='GET':
	cursor.execute('Select telefono,Dur from(select IDTELEFONOR as telefono,duracion as Dur \nfrom LLAMADA \ngroup by IDTELEFONOR,DURACION\norder by DURACION desc) where ROWNUM<6')
        fetch= cursor.fetchall()
	x_series =[] #[0,1,2,3,4,5]
	y_series =[]# [x**2 for x in x_series]
	#plot the two lines
	for dato in fetch:
		x_series.append(dato[0])
		y_series.append(dato[1])
	plt.plot(x_series, y_series)
	plt.savefig("/home/fernando/mysite/python_hol/templates/Reportes/r6.png")
	try:
    		with open(valid_image, "rb") as f:
        	 	return HttpResponse(f.read(), mimetype="Reportes/r6.png")
	except IOError:
    		red = Image.new('RGBA', (1, 1), (255,0,0,0))
    		response = HttpResponse(mimetype="image/jpeg")
    		red.save(response, "JPEG")
    	        return response
        #return render(request,"Reportes/reporte6.html")
		

