from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from facebook import GraphAPI  # type: ignore

from .models import Group
from .models import GroupMessage


@login_required
@require_POST
def create_group(request):
    name = request.POST.get("name")
    group = Group.objects.create(name=name, creator=request.user.user_profile)
    group.members.add(request.user.user_profile)
    return redirect("group_detail", group_id=group.id)


@login_required
def join_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
        group.members.add(request.user.user_profile)
        return redirect("group_detail", group_id=group_id)
    except Group.DoesNotExist:
        return render(request, "group_not_found.html")


@login_required
def leave_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
        group.members.remove(request.user.user_profile)
        return redirect("group_list")
    except Group.DoesNotExist:
        return render(request, "group_not_found.html")


@login_required
def group_detail(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
        members = group.members.all()
        return render(
            request, "group_detail.html",
            {"group": group, "members": members},
        )
    except Group.DoesNotExist:
        return render(request, "group_not_found.html")




def verify_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
        # ... (Implement logic to verify group ID with WhatsApp API)
        # ... (Example using Graph API - adapt based on your specific needs)
        graph = GraphAPI(access_token=settings.PAGE_ACCESS_TOKEN)
        # ... (Make API call to check group existence or retrieve group details)
        # ... (Handle API response and update group.whatsapp_group_id)
        group.save()
        return redirect("group_detail", group_id=group_id)
    except Group.DoesNotExist:
        # ... (Handle group not found)
        return HttpResponse("Invalid group", status=404)

@csrf_exempt
@require_POST
def receive_webhook(request):
    data = request.POST
    # ... (Parse incoming webhook data from WhatsApp)
    sender = data.get("from")  # Extract sender's phone number/ID
    message_body = data.get("text", {}).get("body")
    # ... (Get group ID associated with the webhook)
    try:
        group = Group.objects.get(whatsapp_group_id=sender)
        GroupMessage.objects.create(group=group, sender=sender, message=message_body)
        # ... (Send notifications to group members using your preferred method)
        # ... (Example: using a messaging service like SNS)
        return HttpResponse("OK", status=200)
    except Group.DoesNotExist:
            # ... (Handle invalid group)
        return HttpResponse("Invalid group", status=404)

