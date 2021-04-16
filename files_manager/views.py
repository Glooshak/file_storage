from pathlib import Path
import logging
from logging import getLogger

from django.db import IntegrityError
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser, FormParser

from storage.settings import MEDIA_ROOT
from .models import Data
from .serializers import DataSerializer
from .custom_storage_system import storage
from .utils import obtain_relative_file_path


logger = getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if Data.objects.filter(file_hash=pk).exists() and storage.exists(obtain_relative_file_path(pk)):
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
            return Response(
                data={'file_hash': Data.objects.last().file_hash},
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except IntegrityError:
            logger.warning(f'Somebody deleted a file that has its record in the db,'
                           f' but another file with the same hash was uploaded, so this new file '
                           f'will inherits the record in the db of the old deleted file.')
            return Response(data={'file_hash': Data.objects.last().file_hash}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            obj = get_object_or_404(Data, file_hash=pk)
            self.perform_destroy(obj)
            rel_file_path = obtain_relative_file_path(pk)
            if storage.exists(rel_file_path):
                storage.delete(rel_file_path)
            return Response(status=status.HTTP_202_ACCEPTED)
        except Http404:
            return Response(status=status.HTTP_204_NO_CONTENT)
