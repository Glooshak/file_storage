from pathlib import Path
import logging
from logging import getLogger
from http import HTTPStatus

from django.db import IntegrityError
from rest_framework import viewsets
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponseRedirect, HttpResponse, FileResponse, HttpResponseNotFound, JsonResponse, \
    HttpResponseForbidden, HttpResponsePermanentRedirect
from django.urls import reverse
from rest_framework.response import Response
from django.views.decorators.http import require_GET, require_POST
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser, FormParser

from storage.settings import MEDIA_ROOT
from .models import Data
from .serializers import DataSerializer
from .custom_storage_system import storage
from .utils import obtain_relative_file_path


logger = getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@require_GET
def show_feed(request):
    return render(request, 'files_manager/feed.html', context={'objects': Data.objects.all()})


@require_GET
def show_details(request, file_hash):
    return HttpResponse('<h1>There will be files details</h1>')


@require_GET
def upload_file(request):
    return render(request, 'files_manager/uploading_file.html')


def execute_deletion(request, file_hash: str):
    if Data.objects.filter(file_hash=file_hash).exists():
        file = str(obtain_relative_file_path(file_hash))
        if storage.exists(file):
            storage.delete(file)
        Data.objects.get(file_hash=file_hash).delete()
        return render(request, 'files_manager/successfully_deletion.html', context={'file': file_hash})
    else:
        return HttpResponsePermanentRedirect(redirect_to=reverse('files_manager-files_list'))


def confirm_uploading(request):
    return render(request, 'files_manager/successfully_uploading.html')


class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request, *args, **kwargs):
        queryset = Data.objects.all()
        data = dict(content='There are no uploaded files!')

        if queryset:
            files_dict = dict()
            for number, instance in enumerate(queryset):
                datetime_representation = instance.date_created.strftime("%m/%d/%Y, %H:%M:%S")
                files_dict[number + 1] = dict(
                    zip(
                        ['file_hash', 'size', 'location', 'date_created'],
                        [instance.file_hash, instance.file.size, instance.file.path, datetime_representation]
                    )
                )
            data['content'] = files_dict

        return JsonResponse(data, safe=True)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if Data.objects.filter(file_hash=pk).exists() and storage.exists(obtain_relative_file_path(pk)):
            obj = Data.objects.get(file_hash=pk)
            # FileResponse instance streams a file out in small chunks. The file will be closed automatically.
            response = FileResponse(obj.file.open())
            return response
        else:
            return HttpResponseNotFound()

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
                           f'will inherit the record in the db of the old deleted file.')
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
