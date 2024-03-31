from rest_framework import serializers
from .models import CustomUser
from .models import Paragraph


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'dob', 'created_at', 'modified_at']
        #fields = '__all__'  # Include all fields of the CustomUser model



class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = '__all__'
