# Register your models here.
from django.contrib import admin
from .models import Project, ProjectItem

admin.site.register(Project)
admin.site.register(ProjectItem)
