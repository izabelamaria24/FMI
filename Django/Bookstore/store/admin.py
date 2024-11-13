from django.contrib import admin
from .models import Author, Category, Publisher, Book, Inventory
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta

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
            'fields': ('title', 'authors', 'category', 'description')
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

