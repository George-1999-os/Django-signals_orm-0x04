# messaging/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Prefetch

@login_required
def inbox_view(request):
    # Fetch top-level messages (not replies)
    messages = (
        Message.objects
        .filter(receiver=request.user, parent_message=None)
        .select_related("sender", "receiver")
        .prefetch_related(
            Prefetch(
                "replies",
                queryset=Message.objects.select_related("sender", "receiver")
            )
        )
        .order_by('-timestamp')
    )
    return render(request, "messaging/inbox.html", {"messages": messages})
