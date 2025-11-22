from django.urls import path
from . import views 

urlpatterns = [
    path('get_question', views.get_question),
    path('check_answer', views.check_answer)
]