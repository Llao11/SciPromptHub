from django.db import models

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Prompt(models.Model):
    name = models.TextField(max_length=50, verbose_name="Name", default="Untitled")
    text = models.TextField(verbose_name="Prompt text")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="prompts")

    def __str__(self):
        return self.name[:50]
