from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,logout,login
from .models import *

def index(request):
    return render(request,'index.html')

def login(request):
    error=""
    if request.method=='POST':
        u = request.POST['uname']
        p = request.POST['pswd']
        user = auth.authenticate(username=u,password=p)
        try:
            if user.is_staff:
                auth.login(request,user)
                error="no"
            elif user is not None:
                auth.login(request,user)
                error="not"
            else:
                error="yes"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'login.html',d)

def register(request):
    error=""
    if request.method=='POST':
        fn = request.POST['fname']
        ln = request.POST['lname']
        e = request.POST['email']
        c = request.POST['contact']
        dob = request.POST['dob']
        p = request.POST['pwd']
        g = request.POST['gender']
        i = request.FILES['profile_pic']
        try:
            user = User.objects.create_user(first_name=fn,last_name=ln,username=e,password=p)
            Signup.objects.create(user=user,mobile=c,image=i,gender=g,dob=dob)
            error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'register.html',d)

def user_home(request):
    if not request.user. is_authenticated:
        return redirect('login')
    return render(request,'user_home.html')

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,'admin_home.html')


def logout(request):
    auth.logout(request)
    return redirect('/')

def add_room(request):
    if not request.user.is_authenticated:
        return redirect(login())
    error = ""
    if request.method=='POST':
        n = request.POST['roomno']
        p = request.POST['price']
        rt = request.POST['rtype']
        s = request.POST['status']
        i = request.FILES['image']
        try:
            Room.objects.create(room_no=n,image=i,type=rt,status=s,price=p)
            error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'add_room.html',d)

def view_room_admin(request):
    data = Room.objects.all()
    d = {'data':data}
    return render(request,'view_room_admin.html',d)

def delete_room(request,id):
    data = Room.objects.get(id=id)
    data.delete()
    return redirect('view_room_admin')

def edit_room(request,id):
    error = ""
    data = Room.objects.get(id=id)
    if request.method=='POST':
        rno = request.POST['roomno']
        p = request.POST['price']
        rt = request.POST['rtype']
        s = request.POST['status']
        data.room_no=rno
        data.type=rt
        data.status=s
        data.price=p
        try:
            data.save()
            error="no"
        except:
            error="yes"
        try:
            i = request.FILES['room_img']
            data.image = i
            data.save()
        except:
            pass
    d = {'data':data,'error':error}
    return render(request,'edit_room.html',d)

def view_user(request):
    data = Signup.objects.all()
    d = {'data':data}
    return render(request,'view_user.html',d)

def delete_user(request,id):
    data = User.objects.get(id=id)
    data.delete()
    return redirect('view_user')

def change_password_admin(request):
    error = ""
    if request.method == 'POST':
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    d = {'error': error}
    return render(request,'change_password_admin.html',d)

def view_booking(request):
    data = Booking.objects.all()
    d={'data':data}
    return render(request,'view_booking.html',d)

def view_booking_user(request):
    data = Booking.objects.all()
    d = {'data':data}
    return render(request,'view_booking_user.html',d)

def view_room_user(request):
    data = Room.objects.all()
    d = {'data':data}
    return render(request,'view_room_user.html',d)

def book_room(request,id):
    error=""
    data3 = Room.objects.get(id=id)
    i = request.user
    data2 = Signup.objects.get(user=i)
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        f = f+" "+l
        e = request.POST['email']
        c1 = request.POST['contact']
        c2 = request.POST['contact2']
        bd = request.POST['booking_date']
        day = request.POST['select_days']
        g = request.POST['gender']
        p = request.POST['price']
        dob = request.POST['dob']
        rn = request.POST['roomno']
        p = int(p) * int(day)
        try:
            Booking.objects.create(room_no=rn,name=f,email=e,dob=dob,gender=g,contact1=c1,contact2=c2,
                                   booking_date=bd,total_days=day,price=p,status="Pending")
            error="no"
        except:
            error="yes"
    d = {'data3':data3,'data2':data2,'error':error}
    return render(request,'book_room.html',d)


def room_view(request):
    data = Room.objects.all()
    d = {'data':data}
    return render(request,'room_view.html',d)

def cancel_booking(request,id):
    data = Booking.objects.get(id=id)
    data.delete()
    return redirect('view_booking_user')

def feedback(request):
    error=""
    data = Signup.objects.get(user=request.user)
    if request.method=='POST':
        n = request.POST['fname']
        e = request.POST['email']
        c = request.POST['mobile']
        f = request.POST['purpose']
        try:
            Feedback.objects.create(name=n,email=e,contact=c,comment=f)
            error="no"
        except:
            error="yes"
    d = {'error':error,'data':data}
    return render(request,'feedback.html',d)

def change_password_user(request):
    error=""
    if request.method=='POST':
        c=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d={'error':error}
    return render(request,'change_password_user.html',d)

def delete_booking(request,id):
    data = Booking.objects.get(id=id)
    data.delete()
    return redirect('view_booking')

def change_status(request,id):
    error=""
    data = Booking.objects.get(id=id)
    if request.method=='POST':
        s=request.POST['rstatus']
        data.status=s
        try:
            data.save()
            error="no"
        except:
            error="yes"
    d={'data':data,'error':error}
    return render(request,'change_status.html',d)

def edit_user(request):
    error=""
    data=User.objects.get(id=request.user.id)
    data2= Signup.objects.get(user=request.user)
    if request.method=='POST':
        f=request.POST['fname']
        l= request.POST['lname']
        e=request.POST['email']
        c=request.POST['contact']
        g=request.POST['gender']
        dob=request.POST['dob']
        try:
            i=request.FILES['image']
            data2.image=i
        except:pass
        data.first_name=f
        data.last_name=l
        data.username=e
        data2.mobile=c
        data2.gender=g
        data2.dob=dob
        try:
            data.save()
            data2.save()
            error="no"
        except:
            error="yes"
    d={'data':data,'data2':data2,'error':error}
    return render(request,'edit_user.html',d)

def view_feedback(request):
    data=Feedback.objects.all()
    d={'data':data}
    return render(request,'view_feedback.html',d)

def delete_feedback(request,id):
    data=Feedback.objects.get(id=id)
    data.delete()
    return  redirect('view_feedback')