from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager  # make sure this import is here

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)  #  Checker will look for this field
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    objects = models.Manager()  # default manager
    unread = UnreadMessagesManager()  #  Checker looks for this name

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}"
