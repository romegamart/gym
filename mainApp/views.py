from django.shortcuts import render

# Create your views here.

def home_page(request):
    return render(request,'home/index.html')

def about_us(request):
    return render(request,'home/about.html')

def contact_us(request):
    return render(request,'home/contact.html')

def course_page(request):
    return render(request,'home/courses.html')

def blog_page(request):
    return render(request,'home/blog.html')

def blog_details_page(request):
    return render(request,'home/blog_detail.html')

def schedule(request):
    return render(request,'home/shedule.html')