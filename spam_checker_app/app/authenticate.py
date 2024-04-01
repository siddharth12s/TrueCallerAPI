from django.contrib.auth.backends import ModelBackend
from app.models import User


class CustomBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        user_phone_no = kwargs['phone_no']
        user_email = kwargs['email']
        password = kwargs['password']
        try:
            if user_phone_no:
                user = User.objects.get(phone_no=user_phone_no)
                if user.check_password(password):
                    return user
        except User.DoesNotExist:
            return None
        
    def get_user_by_email(self,email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
