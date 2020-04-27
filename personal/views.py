from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http import FileResponse
from . import models
from django.contrib import messages
import os,io,time
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from .models import Blog,Posts,Comments
from django.contrib.auth.models import User
from django.utils import timezone
from .form import (UserCreationForm,UserLoginForm,
                   UserSignupForm,UserBlogUpdateForm,UserUpdateForm,
                   CreatePostForm,CreateCommentForm)

def findkey():
    search_list = []
    for file in os.listdir('media/pdf'):
        if file.endswith('.pdf'):
            # data.append('/media/pdf' + "/" + file)
            search_list.append(file[:-4].split(" "))
    for file in os.listdir('media/apps'):
        if file.endswith('.exe'):
            # data.append('/media/pdf' + "/" + file)
            search_list.append(file[:-4].split(" "))
    for file in os.listdir('media/images'):
        if file.endswith('.jpg') or file.endswith('.png'):
            # data.append('/media/pdf' + "/" + file)
            search_list.append(file[:-4].split(" "))
    for file in os.listdir('media/codesnippets'):
        if file.endswith('.txt'):
            # data.append('/media/pdf' + "/" + file)
            search_list.append(file[:-4].split(" "))
    for file in os.listdir('media/multimedia'):
        # data.append('/media/pdf' + "/" + file)
        search_list.append(file[:-4].split(" "))

    for usr in User.objects.all():
        t=[str(usr)]
        search_list.append(t)

    for pst in Posts.objects.all():
        u=[str(pst.Title)]
        search_list.append(u)
#here search_str holds string of keywords which is
# to be loaded in each page because javascript doesnot have static
# variable . once you find method to keep tarck of previous variable then you must remove this because this
#slows the webpage as it have to load such gaint sting on refereshment.
    global search_str
    search_str=""
    for itm1 in search_list:  #converting into string seperated by a space
        for itm2 in itm1:
            search_str=search_str+" "+itm2

findkey() #since this required for all fnctions


def home(request):
    global  search_str
    contex = {"search_str": search_str,"home":True}
    return render(request,'personal/home.html',contex)
def about(request):
    global search_str
    return render(request,'personal/about.html',{"search_str":search_str})

def notes(request):
    links = []
    global search_str
    for file in os.listdir('media/pdf'):
        if file.endswith('.pdf'):
            data = []
            data.append('/media/pdf' + "/" + file)
            data.append(file[:-4])
            data.append(round(os.path.getsize('media/pdf' + "/" + file)/1000000,3))
            #this just return the date of last modification in given format
            data.append(
                time.strftime("%m/%d/%Y", time.gmtime(os.path.getctime('media/pdf' + "/" + file))))

            links.append(data)
    contex = {"links": links,"search_str":search_str}
    # print(links)
    return render(request,'personal/notes.html',contex)


def acknlg(request):
    global search_str
    return render(request,'personal/acknlg.html',{"search_str":search_str})

def downloads(request):
    data = []
    global search_str
    for file in os.listdir('media/apps'):
        if file.endswith('.exe'):
            temp1 = []
            temp2=""
            temp1.append((file))
            # print(temp1)
            temp1.append(file[:-4])
            temp1.append("media/apps/" + str(file))
            try:
                with open("media/apps/" + str(file[:-4])+".txt", 'r') as temp:
                    # for line in temp.readlines():
                    #     temp2=temp2+line
                    temp1.append(temp.readlines())

            except:
                temp1.append(["Details are coming soon!!!"])
            temp1.append(round(os.path.getsize('media/apps' + "/" + file) / 1000000, 3))
            temp1.append(time.strftime("%m/%d/%Y",time.gmtime(os.path.getctime('media/apps' + "/" + file))))
            data.append(temp1)
    # print(data)
    contex = {"data": data,"search_str":search_str}
    # print(data)
    if request.method=="POST":  #this checks if page has send any signal
                                #this is signal generated when download button is pressed.
        file_dir=request.POST.get("file_dir")  #request.POST.get() is dict. object containg
        # all the values of name mentioned in form field
        # print(file_dir)
        # redirect('acknlg')
        return FileResponse(open(file_dir,'rb'),as_attachment=True) #it generates a file response for any binary files
        # like .exe,.jpg,.pdf it also contains opt. argument filename

    return render(request,'personal/downloads.html',contex)


def codesnippets(request):
    data = []
    global search_str
    for file in os.listdir('media/codesnippets'):
        if file.endswith('.txt'):
            temp1 = []
            temp1.append((file[:-4]))
            with open("media/codesnippets/"+str(file),'r') as temp:
                temp1.append(temp.readlines())
                data.append(temp1)
    contex = {"data": data,"search_str":search_str}
    # print(data)
    # print(data)
    return render(request, 'personal/codesnippets.html', contex)


def gallery(request):
    links=[]
    global search_str
    for file in os.listdir('media/images'):
        if file.endswith('.jpg') or file.endswith('.png'):
            data = []
            data.append('/media/images' + "/" + file)
            data.append(file[:-4])
            links.append(data)
            print(file)
    contex={"links":links,"search_str":search_str}
    # print(links)
    return render(request,'personal/gallery.html',contex)




def blog(request):
    global search_str
    if request.method=="POST":
        username = request.POST.get('username')
        psw = request.POST.get('password')
        user = authenticate(request, username=username, password=psw)#returns username if user with given usernsme and password exists
        # ohterwise return None
        if str(user)==str(username):
            print(user)
            login(request, user)
            return render(request, 'personal/post.html', {"search_str": search_str})
        else:
            # messages.error(request,f'Incorrect username or password!')
            return render(request, 'personal/blog.html', {"search_str": search_str})

    return render(request,'personal/blog.html',{"search_str":search_str})

@login_required(login_url='blog')
def edit_post(request):
    global search_str
    print('aah')
    if request.method=="POST":
        print('aah')
    return render(request, 'personal/edit_post.html', {"search_str": search_str})



def signup(request):
    global search_str
    if request.method == "POST":
        form=UserCreationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            # instance=Blog(request.POST.get('User_Name'),request.POST.get('Email'),
            #               request.POST.get('Phone_Number'),request.POST.get('Password'))
            # instance.save()
            instance=form.save(commit=False)
            instance.save()
            form2=UserSignupForm(request.POST)
            # print(form2.is_valid())
            if form2.is_valid():
                form2.save()  #this is for blog model
            username=request.POST.get('username')
            # messages.success(request, f'Account created for {username}!')
            return redirect('blog')
        # form.save()
        #    after login flow comes here
        # print("Here")
        # # for extracting information from request object request.POST.get("name") here "name" is key which is mentioned
        # #     in input field of form
        # print(request.POST.get("name"))
        # print(request.POST.get("pass"))
        # print(request.POST.get("eml")+"last")
        # data = []
        # data.append(request.POST.get("name"))
        # data.append(request.POST.get("eml"))
        # data.append(request.POST.get("pass"))
        # # models.database(data)
        # usr = models.User2(User_Name=data[0], Email=data[1], Password=data[2])
        # # print(usr)
        # usr.save()
    return render(request, 'personal/signup.html', {"search_str": search_str})

@login_required(login_url='blog')
def chat_board(request):
    global search_str
    return render(request, 'personal/chat_board.html', {"search_str": search_str})

@login_required(login_url='blog')
def create_post(request):
    global search_str
    if request.method == 'POST':
        p_form=CreatePostForm(request.POST)  #request.user gives current login user
        print(p_form.is_valid())
        if p_form.is_valid():
            p_form.save()
            return render(request,'personal/post.html',{'search_str':search_str})
    contex={"search_str": search_str,'Date':timezone.now()}
    return render(request, 'personal/create_post.html',contex )


@login_required(login_url='blog')
def profile(request):
    global search_str
    if request.method=='POST':
        # print(request.POST.get('username'))
        # print(request.POST.get('email'))
        u_form = UserUpdateForm(request.POST,instance=request.user)
        b_form = UserBlogUpdateForm(request.POST,request.FILES,instance=request.user.blog)
        print(u_form.is_valid())
        if u_form.is_valid() and b_form.is_valid():
            u_form.save()
            b_form.save()
            messages.success(request,'Change saved!')
            return redirect('profile')
        else:
            messages.error(request,'Sorry, some thing went wrong!')
            return redirect('profile')


    u_form=UserUpdateForm(instance=request.user)
    b_form=UserBlogUpdateForm(instance=request.user.blog)
    # print(u_form,b_form)
    contex={"search_str": search_str,'u_form':u_form,'b_form':b_form}
    return render(request, 'personal/profile.html',contex )

@login_required(login_url='blog')
def post(request):
    global search_str
    if request.method=="POST":
        if request.POST.get('edt_btn')!=None:
            post_id=request.POST.get('edt_btn')
            p=Posts.objects.filter(id=post_id).first()
            return render(request, 'personal/edit_post.html', {'search_str':search_str,
                                                               'post':p})
        if request.POST.get('update')!=None:
            # , instance = Posts.objects.filter(username_id=request.POST.get('username'))
            # save garda yadi id provide gareko xa ra tyo id already xa bhane .save() update garxa
            #tyasile update garna tyo post ko id explicitly provide garnu parxa
            update=Posts(username_id=request.POST.get('username'),
                         Post=request.POST.get('Post'),
                         Title=request.POST.get('Title'),
                         id=request.POST.get('id'))
            update.save()
            posts = Posts.objects.all().order_by('-Date')
            comments = Comments.objects.all()
            contex = {"search_str": search_str, 'posts': posts, 'comments': comments}
            return render(request, 'personal/post.html', contex)

        if request.POST.get('delete')!=None:
            delete=Posts(username_id=request.POST.get('username'),
                         Post=request.POST.get('Post'),
                         Title=request.POST.get('Title'),
                         id=request.POST.get('id'))
            delete.delete(keep_parents=True)
            posts = Posts.objects.all().order_by('-Date')
            comments = Comments.objects.all()
            contex = {"search_str": search_str, 'posts': posts, 'comments': comments}
            return render(request, 'personal/post.html', contex)

        if request.POST.get('Comment')!=None:
            c_form=CreateCommentForm(request.POST)
            posts = Posts.objects.all().order_by('-Date')
            comments = Comments.objects.all()
            if c_form.is_valid():
                c_form.save()
            contex = {"search_str": search_str, 'posts': posts, 'comments': comments}
            return render(request, 'personal/post.html', contex)

        s_usr=request.POST.get('s_usr')
        selected_user=User.objects.filter(id=s_usr).first()
        selected_post=Posts.objects.filter(username_id=s_usr).all().order_by('-Date')
        selected_comments=[]
        for pos in selected_post:
            # print(pos.id)
            selected_comments.append(Comments.objects.filter(Post_id=pos.id).all())
        # selected_comments=Comments.objects.filter(Post=selected_post).all()
        # print(selected_comments[0])
        # for itm in selected_comments[0]:
        #     print(itm.Post)
        contex={"search_str": search_str,'selected_post':selected_post,
                'selected_comments':selected_comments,'selected_user':selected_user}
        return render(request,'personal/user_detail.html',contex)
    posts=Posts.objects.all().order_by('-Date')
    # comments=Comments.objects.filter(Post_id=1).all()
    comments=Comments.objects.all()
    # print(comments)
    contex={"search_str": search_str,'posts':posts,'comments':comments}
    return render(request, 'personal/post.html', contex)

@login_required(login_url='blog')
def user_detail(request):
    global search_str
    if request.method=="POST":
        print('done')
    posts = Blog.objects.all()
    return render(request, 'personal/user_detail.html', {"search_str": search_str, 'posts': posts})


def search(list1,list2):
    for itm1 in list1:
        for itm2 in list2:
            if str(itm1).upper()==str(itm2).upper():
                return True



def search_result(request):
    global search_str
    if request.method=="POST":
        if request.POST.get("srch_val")=="":
            return render(request, 'personal/search_result.html',{"messg":True})
        srch_val=request.POST.get("srch_val").split(" ")
        result1=[]
        for file in os.listdir('media/pdf'):
            if file.endswith('.pdf'):
                if search(srch_val,(file[:-4].split(" "))) or srch_val[0]=="pdf":
                    found=[]
                    found.append("pdf")
                    found.append('/media/pdf' + "/" + file)
                    found.append(file)
                    found.append(round(os.path.getsize('media/pdf' + "/" + file) / 1000000, 3))
                    # this just return the date of last modification in given format
                    found.append(
                        time.strftime("%m/%d/%Y",
                                      time.gmtime(os.path.getctime('media/pdf' + "/" + file))))
                    result1.append(found)
        for file in os.listdir('media/apps'):
            if file.endswith('.exe'):
                if search(srch_val, (file[:-4].split(" "))):
                    found = []
                    found.append("apps")
                    found.append('media/apps' + "/" + file)
                    temp2 = ""
                    found.append((file))
                    # print(temp1)
                    found.append(file[:-4])
                    try:
                        with open("media/apps/" + str(file[:-4]) + ".txt", 'r') as temp:
                            found.append(temp.readlines())
                    except:
                        found.append(["Details are coming soon!!!"])
                    found.append(round(os.path.getsize('media/apps' + "/" + file) / 1000000, 3))
                    # this just return the date of last modification in given format
                    found.append(
                        time.strftime("%m/%d/%Y",
                                      time.gmtime(os.path.getctime('media/apps' + "/" + file))))
                    result1.append(found)

        for file in os.listdir('media/images'):
            if file.endswith('.jpg') or file.endswith('.png'):
                if search(srch_val, (file[:-4].split(" "))):
                    found = []
                    found.append("images")
                    found.append(file)
                    found.append('/media/images' + "/" + file)
                    result1.append(found)
        for file in os.listdir('media/codesnippets'):
            if file.endswith('.txt'):
                if search(srch_val, (file[:-4].split(" "))):
                    found = []
                    found.append("code")
                    found.append((file[:-4]))
                    with open("media/codesnippets/" + str(file), 'r') as temp:
                        found.append(temp.readlines())
                        result1.append(found)

        for file in os.listdir('media/multimedia'):
            if search(srch_val, (file[:-4].split(" "))):
                found = []
                found.append("multimedia")
                found.append(file)
                found.append('media/multimedia' + "/" + file)
                result1.append(found)

        for file in User.objects.all():
            if search(srch_val, (str(file).split(" "))):
                found = []
                found.append("user")
                found.append(file)
                result1.append(found)

        for file in Posts.objects.all():
            if search(srch_val, (str(file.Title).split(" "))):
                found = []
                found.append("post")
                found.append(file)
                result1.append(found)


        result=[]
        for val in result1: #filter for none value
            if val[1] ==None:
                pass
            else:
                result.append(val)
        lenght=len(result)
        contex = {"result": result,"lenght":lenght,"srch_val":srch_val,"search_str":search_str}
        print(result)
        return render(request, 'personal/search_result.html',contex)
    return render(request,'personal/search_result.html')
