from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from monitor.serializers import UserSerializer, GroupSerializer
from monitor.models import Monitor, Ping
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


from monitor.models import Monitor
from monitor.serializers import MonitorSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, renderers
from rest_framework.decorators import api_view

from rest_framework import generics
from datetime import datetime, timedelta

class MonitorList(generics.ListCreateAPIView):
    queryset = Monitor.objects.all().order_by('-timestamp')
    serializer_class = MonitorSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100


class PingList(generics.ListCreateAPIView):
    queryset = Ping.objects.all()
    serializer_class = PingSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100



class MonitorListLast(generics.ListCreateAPIView):
    backtime = datetime.now()-timedelta(minutes=10)
    now = datetime.now()+timedelta(minutes=2)

    queryset = Monitor.objects.filter(timestamp__range=[backtime,now])
    serializer_class = MonitorSerializer

    """
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    """

# here you could easily disconnect Update/Destroy functionality
class MonitorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer
    
    
