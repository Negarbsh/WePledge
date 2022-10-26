#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""__description__"""

__author__ = "Christina Ludwig, GIScience Research Group, Heidelberg University"
__email__ = "christina.ludwig@uni-heidelberg.de"


import pytest
import requests
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# Load settings from ./.env file
load_dotenv("../../../../.env")
GRAPHQL_URL = os.environ.get("GRAPHQL_URL")
logger.info(GRAPHQL_URL)

@pytest.mark.parametrize('transportation_mode', ['Car'])
@pytest.mark.parametrize('size', ['small', 'medium', 'large', 'average'])
@pytest.mark.parametrize('fuel_type', ['diesel', 'gasoline', 'cng', 'electric', 'hybrid', 'plug-in_hybrid', 'average'])
@pytest.mark.parametrize('passengers', list(range(1,4)))
@pytest.mark.parametrize('round_trip', [False])
def test_plan_trip_car(transportation_mode, size, fuel_type, passengers, round_trip):
    """Test whether trip planner throws error for different parameter combinations"""
    query = """
        mutation planTrip ($transportationMode: String!, $size: String!, $fuelType: String!, $passengers: Int!, $roundTrip: Boolean!) {
            planTrip (input: {
                transportationMode: $transportationMode
                distance: 200
                size: $size
                fuelType: $fuelType
                passengers: $passengers
                roundtrip: $roundTrip
            }) {
                success
                message
                co2e
            }
        }
    """

    headers = {
        "Content-Type": "application/json",
    }
    variables = {"transportationMode": transportation_mode, "size": size, "fuelType": fuel_type, "passengers": passengers, "roundTrip": round_trip}
    response = requests.post(GRAPHQL_URL, json={"query": query, "variables": variables}, headers=headers)
    logger.warning(response.content)
    assert response.status_code == 200
    data = response.json()
    logger.warning(data)
    assert data["data"]["planTrip"]["success"]

