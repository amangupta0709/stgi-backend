# from django.contrib.auth.tokens import default_token_generator
from knox.models import AuthToken
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from main.models import UserMapping

from main.serializer import UserMappingSerializer
from main.utils import GeneratorUtil

import sys
from io import StringIO
import json


class objlist(list):
    @property
    def item(self):
        if type(self[0]) is not list and type(self[0]) is not dict:
            return self
        keys = set()
        new_objlist = []
        for it in self:
            if type(it) is list:
                new_objlist.append(it[0])
            else:
                new_objlist.append(it)

        for it in new_objlist:
            for k in it.keys():
                keys.add(k)

        itemdict = {}
        for k in keys:
            itemdict[k] = []
            for it in new_objlist:
                v = it.get(k)
                if v:
                    itemdict[k].append(v)

        return dotdict(itemdict)

    @property
    def sum(self):
        res = 0
        if len(self) != 0:
            for num in self:
                num = int(num)
                res += num

        return res


class dotdict(dict):
    __getattr__ = dict.__getitem__

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct):
        for key, val in dct.items():
            if type(val) is dict:
                val = dotdict(val)
            elif type(val) is list and len(val) != 0:
                # print(val)
                val = objlist(val)

            self[key] = val


class GeneratorAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [
        MultiPartParser,
    ]
    serializer_class = UserMappingSerializer

    def post(self, request, *args, **kwargs):
        mapping_file = request.data.get("mapping_file")
        source_json = request.data.get("source_json")

        if not source_json or not mapping_file:
            print("hereeeeeeee")
            return Response(
                {"message": "Missing data"}, status=status.HTTP_400_BAD_REQUEST
            )

        obj = GeneratorUtil()
        res = obj.generate(source_json, mapping_file)
        data = {"user": request.user.id, "name": mapping_file.name, "script": res}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # with open("abcd.py", "w") as file:
        #     file.write(res)
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)


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

        script = obj.script % source_json

        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        exec(script)
        sys.stdout = old_stdout

        target_json = json.loads(redirected_output.getvalue().replace("'", '"').strip())

        return Response({"data": target_json}, status=status.HTTP_200_OK)
