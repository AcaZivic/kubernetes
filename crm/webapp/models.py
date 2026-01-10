from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Customer(models.Model):

    creation_date = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    email = models.CharField(max_length=255)

    phone = models.CharField(max_length=20)

    address = models.CharField(max_length=300)

    city = models.CharField(max_length=255)

    postal_code = models.IntegerField(
        verbose_name="Poštanski broj",
        validators=[
            MinValueValidator(10000, message="Poštanski broj mora biti jednak ili veći od 10000."),
            MaxValueValidator(99999, message="Poštanski broj mora biti jednak ili manji od 99999.")
        ],
        help_text="Enter the postal code between 10000 and 99999"
    )

    country = models.CharField(max_length=125)


    def __str__(self):

        return self.first_name + "   " + self.last_name














