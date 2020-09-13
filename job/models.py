from django.contrib.auth.models import User, AbstractUser
from django.db import models

from stepik_job import settings


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    logo = models.ImageField(upload_to=settings.MEDIA_COMPANY_IMAGE_DIR, blank=True)
    description = models.CharField(max_length=2048)
    employee_count = models.IntegerField()


class Specialty(models.Model):
    code = models.CharField(max_length=64)
    title = models.CharField(max_length=256)
    logo = models.ImageField(upload_to=settings.MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title = models.CharField(max_length=64)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, default='2', related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.CharField(max_length=256)
    description = models.CharField(max_length=2048)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vacancies')

    def __str__(self):
        return self.title


class Application(models.Model):
    written_username = models.CharField(max_length=64, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', default=None, null=True)
    written_phone = models.IntegerField(blank=False)
    written_cover_letter = models.CharField(max_length=1024)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return self.written_username


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)

    RESUME_STATUS = (
        ('n', 'Не ищу работу'),
        ('r', 'Рассматриваю предложения'),
        ('a', 'Ищу работу'),
    )

    status = models.CharField(max_length=1, choices=RESUME_STATUS, blank=False, default='a')
    salary = models.IntegerField()
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, default='2', related_name='resumes')

    RESUME_GRADE = (
        ('st', 'Стажер'),
        ('j', 'Джуниор'),
        ('m', 'Миддл'),
        ('sr', 'Синьор'),
        ('l', 'Лид'),
    )

    grade = models.CharField(max_length=2, choices=RESUME_GRADE, blank=False, default='j')
    education = models.CharField(max_length=64)
    experience = models.CharField(max_length=64)
    portfolio = models.CharField(max_length=1024)

    def __str__(self):
        return self.name

#Расширение модели User
#class User(AbstractUser):
    #name = models.TextField(max_length=64, blank=True)
    #surname = models.CharField(max_length=64, blank=True)
