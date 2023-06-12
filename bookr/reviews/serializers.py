from rest_framework import serializers
from .models import Book, Publisher, Contributor, BookContributor


# class PublisherSerializer(serializers.Serializer):
#
#     name = serializers.CharField()
#     website = serializers.URLField()
#     email = serializers.EmailField()
#
# class BookSerializer(serializers.Serializer):
#     title = serializers.CharField()
#     publication_date = serializers.DateField()
#     isbn = serializers.CharField()
#     # we need to use PublisherSerializer because is publisher is a PK of Book model
#     publisher = PublisherSerializer()
# __________________________________________________________________________________________________

# class-based views using the Model
# We do not need to specify how each field gets serialized, instead, we can simply pass a list of field names,
# and the field types are inferred from the definition in models.py.
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name', 'website', 'email']


class BookSerializer(serializers.ModelSerializer):
    # we need to use PublisherSerializer because is publisher is a FK of Book model
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = ['title', 'publication_date', 'isbn', 'publisher']


class ContributionSerializer(serializers.ModelSerializer):
    # we need to use BookSerializer because FK of BookContributor model
    book = BookSerializer()

    class Meta:
        model = BookContributor
        fields = ['book', 'role']


class ContributorSerializer(serializers.ModelSerializer):
    # add number of bookcontributor_set function set on Contributor
    bookcontributor_set = ContributionSerializer(many=True)
    # number of contributions won't be updated, only read
    number_contributions = serializers.ReadOnlyField()

    class Meta:
        model = Contributor
        # fields requested to pass on the API
        fields = ['first_names', 'last_names', 'email', 'bookcontributor_set', 'number_contributions']
