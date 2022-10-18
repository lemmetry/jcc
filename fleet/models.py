from django.db import models
from django.core.validators import RegexValidator
from inventory.models import Bag
from django.templatetags.static import static


class Station(models.Model):
    station_id = models.CharField(max_length=2)
    logo = models.ImageField(upload_to='fleet/',
                             blank=True,
                             null=True)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                 message="Format: '+1234567890', 9-10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list

    # TODO mailing address field?

    def format_phone_number(self):
        if self.phone_number:
            return '{}.{}.{}'.format(self.phone_number[0:3], self.phone_number[3:6], self.phone_number[6:])
        return

    def get_name(self):
        name = 'Station ' + self.station_id
        return name

    def get_logo(self):
        if self.logo:
            return self.logo.url
        return static('fleet/logo_jcc.png')

    def get_path(self):
        url = 'station_' + self.station_id
        return url

    def __str__(self):
        return self.get_name()


class Vehicle(models.Model):
    name = models.CharField(max_length=40)
    call_sign = models.CharField(max_length=10)
    station = models.ForeignKey(Station,
                                blank=True,
                                null=True,
                                on_delete=models.CASCADE)
    bags = models.ManyToManyField(Bag,
                                  through='VehicleToBagAssociation')

    def get_station_assigned(self):
        return self.station

    def get_path(self):
        return self.name.lower().replace(' ', '_')

    def __str__(self):
        return self.call_sign


class VehicleToBagAssociation(models.Model):
    vehicle = models.ForeignKey(Vehicle,
                                on_delete=models.CASCADE)
    bag = models.ForeignKey(Bag,
                            on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()

    def __str__(self):
        return '{}: {}'.format(self.vehicle.name, self.bag.name)

    class Meta:
        verbose_name = "Vehicle to Bag Association"
