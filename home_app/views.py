from django.shortcuts import render, redirect
from product_app.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    return render(request,'index.html')

def searcher(request):
    query = request.GET.get('query')
    if query == '':
        return redirect('homepage')

    else:
        all_post = Post.objects.filter(title__icontains = query).order_by('-pub_date')
        return render(request, 'browse.html',{'posts':all_post})



def faq(request):
    return render(request, "faq.html")


def about(request):
    return render(request, "about.html")

def error(request):
    return render(request, "err.html")
