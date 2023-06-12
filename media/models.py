from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Post(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    title = models.CharField(max_length=280)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)


    def __str__(self):
        return self.text
    
        
    def to_representation(self):
        return {
            "id": self.id,
            "user": self.user.id,
            "post": self.post.id,
            "text": self.text,
        }
    
class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','post'],  name="unique_like")
        ]

    