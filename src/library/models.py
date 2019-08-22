from django.db import models
from django.contrib.auth.models import User 


class Book(models.Model):

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, help_text="Enter a brief description of a book")
    borrowed = models.ForeignKey(User, related_name='books', on_delete=models.CASCADE)
    pub_date = models.DateField(auto_now=False, auto_now_add=False)  
    age_limit = models.PositiveIntegerField(help_text="Enter a age limit between 0 and 21")  

    class Meta:
        verbose_name_plural = 'Books'
        ordering = ['pub_date']

    def __str__(self):
        """String for representing the Model object."""
        return self.title
    