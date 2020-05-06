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

]
