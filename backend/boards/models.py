from django.db import models

from auth_app.models import CustomUser

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, related_name='owned_boards', on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, related_name='boards', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def member_count(self):
        return self.members.count()
    
    @property
    def ticket_count(self):
        return self.tasks.count()
    
    @property
    def tasks_to_do_count(self):
        return self.tasks.filter(status='to-do').count()
    
    @property
    def tasks_high_prio_count(self):
        return self.tasks.filter(priority='high').count()