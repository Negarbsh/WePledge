"""
Create permission groups
Create permissions (read only) to models for a set of groups
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.db.utils import IntegrityError
import logging
from ...models import User, WorkingGroup, BusinessTrip, PlaneTrip, CarTrip, Heating, Electricity


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = 'Seeds the database.'

    def handle(self, *args, **options):

        # create users
        if len(User.objects.filter(username="Karen")) == 0:
            karen = User(username="Karen",
                            first_name="Karen",
                            last_name="Anderson",
                            email="karen@mpia.com",
                            password="karen")
            karen.save()
            representative_group = Group.objects.get(name='Representative')
            karen.groups.add(representative_group)

            # Creat business trip by plane
            new_trip = BusinessTrip(user=karen,
                                    distance=3000,
                                    co2e=200,
                                    timestamp="2020-05-10",
                                    transportation_mode=BusinessTrip.PLANE)
            new_trip.save()
            plane_trip = PlaneTrip(IATA_start="MUC", IATA_destination="LAX",
                                    flight_class=PlaneTrip.ECONOMY,
                                    round_trip=True,
                                    business_trip=new_trip)
            plane_trip.save()

        if len(User.objects.filter(username="Tom")) == 0:
            tom = User(username="Tom",
                            first_name="Tom",
                            last_name="Tom",
                            email="tom@mpia.com",
                            password="tomtom")
            tom.save()
            researcher_group = Group.objects.get(name='Researcher')
            tom.groups.add(researcher_group)

            new_trip = BusinessTrip(user=tom,
                                    distance=300,
                                    co2e=50,
                                    timestamp="2020-02-01",
                                    transportation_mode=BusinessTrip.TRAIN)
            new_trip.save()

        if len(User.objects.filter(username="Kim")) == 0:
            kim = User(username="Kim",
                            first_name="Kim",
                            last_name="Z",
                            email="kim@giscience.com",
                            password="kim")
            kim.save()
            researcher_group = Group.objects.get(name='Researcher')
            kim.groups.add(researcher_group)

        # Create working groups
        if len(WorkingGroup.objects.filter(name="GIScience")) == 0:
            wg_giscience = WorkingGroup(name="GIScience",
                                        organization=WorkingGroup.Organizations.UNI_HD,
                                        representative=User.objects.get(username="Kim"))
            wg_giscience.save()

        if len(WorkingGroup.objects.filter(name="Planet and Star Formation")) == 0:
            wg_bio = WorkingGroup(name="Planet and Star Formation",
                                  organization=WorkingGroup.Organizations.MPIA,
                                  representative=User.objects.get(username="Karen"))
            wg_bio.save()

        wg_bio = WorkingGroup.objects.filter(name="Planet and Star Formation")[0]
        wg_giscience = WorkingGroup.objects.filter(name="GIScience")[0]

        # Update working groups of users
        if len(User.objects.filter(username="Karen")) == 0:
            karen.working_group = wg_bio
            karen.is_representative = True
            karen.save()
        if len(User.objects.filter(username="Tom")) == 0:
            tom.working_group = wg_bio
            tom.save()
        if len(User.objects.filter(username="Kim")) == 0:
            kim.working_group = wg_giscience
            kim.is_representative = True
            kim.save()

        if len(Electricity.objects.all()) == 0:
            new_electricity = Electricity(working_group= wg_bio,
                                  timestamp="2020-01-01",
                                  consumption_kwh=5000,
                                  fuel_type=Electricity.GERMAN_ELECTRICITY_MIX,
                                  co2e=300)
            new_electricity.save()
            new_electricity2 = Electricity(working_group= wg_bio,
                                  timestamp="2020-02-01",
                                  consumption_kwh=6000,
                                  fuel_type=Electricity.GERMAN_ELECTRICITY_MIX,
                                  co2e=300)
            new_electricity2.save()

        if len(Heating.objects.all()) == 0:
            new_heating = Heating(working_group= wg_bio,
                                  timestamp="2020-01-01",
                                  consumption_kwh=2500,
                                  cost_kwh=0.30,
                                  fuel_type=Heating.OIL,
                                  co2e=300)
            new_heating.save()




