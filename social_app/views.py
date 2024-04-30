from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import JsonResponse
from .forms import PostModelForm
from .models import Post,Comment,Action
from accounts.models import MyUser as User
from accounts.models import Contact
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .serializers import PostSerializer,CommentSerializer
from django.db.models import Q
from .utils import create_action
# Create your views here.


@login_required
def home(request):
    form=PostModelForm()
    posts=Post.objects.all()
    
    followers=Contact.objects.filter(user_from=request.user).values('user_to_id')
    arr_id=[i['user_to_id'] for i in followers]
    arr_id.append(request.user.id)
    suggestion=Contact.objects.filter(user_from__in=arr_id).exclude(user_to__in=arr_id).order_by('?')[:5]


    actions=Action.objects.exclude(user=request.user)
    following_ids=[i['user_to_id'] for i in followers]
    if following_ids:
        actions=actions.filter(user_id__in=following_ids)
    actions=actions[:8]



    
    return render(request,'social_app/home.html',{'posts':posts,'form':form,'suggestion':suggestion,'actions':actions})

@login_required
def create_post(request):
    if request.method=='POST':
        user=request.user
        form=PostModelForm(request.POST,request.FILES)
        if form.is_valid():

            postid=request.POST.get('p-id','')
            content=form.cleaned_data.get('content')
            image=form.cleaned_data.get('image')
            if postid =='':
                 newpost=Post(user=user,content=content,image=image)
                 newpost.save()
                 create_action(user=user,verb='add post',target=newpost)
            else:
                post=Post.objects.get(id=postid)
                post.user=user
                post.content=content
                post.image=image
                post.save()
            
            return JsonResponse({'status':'OK'})
        else:
            return JsonResponse({'status':'Error','errors':form.errors})       
    return JsonResponse({'status':'Error','message':'Invalid request method'})


def posts(request):
    if request.method=='GET':
        posts = Post.objects.all()
        serialized_posts = PostSerializer(posts, many=True)
        return JsonResponse(serialized_posts.data, safe=False)
    else:
        return JsonResponse({'status':'Eerror','message':'Invalid request method'})


@login_required
def delete_post(request):
    if request.method=='POST':
        id=request.POST['id']
        post=Post.objects.get(pk=id)
        post.delete()
        return JsonResponse({'status':'OK'})
    else:
        return JsonResponse({'status':'Error'})


@login_required
def update_post(request):
    id=request.POST.get('id')
    post=Post.objects.get(id=id)
    image=''
    if post.image:
        image=post.image.url
    if request.method=='POST':
        postdetail={'id':post.id,"content":post.content,"image":image}
        return JsonResponse({'status':'OK','postdetail':postdetail})
    else:
        return JsonResponse({'status':'Error','errors':dict(form.errors)})
        

@login_required
@require_POST 
def like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    post=Post.objects.get(id=post_id)
    if(request.user in post.likes.all()):
        action='dislike'
    else:
        action='like'
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.likes.add(request.user)
                create_action(user=request.user,verb='like',target=post)
            else:
                post.likes.remove(request.user) 
                create_action(user=request.user,verb='dislike',target=post)
            return JsonResponse({'status': 'ok','data':{'postid':post_id,'action':action}})
        except Post.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})

@login_required
def comment(request):
    comment_id=request.POST.get('comment_id','')
    post_id=request.POST.get('postid')
    content=request.POST.get('comment')
    post=Post.objects.get(id=post_id)
    user=request.user
    if request.method=="POST":

        if comment_id=='':
            comment=Comment(user=user,post=post,content=content)
            comment.save()
            create_action(user=user,verb='comment',target=comment)

        else:
            comm=Comment.objects.get(id=comment_id)
            comm.user=user
            comm.post=post
            comm.content=content
            comm.save()

        comments = Comment.objects.all()
        serialized_comments = CommentSerializer(comments, many=True)
        return JsonResponse(serialized_comments.data, safe=False)
    else:
        return JsonResponse({'status':'Error'})


def update_comment(request):

    if request.method=='POST':
        comment_id=request.POST.get('comment_id','')
        comm=Comment.objects.get(id=comment_id)
        data={'id':comm.id,'content':comm.content}
        return JsonResponse({'status':'OK','data':data})
    else:
        return JsonResponse({'status':'Error'})

        

@require_POST
def delete_comment(request):
    comment_id=request.POST.get('comment_id')
    c=Comment.objects.get(id=comment_id)
    c.delete()
    return JsonResponse({'status':'OK'})


@login_required
@require_POST
def save_post(request):
    post_id = request.POST.get('postid')
    action = request.POST.get('action')
    post=Post.objects.get(id=post_id)
    if(request.user in post.saves.all()):
        action='disave'
    else:
        action='save'
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'save':
                post.saves.add(request.user)
            else:
                post.saves.remove(request.user) 
            return JsonResponse({'status': 'ok','data':{'postid':post_id,'action':action}})
        except Post.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})



@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    
    
    if user_id and action:
        try: 
            user = User.objects.get(id=user_id)
            if action == 'follow': 
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(user=request.user,verb='starts follow',target=user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete() 
                create_action(user=request.user,verb='unfollow',target=user)
            return JsonResponse({'status':'ok','action':action})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'}) 



def saves(request):

    form=PostModelForm()
    followers=Contact.objects.filter(user_from=request.user).values('user_to_id')
    arr_id=[i['user_to_id'] for i in followers]
    arr_id.append(request.user.id)
    suggestion=Contact.objects.filter(user_from__in=arr_id).exclude(user_to__in=arr_id).order_by('?')[:5]
    return render(request,'social_app/saves.html',{'form':form,'suggestion':suggestion})



    
def following(request):
    form=PostModelForm()
    followers_id=Contact.objects.filter(user_from=request.user).values('user_to_id')
    arr_id=[i['user_to_id'] for i in followers_id]
    arr_id.append(request.user.id)
    suggestion=Contact.objects.filter(user_from__in=arr_id).exclude(user_to__in=arr_id).order_by('?')[:5]
    followers_user=Contact.objects.filter(user_from=request.user)
    return render(request,'social_app/following.html',{'form':form,'suggestion':suggestion ,'followers':followers_user})



@require_POST
def search(request):
    data=request.POST.get('user_data')
    users=User.objects.filter( Q(username__icontains=data) | Q(email__icontains=data) ).exclude(id=request.user.id)[:5].values()
    users_json=list(users)

    following_id=Contact.objects.filter(user_from=request.user).values('user_to_id')
    arr=list(following_id)
    following_arr=[i['user_to_id'] for i in arr]

    return JsonResponse({'status':'ok','users':users_json,'following_id':following_arr})






