# from django.contrib.auth.tokens import default_token_generator
from knox.models import AuthToken
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from main.models import UserMapping

from main.serializer import UserMappingSerializer


class GeneratorAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [
        MultiPartParser,
    ]
    serializer_class = UserMappingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.initial_data["user"] = request.user.id
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Mapping Uploaded"}, status=status.HTTP_201_CREATED)


class ExecutorAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserMappingSerializer
    queryset = UserMapping.objects.all()

    def get(self, request, *args, **kwargs):
        objs = UserMapping.objects.filter(user=request.user)
        serializer = self.get_serializer(objs, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        mapping_id = request.data.get("mapping_id")
        source_json = request.data.get("source_json")
        if not mapping_id and not source_json:
            return Response(
                {"message": "Missing Data"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            obj = UserMapping.objects.get(id=mapping_id)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        mapping_file = obj.file

        return Response({"message": "target json"}, status=status.HTTP_200_OK)
