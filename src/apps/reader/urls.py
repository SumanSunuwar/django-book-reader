from django.urls import path
from . import views

app_name = "reader"

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register, name='register'),
    path('reading/', views.reading_list_view, name='reading_list'),
    path('reading/add/', views.add_to_reading_view, name='add_to_reading_list'),
    path('update-reading-list/', views.update_reading_view, name='update_reading_list'),
    path('reading/remove/<uuid:uid>/', views.remove_from_reading_view, name='remove_from_reading_list'),
]

