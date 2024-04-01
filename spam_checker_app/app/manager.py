from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, phone_no, name,  password,email=None, **extra_fields):
        if not phone_no :
            raise ValueError('Phone number must be set')
        if not name:
            raise ValueError('Name must be set')

        if email is not None:
            email = self.normalize_email(email) 
        else:
            email = None

        user =  self.model(
            phone_no = phone_no,
            name = name,
            email = email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, phone_no, name, password, email=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_no,name, password,email, **extra_fields)



    def create_superuser(self, phone_no, name, password, email=None,**extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        email=None
        return self._create_user(phone_no,name, password, email, **extra_fields)
