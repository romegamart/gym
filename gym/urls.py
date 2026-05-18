from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page),
    path('about-us/', views.about_us),
    path('contact-us/', views.contact_us),
    path('courses/', views.course_page),
    path('blog/', views.blog_page),
    path('blog-details/<str:slug>/', views.blog_details_page),
    path('schedule/', views.schedule),
    #AJAX
    path('ajax/courses/',views.ajax_courses,name="ajax_courses"),
    path('ajax/gallery/',views.ajax_gallery,name="ajax_gallery"),
    path('ajax/blog/',views.ajax_blog,name="ajax_blog"),
    path('<str:slug>/', views.course_details_page),
]

# Static & Media Files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)