from decimal import Decimal

from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES, SnippetCategory
from django.contrib.auth.models import User

# # long way to do serializer by using serializers.Serializer
# class SnippetCategorySerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, max_length=255)
#
#
# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#     owner = serializers.ReadOnlyField(source='owner.username')
#
#     # get name of category related to this snippet
#
#     # when we call to StringRelatedField() of a relationship table like this,
#     # it will trigger __str__() of that table "category" in file models.py
#     # and in the __str__() function, it called to self.title, which is category.title
#     # and it gonna call a tons of query if we don't set select_related()
#     # so to avoid this, we need to set select_related('category') in queryset inside file views.py
#     category = serializers.StringRelatedField()
#
#     # get category data as a nested dictionary inside the main response
#     # Ex:
#     # {
#     #     "id": 1,
#     #     "title": "",
#     #     ...
#     #     "category": {
#     #         "id": 1,
#     #         "title": "cat 1"
#     #     },
#     #     ...
#     # }
#     category = SnippetCategorySerializer()
#
#     # original field
#     decimal_field = serializers.DecimalField(max_digits=6, decimal_places=2, required=False)
#     # renamed field
#     # to rename a field, we need to set "source" for it, such as "source='decimal_field'",
#     # or else, it will not appear or it will throw an error
#     renamed_decimal_field = serializers.DecimalField(max_digits=6, decimal_places=2,
#                                                      required=False, source='decimal_field')
#     # custom field by using function
#     # we need to define a function and transfer it to "method_name"
#     custom_decimal_field = serializers.SerializerMethodField(method_name='calculate_custom_decimal_field')
#
#     # function used to set data for "custom_decimal_field"
#     def calculate_custom_decimal_field(self, snippet: Snippet):
#         return snippet.decimal_field * Decimal(2.0)
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.decimal_field = validated_data.get('decimal_field', instance.decimal_field)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         # instance.owner = validated_data.get('owner', instance.owner)
#         instance.save()
#         return instance


# fast way to do serializer by using serializers.ModelSerializer
class SnippetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SnippetCategory
        fields = ['id', 'title']


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'decimal_field', 'renamed_decimal_field', 'custom_decimal_field',
                  'linenos', 'language', 'style', 'owner', 'category']

    # we can do the same as what we do with the field in the previous section, which is serializers.Serializer
    # such as category, renamed_decimal_field, custom_decimal_field
    category = SnippetCategorySerializer(required=False)
    renamed_decimal_field = serializers.DecimalField(max_digits=6, decimal_places=2,
                                                         required=False, source='decimal_field')
    custom_decimal_field = serializers.SerializerMethodField(method_name='calculate_custom_decimal_field')

    # function used to set data for "custom_decimal_field"
    def calculate_custom_decimal_field(self, snippet: Snippet):
        return Decimal(snippet.decimal_field) * Decimal(2.0)

    # Example of custom validator
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('password do not match')
    #     return data

    # Example of custom create method
    def create(self, validated_data):
        snippets = Snippet(**validated_data)
        snippets.title = 'new title'
        snippets.save()
        return snippets

    # Example of custom update method
    def update(self, instance, validated_data):
        instance.title = 'updated title'
        instance.save()
        return instance


# serializers for Users
class UserSerializer(serializers.ModelSerializer):
    # Because 'snippets' is a reverse relationship on the User model,
    # it will not be included by default when using the ModelSerializer class,
    # so we needed to add an explicit field for it.
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']
