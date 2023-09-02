from rest_framework import serializers

from main.models import Bb, Comment, SubRubric, SuperRubric


class BbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = ('id', 'title', 'content', 'price', 'created_at', 'image')


class BbDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = (
            'id', 'title', 'content', 'price', 'created_at',
            'contacts', 'image'
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('bb', 'author', 'content', 'created_at')


class SubRubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubRubric
        fields = ('id', 'name')


class RubricSerializer(serializers.ModelSerializer):
    rubrics = SubRubricSerializer(many=True, read_only=True)

    class Meta:
        model = SuperRubric
        fields = ('id', 'name', 'rubrics')
