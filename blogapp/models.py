from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Blogpost(models.Model):
    idno = models.AutoField(primary_key=True)
    heading = models.CharField(max_length=90)
    content = models.TextField(max_length=15000)
    author= models.CharField(max_length=50)
    slug = models.CharField(max_length=150)
    timestamp = models.DateTimeField(blank=True)


    def __str__(self):
        return self.heading



class Comments(models.Model):
    sno=models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Blogpost,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True)

    
   
    timestamp = models.DateTimeField(default = now)

    def __str__(self):
        return self.comment[0:15]+"..." +"by" + self.user.email