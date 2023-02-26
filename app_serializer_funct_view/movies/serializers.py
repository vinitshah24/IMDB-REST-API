from rest_framework import serializers
from movies.models import Movie


def name_length(value):
    if len(value) < 2:
        raise serializers.ValidationError("Name is too short!")


class MovieSerializer(serializers.Serializer):
    # We hae to ensure that the validation is enforeced which we set for models columns
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(validators=[name_length])
    description = serializers.CharField(max_length=200)
    active = serializers.BooleanField()

    # Calling .save() will either create a new instance, or update an existing instance,
    # depending on if an existing instance was passed when instantiating the serializer class

    def create(self, validated_data):
        # MUST BE IMPLEMENTED FOR CREATE
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # MUST BE IMPLEMENTED FOR UPDATE
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance

    def validate(self, data):
        # Object level validation
        if data['name'] == data['description']:
            raise serializers.ValidationError("Title and Description should be different!")
        else:
            return data

    # def validate_name(self, value):
    #     # Method should be named validate_FIELD
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short!")
    #     else:
    #         return value

