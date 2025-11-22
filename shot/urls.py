from django.urls import path
from . import views 

urlpatterns = [
    path("", views.Index,  name="Index"),
    path("SubmitAnswer", views.SubmitAnswer, name="SubmitAnswer")
]
