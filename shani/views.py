# from django.shortcuts import render

# # Create your views here.


# from django.shortcuts import render, redirect
# from .forms import ContactMessageForm
# from django.http import JsonResponse
# from django.conf import settings
# from django.core.mail import send_mail, EmailMessage
# from django.db import transaction


# def home(request):
#     if request.method == "POST":
#         contact_form = ContactMessageForm(request.POST)

#         if contact_form.is_valid():
#             data = contact_form.cleaned_data

#             from django.utils import timezone
#             from datetime import timedelta
#             from .models import ContactMessage

#             recent = ContactMessage.objects.filter(
#                 email=data["email"],
#                 created_at__gte=timezone.now() - timedelta(seconds=10),
#             ).exists()

#             if recent:
#                 return JsonResponse(
#                     {"success": False, "errors": ["Please wait before sending again."]},
#                     status=400,
#                 )

#             try:
#                 with transaction.atomic():
#                     contact_form.save()

#                 # ===== EMAIL TO YOU =====
#                 # email_to_me = EmailMessage(
#                 #     subject=f"New Contact Message – {data['name']}",
#                 #     body=f"Name: {data['name']}\nEmail: {data['email']}\n\nMessage:\n{data['message']}",
#                 #     from_email=settings.EMAIL_HOST_USER,
#                 #     to=[settings.EMAIL_HOST_USER],
#                 #     reply_to=[data["email"]],  # ab EmailMessage me safe hai
#                 # )

#                 # # email_to_me.send(fail_silently=True)
#                 # try:
#                 #     email_to_me.send(fail_silently=False)
#                 # except:
#                 #     pass
                
                
                
#                 email_to_me = EmailMessage(
#                     subject=f"New Contact Message – {data['name']}",
#                     body=f"""
#                 New Contact Message Received

#                 Name: {data['name']}
#                 Email: {data['email']}

#                 Message:
#                 {data['message']}
#                 """,
#                     from_email=settings.DEFAULT_FROM_EMAIL,
#                     to=[settings.DEFAULT_FROM_EMAIL],
#                     reply_to=[data["email"]],
#                 )

#                 try:
#                     email_to_me.send()
#                 except Exception as e:
#                     print("Admin email failed:", e)
                
                
                
                

#                 # ===== AUTO REPLY TO USER =====

#                 # auto_reply = EmailMessage(
#                 #     subject="Thank you for contacting Er. Shani",
#                 #     body=f"""
#                 #     Hi {data['name']},
#                 #     Thank you for contacting me through my portfolio website.
                    
#                 #     I have received your message and will respond within 24 hours.

#                 #     Best Regards,
#                 #     Er. Shani
#                 #     Portfolio Website
#                 #     """,
#                 #     # from_email=settings.EMAIL_HOST_USER,
#                 #     from_email=settings.DEFAULT_FROM_EMAIL,
#                 #     to=[data["email"]],
#                 # )
#                 # try:
#                 #     auto_reply.send(fail_silently=False)
#                 # except:
#                 #     pass
#                 # auto_reply.send(fail_silently=True)
                
                
#                 auto_reply = EmailMessage(
#                     subject="Thank you for contacting Er. Shani",
#                     body=f"""
#                 Hi {data['name']},

#                 Thank you for contacting me.

#                 Here is a copy of your message:

#                 ---------------------------------
#                 {data['message']}
#                 ---------------------------------

#                 I will respond within 24 hours.

#                 Best Regards,
#                 Er. Shani
#                 Portfolio Website
#                 """,
#                     from_email=settings.DEFAULT_FROM_EMAIL,
#                     to=[data["email"]],
#                 )

#                 try:
#                     auto_reply.send(fail_silently=False)
#                 except Exception as e:
#                     print("Auto reply failed:", e)
                
                
#             except Exception as e:
#                 if request.headers.get("x-requested-with") == "XMLHttpRequest":
#                     print("EMAIL ERROR:", str(e)) 
#                     return JsonResponse(
#                         {
#                             "success": False,
#                            "errors": [str(e)],
#                         },
#                         status=500,
#                     )
#                 return redirect("home")

#             if request.headers.get("x-requested-with") == "XMLHttpRequest":
#                 return JsonResponse({"success": True}, status=200)
#             return redirect("home")
#         else:
#             errors = [
#                 str(err) for field in contact_form.errors.values() for err in field
#             ]
#             if request.headers.get("x-requested-with") == "XMLHttpRequest":
#                 return JsonResponse({"success": False, "errors": errors}, status=400)
#     else:
#         contact_form = ContactMessageForm()

#     return render(request, "shani/index.html", {"contact_form": contact_form})











from django.shortcuts import render, redirect
from .forms import ContactMessageForm
from django.http import JsonResponse
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import ContactMessage
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def home(request):
    if request.method == "POST":
        contact_form = ContactMessageForm(request.POST)

        if contact_form.is_valid():
            data = contact_form.cleaned_data

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

                sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))

                # ===== EMAIL TO YOU =====
                admin_message = Mail(
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to_emails=settings.DEFAULT_FROM_EMAIL,
                    subject=f"New Contact Message – {data['name']}",
                    html_content=f"""
                        <strong>New Contact Message Received</strong><br><br>
                        Name: {data['name']}<br>
                        Email: {data['email']}<br><br>
                        Message:<br>
                        {data['message']}
                    """,
                )

                try:
                    sg.send(admin_message)
                except Exception as e:
                    print("Admin email failed:", e)

                # ===== AUTO REPLY TO USER =====
                auto_reply = Mail(
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to_emails=data["email"],
                    subject="Thank you for contacting Er. Shani",
                    html_content=f"""
                        Hi {data['name']},<br><br>

                        Thank you for contacting me.<br><br>

                        Here is a copy of your message:<br><br>

                        ---------------------------------<br>
                        {data['message']}<br>
                        ---------------------------------<br><br>

                        I will respond within 24 hours.<br><br>

                        Best Regards,<br>
                        Er. Shani<br>
                        Portfolio Website
                    """,
                )

                try:
                    sg.send(auto_reply)
                except Exception as e:
                    print("Auto reply failed:", e)

            except Exception as e:
                print("EMAIL ERROR:", str(e))
                return JsonResponse(
                    {"success": False, "errors": [str(e)]},
                    status=500,
                )

            return JsonResponse({"success": True}, status=200)

        else:
            errors = [
                str(err) for field in contact_form.errors.values() for err in field
            ]
            return JsonResponse({"success": False, "errors": errors}, status=400)

    else:
        contact_form = ContactMessageForm()

    return render(request, "shani/index.html", {"contact_form": contact_form})