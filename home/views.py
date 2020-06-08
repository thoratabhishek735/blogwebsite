

# Create your views here.
from django.shortcuts import render,redirect,HttpResponse
from home.models import Contact
from django.contrib import messages
from blogapp.models import Blogpost
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from newsapi import NewsApiClient
from math import ceil
from datetime import datetime

# Create your views here.
def home(request):
    c=0
    newsapi = NewsApiClient(api_key='a2a0c009161743e7906e37aa1f56de09')
    top_headlines = newsapi.get_top_headlines(sources = "techcrunch",
                                         language = "en",
                                           )
    articles = top_headlines['articles']

    desc=[]
    news=[]
    img=[]

    for i in range(len(articles)):
        myart = articles[i]

        news.append(myart['title'])
        c+=1
        desc.append(myart['description'])
        img.append(myart['urlToImage'])

    myitems = zip(news,desc,img)
    
    count=c
    
    nslides= count//3 + ceil((count/3)-(count//3))
    print(nslides)
    allprods={'nslides':nslides,'myitems':myitems,'range':range(1,nslides)}
    
   
    return render(request,'home/home.html',allprods)




def about(request):
    return render(request, 'home/about.html')

def contact(request):
    
    if request.method=='POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        message = request.POST['message']
        
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(message)<4:
            messages.error(request,"Please fill the form correctly")
        else:
            contact = Contact(name=name,phone=phone,email=email,message=message)
            contact.save()
            messages.success(request, 'Form submitted successfully.')
    user = request.user  
    if user.is_authenticated:
       return render(request,'home/contact.html')
    else:
        return HttpResponse('Error not found please login first to contact')
def searchres(request):
    
    if request.method=="GET":
        query = request.GET['search']
        if len(query)<1:
           allres = Blogpost.objects.none()
           
        else:
              allrestitle = Blogpost.objects.filter(heading__icontains=query)
              allrescontent = Blogpost.objects.filter(content__icontains=query)
              allres = allrestitle.union(allrescontent)
              
        if allres.count() == 0:
           messages.error(request,"Results not found")
        params = {'allres': allres,'query':query}
        

        
    return render(request,'blog/searchres.html',params)

# Api for login logout
def handlesignup(request):
    if request.method == 'POST':
       
       firstname =  request.POST['firstname']
       lastname =  request.POST['lastname']
       username = request.POST['username']
       email =  request.POST['email']
       password =  request.POST['pass']
       comfpassword =  request.POST['pass1']

       #Checkforinputs

       if (len(username)> 10):
           messages.error(request,"Username must be under 10 characters")
           return redirect('/')
       if password != comfpassword:
           messages.error(request,"Passwords doesnt match")
           return redirect('/')
       if not username.isalnum():
           messages.error(request,"Username should contain numbers and alphabets only")
           return redirect('/')
       if not firstname.isalnum():
           messages.error(request,"name shouldnt contain special characters")
           return redirect('/')
      
       if not lastname.isalnum():
           messages.error(request,"name shouldnt contain special characters")
           return redirect('/')
      

    

       myuser = User.objects.create_user(username,email,password)
       myuser.first_name=firstname
       myuser.last_name=lastname
       myuser.save()
       messages.success(request,"Account created successfully")
       return redirect('/')

    else:
        return HttpResponse('404 not found')

def handlelogin(request):
    if request.method == 'POST':
        logusername = request.POST['logusername']
        logpassword = request.POST['logpass']

        usr = authenticate(username = logusername , password = logpassword)
        if usr is not None:
            login(request,usr)
            messages.success(request,"successfully logged in as")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials Please enter correct details")
            return redirect('/')
    else:
        return HttpResponse('404 not found')
        
def handlelogout(request):
    logout(request)
    messages.success(request,"Logged out successfully")

    return redirect('/')


def postingblog(request):
    if request.method=='POST':
        timestamp = 1545730073
        heading = request.POST['heading']
        content = request.POST['content']
        author = request.user
        slug = request.POST['slug']
        timestamp=datetime.fromtimestamp(timestamp)
        author=str(author)
        if len(heading)<3 or len(content)<100 or len(slug)<1 or author=="AnonymousUser":
            messages.error(request,"Please fill the form correctly")
        else:
            userpost = Blogpost(heading=heading,content=content,author=author,slug=slug, timestamp= timestamp)
            userpost.save()
            messages.success(request, 'Form submitted successfully.')

       
       
    
    
    
    return render(request,'home/postingblog.html')