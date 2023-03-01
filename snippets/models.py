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
    decimal_field = models.DecimalField(max_digits=6, decimal_places=2, default=1.0)
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
