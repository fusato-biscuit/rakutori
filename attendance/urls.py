from django.urls import path
from . import views


app_name = 'attendance'
urlpatterns = [
    path('attend/', views.attend, name='attend'),
    path('success/', views.success, name='success'),
    path('output_to_excel/', views.output_to_excel, name='output_to_excel'),
    path('for_attend/', views.For_attendView.as_view(), name='for_attend'), #URL生成用
    path('for_attend/<str:token>/', views.For_attendView.as_view(), name='for_attend'),#URL検証用
]
