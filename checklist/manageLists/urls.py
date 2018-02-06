from django.urls import path

from . import views

app_name = 'manageLists'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:list_id>/', views.show_list, name='lists'),
    path('<int:list_id>/edit', views.edit_list, name='edit'),
    path('<int:list_id>/edit/<int:item_id>', views.edit_list, name='edit_item'),
    path('<int:list_id>/submit/', views.submit_changes, name='submit'),
    path('<int:list_id>/add/', views.add_item, name='add'),
    path('<str:list_name>/', views.show_list_by_name, name='lists')
]
