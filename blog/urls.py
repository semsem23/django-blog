from django.urls import path
from .views import SignUpView
from .import views

urlpatterns = [
    path('', views.index, name ='index'),
    path('news/<slug:slug>/', views.post_detail, name ='post_detail'),
    path('category/<slug:slug>/', views.view_category, name='post_category'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('404/', views.error_404, name='error_404'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('contact/', views.contact, name ='contact'),
    path('contact/thanks/', views.thanks, name ='thanks'),


]


