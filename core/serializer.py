from rest_framework import serializers
from . models import *

## this is the serializers file that add all serializer of the database
## this is helpful to send the data to the front end

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class BasicSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicSubject
        fields = '__all__'
class GradeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeType
        fields = '__all__'

