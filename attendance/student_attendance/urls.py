from django.contrib import admin
from django.urls import path
from student_attendance import views

urlpatterns = [
    path("",views.index,name="index"),
    path("student",views.student,name="student"),
    path("teacher",views.teacher,name="teacher"),
    path("admins",views.admins,name="admins"),
    path("register",views.new,name="register"),
    path("attendance",views.present,name="attend"),
    path("logout",views.logout,name="logout"),
    path("attendlist",views.all_attend,name="list_attend"),
    path("updatelist",views.all_update,name="list_update"),
    path("edit/<str:Lname>",views.editattend),
    path("update/<str:Lname>",views.updateattend),
    path("req",views.req)
]