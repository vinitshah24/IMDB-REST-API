from rest_framework import serializers
from movies.models import Movie

class MovieSerializer(serializers.ModelSerializer):

    name_length = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'
        # include = ['id', 'name']
        # exclude = ['description']

    def get_name_length(self, obj):
        # Custom field not present in the model
        return len(obj.name)

    def validate(self, data):
        # Object level validation
        if data['name'] == data['description']:
            raise serializers.ValidationError("Title and Description should be different!")
        else:
            return data

    def validate_name(self, value):
        # Method should be named validate_FIELD
        if len(value) < 2:
            raise serializers.ValidationError("Name is too short!")
        else:
            return value

