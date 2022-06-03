from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email),
             username=username,)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(email, username=username, password=password,)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email       = models.EmailField(verbose_name='email', max_length=255, unique=True,)
    is_active   = models.BooleanField(default=True)
    is_admin    = models.BooleanField(default=False)
    username    = models.CharField(max_length=20, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login  = models.DateTimeField(null=True)

    objects   = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
           
 
class Author(models.Model):
    firstName       = models.CharField(max_length=20, null=False)
    lastName        = models.CharField(max_length=20, null=True, blank=True)
    createdDate     = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{} {}'.format(self.firstName, self.lastName)


class Category(models.Model):
    name         = models.CharField(max_length=20, null=False)
    slug         = models.SlugField(max_length=20, unique=True)
    createdDate  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('post_category', kwargs={'slug':self.slug})    
        

class Like(models.Model):
    picture        = models.FileField(upload_to=None, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    like           = models.PositiveIntegerField(default=0)
        
    def total_likes(self):
        return self.like.count()

        
class Post(models.Model):
    title           = models.CharField(max_length=160, null=False)
    summary         = models.CharField(max_length=255, null=True, blank=True)
    content         = models.TextField(null=False)
    slug            = models.SlugField(unique = True)
    image           = models.ImageField(upload_to='', blank=True)
    publishedDate   = models.DateTimeField(default=timezone.now)
    createdDate     = models.DateTimeField(auto_now_add=True)
    updatedDate     = models.DateTimeField(default=timezone.now)
    isPublished     = models.BooleanField(default=False)
    author          = models.ForeignKey(Author, on_delete=models.CASCADE)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    like            = models.ManyToManyField(Like, related_name='likes', blank=True)
    
    class Meta:
        ordering = ['-publishedDate']
     
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug':self.slug})
        
    def __str__(self):
        return self.title



class Comment(models.Model):
    post            = models.ForeignKey(Post, on_delete = models.CASCADE, related_name ='comments')
    user            = models.ForeignKey(User, on_delete = models.CASCADE)
    content         = models.TextField()
    active          = models.BooleanField(default=False)
    createdDate     = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-createdDate']
        
    def __str__(self):
        return self.content