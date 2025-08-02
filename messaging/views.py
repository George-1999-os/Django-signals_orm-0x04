from django.shortcuts import render
from .models import Message

def get_threaded_messages(message):
    """Recursively get replies to a message."""
    thread = []
    for reply in message.replies.all().select_related('sender'):
        thread.append({
            'message': reply,
            'replies': get_threaded_messages(reply)
        })
    return thread

def inbox_view(request):
    top_messages = Message.objects.filter(receiver=request.user, parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related('replies')

    threaded_conversations = []
    for msg in top_messages:
        threaded_conversations.append({
            'message': msg,
            'replies': get_threaded_messages(msg)
        })

    return render(request, 'messaging/inbox.html', {
        'threads': threaded_conversations
    })
