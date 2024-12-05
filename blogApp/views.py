from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogInfo,Comment,Like
from .forms import BlogForm, CommentForm
from django.contrib import messages
from Biznews.userApp.models import profile
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User



# Create your views here.
def allpostView(request): 
    allpost = BlogInfo.objects.all() #{(),()}
    blog_data = []

    for post in allpost:
        if post.approved:
            blog_data.append(
            {
                'post':post,
                'likes':post.total_likes(),
                'comments':post.total_comments()
            }
        )
    print(blog_data)
    
    return render(request, template_name= 'index.html', context={'post_data':blog_data})

@login_required
def allBlogView(request):
    blogs = BlogInfo.objects.all() #{(),()}

    return render(request, template_name= 'blogApp/all_blog.html', context={'allBlog':blogs})




@login_required
def createdBlogView(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blogForm = form.save(commit=False)
            title = blogForm.title
            author = profile.objects.get(user_id = request.user.id)
            blogForm.author = author
            blogForm.save()
            # send mail to the user that created the blog
            send_mail(
                 subject = 'Blog created successfully',
                message = f'You have successsfully created a blog titled{title},Kindly wait as it get approved.\nThank you for using our service',
                from_email = 'biznews@gmail.com',
                recipient_list =[request.user.email],
                fail_silently = True
            )
            staffs =  User.objects.filter(is_staff = True)
            emails = [staff.email for staff in staffs]
            send_mail(
                subject = 'Approve Request',
                message= f'A blog titled {title} was just created by {request.user.first_name}  {request.user.last_name}. Kindly review via http://127.0.0.1:8000/userApp/all-blog',
                from_email= 'biznews@gmail.com',
                recipient_list= emails,
                fail_silently= True

            )
           
            
            messages.success(request, 'post created succesfully')
            return redirect('home')
        else:
            messages.error(request, 'Error creating a post')
            return render(request, template_name='blogApp/create_blog.html', context={'blogForm':form})
    else:
        form = BlogForm()
        return render(request, template_name='blogApp/create_blog.html', context={'blogForm':form})
    
@login_required
def displayPostView(request, id):
    user = get_object_or_404(profile, user_id = request.user.id)
    blog = BlogInfo.objects.get(blog_id = id)
    likes = blog.total_likes()
    # comments = blog.total_comments()
    noOfComments = blog.total_comments()

    all_comment = Comment.objects.filter(blog_id = id)
    print(all_comment)


    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            validform = form.save(commit=False)
            validform.user = user
            validform.blog = blog

            validform.save()

            messages.success(request, 'comment successfully')
        else:
            messages.error(request, 'error occured')
        
        return redirect('view-blog', id)


    else:
        form = CommentForm()

    return render(request, template_name='blogApp/view_blog.html', context={'blog':blog, 'likes':likes, 'comments':noOfComments, 'commentForm':form, 'all_comment':all_comment}) 

    # return render(request, template_name='blogApp/view_blog.html', context={'blog':blog,'likes':likes, 'comments':comments}) 
    
def deleteBlogView(request, id):
    blog = BlogInfo.objects.get(blog_id = id)
    blog.delete()

    messages.success(request, 'post deleted succesfully')
    return redirect('home')

@login_required
def editBlogView(request, id):
    blog = get_object_or_404(BlogInfo ,blog_id = id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'post Edited succesfully')
            return redirect('view-blog', id)
        else:
            messages.success(request, 'post could not be edited')
            return render(request, template_name="blogApp/edit_blog.html", context= {'editForm':form})



    else:
        form = BlogForm(instance=blog)
        return render(request, template_name="blogApp/edit_blog.html", context= {'editForm':form})


@login_required
def approvedView(request, id):
    blog = BlogInfo.objects.get(blog_id = id)

    if blog.approved:
        BlogInfo.objects.filter(blog_id = id ).update(approved = False)
    else:
         BlogInfo.objects.filter(blog_id = id ).update(approved = True)

         return redirect('all-blog')
    
@login_required
def likeView(request, blog_id):
    blog = get_object_or_404(BlogInfo, blog_id = blog_id)
    user = get_object_or_404(profile, user_id = request.user.id)
    # print(user.profile_id)

    exists = Like.objects.filter(blog_id = blog_id, user_id = request.user.id ).exists()
    print(exists)
    if exists: 
        Like.objects.filter(user_id = request.user.id, blog_id = blog_id).delete()
    else:
        Like.objects.create(user = user, blog = blog)

    return redirect('view-blog', blog_id )

@login_required
def alllikesView(request, blog_id):
    alllikes = Like.objects.filter(blog_id=blog_id)
    print(alllikes)
    return render(request, template_name='blogApp/all_likes.html', context={'alllikes': alllikes})

@login_required
def commentView(request, blog_id):
    blog = get_object_or_404(BlogInfo, blog_id = blog_id)
    user = get_object_or_404(profile, user_id = request.user.id)
    # print(user.profile_id)

    if request.method == 'POST':
        content = request.POST['content']
        Comment.objects.create(user = user, blog = blog, content = content)
    
    return redirect('view-blog', blog_id  )
 
@login_required
def replyCommentView(request, comment_id):
    reply_comment = get_object_or_404(Comment, id = comment_id)
    blog= reply_comment.blog
    # print(user.profile_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content: 
            Comment.objects.create(
                blog = blog,
                User=request.user.profile,
                content= content,
                reply= reply_comment

                )
            messages.success(request, 'Reply posted succesfully')
        else:
            messages.error(request, 'post a reply')
            
    return render(request, 'view-blog', {'blog': blog})




# @login_required
# def addCommentVIew(request, blog_id):
#     user = get_object_or_404(profile, user_id = request.user.id)
#     blog = get_object_or_404(BlogInfo, blog_id = blog_id)
#     if request.method == 'POST':
#         pass

#     else:
#         form = CommentForm()
#