# messaging/views.py
from django.shortcuts import render
from .models import Message
from django.contrib.auth.decorators import login_required

@login_required
def inbox(request):
    """
    View to list top-level messages and their threaded replies for the logged-in user.
    Optimized with select_related and prefetch_related.
    """
    # Only fetch top-level messages (not replies)
    messages = Message.objects.filter(receiver=request.user, parent_message=None)\
        .select_related('sender', 'receiver')\
        .prefetch_related('replies')

    return render(request, 'messaging/inbox.html', {'messages': messages})
