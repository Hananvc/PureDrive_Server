# vehicleapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from userapp.models import Dealer
from .models import Vehicle
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import testride


@receiver(post_save, sender=Vehicle)
def send_notification_email(sender, instance, created, **kwargs):
    if created:
        print("Sending notification email for new vehicle...")
        
        brand = instance.brand
        dealers = Dealer.objects.filter(brand=brand)
        for dealer in dealers:
            vehicle_detail_url = f"http://localhost:5173/vehicle/{instance.pk}/"
            subject = 'New Vehicle Added'
            message = f'A new vehicle of your brand has been added to the database. You can view it here: {vehicle_detail_url}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [dealer.user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
            print(f"Email sent to: {dealer.user.email}")

@receiver(post_save, sender=testride)
def send_booking_emails(sender, instance, created, **kwargs):
    if created:
        # Send confirmation email to the user
        user_subject = 'Test Ride Booking Confirmation'
        user_message = render_to_string('email/user_booking_confirmation.html', {'booking': instance})
        user_plain_message = strip_tags(user_message)
        user_from_email = settings.EMAIL_HOST_USER
        user_to_email = instance.customer_email
        send_mail(user_subject, user_plain_message, user_from_email, [user_to_email], html_message=user_message)

        # Send notification email to the dealer
        dealer_subject = 'New Test Ride Booking Notification'
        dealer_message = render_to_string('email/dealer_notification.html', {'booking': instance})
        dealer_plain_message = strip_tags(dealer_message)
        dealer_from_email = settings.EMAIL_HOST_USER
        dealer_to_email = instance.dealer_email
        send_mail(dealer_subject, dealer_plain_message, dealer_from_email, [dealer_to_email], html_message=dealer_message)
        
        print(f"Confirmation email sent to user: {user_to_email}")
        print(f"Notification email sent to dealer: {dealer_to_email}")

