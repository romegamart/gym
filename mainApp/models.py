from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class Trainer(models.Model):
    id=models.AutoField(primary_key=True)
    image=models.ImageField(upload_to="trainer")
    name=models.CharField(max_length=150)
    expert_in=models.CharField(max_length=200)



class Course(models.Model):
    id=models.AutoField(primary_key=True)
    image=models.ImageField(upload_to="course")
    name=models.CharField(max_length=150)
    slug=models.CharField(max_length=150,default='')

    content=HTMLField(default='',null=True,blank=True)
    meta_title=models.CharField(max_length=65,null=True,blank=True)
    meta_description=models.CharField(max_length=150,null=True,blank=True)
    meta_keyword=models.CharField(max_length=65,null=True,blank=True)
    date=models.DateField(auto_now_add=True)



class Blog(models.Model):
    id=models.AutoField(primary_key=True)
    image=models.ImageField(upload_to="blog")
    title=models.CharField(max_length=150)
    slug=models.CharField(max_length=150,default='')

    content=HTMLField(default='',null=True,blank=True)
    meta_description=models.CharField(max_length=150,null=True,blank=True)
    meta_keyword=models.CharField(max_length=65,null=True,blank=True)
    date=models.DateField(auto_now_add=True)

class Contact(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=150)
    phone=models.CharField(max_length=10)
    message=models.TextField()
    date=models.DateTimeField(auto_now_add=True)


class Gallery(models.Model):
    id=models.AutoField(primary_key=True)
    image=models.ImageField(upload_to="gallery")