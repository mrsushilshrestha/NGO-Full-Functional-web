import uuid
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from .models import ContactInfo, ChatMessage, ChatSettings, QuickResponse
from .forms import ContactForm


def contact(request):
    info = ContactInfo.objects.first()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form, 'info': info})


def contact_chat(request):
    """Chat with us page - same chat UI as widget, full page."""
    info = ContactInfo.objects.first()
    return render(request, 'contact/contact_chat.html', {'info': info})


# Live Chat API for frontend
@csrf_exempt
@require_POST
def chat_send(request):
    """User sends a chat message"""
    session_id = request.session.get('chat_session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session['chat_session_id'] = session_id
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    message = request.POST.get('message', '').strip()
    if not message:
        return JsonResponse({'error': 'Message required'}, status=400)
    ChatMessage.objects.create(
        session_id=session_id,
        sender_type='user',
        sender_name=name or 'Anonymous',
        sender_email=email,
        message=message
    )
    # Old behavior: simple auto-response whenever enabled
    settings = ChatSettings.get()
    if settings.is_enabled and settings.auto_response_enabled:
        ChatMessage.objects.create(
            session_id=session_id,
            sender_type='admin',
            sender_name='System',
            message=getattr(settings, 'auto_response_message', 'Thank you for contacting us. Our team will respond shortly.')
        )
    return JsonResponse({'ok': True, 'session_id': session_id})


@require_GET
def chat_get(request):
    """Get chat messages for current session"""
    session_id = request.session.get('chat_session_id')
    if not session_id:
        return JsonResponse({'messages': []})
    messages_list = ChatMessage.objects.filter(session_id=session_id).order_by('created_at')
    data = [{'id': m.id, 'sender': m.sender_type, 'name': m.sender_name, 'message': m.message, 'time': m.created_at.isoformat()} for m in messages_list]
    return JsonResponse({'messages': data})


def members_page(request):
    """Members page - accessible via Terms > Members navigation"""
    from apps.team.models import Member
    members = Member.objects.filter(is_active=True).order_by('order', 'name')
    role_filter = request.GET.get('role', '')
    if role_filter:
        members = members.filter(role__icontains=role_filter)
    return render(request, 'team/members_page.html', {'members': members, 'role_filter': role_filter})


def gallery_page(request):
    """Gallery page - accessible via Programs > Gallery navigation. Images loaded from backend with fast loading (lazy)."""
    from apps.core.models import GalleryImage
    from apps.programs.models import Program
    program_filter = request.GET.get('program', '')
    images = GalleryImage.objects.filter(is_active=True).order_by('order', 'id').only('id', 'image', 'title', 'caption', 'program_id')
    if program_filter:
        images = images.filter(program_id=program_filter)
    programs = Program.objects.all().only('id', 'title')
    return render(request, 'core/gallery.html', {'images': images, 'programs': programs, 'program_filter': program_filter})
