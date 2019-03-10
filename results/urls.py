from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('newhome', views.newhome, name='newhome'),
    path('newresults/<int:newresult_id>/', views.newresult, name='newresult'),
    path('check/', views.check, name='check'),
    path('check/compoundone', views.compoundone, name='compoundone'),
    path('check/compoundtwo', views.compoundtwo, name='compoundtwo'),
    path('<int:result_id>/', views.result, name='result')
]