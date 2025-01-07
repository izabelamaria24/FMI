from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch
from datetime import timedelta, datetime
from store.models import User, UserProfile, Cart, CartItem, Inventory, Book, Category
from store.scheduled_tasks import delete_unconfirmed_users, send_inactive_user_reminder, send_newsletter, cleanup_old_cart_items

class ScheduledTaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )

        self.user_profile = UserProfile.objects.create(
            user=self.user,
            email_confirmed=True,
            last_active=timezone.now(),
            phone_number="123456789",
            date_of_birth="1990-01-01",
            address="123 Test St.",
            loyalty=10,
            code="ABC123"
        )

        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(name="Test Category")

        self.book = Book.objects.create(
            title="Test Book",
            isbn="1234567890",
            price=10.99,
            publication_date="2025-01-01",
            category=self.category
        )

        self.inventory_item = Inventory.objects.create(
            book=self.book,  
            stock_qty=10 
        )

        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            inventory=self.inventory_item,
            quantity=1,
            created_at=timezone.now() - timedelta(days=31)  
        )

        self.unconfirmed_user = User.objects.create_user(
            username='unconfirmed_user',
            password='testpassword',
            email='unconfirmed@example.com'
        )
        UserProfile.objects.create(
            user=self.unconfirmed_user,
            email_confirmed=False,
            last_active=timezone.now() - timedelta(days=5),
        )

    @patch('store.scheduled_tasks.datetime')
    @patch('time.sleep') 
    def test_delete_unconfirmed_users(self, mock_sleep, mock_datetime):
        mock_datetime.now.return_value = datetime(2025, 1, 4, 12, 0, 0) 

        user = User.objects.create_user(
            username=f'unconfirmed_user_{datetime.now().timestamp()}',
            email='unconfirmed_user@example.com',
            password='testpassword',
            date_joined=datetime(2024, 12, 1)  
        )
        
        profile = UserProfile.objects.create(
            user=user,
            email_confirmed=False,  
            last_active=datetime(2024, 12, 1)  
        )

        delete_unconfirmed_users()

        self.assertFalse(UserProfile.objects.filter(email_confirmed=False).exists())


    @patch('store.scheduled_tasks.send_mail') 
    @patch('store.scheduled_tasks.datetime')  
    @patch('time.sleep')  
    def test_send_inactive_user_reminder(self, mock_sleep, mock_datetime, mock_send_mail):
        mock_datetime.now.return_value = datetime(2025, 1, 4, 12, 0, 0)  

        user = User.objects.create_user(
            username=f'inactive_user_{datetime.now().timestamp()}', 
            email='inactive_user@example.com',
            password='testpassword',
            date_joined=datetime(2024, 12, 1)
        )
        
        profile = UserProfile.objects.create(
            user=user,
            last_active=datetime(2024, 11, 1),  
            email_confirmed=True 
        )

        send_inactive_user_reminder()

        mock_send_mail.assert_called()


    @patch('store.scheduled_tasks.send_mail')  
    @patch('store.scheduled_tasks.datetime')
    @patch('time.sleep') 
    def test_send_newsletter(self, mock_sleep, mock_datetime, mock_send_mail):
        mock_datetime.now.return_value = datetime(2025, 1, 4, 12, 0, 0)  

        user = User.objects.create_user(
            username='newsletter_user',
            email='newsletter_user@example.com',
            password='testpassword',
            date_joined=datetime(2024, 12, 1) 
        )

        send_newsletter()

        mock_send_mail.assert_called()


    @patch('store.scheduled_tasks.datetime')  
    @patch('time.sleep') 
    def test_cleanup_old_cart_items(self, mock_sleep, mock_datetime):
        mock_datetime.now.return_value = datetime(2025, 1, 4, 12, 0, 0) 

        self.cart_item.created_at = datetime(2024, 12, 1)
        self.cart_item.save()

        cleanup_old_cart_items()

        self.assertFalse(CartItem.objects.exists())
