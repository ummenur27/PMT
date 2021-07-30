from django.shortcuts import render
from django.utils import timezone
from .models import Project, ProjectItem
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .forms import ProjectForm, ProjectItemForm, CreateUserForm, ProjectItemStatusForm
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'account/registration.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password= password)

        if user is not None:
            login(request, user)
            return redirect('project_list')
    context = {}
    return render(request, 'account/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def demo(request):
    context = {}
    return render(request, 'project/navbar.html', context)

@login_required(login_url='login')
def project_list(request):
    if request.user.is_superuser:
        projects = Project.objects.all()
        print("admin")
    else:
        projects = Project.objects.filter(user=request.user)
        print("user")
    return render(request, 'project/project_list.html',  {'projects': projects})

@login_required(login_url='login')
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    projects = ProjectItem.objects.filter(project=pk).all()
    projectitemform = ProjectItemStatusForm()
    context = {
        'project': project,
        'projects': projects,
        'projectitemform': projectitemform,
    }
    return render(request, 'project/project_detail.html', context)

@login_required(login_url='login')
def project_add(request):
    if not request.user == request.user.is_superuser:
        if request.method == "POST":
            form = ProjectForm(request.POST)
            if form.is_valid():
                project = form.save(commit=False)
                project.save()
                return redirect('project_detail', pk=project.pk)
        else:
            form = ProjectForm()
        return render(request, 'project/project_edit.html', {'form': form})

@login_required(login_url='login')
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project/project_edit.html', {'form': form})

@login_required(login_url='login')
def project_delete(request, pk):
    instance = Project.objects.get(id=pk)
    if request.method =="POST":
        instance.delete()
        context = {
            "instance": instance,
        }
        return HttpResponseRedirect(reverse('project_list'))

    return redirect('project_detail', context)

@login_required(login_url='login')
def project_item_add(request, pk):
    project = Project.objects.get(pk=pk)
    if request.method == "POST":
        projectitemform = ProjectItemForm(request.POST)
        if projectitemform.is_valid():
            projectitem = projectitemform.save(commit=False)
            projectitem.project = project
            projectitem.save()
            return redirect('project_detail', pk=project.pk)
    else:
        projectitemform = ProjectItemForm()
    return render(request, 'project/project_item_edit.html', {'projectitemform': projectitemform})

@login_required(login_url='login')
def project_item_status_update(request, pk):
    project_item = get_object_or_404(ProjectItem, pk=pk)
    if request.method == "POST":
        projectitemform = ProjectItemStatusForm(request.POST, instance=project_item)
        if projectitemform.is_valid():
            projectitem = projectitemform.save(commit=False)
            # projectitem.project = project_item.project_id
            # projectitem. =
            project_item.save()
            return redirect('project_detail', pk=project_item.project_id)
    else:
        projectitemform = ProjectItemStatusForm(instance=project_item)
    return redirect('project_detail', project_item.project_id)

@login_required(login_url='login')
def project_item_edit(request, pk):
    project_item = get_object_or_404(ProjectItem, pk=pk)
    if request.method == "POST":
        projectitemform = ProjectItemForm(request.POST, instance=project_item)
        if projectitemform.is_valid():
            project_item = projectitemform.save(commit=False)
            project_item.save()
            return redirect('project_detail', pk=project_item.project_id)
    else:
        projectitemform = ProjectItemForm(instance=project_item)
    return render(request, 'project/project_item_edit.html', {'projectitemform': projectitemform})

@login_required(login_url='login')
def project_item_delete(request, pk):
    instance = ProjectItem.objects.get(id=pk)
    if request.method =="POST":
        instance.delete()
        context = {
            "instance": instance,
        }
        return HttpResponseRedirect(reverse('project_detail', args=[instance.project.id]))

    return redirect('project_detail', context)
