"""Models for 'markets' app"""
import datetime
from django.db import models


class County(models.Model):
    """
    County model - to hold counties in Ireland plus Dublin codes.
    Foreign key in Market model so markets list can be filtered by
    standardised list of counties in Ireland + by Dublin areas.
    """

    class Meta:
        """Specify correct plural so it doesn't appear as Countys"""
        verbose_name_plural = 'Counties'

    name = models.CharField(max_length=20, unique=True)
    friendly_name = models.CharField(max_length=20)

    def __str__(self):
        """string method - return the county name"""
        return self.name

    def get_friendly_name(self):
        """return the user friendly name for views/frontend"""
        return self.friendly_name


class Market(models.Model):
    """Details about the markets - date time etc."""
    class Meta:
        """order by date, newest date first"""
        ordering = ['-date']

    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    county = models.ForeignKey(
        County, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='markets',
        )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    website = models.URLField(max_length=254,)

    @property
    def date_passed(self):
        """For superuser views so can flag event has passed"""
        return self.date < datetime.date.today()

    def __str__(self):
        """string method - return the market name and formatted date"""
        market_date = self.date.strftime('%d/%m/%Y')
        return f'{self.name} on {market_date}'
