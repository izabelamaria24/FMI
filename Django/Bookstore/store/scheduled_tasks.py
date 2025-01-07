import os
import django
import schedule
from datetime import datetime, timedelta
from django.core.mail import send_mail
from store.models import User, CartItem, UserProfile
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bookstore.settings') 
django.setup()

def schedule_monthly_task(task):
    def wrapper():
        if datetime.now().day == 1:
            task()
    return wrapper

def delete_unconfirmed_users():
    K = 2  
    threshold = datetime.now() - timedelta(minutes=K)
    unconfirmed_users = User.objects.filter(profile__email_confirmed=False, date_joined__lt=threshold)
    count = unconfirmed_users.count()
    unconfirmed_users.delete()
    print(f"[{datetime.now()}] Deleted {count} unconfirmed users.")

def send_newsletter():
    X = 1440  
    threshold = datetime.now() - timedelta(minutes=X)
    users = User.objects.filter(date_joined__lt=threshold)
    for user in users:
        send_mail(
            subject="Weekly Newsletter",
            message="This is your weekly newsletter!",
            from_email="newsletter@yourproject.com",
            recipient_list=[user.email],
        )
    print(f"[{datetime.now()}] Sent newsletter to {users.count()} users.")

def send_inactive_user_reminder():
    inactivity_threshold = datetime.now() - timedelta(days=30) 
    inactive_users = User.objects.filter(profile__last_active__lt=inactivity_threshold)
    count = inactive_users.count()
    print(f"[{datetime.now()}] Found {count} inactive users.")

def cleanup_old_cart_items():
    cleanup_threshold = datetime.now() - timedelta(days=30)  
    old_cart_items = CartItem.objects.filter(created_at__lt=cleanup_threshold)
    count = old_cart_items.count()
    old_cart_items.delete()
    print(f"[{datetime.now()}] Deleted {count} old cart items.")

schedule.every(2).minutes.do(delete_unconfirmed_users)
schedule.every().monday.at("09:00").do(send_newsletter)
schedule.every().day.at("00:00").do(schedule_monthly_task(send_inactive_user_reminder))
schedule.every().day.at("02:00").do(cleanup_old_cart_items)

def run_scheduled_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)  
