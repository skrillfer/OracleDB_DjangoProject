from django.conf.urls import patterns,url
#from django.conf.urls import url

from python_hol.views import *

urlpatterns = patterns('',

    url(r'^login/',loginUsuario,name='loginUsuario',),
    url(r'^loginAdmin/',loginAdmin,name='loginAdmin',),
    url(r'^registroUsuario/',registroUsuario,name='registroUsuario',),
    url(r'^registroAdmin/',registroAdmin,name='registroAdmin',),
    url(r'^abc_tablas/', abc_tablas,name='abc_tablas',),
    url(r'^upload_file/',upload_file,name='upload_file',),
    url(r'^listarReportes/',listarReportes,name='listarReportes',),
    url(r'^listarReportesU/',listarReportesU,name='listarReportesU',),
    url(r'^clientes/', ListContactView.as_view(),name='cliente-list',),
    url(r'^listacliente_plan/',listacliente_plan,name='listacliente_plan',),
    url(r'^listacliente_servicio/',listacliente_servicio,name='listacliente_servicio',),
    url(r'^create_save_cliente/',create_save_cliente,name='create_save_cliente',),
    url(r'^update_save_cliente/(?P<numcliente>[0-9]+)',update_save_cliente,name='update_save_cliente',),
    url(r'^delete_save_cliente/(?P<numc>[0-9]+)',delete_save_cliente,name='delete_save_cliente',),
    url(r'^create_save_cliente_servicio/',create_save_cliente_servicio,name='create_save_cliente_servicio',),
    url(r'^update_save_cliente_servicio/(?P<numcliente>[0-9]+)',update_save_cliente_servicio,name='update_save_cliente_servicio',),
    url(r'^delete_save_cliente_servicio/(?P<numc>[0-9]+)',delete_save_cliente_servicio,name='delete_save_cliente_servicio',),
    url(r'^create_save_plan_telefonico/',create_save_plan_telefonico,name='create_save_plan_telefonico',),
    url(r'^update_save_plan_telefonico/(?P<numplan>[0-9]+)',update_save_plan_telefonico,name='update_save_plan_telefonico',),
    url(r'^delete_save_plan_telefonico/(?P<numc>[0-9]+)',delete_save_plan_telefonico,name='delete_save_plan_telefonico',),
    url(r'reporte1/',reporte1,name='reporte1',),
    url(r'^metodo_Reporte2/',metodo_Reporte2,name='metodo_Reporte2',),
    url(r'^metodo_Reporte3/',metodo_Reporte3,name='metodo_Reporte3',),
    url(r'^metodo_Reporte4/',metodo_Reporte4,name='metodo_Reporte4',),
    url(r'^metodo_Reporte5/',metodo_Reporte5,name='metodo_Reporte5',),
    url(r'reporte6/',reporte6,name='reporte6',),
    url(r'reporte9/',reporte9,name='reporte9',),
    url(r'reporte10/',reporte10,name='reporte10',),
    url(r'reporte11/',reporte11,name='reporte11',),

)

