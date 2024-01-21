from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.db.models import Q
from django.contrib import messages
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import RoomModel, TopicModel, MassageModel, CustomUser
from .forms import RoomForm, CustomUserCreationForm, updateUserProfileForm

# Create your views here.


def userRegister(request):
  form = CustomUserCreationForm()
  
  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request,user)
      return redirect('home')
  context ={'form':form}
  return render(request,"user_register.html",context)

def userLogin(request):
  if request.method =='POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
      user = CustomUser.objects.get(username=username)
    except:
      messages.error(request,"user doesn't exit")
    
    user = authenticate(request, username=username,password=password)
    
    if user is not None:
      login(request,user)
      return redirect('home')
    else:
      messages.error(request,"User Name or Password is wrong")
  return render(request, "user_login.html")


def userLogout(request):
  logout(request)
  return redirect('home')




def home(request):
  if request.GET.get('q') != None :
    q = request.GET.get('q')
    rooms = RoomModel.objects.filter(
      Q(topic__name__icontains=q)|
      Q(host__username__icontains=q)|
      Q(description__icontains=q)|
      Q(name__icontains=q)
    )
    room_massage = MassageModel.objects.filter(Q(room__topic__name__icontains=q)).order_by('-created')
  else:
    room_massage = MassageModel.objects.all().order_by('-created')
    rooms = RoomModel.objects.all()
  topics = TopicModel.objects.all()
  rooms_count = rooms.count()
  context = {'rooms': rooms, 'topics': topics, 'rooms_count':rooms_count, 'room_massage': room_massage}
  return render(request, "home.html", context)


def room(request,pk):
  room = RoomModel.objects.get(id=pk)
  room_massage = room.massagemodel_set.all()
  participants = room.participants.all()
  if request.method =='POST':
    massage = MassageModel.objects.create(
      user = request.user,
      room = room,
      body = request.POST.get('body')
    )
    room.participants.add(request.user)
    return redirect('room', pk=room.id)
  context={'room': room, 'room_massage': room_massage, 'participants': participants}
  return render(request, "room.html", context)

@login_required(login_url='userlogin')
def userProfile(request,pk):
  user = CustomUser.objects.get(id=pk)
  rooms = user.roommodel_set.all()
  rooms_count = rooms.count()
  room_massage = user.massagemodel_set.all()
  topics = TopicModel.objects.all()
  context={'user':user, 'rooms': rooms, 'room_massage': room_massage, 'topics': topics, 'rooms_count':rooms_count}
  return render(request, "profile.html",context)

@login_required(login_url='userlogin')
def update_userProfile(request,pk):
  user = CustomUser.objects.get(id=pk)
  form = updateUserProfileForm(instance=user)
  print(user.username)
  if request.method=='POST':
      user.name = request.POST.get('name')
      user.email = request.POST.get('email')
      user.username = request.POST.get('username')
      user.bio = request.POST.get('bio')
      user.save()
      return redirect('profile', user.id )
  return render(request, "update_user_profile.html", {'user_form': form }) 

@login_required(login_url='userlogin')
def create_room(request):
  form = RoomForm()
  topics = TopicModel.objects.all()
  if request.method == 'POST':
    topic_name = request.POST.get('topic')
    topic, created = TopicModel.objects.get_or_create(name=topic_name)
    room = RoomModel.objects.create(
      host= request.user,
      topic = topic,
      name = request.POST.get('name'),
      description = request.POST.get('description'),
    )
    room.participants.add(request.user)
    
    return redirect('home')
  context={'form': form, 'topics': topics}
  return render(request, "room_form.html", context)



@login_required(login_url='userlogin')
def update_room(request,pk):
  room = RoomModel.objects.get(id=pk)
  form = RoomForm(instance=room)
  topics = TopicModel.objects.all()
  
  if request.user == room.host:
    if request.method=='POST':
      topic_name = request.POST.get('topic')
      topic , created = TopicModel.objects.get_or_create(name=topic_name)
      room.name = request.POST.get('name')
      room.topic = topic
      room.description = request.POST.get('description')
      room.save()
      return redirect('home')
  else:
    HttpResponse("Only Creator of the room can edit ")
    return redirect('home')
  context = {'form':form,'topics':topics, 'room': room}
  return render(request, "room_form.html", context)



@login_required(login_url='userlogin')
def DeleteRoom(request,pk):
  room = RoomModel.objects.get(id=pk)
  if request.user == room.host:
    if request.method == 'POST':
      room.delete()
      return redirect('home')
  else:
    HttpResponse("Only Creator of the room can delete ")
    return redirect('home')
  context = {'obj': room}
  return render(request, 'delete.html', context)


@login_required(login_url='userlogin')
def DeleteMassage(request,pk):
  massage = MassageModel.objects.get(id=pk)
  if request.user == massage.user:
    if request.method == 'POST':
      massage.delete()
      room_id = massage.room.id
      # return redirect('room', pk=room_id)
      return redirect(request.path_info)
  else:
    HttpResponse("Only Creator of the room can delete ")
    return redirect('home')
  context = {'obj': massage}
  return render(request, 'delete.html', context)