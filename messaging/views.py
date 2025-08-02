from django.shortcuts import render
from .models import Message

def get_threaded_messages(message):
    """Recursively get replies to a message."""
    thread = []
    for reply in message.replies.all().select_related('sender', 'receiver'):
        thread.append({
            'message': reply,
            'replies': get_threaded_messages(reply)
        })
    return thread

def inbox_view(request):
    if not request.user.is_authenticated:
        return render(request, 'messaging/inbox.html', {'threads': []})

    top_level_messages = Message.objects.filter(
        sender=request.user,
        receiver=request.user,
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related('replies')

    threaded_conversations = []
    for message in top_level_messages:
        threaded_conversations.append({
            'message': message,
            'replies': get_threaded_messages(message)
        })

    return render(request, 'messaging/inbox.html', {'threads': threaded_conversations})
