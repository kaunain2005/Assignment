from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Client, Project
from .serializers import (
    ClientSerializer,
    ClientDetailSerializer,
    ProjectSerializer,
    ProjectCreateSerializer
)
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

# Create your views here.

class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("Only staff can create clients.")
        serializer.save(created_by=self.request.user)

class ClientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ClientDetailSerializer
        return ClientSerializer
    
    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("Only staff can update clients.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_staff:
            raise PermissionDenied("Only staff can delete clients.")
        instance.delete()

class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("Only staff can create projects.")
        client_id = self.kwargs['pk']
        client = Client.objects.get(pk=client_id)
        serializer.save(client=client, created_by=self.request.user)

class UserProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.projects.all()
