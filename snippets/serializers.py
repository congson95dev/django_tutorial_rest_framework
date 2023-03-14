from decimal import Decimal

from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES, SnippetCategory, SnippetTag, Cart, CartItem
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
#     unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, required=False)
#     # renamed field
#     # to rename a field, we need to set "source" for it, such as "source='unit_price'",
#     # or else, it will not appear or it will throw an error
#     renamed_unit_price = serializers.DecimalField(max_digits=6, decimal_places=2,
#                                                      required=False, source='unit_price')
#     # custom field by using function
#     # we need to define a function and transfer it to "method_name"
#     custom_unit_price = serializers.SerializerMethodField(method_name='calculate_custom_unit_price')
#
#     # function used to set data for "custom_unit_price"
#     def calculate_custom_unit_price(self, snippet: Snippet):
#         return snippet.unit_price * Decimal(2.0)
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
#         instance.unit_price = validated_data.get('unit_price', instance.unit_price)
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
        fields = ['id', 'title', 'code', 'unit_price', 'renamed_unit_price', 'custom_unit_price',
                  'linenos', 'language', 'style', 'owner', 'category', 'tag_count']

    tag_count = serializers.IntegerField(read_only=True)

    # we can do the same as what we do with the field in the previous section, which is serializers.Serializer
    # such as category, renamed_unit_price, custom_unit_price

    # when we call to StringRelatedField() of a relationship table like this,
    # it will trigger __str__() of that table "category" in file models.py
    # and in the __str__() function, it called to self.title, which is category.title
    # and it gonna call a tons of query if we don't set select_related()
    # so to avoid this, we need to set select_related('category') in queryset inside file views.py
    category = serializers.StringRelatedField()

    # get category data as a nested dictionary inside the main response
    # Ex:
    # {
    #     "id": 1,
    #     "title": "",
    #     ...
    #     "category": {
    #         "id": 1,
    #         "title": "cat 1"
    #     },
    #     ...
    # }
    category = SnippetCategorySerializer(required=False)

    # renamed field
    # to rename a field, we need to set "source" for it, such as "source='unit_price'",
    # or else, it will not appear or it will throw an error
    renamed_unit_price = serializers.DecimalField(max_digits=6, decimal_places=2,
                                                         required=False, source='unit_price')

    # custom field by using function
    # we need to define a function and transfer it to "method_name"
    custom_unit_price = serializers.SerializerMethodField(method_name='calculate_custom_unit_price')

    # function used to set data for "custom_unit_price"
    def calculate_custom_unit_price(self, snippet: Snippet):
        return Decimal(snippet.unit_price) * Decimal(2.0)

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


# serializers for SnippetTag
class SnippetTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = SnippetTag
        fields = ['id', 'title', 'snippet']

    # set to read_only mode
    snippet = serializers.PrimaryKeyRelatedField(read_only=True)

    # set snippet_id to table snippet_tags when create new record
    # Ex we have this url: /snippets/2/snippet_tags/
    # this url is following by format: /snippets/<snippet_pk>/snippet_tags/
    # we will get the "snippet_pk" params by url and save it to db

    # for the get "snippet_pk" params by url and transfer it to context, we've already done it in snippets/views.py
    # in function get_serializer_context()
    def create(self, validated_data):
        # get data from context
        snippet_id = self.context['snippet_id']
        # save to db
        return SnippetTag.objects.create(snippet_id=snippet_id, **validated_data)


class CartItemSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    # IMPORTANT: need to set this before call it in the "fields"
    snippet = CartItemSnippetSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'snippet', 'quantity', 'total_price']

    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')

    # calculate total_price
    def calculate_total_price(self, item: CartItem):
        return item.snippet.unit_price * item.quantity


# serializers for Cart
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'items', 'created_date', 'total_price']

    # set to read_only mode
    created_date = serializers.DateTimeField(read_only=True)

    # set many=True to get multiple items
    # because 1 cart have multiple cart items
    items = CartItemSerializer(many=True, read_only=True)

    # render total_price get from views.py
    # total_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')

    def calculate_total_price(self, cart: Cart):
        return sum([item.quantity * item.snippet.unit_price for item in cart.items.all()])


# serializers for CartItem
class CartItemCRDSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'snippet', 'quantity']

    # set to read_only mode
    cart = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        # get data from context
        snippet_id = self.validated_data['snippet']
        quantity = self.validated_data['quantity']
        cart_id = self.context['cart_id']

        # save to db
        try:
            # if already exists in db, update cart_item.quanity += quantity
            cart_item = CartItem.objects.get(cart_id=cart_id, snippet_id=snippet_id)
            cart_item.quantity += quantity
            cart_item.save()
            instance = cart_item
        except CartItem.DoesNotExist:
            # if not exists, create new
            instance = CartItem.objects.create(cart_id=cart_id, **validated_data)

        return instance


class UpdateCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'snippet', 'quantity']

    # set to read_only mode
    id = serializers.IntegerField(read_only=True)
    cart = serializers.PrimaryKeyRelatedField(read_only=True)
    snippet = serializers.PrimaryKeyRelatedField(read_only=True)
