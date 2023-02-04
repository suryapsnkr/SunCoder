from django.shortcuts import render, redirect
from django.contrib import messages
from blog.models import Comment, Post


# Create your views here.
def blogHome(request):
    #messages.success(request, "Welcome to SunCoder Blog Home.")
    allPosts=Post.objects.all()
    print(allPosts)
    context={'allPosts': allPosts}
    return render(request, 'blog/bloghome.html', context)

    
    
def blogPost(request, slug):
    #messages.success(request, "Welcome to SunCoder Blog post.")
    post=Post.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(post=post, parent=None)
    replies= Comment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context={'post':post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request,'blog/blogpost.html', context)

def addPost(request):
    if request.method=='POST':
        title=request.POST['title']
        author=request.POST['author']
        slug=request.POST['slug']
        content = request.POST['content']
        post=Post(title=title, author=author, slug=slug, content=content)
        post.save()
        messages.success(request, "Your post has been successfully added")
    return redirect('blogHome')


def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=Comment(Comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= Comment.objects.get(sno=parentSno)
            reply=Comment(Comment= comment, user=user, post=post, parent=parent)
            reply.save()
            messages.success(request, "Your reply has been posted successfully")
        
    return redirect(f'/blog/{post.slug}')

