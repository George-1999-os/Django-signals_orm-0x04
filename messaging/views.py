from django.shortcuts import render
from .models import Message


def get_threaded_replies(message):
    """Recursively fetch replies to a message."""
    thread = []
    for reply in message.replies.all().select_related('sender'):
        thread.append({
            'message': reply,
            'replies': get_threaded_replies(reply)
        })
    return thread


def inbox_view(request):
    """Inbox with threaded messages."""
    top_messages = Message.objects.filter(
        receiver=request.user,
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related('replies')

    threads = []
    for msg in top_messages:
        threads.append({
            'message': msg,
            'replies': get_threaded_replies(msg)
        })

    return render(request, 'messaging/inbox.html', {'threads': threads})
