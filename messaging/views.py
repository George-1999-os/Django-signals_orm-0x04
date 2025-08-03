from django.shortcuts import render
from .models import Message


def inbox_view(request):
    user = request.user  # current logged-in user

    #  Use custom manager to get unread messages
    unread_messages = Message.unread.unread_for_user(user)

    #  Use default manager to get optimized unread messages with only necessary fields
    optimized_messages = Message.objects.filter(
        receiver=user, read=False
    ).only('id', 'sender', 'content', 'timestamp').select_related('sender')

    return render(request, 'messaging/inbox.html', {
        'unread_messages': unread_messages,
        'optimized_messages': optimized_messages
    })
