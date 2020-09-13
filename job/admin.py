from django.contrib import admin

from .models import Company, Vacancy, Application, Specialty, Resume


class CompanyAdmin(admin.ModelAdmin):
    pass


class VacancyAdmin(admin.ModelAdmin):
    pass


class ApplicationAdmin(admin.ModelAdmin):
    pass


class SpecialtyAdmin(admin.ModelAdmin):
    pass


class ResumeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company, CompanyAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Resume, ResumeAdmin)
