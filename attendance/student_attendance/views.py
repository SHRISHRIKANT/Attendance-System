from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from student_attendance.models import attend
from django.contrib import messages
from django.contrib.auth.models import User,auth

# Create your views here. render- whereevr we want to diplay the page, render-.html,request, redirect-path
def index(request):
    return (render(request,'index.html'))

def student(request):
    if request.method =='POST':
        username = request.POST.get('username',False)
        password = request.POST.get('password',False)

        user1 = auth.authenticate(username=username,password=password)

        if user1 is not None:
            if user1.is_staff==True:
                messages.error(request, 'Try Student-credentials')
                return(redirect('student'))
            else:
                auth.login(request,user1)
                return(redirect("attend"))
                
        else:
            messages.error(request, 'Invalid Credentials')
            return(redirect('student'))
            
    
    return (render(request,'student.html'))

def teacher(request):
    if request.method =='POST':
        username = request.POST.get('username',False)
        password = request.POST.get('password',False)

        user1 = auth.authenticate(username=username,password=password)

        if user1 is not None:
            if user1.is_superuser==True:
                messages.error(request, 'Try Teacher Credentials')
            elif user1.is_staff==False:
                    messages.error(request, 'Try Teacher Credentials')
            else:
                auth.login(request,user1)
                return(redirect("list_update"))
        else:
            messages.error(request, 'Invalid Credentials')
            return(redirect('teacher'))
            
    
    return (render(request,'teacher.html'))

def admins(request):
    if request.method =='POST':
        username = request.POST.get('username',False)
        password = request.POST.get('password',False)

        user1 = auth.authenticate(username=username,password=password)

        if user1 is not None:
            if user1.is_superuser==True:
                if user1.is_staff==True:
                    auth.login(request,user1)
                    messages.success(request, 'Succesfully, loged-in!!!')
                    return(redirect("list_attend"))
                else:
                    pass
            else:
                messages.error(request, 'Try Admin-Credentials!!!')
        else:
            messages.error(request, 'Invalid Credentials')
            return(redirect('admins'))
            
    
    return (render(request,'admins.html'))

def present(request):
    
    if request.method == "POST":
        Fname = auth.get_user(request).first_name
        Lname = auth.get_user(request).last_name
        Status = None

        if User.objects.filter(first_name=Fname).exists():
            if not attend.objects.filter(Lname=Lname).exists():

                user = attend(Fname=Fname,Lname=Lname,Status=Status)
                user.save()
                messages.success(request, 'Attendance Request Sent!!!')
                return(redirect("list_attend"))
            else:
                messages.error(request,"Already,exits")
                return (redirect('list_attend'))
        else:
            messages.error("Not a student!!!")
            return (render(request,'attendance.html'))

    else:
        return (render(request,'attendance.html',context={
            'Fname':auth.get_user(request).first_name,'Lname':auth.get_user(request).last_name}))
    
def new(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name=request.POST.get("Lname")

        if User.objects.filter(username=username).exists():
            messages.success(request, 'Username already exits')
            return(redirect('register'))
        
        if User.objects.filter(last_name=last_name).exists():
            messages.success(request, 'Roll number already exits')
            return(redirect('register'))
        Student = User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name)
        
        messages.success(request, 'Registration successfully done!!!')
        
        

        Student.save()
    else:
        messages.error(request,"authentication needed")
        render(request,'index.html')

    return (render(request,'register.html'))

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return(redirect('/'))
    else:
        messages.error(request,"authentication needed")
        return(redirect('/'))

def all_attend(request):

    if request.user.is_authenticated:
        attend_list=attend.objects.all()
        return render(request,('attend_list.html'),{'attend_list':attend_list})
    else:
        messages.error(request,"authentication needed")
        return(redirect,'index.html')

def all_update(request):

    if request.user.is_authenticated:
        attend_list2=attend.objects.all()
        return render(request,('update.html'),{'attend_list':attend_list2})
    else:
        messages.error(request,"authentication needed")
        render(request,'index.html')
    
def editattend(request,Lname):
    if request.user.is_authenticated:
        attend_list1=attend.objects.get(Lname=Lname)
        return render(request,("edit.html"),{"attend":attend_list1})
    else:
        messages.error(request,"authentication needed")
        render(request,'index.html')
    
def updateattend(request,Lname):
    if request.user.is_authenticated:
        updateattend1=attend.objects.get(Lname=Lname)
        updateattend1.Status=request.POST["Status"]
        updateattend1.save()
    else:
        messages.error(request,"authentication needed")
        render(request,'index.html')
    return redirect("list_update")

def req(request):
    current_user=auth.get_user(request)
    current_user.last_name="Requested"
    current_user.save()
    return redirect("attendance")