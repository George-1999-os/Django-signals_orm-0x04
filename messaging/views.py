# Django-signals_orm-0x04/messaging/views.py

from django.shortcuts import render
from .models import Message
from django.contrib.auth.decorators import login_required

@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user, parent_message__isnull=True) \
        .select_related('sender', 'receiver') \
        .prefetch_related('replies')

    return render(request, 'messaging/inbox.html', {'messages': messages})
