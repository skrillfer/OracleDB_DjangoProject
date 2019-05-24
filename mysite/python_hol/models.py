# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm




class Administrador(models.Model):
    idadministrador = models.BigIntegerField(primary_key=True)
    nickname = models.CharField(max_length=50, blank=True)
    contrasena = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    class Meta:
        managed = False
        db_table = 'administrador'

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=160, blank=True)
    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        managed = False
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=200, blank=True)
    class Meta:
        managed = False
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=256, blank=True)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=60, blank=True)
    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    email = models.CharField(max_length=150, blank=True)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        managed = False
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'

class Cliente(models.Model):
    idcliente = models.BigIntegerField(primary_key=True)
    nit = models.CharField(max_length=50, blank=True)
    nombre = models.CharField(max_length=50, blank=True)
    direccion = models.CharField(max_length=50, blank=True)
    fecha_nacimiento = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'cliente'
    def __unicode__(self):
        return u'{0}'.format(self.nombre)

class ClienteServicio(models.Model):
    idclienteservicio = models.BigIntegerField(primary_key=True)
    idcliente = models.ForeignKey(Cliente, related_name='creator1', db_column='idcliente', blank=True, null=True)
    idservicio = models.ForeignKey('Servicio', related_name='creator2', db_column='idservicio', blank=True, null=True)
    fecha_contrato = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'cliente_servicio'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=400, blank=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    app_label = models.CharField(max_length=200, blank=True)
    model = models.CharField(max_length=200, blank=True)
    class Meta:
        managed = False
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=80)
    session_data = models.TextField(blank=True)
    expire_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'django_session'

class Factura(models.Model):
    idfactura = models.BigIntegerField(primary_key=True)
    idplan = models.BigIntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    total = models.BigIntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'factura'

class Llamada(models.Model):
    idllamada = models.BigIntegerField(primary_key=True)
    idtelefonor = models.BigIntegerField(blank=True, null=True)
    idtelefonod = models.BigIntegerField(blank=True, null=True)
    duracion = models.BigIntegerField(blank=True, null=True)
    fecha_hora_inicio = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'llamada'

class Mensaje(models.Model):
    idmensaje = models.BigIntegerField(primary_key=True)
    numrmensaje = models.BigIntegerField(blank=True, null=True)
    numdmensaje = models.BigIntegerField(blank=True, null=True)
    dia_mensaje = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'mensaje'

class Metadata(models.Model):
    nit = models.CharField(max_length=50, blank=True)
    nombre = models.CharField(max_length=50, blank=True)
    direccion = models.CharField(max_length=50, blank=True)
    fecha_nacimiento = models.CharField(max_length=50, blank=True)
    mensaje_no_envio = models.CharField(max_length=50, blank=True)
    mensaje_fechahoramandado = models.CharField(max_length=50, blank=True)
    servicio_fechacontrato = models.CharField(max_length=50, blank=True)
    tipo_servicio = models.CharField(max_length=50, blank=True)
    telefono_clasificacion = models.CharField(max_length=10, blank=True)
    telefono_limite = models.CharField(max_length=50, blank=True)
    numero = models.CharField(max_length=50, blank=True)
    operadora = models.CharField(max_length=50, blank=True)
    llamada_duracion = models.CharField(max_length=50, blank=True)
    llamada_hora_inicio = models.CharField(max_length=50, blank=True)
    llamada_no_llamada = models.CharField(max_length=50, blank=True)
    internet_velocidad = models.CharField(max_length=50, blank=True)
    class Meta:
        managed = False
        db_table = 'metadata'

class PlanTelefonico(models.Model):
    idplan = models.BigIntegerField(primary_key=True)
    idcliente = models.ForeignKey(Cliente, db_column='idcliente', blank=True, null=True)
    idtelefono = models.ForeignKey('Telefono', db_column='idtelefono', blank=True, null=True)
    limite = models.BigIntegerField(blank=True, null=True)
    clasificacion = models.CharField(max_length=10, blank=True)
    velocidadinternet = models.CharField(max_length=50, blank=True)
    class Meta:
        managed = False
        db_table = 'plan_telefonico'

class Servicio(models.Model):
    idservicio = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True)
    class Meta:
        managed = False
        db_table = 'servicio'
    def __unicode__(self):
        return str(self.nombre)

class Telefono(models.Model):
    idtelefono = models.BigIntegerField(primary_key=True)
    numero = models.BigIntegerField(blank=True, null=True)
    operadora = models.CharField(max_length=50, blank=True)
    class Meta:
        managed = False
        db_table = 'telefono'
    def __unicode__(self):
        return str(self.numero)

class Usuario(models.Model):
    idusuario = models.BigIntegerField(primary_key=True)
    nickname = models.CharField(max_length=50, blank=True)
    contrasena = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    nit = models.CharField(max_length=50, blank=True)
    class Meta:
        managed = False
        db_table = 'usuario'

