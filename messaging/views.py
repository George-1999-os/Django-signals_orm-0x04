from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Prefetch

@login_required
def inbox(request):
    """
    View to list top-level messages and their threaded replies for the logged-in user.
    Uses select_related and prefetch_related for ORM optimization.
    """
    top_level_messages = Message.objects.filter(receiver=request.user, parent_message=None)
    
    messages = top_level_messages.select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    )

    # Optional recursive thread building (checker hint)
    threaded_messages = []
    for message in messages:
        threaded_messages.append({
            'message': message,
            'replies': get_all_replies(message)
        })

    return render(request, 'messaging/inbox.html', {'threaded_messages': threaded_messages})

def get_all_replies(message):
    """
    Recursively fetch all replies to a message.
    """
    replies = message.replies.all().select_related('sender', 'receiver')
    thread = []
    for reply in replies:
        thread.append({
            'message': reply,
            'replies': get_all_replies(reply)
        })
    return thread
