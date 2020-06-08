from django.shortcuts import render,HttpResponse,redirect
from blogapp.models import Blogpost,Comments
from django.contrib import messages
from blogapp.templatetags import extras
# Create your views here.
def bloghome(request):
    allposts = Blogpost.objects.all()
    print(allposts)
    context = {'allposts':allposts}
    return render(request,'blog/bloghome.html',context)

def blogpost(request, slug):
    post = Blogpost.objects.filter(slug=slug).first()
    
    comments = Comments.objects.filter(post=post,parent=None)
    replies = Comments.objects.filter(post=post).exclude(parent=None)
    
    repdict={}
    for reply in replies:
        if reply.parent.sno not in repdict.keys():
            repdict[reply.parent.sno]=[reply]
        else:
            print("cream")
            repdict[reply.parent.sno].append(reply)
    print(repdict)

    params = {'post':post,'comments':comments,'user':request.user,'repdict':repdict}
    
    
    return render(request,'blog/blogpost.html',params)

def postcomment(request):
    if request.method == 'POST':
      comment = request.POST.get("comment")
      user = request.user
      postsno = request.POST.get("postsno") 
      post = Blogpost.objects.get(idno=postsno)
      parentsno = request.POST.get("parentsno")
      if parentsno =="":
        comment= Comments(comment=comment,user=user,post=post)
        messages.success(request,"Commment posted successfully")
      else:
          parent = Comments.objects.get(sno=parentsno)
          comment= Comments(comment=comment,user=user,post=post,parent=parent)
          
      comment.save()
      messages.success(request,"Reply posted successfully")
      
    return redirect(f"/blogapp/{post.slug}")# means redirect on particular page that it was on before

