from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect
from .forms import ContactMessageForm
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.db import transaction


def home(request):
    if request.method == "POST":
        contact_form = ContactMessageForm(request.POST)

        if contact_form.is_valid():
            data = contact_form.cleaned_data

            from django.utils import timezone
            from datetime import timedelta
            from .models import ContactMessage

            recent = ContactMessage.objects.filter(
                email=data["email"],
                created_at__gte=timezone.now() - timedelta(seconds=10),
            ).exists()

            if recent:
                return JsonResponse(
                    {"success": False, "errors": ["Please wait before sending again."]},
                    status=400,
                )

            try:
                with transaction.atomic():
                    contact_form.save()

                # ===== EMAIL TO YOU =====
                email_to_me = EmailMessage(
                    subject=f"New Contact Message – {data['name']}",
                    body=f"Name: {data['name']}\nEmail: {data['email']}\n\nMessage:\n{data['message']}",
                    from_email=settings.EMAIL_HOST_USER,
                    to=[settings.EMAIL_HOST_USER],
                    reply_to=[data["email"]],  # ab EmailMessage me safe hai
                )

                email_to_me.send(fail_silently=False)

                # ===== AUTO REPLY TO USER =====

                auto_reply = EmailMessage(
                    subject="Thank you for contacting Er. Shani",
                    body=f"""
                    Hi {data['name']},
                    Thank you for contacting me through my portfolio website.
                    
                    I have received your message and will respond within 24 hours.

                    Best Regards,
                    Er. Shani
                    Portfolio Website
                    """,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[data["email"]],
                )
                
                auto_reply.send(fail_silently=False)
            except Exception as e:
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse(
                        {
                            "success": False,
                            "errors": ["Something went wrong. Please try again later."],
                        },
                        status=500,
                    )
                return redirect("home")

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": True}, status=200)
            return redirect("home")
        else:
            errors = [
                str(err) for field in contact_form.errors.values() for err in field
            ]
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "errors": errors}, status=400)
    else:
        contact_form = ContactMessageForm()

    return render(request, "shani/index.html", {"contact_form": contact_form})
