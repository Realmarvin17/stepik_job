"""stepik_job URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.urls import re_path
from django.views.static import serve

from job.views import CompaniesView, my_resume_edit, my_resume_create, my_company_edit, my_company_create, \
    my_vacancy_create, my_vacancy_edit
from job.views import CompanyView
from job.views import MainView
from job.views import MyCompanyView
from job.views import MyLoginView
from job.views import MyResumeView
from job.views import MySignUpView
from job.views import MyVacanciesView
from job.views import SendView
from job.views import SpecializationView
from job.views import VacanciesView
from job.views import VacancyView

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    re_path(r'jobs/(?P<pk>\d+)/$', VacancyView.as_view(), name='vacancy'),
    re_path(r'jobs/(?P<pk>\d+)/send/$', SendView.as_view(), name='send'),
    path('jobs/cat/<str:specialization>', SpecializationView.as_view(), name='specialization'),
    path('companies/', CompaniesView.as_view(), name='companies'),
    path('companies/<int:id>/', CompanyView.as_view(), name='company'),

    path('myresume/', MyResumeView.as_view(), name='myresume'),
    path('myresume/edit/', my_resume_edit, name='myresume_edit'),
    path('myresume/create/', my_resume_create, name='myresume_create'),

    path('mycompany/', MyCompanyView.as_view(), name='mycompany'),
    path('mycompany/edit/', my_company_edit, name='mycompany_edit'),
    path('mycompany/create/', my_company_create, name='mycompany_create'),

    path('mycompany/vacancies/', MyVacanciesView.as_view(), name='mycompany_vacancies'),
    path('mycompany/vacancies/create', my_vacancy_create, name='mycompany_vacancies_create'),
    re_path('mycompany/vacancies/(?P<id>[0-9]+)/$', my_vacancy_edit, name='mycompany_vacancy_edit'),

    path('media/', MainView.as_view(), name='media'),

    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('login', MyLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name ='logout'),
    path('signup', MySignUpView.as_view(), name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', 
    serve,
    {'document_root': settings.MEDIA_ROOT})
]