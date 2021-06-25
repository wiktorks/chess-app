from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    name = models.CharField(max_length=150, unique=True, null=True)
    matches_won = models.PositiveIntegerField(default=0)
    matches_lost = models.PositiveIntegerField(default=0)


