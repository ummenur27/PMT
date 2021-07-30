from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('project_list', views.project_list, name='project_list'),
    path('registration', views.registerPage, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('demo', views.demo, name='demo'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/add/', views.project_add, name='project_add'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('project/delete/<int:pk>', views.project_delete, name='project_delete'),
    path('project/<int:pk>/item/add/', views.project_item_add, name='project_item_add'),
    path('project/item/status/<int:pk>', views.project_item_status_update, name='project_item_status_update'),
    path('project/item/edit/<int:pk>', views.project_item_edit, name='project_item_edit'),
    path('project/item/delete/<int:pk>', views.project_item_delete, name='project_item_delete'),
]
