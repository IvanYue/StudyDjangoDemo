"""classManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from app01 import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('class/',views.classes),
    path('addclass/',views.add_class),
    path('delete_class/',views.delete_class),
    path('edit_class/', views.edit_class),

    path('students/',views.students),
    path('addStudent/',views.addStudent),
    path('editStudent/',views.edit_student),
    path('delete_student/',views.deleteStudent),

    path('tearchers/',views.tearchers),
    path('addtearcher/',views.addtearchers),
    path('editTearcher/',views.editTearcher),
    path('deleteTearcher/',views.deleteTearcher),


    #模态框
    ###班级
    path('model_add_class/',views.model_add_class),
    path('model_edit_class/',views.model_edit_class),
    path('model_delete_class/',views.model_delete_class),

    ###学生
    path('model_add_student/', views.model_add_student),
    path('model_edit_student/', views.model_edit_student),
    path('model_delete_student/', views.model_delete_student),

    ###老师
    path('model_add_teacher/', views.model_add_teacher),
    path('get_all_class/',views.get_all_class),


    ###登录
    path('login/',views.login),
    ###注册
    path('register/',views.register),
    
    
    
    ###
    path('layout/',views.layout)

]
