from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


User._meta.get_field('email')._unique = True
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    matches_won = models.PositiveIntegerField(default=0)
    matches_lost = models.PositiveIntegerField(default=0)
    matches_draw = models.PositiveIntegerField(default=0)
    description = models.TextField(max_length=1000, default='')

    def __str__(self):
        return f'Profile: {self.user.username}'