from django.contrib import admin
from django.urls import path
from mainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_page),
    path('about-us/',views.about_us),
    path('contact-us/',views.contact_us),
    path('courses/',views.course_page),
    path('blog/',views.blog_page),
    path('blog-details/',views.blog_details_page),
    path('schedule/',views.schedule),
]
