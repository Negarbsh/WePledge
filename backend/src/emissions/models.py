from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Researcher. May be normal user or a group representative
    """
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=100, unique=True)
    working_group = models.ForeignKey('WorkingGroup', on_delete=models.SET_NULL, null=True)
    is_representative = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class WorkingGroup(models.Model):
    """
    Working group
    """
    name = models.CharField(max_length=100, blank=False)

    class Organizations(models.TextChoices):
        UNI_HD = 'Heidelberg University', _('Heidelberg University')
        MPIA = 'MPIA', _('Max-Planck Institute')
        EMBL = 'EMBL', _('European Molecular Biology Laboratory')

    organization = models.CharField(max_length=100, choices=Organizations.choices, blank=False)
    representative = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    class Meta:
        unique_together = ("name", "organization")

    def __str__(self):
        return self.organization + " - " + self.name


class BusinessTrip(models.Model):
    """
    Business trip
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateField()
    distance = models.FloatField()
    co2e = models.FloatField()

    CAR = 'CAR'
    BUS = 'BUS'
    TRAIN = 'TRAIN'
    PLANE = 'PLANE'
    transportation_choices = [(CAR, "Car"),
                              (BUS, "Bus"),
                              (TRAIN, "Train"),
                              (PLANE, "Plane")]
    transportation_mode = models.CharField(max_length=10,
                                           choices=transportation_choices,
                                           blank=False,
                                           )

    #def __str__(self):
    #    return "{} on ".format(self.user.username, self.date)


class CarTrip(models.Model):
    """
    Additional data for business trips by car
    """
    passengers = models.IntegerField()

    ELECTRIC = 'ELECTRIC'
    NATURAL = 'NATURAL'
    GAS = 'GAS'
    GASOLINE = 'GASOLINE'
    DIESEL = 'DIESEL'
    UNKNOWN = 'UNKNOWN'
    fuel_type_choices = [(ELECTRIC, "Electric"),
                         (NATURAL, "Natural"),
                         (GAS, "Gas"),
                         (GASOLINE, "Gasoline"),
                         (DIESEL, 'Diesel'),
                         (UNKNOWN, 'Unknown')]

    fuel_type = models.CharField(max_length=10, choices=fuel_type_choices, default=UNKNOWN, blank=False)

    SMALL = 'SMALL'
    MEDIUM = 'MEDIUM'
    LARGE = 'LARGE'
    UNKNOWN = 'UNKNOWN'

    size_choices = [(SMALL, "Small"),
                    (MEDIUM, "Medium"),
                    (LARGE, "Large"),
                    (UNKNOWN, 'Unknown')]

    size = models.CharField(max_length=10, choices=size_choices, default=UNKNOWN, blank=False)

    business_trip = models.ForeignKey(BusinessTrip, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.id


class BusTrip(models.Model):
    """
    Additional data for business trips by bus
    """
    capacity = models.FloatField(null=True)
    occupancy = models.IntegerField(null=True)

    ELECTRIC = 'ELECTRIC'
    NATURAL = 'NATURAL'
    GAS = 'GAS'
    GASOLINE = 'GASOLINE'
    DIESEL = 'DIESEL'
    UNKNOWN = 'UNKNOWN'
    fuel_type_choices = [(ELECTRIC, "Electric"),
                         (NATURAL, "Natural"),
                         (GAS, "Gas"),
                         (GASOLINE, "Gasoline"),
                         (DIESEL, 'Diesel'),
                         (UNKNOWN, 'Unknown')]
    fuel_type = models.CharField(max_length=10, choices=fuel_type_choices, default=UNKNOWN, blank=False)

    SMALL = 'SMALL'
    MEDIUM = 'MEDIUM'
    LARGE = 'LARGE'
    UNKNOWN = 'UNKNOWN'
    size_choices = [(SMALL, "Small"),
                    (MEDIUM, "Medium"),
                    (LARGE, "Large"),
                    (UNKNOWN, 'Unknown')]
    size = models.CharField(max_length=10, choices=size_choices, default=UNKNOWN, blank=False)

    business_trip = models.ForeignKey(BusinessTrip, on_delete=models.CASCADE, blank=False)


class TrainTrip(models.Model):
    """
    Additional data for business trips by train
    """
    ELECTRIC = 'ELECTRIC'
    DIESEL = 'DIESEL'
    UNKNOWN = 'UNKNOWN'
    fuel_type_choices = [(ELECTRIC, "Electric"),
                         (DIESEL, 'Diesel'),
                         (UNKNOWN, 'Unknown')]
    fuel_type = models.CharField(max_length=10, choices=fuel_type_choices, default=UNKNOWN, blank=False)

    business_trip = models.ForeignKey(BusinessTrip, on_delete=models.CASCADE, blank=False)


class PlaneTrip(models.Model):
    """
    Additional data for business trips by plane
    """
    IATA_start = models.CharField(max_length=3)
    IATA_destination = models.CharField(max_length=3)
    ECONOMY = 'ECONOMY'
    BUSINESS = 'BUSINESS'
    FIRST = 'FIRST'
    UNKNOWN = 'UNKNOWN'
    flight_class_choices = [(ECONOMY, "Economy"),
                            (BUSINESS, "Business"),
                            (FIRST, 'First Class'),
                            (UNKNOWN, 'Unknown')]

    flight_class = models.CharField(max_length=15, choices=flight_class_choices, default=UNKNOWN, blank=False)
    round_trip = models.BooleanField(default=True)

    business_trip = models.ForeignKey(BusinessTrip, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return "{} - {} on {}".format(self.IATA_start, self.IATA_destination, str(self.business_trip.timestamp))


class Heating(models.Model):
    """
    Heating consumption per year
    """
    working_group = models.ForeignKey(WorkingGroup, on_delete=models.CASCADE)
    consumption_kwh = models.FloatField(null=False)
    timestamp = models.DateField(null=False)

    PUMPAIR = 'PUMPAIR'
    PUMPGROUND = 'PUMPGROUND'
    PUMPWATER = 'PUMPWATER'
    LIQUID = 'LIQUID'
    OIL = 'OIL'
    PELLETS = 'PELLETS'
    SOLAR = 'SOLAR'
    WOODCHIPS = 'WOODCHIPS'
    ELECTRICITY = 'ELECTRICITY'
    GAS = 'GAS'
    fuel_type_choices = [(PUMPAIR, 'Pump air'), (PUMPGROUND, 'Pump ground'), (PUMPWATER, 'Pump water'),
                         (LIQUID, 'Liquid'), (OIL, 'Oil'), (PELLETS, 'Pellets'), (SOLAR, 'Solar'),
                         (WOODCHIPS, 'Woodchips'),
                         (ELECTRICITY, 'Electricity'), (GAS, 'Gas')]
    fuel_type = models.CharField(max_length=20, choices=fuel_type_choices, blank=False)

    cost_kwh = models.FloatField()
    co2e = models.FloatField()


class Electricity(models.Model):
    """
    Electricity consumption per year
    """
    working_group = models.ForeignKey(WorkingGroup, on_delete=models.CASCADE)
    consumption_kwh = models.FloatField(null=False)
    timestamp = models.DateField(null=False)

    GERMAN_ELECTRICITY_MIX = 'german energy mix' # must be same as in data of co2calculator
    #GREEN_ENERGY = 'GREEN_ENERGY'
    SOLAR = 'solar'
    fuel_type_choices = [(GERMAN_ELECTRICITY_MIX, 'German Energy Mix'),
                         #(GREEN_ENERGY, 'Green energy'),
                         (SOLAR, 'Solar')]
    fuel_type = models.CharField(max_length=30, choices=fuel_type_choices, blank=False)

    co2e = models.FloatField()