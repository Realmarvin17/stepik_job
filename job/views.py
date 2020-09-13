from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import Http404, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import FormMixin

from job.models import Application
from job.models import Company
from job.models import Resume
from job.models import Specialty
from job.models import Vacancy
from .forms import ApplicationForm, CompanyForm, VacancyForm, UserForm, ResumeForm


class MainView(View):
    def get(self, request):
        return render(
            request, 'index.html', {
                'specialities': Specialty.objects.all(),
                'companies': Company.objects.all()
            }
        )


class VacanciesView(View):
    def get(self, request, ):
        search_query = request.GET.get('search','')

        if search_query:
            vacancies=Vacancy.objects.filter(Q(title__icontains=search_query) | Q(skills__icontains=search_query))
        else:
            vacancies = Vacancy.objects.all()
        return render(
            request, 'list.html', {
                'vacancies': vacancies,
            }
        )


class VacancyView(FormMixin, DetailView):
    model = Vacancy
    template_name = "vacancy.html"
    form_class = ApplicationForm

    def get_success_url(self):
        return reverse('send', kwargs={'pk': self.object.pk})

    def post(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            application = form.save(commit=False)
            if request.user.is_authenticated:
                application.user = request.user
            application.vacancy = self.object
            application.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)


class SpecializationView(View):
    def get(self, request, specialization: str):
        speciality = Specialty.objects.filter(code=specialization).first()
        if not speciality:
            raise Http404('Страница не найдена')

        return render(
            request, 'list.html', {
                'vacancies': Vacancy.objects.filter(specialty__code=specialization),
                'speciality': speciality
            }
        )


class CompaniesView(View):
    def get(self, request, ):
        return render(
            request, 'list.html',
        )


class CompanyView(View):
    def get(self, request, id: int):
        company = Company.objects.filter(id=id).first()
        if not company:
            raise Http404('Страница не найдена')
        return render(
            request, 'company.html', {
                'company': company,
                'vacancies': Vacancy.objects.filter(company__id=id),
            }
        )


class SendView(View):
    def get(self, request, pk: int):
        return render(
            request, 'sent.html',
        )


class MyResumeView(View):
    def get(self, request, ):
        if request.user.is_authenticated:
            if Resume.objects.filter(user=request.user):
                return redirect('myresume_edit')
            else:
                return render(
                    request, 'resume-create.html',
                )
        else:
            raise Http404


def my_resume_create(request):
    if request.user.is_authenticated:
        if Resume.objects.filter(user=request.user):
            return redirect('myresume_edit')
        else:
            form = ResumeForm(request.POST or None)
            if form.is_valid():
                resume = form.save(commit=False)
                resume.user = request.user
                resume.save()
                return redirect('myresume_edit')
            return render(request, 'resume-edit.html', {'form': form})

    else:
        raise Http404


def my_resume_edit(request):
    if request.user.is_authenticated:
        instance = get_object_or_404(Resume, user=request.user)
        form = ResumeForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше резюме обновлено!')
            return redirect('myresume_edit')
        return render(request, 'resume-edit.html', {'form': form})

    else:
        raise Http404


def my_company_create(request):
    if request.user.is_authenticated:
        if Company.objects.filter(user=request.user):
            return redirect('mycompany_edit')
        else:
            form = CompanyForm(request.POST or None, request.FILES)
            if form.is_valid():
                company = form.save(commit=False)
                company.user = request.user
                company.save()
                return redirect('mycompany_edit')
            return render(request, 'company-edit.html', {'form': form})
    else:
        raise Http404


def my_company_edit(request):
    if request.user.is_authenticated:
        instance = get_object_or_404(Company, user=request.user)
        form = CompanyForm(request.POST or None, request.FILES or None, instance=instance)

        if form.is_valid():
            form.save()
            messages.success(request, 'Ваша компания обновлена!')
            return redirect('mycompany_edit')
        return render(request, 'company-edit.html', {'form': form, 'company': instance})

    else:
        raise Http404


def my_vacancy_create(request):
    if request.user.is_authenticated:
        form = VacancyForm(request.POST or None)
        company = get_object_or_404(Company, user=request.user)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.company = company
            vacancy.owner = request.user
            vacancy.save()
            return redirect('mycompany_vacancies')
        return render(request, 'vacancy-edit.html', {'form': form})
    else:
        raise Http404


def my_vacancy_edit(request, id: int):
    if request.user.is_authenticated:
        instance = get_object_or_404(Vacancy, id=id, owner=request.user)
        form = VacancyForm(request.POST or None, instance=instance)
        applications = Application.objects.filter(vacancy=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваша вакансия обновлена!')
            return redirect('mycompany_vacancy_edit', id=id)
        return render(request, 'vacancy-edit.html', {'form': form, 'applications': applications, 'id': id})
    else:
        raise Http404


class MyCompanyView(View):
    def get(self, request, ):
        if request.user.is_authenticated:

            if Company.objects.filter(user=request.user):
                return redirect('mycompany_edit')
            else:
                return render(
                    request, 'company-create.html',
                )
        else:
            raise Http404


class MyVacanciesView(View):
    def get(self, request, ):
        return render(
            request, 'vacancy-list.html', {
                'vacancies': Vacancy.objects.filter(owner=request.user),
            }
        )


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


class MySignUpView(CreateView):
    form_class = UserForm
    template_name = 'signup.html'
    success_url = 'login'
