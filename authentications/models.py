from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission,AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

# User Manager


# User Model
class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    def update_profile(self, first_name=None, last_name=None, profile_image=None):
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if profile_image:
            self.profile_image = profile_image
        self.save()
        return self
