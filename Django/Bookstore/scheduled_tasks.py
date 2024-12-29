import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bookstore.settings') 
django.setup()

from store.models import User  
import schedule
import time
from datetime import datetime, timedelta
from django.core.mail import send_mail

def delete_unconfirmed_users():
    K = 2 
    threshold = datetime.now() - timedelta(minutes=K)
    unconfirmed_users = User.objects.filter(email_confirmed=False, date_joined__lt=threshold)
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

def custom_task_every_m_minutes():
    print(f"[{datetime.now()}] Custom task executed every M minutes.")

def custom_daily_task():
    print(f"[{datetime.now()}] Custom daily task executed.")

schedule.every(2).minutes.do(delete_unconfirmed_users)
schedule.every().monday.at("09:00").do(send_newsletter)
schedule.every(10).minutes.do(custom_task_every_m_minutes)
schedule.every().tuesday.at("15:00").do(custom_daily_task)

print("Scheduler started...")
while True:
    schedule.run_pending()
    time.sleep(1)
