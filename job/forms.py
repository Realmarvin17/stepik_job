from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _

from .models import Application, Company, Vacancy
from .models import Resume


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ApplicationForm(ModelForm):

    def clean(self):
        cleaned_data = super(ApplicationForm, self).clean()
        return cleaned_data

    class Meta:
        model = Application
        widgets = {
            'written_cover_letter': Textarea(attrs={'cols': 80, 'rows': 10}),
        }

        fields = ('written_username', 'written_phone', 'written_cover_letter')

        labels = {
            'written_username': _('Вас зовут'),
            'written_phone': _('Ваш телефон'),
            'written_cover_letter': _('Сопроводительное письмо'),
        }


class VacancyForm(ModelForm):

    def clean(self):
        cleaned_data = super(VacancyForm, self).clean()
        return cleaned_data

    class Meta:
        model = Vacancy
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 15}),
        }
        fields = ('title',
                  'specialty',
                  'skills',
                  'description',
                  'salary_min',
                  'salary_max',
                  )
        labels = {
            'title': _('Название вакансии'),
            'specialty': _('Специализация'),
            'skills': _('Требуемые навыки'),
            'description': _('Описание вакансии'),
            'salary_min': _('Зарплата от'),
            'salary_max': _('Зарплата до'),
        }


class ResumeForm(ModelForm):

    def clean(self):
        cleaned_data = super(ResumeForm, self).clean()
        return cleaned_data

    class Meta:
        model = Resume
        widgets = {
            'education': Textarea(attrs={'cols': 80, 'rows': 10}),
            'experience': Textarea(attrs={'cols': 80, 'rows': 15}),
        }
        fields = ('name',
                  'surname',
                  'status',
                  'salary',
                  'specialty',
                  'grade',
                  'education',
                  'experience',
                  'portfolio')
        labels = {
            'name': _('Имя'),
            'surname': _('Фамилия'),
            'status': _('Готовность к работе'),
            'salary': _('Ожидаемое вознаграждение'),
            'specialty': _('Специализация'),
            'grade': _('Квалификация'),
            'education': _('Образование'),
            'experience': _('Опыт работы'),
            'portfolio': _('Ссылка на портфолио'),
        }


class CompanyForm(ModelForm):
    logo = forms.ImageField(label=_('Логотип'), required=False, widget=forms.FileInput)

    def clean(self):
        cleaned_data = super(CompanyForm, self).clean()
        return cleaned_data

    class Meta:
        model = Company
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 10}),
        }
        fields = ('name',
                  'location',
                  'logo',
                  'employee_count',
                  'description',

                  )

        labels = {
            'name': _('Название компании'),
            'location': _('География'),
            'logo': _('Логотип'),
            'employee_count': _('Количество человек в компании'),
            'description': _('Информация о компании'),
        }