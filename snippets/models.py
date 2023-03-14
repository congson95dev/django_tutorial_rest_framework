from django.core.validators import MinValueValidator
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


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
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(SnippetCategory, related_name='snippets', on_delete=models.CASCADE,
                                 null=True, blank=True)

    class Meta:
        ordering = ['created']


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
