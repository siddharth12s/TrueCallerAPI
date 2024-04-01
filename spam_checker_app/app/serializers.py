from rest_framework import serializers
from app.models import User, Contacts, SpamNumber

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone_no', 'password', 'email']

    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

    def validate(self, data):
        phone_no = data['phone_no']

        if len(phone_no) != 10:
            raise serializers.ValidationError('Invalid Phone Number')

        return data

class ContactSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Contacts
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        contact = Contacts.objects.create(user=user, **validated_data)
        return contact
    
    def validate(self, data):
        phone_no = data['contact_number']

        if len(phone_no) != 10:
            raise serializers.ValidationError('Invalid Phone Number')
    
        return data

        

class SpamNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamNumber
        fields = '__all__'
    
    def validate(self, data):
        phone_no = data['spam_number']

        if len(phone_no) != 10:
            raise serializers.ValidationError('Invalid Phone Number')
        
        return data

