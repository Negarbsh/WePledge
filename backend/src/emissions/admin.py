#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Admin settings"""


from django.contrib import admin
from django.apps import apps
from emissions.models import (
    CustomUser,
    WorkingGroup,
    Institution,
    Heating,
    Electricity,
    Commuting,
    CommutingGroup,
    BusinessTrip,
    BusinessTripGroup,
    ResearchField,
    WorkingGroupJoinRequest
)

# Admin Models: Configure how information is displayed on Django Admin page

class CustomUserAdmin(admin.ModelAdmin):
    """Configures how CustomUser info is displayed"""
    readonly_fields = ('is_representative', 'username', )


# Register your models here
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(WorkingGroup)
admin.site.register(Institution)
admin.site.register(Heating)
admin.site.register(Electricity)
admin.site.register(Commuting)
admin.site.register(CommutingGroup)
admin.site.register(BusinessTrip)
admin.site.register(BusinessTripGroup)
admin.site.register(ResearchField)
admin.site.register(WorkingGroupJoinRequest)

# GraphQL
app = apps.get_app_config("graphql_auth")

for _, model in app.models.items():
    admin.site.register(model)
