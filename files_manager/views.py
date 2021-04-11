from pathlib import Path

from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from storage.settings import MEDIA_ROOT

from .models import Data
from .serializers import DataSerializer


class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format_=None):
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            for k, v in kwargs.items():
                for id in v.split(','):
                    obj = get_object_or_404(Data, file_hash=id)
                    file_path = Path(MEDIA_ROOT) / Path(str(obj))
                    self.perform_destroy(obj)
                    file_path.unlink(missing_ok=True)
                    return Response(status=status.HTTP_202_ACCEPTED)
        except Http404:
            return Response(status=status.HTTP_204_NO_CONTENT)
