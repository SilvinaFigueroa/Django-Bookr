from django.contrib import admin
from reviews.models import (Publisher, Contributor, Book, BookContributor, Review)


class BookAdmin(admin.ModelAdmin):
    # To search on ForeignKeyField or ManyToManyField, we just need to specify the field name on
    # the current model and the field on the related model separated by two underscores
    # Another useful options: __exact  - __startswith

    search_fields = ('title', 'isbn', 'publisher__name')

    date_hierarchy = 'publication_date'
    list_display = ('title', 'isbn13')
    list_filter = ('publisher', 'publication_date')

    def isbn13(self, obj):
        """ '9780316769174' => '978-0-31-676917-4' """
        return "{}-{}-{}-{}-{}".format(obj.isbn[0:3], obj.isbn[3:4],
                                       obj.isbn[4:6], obj.isbn[6:12],
                                       obj.isbn[12:13])

def initialled_name(obj):
    return "{},{}".format(Contributor.last_names, obj.first_names[0:1])

class ReviewAdmin(admin.ModelAdmin):
    # exclude = 'date_edited'
    # fields = ('content', 'rating', 'creator', 'book')

    fieldsets = ((None, {'fields': ('creator', 'book')}),
                 ('Review content',
                  {'fields': ('content', 'rating')}))


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('last_names', 'first_names')
    list_filter = ('last_names',)
    search_fields = ('last_names__startswith', 'first_names')


# Register your models here.

admin.site.register(Publisher)
admin.site.register(Contributor,ContributorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookContributor)
admin.site.register(Review, ReviewAdmin)

# subclass ModelAdmin as BookAdmin and specify the custom list_display
