from django.contrib import admin
from .models import Author, Category, Publisher, Book, Inventory, Order, OrderItem
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from .models import UserProfile

admin.site.site_header = "My Bookstore Admin"
admin.site.site_title = "Bookstore Admin Portal"
admin.site.index_title = "Welcome to the Bookstore Management"

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['last_name'] 


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name'] 


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    search_fields = ['name']  


class CategoryFilter(admin.SimpleListFilter):
    title = _('Category')
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        categories = Category.objects.all()
        return [(category.id, category.name) for category in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category_id=self.value())
        return queryset


class PublisherFilter(admin.SimpleListFilter):
    title = _('Publisher')
    parameter_name = 'publisher'

    def lookups(self, request, model_admin):
        publishers = Publisher.objects.all()
        return [(publisher.id, publisher.name) for publisher in publishers]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(publisher_id=self.value())
        return queryset


class PublicationDateFilter(admin.SimpleListFilter):
    title = _('Publication Date')
    parameter_name = 'publication_date'

    def lookups(self, request, model_admin):
        return [
            ('today', _('Today')),
            ('last_7_days', _('Last 7 Days')),
            ('this_month', _('This Month')),
            ('this_year', _('This Year')),
        ]

    def queryset(self, request, queryset):
        today = datetime.today()
        if self.value() == 'today':
            return queryset.filter(publication_date=today.date())
        elif self.value() == 'last_7_days':
            return queryset.filter(publication_date__gte=today - timedelta(days=7))
        elif self.value() == 'this_month':
            return queryset.filter(publication_date__month=today.month, publication_date__year=today.year)
        elif self.value() == 'this_year':
            return queryset.filter(publication_date__year=today.year)
        return queryset


class PriceFilter(admin.SimpleListFilter):
    title = _('Price Range')
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return [
            ('0-20', '0 - 20'),
            ('20-50', '20 - 50'),
            ('50-100', '50 - 100'),
            ('100+', '100+'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '0-20':
            return queryset.filter(price__lte=20)
        elif self.value() == '20-50':
            return queryset.filter(price__gt=20, price__lte=50)
        elif self.value() == '50-100':
            return queryset.filter(price__gt=50, price__lte=100)
        elif self.value() == '100+':
            return queryset.filter(price__gt=100)
        return queryset


class AuthorFilter(admin.SimpleListFilter):
    title = _('Author')
    parameter_name = 'authors'

    def lookups(self, request, model_admin):
        authors = Author.objects.all()
        return [(author.id, author.last_name) for author in authors]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(authors__id=self.value())
        return queryset


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'authors', 'category', 'description', 'image')
        }),
        ('Publishing Details', {
            'fields': ('publisher', 'publication_date', 'price', 'isbn'),
            'classes': ('collapse',), 
        }),
    )
    
    search_fields = ['title']  
    list_filter = list_filter = [
        AuthorFilter,
        CategoryFilter,
        PublisherFilter,
        PublicationDateFilter,
        PriceFilter,
    ]
    
    list_per_page = 10

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    search_fields = ['book']


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'date_of_birth', 'address', 'loyalty', 'email_confirmed', 'blocked')
    list_filter = ('blocked',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    actions = ['block_user', 'unblock_user']

    def block_user(self, request, queryset):
        queryset.update(blocked=True)
        self.message_user(request, "Selected users have been blocked.")
    
    def unblock_user(self, request, queryset):
        queryset.update(blocked=False)
        self.message_user(request, "Selected users have been unblocked.")

admin.site.register(UserProfile, UserProfileAdmin)


# Inline model for OrderItem
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Number of empty forms to display by default

# Custom admin for Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price')  # Fields to display in the list view
    search_fields = ('user__username',)  # Allow search by username of the user
    list_filter = ('created_at',)  # Filter by creation date
    inlines = [OrderItemInline]  # Show OrderItem inline within the Order admin page

# Register OrderItem model separately
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'inventory', 'quantity', 'price')  # Fields to display in the list view
    search_fields = ('order__id', 'inventory__book__title')  # Allow search by order id and book title