from pathlib import Path

from django.db import IntegrityError
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser, FormParser

from storage.settings import MEDIA_ROOT, MEDIA_URL
from .models import Data
from .serializers import DataSerializer


class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if Data.objects.filter(file_hash=pk).exists():
            obj = Data.objects.get(file_hash=pk)
            return HttpResponseRedirect(redirect_to=obj.file.url)
        else:
            get_object_or_404(Data, file_hash=pk)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            serializer.data.pop('file')
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # If we receive a file with a hash that already exists in db.
        except IntegrityError:
            return Response(status.HTTP_409_CONFLICT)

    def destroy(self, request, *args, **kwargs):
        try:
            for k, v in kwargs.items():
                for id_ in v.split(','):
                    obj = get_object_or_404(Data, file_hash=id_)
                    file_path = Path(MEDIA_ROOT) / Path(str(obj))
                    self.perform_destroy(obj)
                    file_path.unlink(missing_ok=True)
                    return Response(status=status.HTTP_202_ACCEPTED)
        except Http404:
            return Response(status=status.HTTP_204_NO_CONTENT)
