from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'vitrine'

urlpatterns = [
    path('', views.showcase, name='showcase'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('remover', views.remover, name='remover'),
    path('curso/<int:curso>', views.showcase_tipo_curso, name='showcase_tipo_curso'),
    path('tipo/<int:tipo_vaga>', views.showcase_tipo_vaga, name='showcase_tipo_vaga'),
    path('api/vitrine/', views.VitrineList.as_view(), name='vitrine-list'),
    path('api/vitrine/<int:pk>/', views.VitrineDetail.as_view(), name='vitrine-Detail'),
]
