from django.shortcuts import render
from .models import *
from django_ratelimit.decorators import ratelimit
# Create your views here.


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def home_page(request):
    trainer=Trainer.objects.all()
    return render(request,'home/index.html',{'trainer':trainer})



@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def about_us(request):
    return render(request,'home/about.html')


@ratelimit(key='ip', rate='3/h', method='POST', block=True)
def contact_us(request):
    msg=''
    if request.method=="POST":
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        message=request.POST.get('message')
        Contact.objects.create(name=name,phone=phone,message=message)
        msg="done"
    return render(request,'home/contact.html',{'msg':msg})



@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def course_page(request):
    data=Course.objects.all()
    return render(request,'home/courses.html',{'data':data})



@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def course_details_page(request,slug):
    data=Course.objects.filter(slug=slug).first()
    similar_blog=Course.objects.exclude(id=data.id)[:10]
    return render(request,'home/course-details.html',{'data':data,'similar_blog':similar_blog})

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Blog


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def blog_page(request):
    blog_list = Blog.objects.all().order_by('-id')  # latest first

    paginator = Paginator(blog_list, 6)  # 6 blogs per page
    page_number = request.GET.get('page')
    data = paginator.get_page(page_number)

    return render(request, 'home/blog.html', {
        'data': data
    })



@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def blog_details_page(request,slug):
    data=Blog.objects.filter(slug=slug).first()
    similar_blog=Blog.objects.exclude(id=data.id)[:10]
    return render(request,'home/blog_detail.html',{'data':data,'similar_blog':similar_blog})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def schedule(request):
    return render(request,'home/shedule.html')


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def pricing_page(request):
    return render(request,'home/pricing.html')

#AJAX

from django.http import JsonResponse
from .models import Course


def ajax_courses(request):
    course = Course.objects.all()

    data = []
    for item in course:
        data.append({
            'id': item.id,
            'name': item.name,
            'image': item.image.url if item.image else '',
        })

    return JsonResponse({'data': data})


def ajax_gallery(request):
    gallery = Gallery.objects.all()

    data = []
    for item in gallery:
        data.append({
            'id': item.id,
            'image': item.image.url if item.image else '',
        })

    return JsonResponse({'data': data})


from django.http import JsonResponse
from .models import Blog


def ajax_blog(request):
    blogs = Blog.objects.all().order_by('-id')[:6]

    data = []

    for item in blogs:
        data.append({
            'id': item.id,
            'title': item.title,
            'description': item.meta_description[:120] + '...' if item.meta_description else '',
            'image': item.image.url if item.image else '',
            'slug': item.slug,
        })

    return JsonResponse({'data': data})