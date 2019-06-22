import django
django.setup()
from django.shortcuts import render,redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PostForm,CommentForm,editProfileForm
from .models import Post,Comment,Reaction
from django.contrib.auth.decorators import login_required
import datetime,time
import hashlib
from multiprocessing import Process,Pool
import threading, multiprocessing, math, time
from .blockchain import Blockchain, Block
import random,string, decimal
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
@login_required(login_url='/signup')
def submit(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.category = request.POST.get('category')
            profile.pub_date = datetime.datetime.now()
            profile.image = request.FILES['image']
            profile.save()
            print("\nSAVED\n")
            return redirect('homepage')

        else:
            print("\nNOT SAVED\n")
            form = PostForm()
            return render(request, 'submit.html', {'form': form, 'error':"Invalid login details given"})

    else:
        form = PostForm()
    return render(request,'submit.html',  {'form': form})


@login_required(login_url='/login')
def my_acc(request):
    all_post = Post.objects.filter(user= request.user).order_by('-pub_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(all_post, 3)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    user = request.user
    currentuser = get_object_or_404(User, username=user)
    print(currentuser.first_name)
    print(currentuser.last_name)
    return render(request, 'myaccount.html',{'posts':all_post,'username' : user, 'currentuser': currentuser })


@login_required(login_url='/login')
def edit_profile(request):
    if request.method == 'POST':
        form = editProfileForm(request.POST, instance=request.user)

        if request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get('username') and request.POST.get('email'):
            form.save()
            return redirect('my_account')
        else:
            form = editProfileForm(instance=request.user)
            args = {'form': form, 'error': "Oops! Something went wrong"}
            return render(request, 'edit_profile.html', args)

    else:
        form = editProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'edit_profile.html', args)


@login_required(login_url='/login')
def changepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('my_account')
        else:
            form = PasswordChangeForm(user=request.user)
            args = {'form': form, 'error': "Either old password is wrong or Newpassword fields are different."}
            return render(request, 'change_password.html', args)

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        print(args)
        return render(request, 'change_password.html', args)



@login_required(login_url='/login')
def upvote(request, product_id):
    details = get_object_or_404(Post, pk=product_id)
    if request.method == 'POST':
        try:
            reaction = Reaction.objects.get(post_name=details, user = request.user)
            reaction.upvote = 1
            reaction.report = 0
            reaction.save()
            # print("already a member")

        except:
            reaction=Reaction()
            reaction.user = request.user
            reaction.post_name = details
            reaction.upvote += 1
            reaction.save()
            # print("not a member")
    return redirect('/'+str(product_id)+'/')



@login_required(login_url='/login')
def report(request, product_id):
    details = get_object_or_404(Post, pk=product_id)
    if request.method == 'POST':
        try:
            reaction = Reaction.objects.get(post_name=details, user = request.user)
            reaction.report = 1
            reaction.upvote = 0
            reaction.save()
            # print("already a member")

        except:
            reaction=Reaction()
            reaction.user = request.user
            reaction.post_name = details
            reaction.report += 1
            reaction.save()
            # print("not a member")
    return redirect('/'+str(product_id)+'/')

project_name = ''

def detail(request, product_id):
    details = get_object_or_404(Post, pk=product_id)
    comments = Comment.objects.filter(post_name= details)
    total_upvotes = len(Reaction.objects.filter(post_name= details, upvote=1))
    total_reports = len(Reaction.objects.filter(post_name= details, report=1))
    if request.method == 'POST':
        comm = CommentForm(request.POST)
        if comm.is_valid():
            comment = comm.save(commit=False)
            comment.author = request.user
            comment.pub_date = datetime.datetime.now()
            comment.post_name = details
            comment.save()
            print("\nSAVED comment\n")
        else:
            global project_name

            try:
                percent = int(request.POST.get('selector'))
                usage=math.ceil((percent/100) * multiprocessing.cpu_count())
                project_name = details

                miner(usage)
            except:
                print("\nyou are stoping \n")
                project_name = ''
                miner(0)
                return redirect('/'+str(product_id)+'/')
    form = CommentForm()
    return render(request, 'detail.html',{'details':details, 'form': form, 'comments':comments, 'upvotes': total_upvotes,'reports': total_reports })

def comment(request):
    # if request.method == 'POST':
    form = CommentForm()
    return render(request,'comment.html', {'form': form})





def deleter(request, product_id):
    if request.method == 'POST':
        Post.objects.get(pk=product_id).delete()
    all_post = Post.objects.filter(user= request.user)
    return render(request, 'myaccount.html',{'posts':all_post})



def browse(request, product_category=None):
    if product_category:
            all_post = Post.objects.filter(category = product_category).order_by('-pub_date')
    else:
            all_post = Post.objects.order_by('-pub_date')

    print(product_category)
    page = request.GET.get('page', 1)
    paginator = Paginator(all_post, 3)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'browse.html',{'posts':users})



def foo():
    # print("in the foo")
    outstr = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(20)])
    blockchain = Blockchain()
    blockchain.mine(Block(outstr))
    # print("solved")
    return Block.hash_solved



global process_value
processes = []

start_time = 0

def hash_rate(request):
    ha_r = 0
    try:
        for ha_r in processes:
            ha_r += ha_r
        end_time = round(time.time(),2)
        hash_sec = round(ha_r/round(end_time-start_time,2),3)
    except:
        pass
    print(processes)
    return render(request, 'hashes.html', {'total_hash':ha_r,"hash_rate":hash_sec, "name":project_name})


mypool = []
def miner(percent):
    global start_time
    start_time = round(time.time(),2)
    processes.clear()
    try:
        pool = Pool(processes=percent)
        while True:
            mypool.append(pool)
            for i in range(0, 4):
                t_name = "t" + str(i)
                t_name = pool.apply_async(foo, ())
                # print(t_name)
                # mypool.append(t_name)
            h = t_name.get()
            print("hash: {}".format(h))
            processes.append(h)
            earn = h*0.00000001
            # print("earned {}".format(earn))
            project=Post.objects.get(title=project_name)
            # print("got the project")
            # print(project.earn + decimal.Decimal(earn))
            project.earn += decimal.Decimal(earn)
            project.save()
            # print("saved")
            # print("in the end")
            # print(processes)
    except Exception as e:
        print(e)
        processes.clear()
        # print("\n\nBREAKING\n\n")
        for p in mypool:
            p.terminate()


def example(request):
    product_id=30
    details = get_object_or_404(Post, pk=product_id)
    comments = Comment.objects.filter(post_name= details)
    if request.method == 'POST':
        comm = CommentForm(request.POST)
        if comm.is_valid():
            comment = comm.save(commit=False)
            comment.author = request.user
            comment.pub_date = datetime.datetime.now()
            comment.post_name = details
            comment.save()
            print("\nSAVED comment4\n")

        else:
            try:
                percent = int(request.POST.get('selector'))
                usage=math.ceil((percent/100) * multiprocessing.cpu_count())
                miner(usage, False)
            except:
                print("\nyou are stoping \n")
                miner(0,True)
    form = CommentForm()
    return render(request, 'example.html',{'details':details, 'form': form, 'comments':comments})
