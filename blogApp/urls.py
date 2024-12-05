from django.urls import path
from .views import *
urlpatterns = [
    path('create-blog/', createdBlogView, name='create-blog'),
    path('view-blog/<int:id>/',displayPostView, name='view-blog' ),
    path('delete-blog/<int:id>/', deleteBlogView, name='delete-blog'),
    path('edit-blog/<int:id>/', editBlogView, name='edit-blog'),
    path('all-blog', allBlogView, name= 'all-blog'),
    path('approve/<int:id>/', approvedView, name='approve'),
    path('like/<int:blog_id>/', likeView, name = 'like' ),
    path('all-likes/<int:blog_id>/', alllikesView, name='all-likes'),
    path('comment/<int:blog_id>/', commentView, name='comment'),
    path('reply_comment/<int:comment_id>/reply/', replyCommentView, name='reply_comment'),
    # path('comment/<int:blog_id>/', commentView, name = 'comment' ),
    # path('all-comment/<int:blog_id>/', allcommentView, name='all-comment'),
]
