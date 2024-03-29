from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from auth_custom.models import MEMBERSHIP, MEMBERSHIP_BRONZE

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

PAYMENT_STATUS_PENDING = 'P'
PAYMENT_STATUS_COMPLETE = 'C'
PAYMENT_STATUS_FAILED = 'F'

PAYMENT_STATUS = [
    (PAYMENT_STATUS_PENDING, 'Pending'),
    (PAYMENT_STATUS_COMPLETE, 'Complete'),
    (PAYMENT_STATUS_FAILED, 'Failed')
]


class SnippetCategory(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, default=1.0)
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    # set current user as "owner"
    # this field is like "created_by" in other project

    # because we custom the user model in auth_custom module
    # so we need to call get_user_model() to get the new user model
    owner = models.ForeignKey(get_user_model(), related_name='snippets', on_delete=models.CASCADE, null=True)
    # normally, we just need to call 'auth.User' as below
    # owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE, null=True)

    category = models.ForeignKey(SnippetCategory, related_name='snippets', on_delete=models.CASCADE,
                                 null=True, blank=True)

    class Meta:
        ordering = ['created']


class SnippetImage(models.Model):
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE, related_name='images')
    # to use this ImageField(), we need to run "pip install pillow"
    image = models.ImageField(upload_to='snippet/images')


class SnippetTag(models.Model):
    title = models.CharField(max_length=255)
    snippet = models.ForeignKey(Snippet, related_name='snippet_tags', on_delete=models.CASCADE)


class Cart(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE)

    # max = 9999.99 => 6 number before . and 2 number after .
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    # set unique for a collection of cart and snippet
    # which mean if we already have cart = 1, snippet = 1 in db
    # and we add snippet = 1 to cart = 1, it won't create another record in table snippets_cartitem
    # it will make quantity = quantity + 1
    # THIS DOESN'T WORK YET
    # class Meta:
    #     unique_together = [['cart'], ['snippet']]


class Customer(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP, default=MEMBERSHIP_BRONZE)


class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    snippet = models.ForeignKey(Snippet, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
