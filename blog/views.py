from django.shortcuts import render
from .models import Post, Author, Category, Comment
from django.views.generic import TemplateView, ListView, DetailView
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserCreationForm, CommentForm, ContactForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.db.models import Count
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
   categories = Category.objects.order_by('name')
   posts = Post.objects.filter(isPublished=True)
   most_commented_posts = Post.objects.values('title').exclude(comments__isnull=True).annotate(most_commented=Count('comments')).order_by('-most_commented')
   special_posts = Post.objects.select_related('category').filter(category__name="economie")
   last_comments = Comment.objects.all()
   
   return render(request,'index.html', {
       'categories': categories,
       'posts': posts,
       'most_commented_posts' : most_commented_posts,
       'special_posts': special_posts,
       'last_comments': last_comments,   
   })

            
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

   
def post_detail(request, slug, year):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    posts = Post.objects.filter(isPublished=True)
    new_comment = None
    if request.method == "POST":
  
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'news/post_detail.html', {'comments': comments,
                                                           'new_comment': new_comment,
                                                           'post': post,
                                                           'form': form,
                                                           'posts':posts,
                                                           })
                                                    
        
def view_category(request, slug):
       category = get_object_or_404(Category, slug=slug)
       
       if slug == 'actu':
           posts = Post.objects.all()

           paginator = Paginator(posts, 5) 
           page_number = request.GET.get('page')
           page_obj = paginator.get_page(page_number)
   
           return render(request,'category.html', 
            {'category': category, 
             'posts': posts, 
             'page_obj': page_obj
            })
            
       if slug != 'actu':
           posts = Post.objects.filter(category=category)

           paginator = Paginator(posts, 5) 
           page_number = request.GET.get('page')
           page_obj = paginator.get_page(page_number)
   
           return render(request,'category.html', 
            {'category': category, 
             'posts': posts, 
             'page_obj': page_obj
            })
           

def error_404(request):
    return render(request, '404.html')
    
    
def aboutus(request):
    return render(request, 'aboutus.html')


def contact(request):

    if request.method == 'POST':

        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']
        send_mail(subject, message, sender, ['sami.nouari@gmail.com'])
        return HttpResponseRedirect('thanks/')

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def thanks(request):
    return render(request, 'thanks.html')