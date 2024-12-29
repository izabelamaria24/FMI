from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Book, Author, Category, Publisher, Promotie

class BookSitemap(Sitemap):
    def items(self):
        return Book.objects.all()

    def location(self, obj):
        return reverse('book_detail', args=[obj.id])

class AuthorSitemap(Sitemap):
    def items(self):
        return Author.objects.all()

    def location(self, obj):
        return reverse('author_detail', args=[obj.id])

class CategorySitemap(Sitemap):
    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('category_detail', args=[obj.id])

class PublisherSitemap(Sitemap):
    def items(self):
        return Publisher.objects.all()

    def location(self, obj):
        return reverse('publisher_detail', args=[obj.id])

class PromotieSitemap(Sitemap):
    def items(self):
        return Promotie.objects.all()

    def location(self, obj):
        return reverse('promotie_detail', args=[obj.id])


class StaticViewSitemap(Sitemap):
    # def items(self):
    #     return ['home']  

    def location(self, item):
        return reverse(item)
