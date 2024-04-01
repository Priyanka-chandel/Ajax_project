from django.shortcuts import render,redirect
from django.http import HttpResponse
from Ajax_app.form import UserRegistrationform,UserLoginForm,NoteForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from Ajax_app.models import Note

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        form =NoteForm
        notes = Note.objects.filter(user=request.user).order_by('-id')
        data={
            'form':form,
            'notes':notes,
        }
        if request.method=="POST":
            title=request.POST.get('title')
            description=request.POST.get('description')
            print(title,description)

            note=Note()
            note.title=title
            note.description=description
            note.user =request.user
            note.save()
            notes=Note.objects.values().filter(user =request.user).order_by('-id')
            user_notes=list(notes)
            return JsonResponse({"status":"1","status_message":'Your Note Added Successfully','notes':'user_notes'})

        return render(request, 'notes/index.html',context=data)
    else:
        return redirect('login')
    
def edit_note(request):
    edit_id =request.POST.get('edit_id')
    title =request.POST.get('title')
    description =request.POST.get('description')
    Note.objects.filter(id=edit_id).update(title=title,description=description)
    notes=Note.objects.values().filter(user =request.user).order_by('-id')
    user_notes=list(notes)
    return JsonResponse({"status":"1","status_message":'Your Note Updated Successfully','notes':'user_notes'})

def delete_note(request):
    delete_id =request.GET.get('delete_id')
    print(delete_id)
    Note.objects.filter(id=delete_id).delete()
    notes=Note.objects.values().filter(user =request.user).order_by('-id')
    user_notes=list(notes)
    return JsonResponse({"status":"1","status_message":'Your Note Deleted Successfully','notes':'user_notes'})


def signup(request):
    form =UserRegistrationform()
    data={
        'form':form,
    }
    if request.method =='POST':
        username =request.POST.get('username')
        email =request.POST.get('email')
        password =request.POST.get('password')
        re_password =request.POST.get('re_password')

        if(password !=re_password):
            messages.error(request, "password do not match")
        else:
            user =User.objects.create_user(username=username,password=password,email=email)
            if(user.is_active):
                print('register')
                messages.success(request, "user created")
                
            else:
                print('error')

    return render(request,template_name='notes/signup.html',context=data)

def userlogin(request):
    form=UserLoginForm()
    data = {
        'form':form,
    }
    if request.method =="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user = authenticate(request,username=username,password=password)
        except:
            return JsonResponse({"status":"Invalid Credential"})

        if user is not None:
            login(request,user)
            return JsonResponse({"status":"User login successfull"})
            
        else:
            return JsonResponse({"status":"Invalid Credential"})
        
        print( username, password)
        
    
    return render(request,template_name='notes/login.html',context=data)

def userlogout(request):
    logout(request)
    return redirect('login')

