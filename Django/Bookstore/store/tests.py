from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch
from datetime import timedelta, datetime
from store.models import User, UserProfile, Cart, CartItem, Inventory, Book, Category
from store.scheduled_tasks import delete_unconfirmed_users, send_inactive_user_reminder, send_newsletter, cleanup_old_cart_items

class ScheduledTaskTests(TestCase):
    def setUp(self):
        # Create the User
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )

        # Create the UserProfile associated with the User
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

        # Create a Cart for the user
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(name="Test Category")

        # Create a Book instance (needed for the Inventory item)
        self.book = Book.objects.create(
            title="Test Book",
            isbn="1234567890",
            price=10.99,
            publication_date="2025-01-01",
            category=self.category
        )

        # Create an Inventory item for the CartItem
        self.inventory_item = Inventory.objects.create(
            book=self.book,  # Use the 'book' field, not 'book_title'
            stock_qty=10  # Use 'stock_qty' instead of 'stock_quantity'
        )

        # Create a CartItem linked to the Cart and Inventory
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            inventory=self.inventory_item,
            quantity=1,
            created_at=timezone.now() - timedelta(days=31)  # Ensure it's older than the threshold
        )

        # Create another user with unconfirmed email for delete_unconfirmed_users test
        self.unconfirmed_user = User.objects.create_user(
            username='unconfirmed_user',
            password='testpassword',
            email='unconfirmed@example.com'
        )
        UserProfile.objects.create(
            user=self.unconfirmed_user,
            email_confirmed=False,
            last_active=timezone.now() - timedelta(days=5),  # Ensure they meet the threshold for deletion
        )

    @patch('store.scheduled_tasks.datetime')  # Mock datetime
    @patch('time.sleep')  # Mock time.sleep
    def test_delete_unconfirmed_users(self, mock_sleep, mock_datetime):
        # Mock datetime to simulate the cleanup of old unconfirmed users
        mock_datetime.now.return_value = datetime(2025, 1, 4, 12, 0, 0)  # Set a fixed datetime

        # Create unconfirmed user with a unique username to avoid duplication
        user = User.objects.create_user(
            username=f'unconfirmed_user_{datetime.now().timestamp()}',  # Ensure unique username
            email='unconfirmed_user@example.com',
            password='testpassword',
            date_joined=datetime(2024, 12, 1)  # Ensure the user is old enough to be deleted
        )
        
        # Create the corresponding UserProfile for the user
        profile = UserProfile.objects.create(
            user=user,
            email_confirmed=False,  # Set the email confirmation to False
            last_active=datetime(2024, 12, 1)  # Set the last_active date appropriately
        )

        # Run the task to delete unconfirmed users
        delete_unconfirmed_users()

        # Check that no unconfirmed users remain
        self.assertFalse(UserProfile.objects.filter(email_confirmed=False).exists())


    @patch('store.scheduled_tasks.send_mail')  # Mock send_mail
    @patch('store.scheduled_tasks.datetime')  # Mock datetime
    @patch('time.sleep')  # Mock time.sleep
    def test_send_inactive_user_reminder(self, mock_sleep, mock_datetime, mock_send_mail):
        # Mock datetime to simulate sending the reminder for inactive users
        mock_datetime.now.return_value = datetime(2025, 1, 4, 12, 0, 0)  # Set a fixed datetime

        user = User.objects.create_user(
            username=f'inactive_user_{datetime.now().timestamp()}',  # Ensure unique username
            email='inactive_user@example.com',
            password='testpassword',
            date_joined=datetime(2024, 12, 1)
        )
        
        # Create the corresponding UserProfile instance
        profile = UserProfile.objects.create(
            user=user,
            last_active=datetime(2024, 11, 1),  # Ensure the user is inactive
            email_confirmed=True  # Ensure the user is confirmed
        )

        # Run the task to send reminders to inactive users
        send_inactive_user_reminder()

        # Check if send_mail was called (meaning the reminder was sent)
        mock_send_mail.assert_called()



    @patch('store.scheduled_tasks.send_mail')  # Mock send_mail
    @patch('store.scheduled_tasks.datetime')  # Mock datetime
    @patch('time.sleep')  # Mock time.sleep
    def test_send_newsletter(self, mock_sleep, mock_datetime, mock_send_mail):
        # Mock datetime to simulate sending the newsletter
        mock_datetime.now.return_value = datetime(2025, 1, 4, 12, 0, 0)  # Set a fixed datetime

        # Create a user that qualifies for the newsletter
        user = User.objects.create_user(
            username='newsletter_user',
            email='newsletter_user@example.com',
            password='testpassword',
            date_joined=datetime(2024, 12, 1)  # Ensure the user is eligible for the newsletter
        )

        send_newsletter()

        # Check if send_mail was called (meaning the newsletter was sent)
        mock_send_mail.assert_called()


    @patch('store.scheduled_tasks.datetime')  # Mock datetime
    @patch('time.sleep')  # Mock time.sleep
    def test_cleanup_old_cart_items(self, mock_sleep, mock_datetime):
        # Mock datetime to simulate the cleanup of old cart items
        mock_datetime.now.return_value = datetime(2025, 1, 4, 12, 0, 0)  # Set a fixed datetime

        # Ensure the CartItem is older than the threshold
        self.cart_item.created_at = datetime(2024, 12, 1)
        self.cart_item.save()

        cleanup_old_cart_items()

        # Assert that the cart item older than 30 days was deleted
        self.assertFalse(CartItem.objects.exists())

