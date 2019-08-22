from datetime import date  

from django.contrib.auth.models import User 
from rest_framework import serializers
from rest_framework.reverse import reverse 

from .models import Book


class BookSerializer(serializers.ModelSerializer):  
    borrowed = serializers.ReadOnlyField(source='borrowed.username', read_only=True)
    links = serializers.SerializerMethodField('get_links', read_only=True)

    class Meta:
        model = Book
        fields = (
            'id',
            'borrowed',
            'title',
            'author',
            'description',
            'pub_date',
            'age_limit',
            'links',
        )

    def get_links(self, obj):
        request = self.context.get('request')
        return {
            'self': reverse('book-detail',
                kwargs={'pk': obj.pk, 'username': obj.borrowed},request=request),
            'borrowed': reverse('user-detail',
                kwargs={'username': obj.borrowed}, request=request)
        }
    
    def validate_age_limit(self, age_limit):
        if age_limit < 0 or age_limit > 21:
            msg = 'Age limit must be between 0 and 21.'  
            raise serializers.ValidationError(msg)
        return age_limit

    def validate_pub_date(self, pub_date):
        if pub_date > date.today():
            msg = 'Publication date cannot be in the future.'
            raise serializers.ValidationError(msg)
        return pub_date



class UserSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField('get_links', read_only=True)
    
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'date_joined',
            'last_login',
            'links'
        )
        read_only_fields = (
            'id',
            'date_joined',
            'last_login',
        )

    def get_links(self, obj):
        request = self.context.get('request')
        username = obj.get_username()
        if request is None:
            return {}
        return {
            'self': reverse('user-detail',
                kwargs={'username': username}, request=request),
            'books': reverse('book-list', kwargs={'username': username}, request=request),
        }