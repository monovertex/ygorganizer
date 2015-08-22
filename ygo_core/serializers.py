from rest_framework import serializers
from .models import Constant


class ConstantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Constant
        fields = ('id', 'identifier', 'name',)
