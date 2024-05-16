from rest_framework import serializers
from main.models import Question, Photo

class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ('image',)

class QuestionSerializer(serializers.ModelSerializer):

    images = PhotoSerializer(many=True, read_only=True)

    class Meta:

        model = Question
        fields = ['subject', 'content', 'images']

    def create(self, validated_data):

        images_data = self.context['request'].FILES
        post = Question.objects.create(**validated_data)

        for image_data in images_data.getlist('image'):

            Photo.objects.create(post=post, image=image_data)

        return post