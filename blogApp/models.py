from django.db import models
from Biznews.userApp.models import profile

# Create your models here.

class BlogInfo(models.Model):

    category= [
        ('Business', 'Business'),
        ('Technology', 'Technology'),
        ('Sports', 'Sports'),
        ('Food', 'Food'),
        ('Fashion', 'Fashion'),
        ('Others', 'Others')

    ]

    
    blog_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(profile, on_delete=models.CASCADE)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=category)
    approved = models.BooleanField(default=False)
    image = models.ImageField(upload_to='blogImages/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
            return self.likes.count()

    def total_comments(self):
            return self.comments.count()

    def __str__(self):
            return self.title


class Like(models.Model):
    blog = models.ForeignKey(BlogInfo, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(profile, on_delete=models.CASCADE) 
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blog', 'user')  # Ensures a user can only like a blog post once

    def __str__(self):
        return f"{self.user.user.username} liked {self.blog.title}"


class Comment(models.Model):
    blog = models.ForeignKey(BlogInfo, related_name="comments", on_delete=models.CASCADE)
    reply = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(profile, on_delete=models.CASCADE)  # Assuming you're using the default User model
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.user.username} on {self.blog.title}"
    
    # class Comment(models.Model):
    # post = models.ForeignKey('Post', on_delete=models.CASCADE)
    # parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    # content = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.content