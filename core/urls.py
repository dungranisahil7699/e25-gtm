from django.urls import path, re_path
from . import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('', views.singup, name='singup'),
    path('home/', views.home, name='home'),
    path('mainform/', views.mainform, name='mainform'),
    path('download_file/<int:id>', views.download_file, name='download_file'),
    path('logout/', views.logout, name='logout'),
    re_path(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT}),

]