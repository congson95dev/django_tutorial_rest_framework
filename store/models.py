from django.db import models


# Knowledge:

# relation: one to one, one to many, many to many

# on_delete=models.PROTECT:
#   with this, we will prevent the user to delete the parent item if it have child item inside
#   such as if we have "category" as parent item, and "product" as child item inside
#   if we try to delete the category, the django will show a warning message

# auto_now_add and auto_now:
#   auto_now_add will use timezone.now() when the instance is created only.
#   so it's suitable for created_date fields
#   auto_now will use timezone.now() whenever "save()" method is called
#   so it's suitable for updated_date fields

# handle "circular relationship"

# handle "generic relationship"


MEMBERSHIP_GOLD = 'G'
MEMBERSHIP_SILVER = 'S'
MEMBERSHIP_BRONZE = 'B'

MEMBERSHIP = [
    (MEMBERSHIP_GOLD, 'Gold'),
    (MEMBERSHIP_SILVER, 'Silver'),
    (MEMBERSHIP_BRONZE, 'Bronze')
]

PAYMENT_STATUS_PENDING = 'P'
PAYMENT_STATUS_COMPLETE = 'C'
PAYMENT_STATUS_FAILED = 'F'

PAYMENT_STATUS = [
    (PAYMENT_STATUS_PENDING, 'Pending'),
    (PAYMENT_STATUS_COMPLETE, 'Complete'),
    (PAYMENT_STATUS_FAILED, 'Failed')
]


class Category(models.Model):
    title = models.CharField(max_length=255)

    # Handle "circular relationships"
    # this is some special case called "circular relationships"
    # which is parent depend on child, but also, child is depend on parent at the same time
    # in this case, product is a foreign key of category, but also, category is a foreign key of product
    # to resolve this, we need to add '' to the class name, ex: 'Product'

    # after that, if you got issue "Reverse query name clashes with field name",
    # this is because when we set ForeignKey, it will automatically create a call back variable
    # with name based on our class, in this situation, it's called "category"
    # but "category" variable are already exists in Product class
    # that's why the error appear
    # to resolve this, we need to set related_name to something else
    # or to simple, just use related_name='+',
    # with this, the system won't create call back variable anymore.
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    # slug is the last part of the URL address that serves as a unique identifier of the page.
    # For example, we have a URL that looks like this:
    # example.com/hello-world
    # then "hello-world" is a slug
    # in this slug, it only allow text, number, and "-"
    slug = models.SlugField(default='-')

    # max = 9999.99 => 6 number before . and 2 number after .
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()

    # auto_now_add will use timezone.now() when the instance is created only.
    # so it's suitable for created_date fields
    created_date = models.DateTimeField(auto_now_add=True)
    # auto_now will use timezone.now() whenever "save()" method is called
    # so it's suitable for updated_date fields
    updated_date = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    # with this many to many, it will automatically create a relation field in table "promotion"
    # named "table_name + _set", ex: "product_set"
    # so we can call back in the "promotion" object, such as "promotion.product_set"
    # we can change this default name by insert "related_name" into this many to many field
    # ex: promotion = models.ManyToManyField(Promotion, related_name="products")
    # so now we can call back in the "promotion" object with "promotion.products"
    promotion = models.ManyToManyField(Promotion)


class Customer(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.BigIntegerField()
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP, default=MEMBERSHIP_BRONZE)

    class Meta:
        indexes = [
            models.Index(fields=['firstname', 'lastname'])
        ]


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    # with this, we expect that each customer can have only 1 address, and 1 address can belong to 1 customer only,
    # which is 1 to 1
    # when we set primary_key=True, it won't create field "id" to this table anymore
    # instead, it will treat this field as primary key
    # ex:
    # customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)

    # but in reality, 1 customer can have multiple address, so we will use 1 to many, which is ForeignKey
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # max = 9999.99 => 6 number before . and 2 number after .
    quantity = models.PositiveSmallIntegerField()



