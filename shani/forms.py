from django import forms
from .models import ContactMessage
import re


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = "__all__"

    # Name validation
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters.")
        return name

    # Message validation
    def clean_message(self):
        message = self.cleaned_data.get("message")
        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters.")
        return message

    # Email validation for specific domains
    def clean_email(self):
        email = self.cleaned_data.get("email")
        allowed_domains = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com"]
        domain = email.split("@")[-1]

        if domain not in allowed_domains:
            raise forms.ValidationError(
                f"Please use a valid email from: {', '.join(allowed_domains)}"
            )
        # Optional: Regex check for email format
        regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(regex, email):
            raise forms.ValidationError("Enter a valid email address.")
        return email

    # Phone validation
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        # Remove spaces, hyphens etc.
        phone_digits = re.sub(r"\D", "", phone)

        if not phone_digits.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone_digits) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits.")
        return phone_digits
