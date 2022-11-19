#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Testing of GraphQL API queries related to user authentication"""

import os
import requests
from dotenv import load_dotenv, find_dotenv

# Load settings from ./.env file
load_dotenv(find_dotenv())

GRAPHQL_URL = os.environ.get("GRAPHQL_URL")
TEST_EMAIL = os.environ.get("TEST_EMAIL")
TEST_PASSWORD = os.environ.get("TEST_PASSWORD")
TOKEN = ""
REFRESH_TOKEN = ""


def test_register():
    """Test user registration"""

    register_query = """
            mutation ($email: String!,  $password1: String! $password2: String!) {
            register (
            email: $email,
            password1: $password1,
            password2: $password2
          ) {
             success
            errors
          }
        }
        """
    variables = {
        "email": TEST_EMAIL,
        "password1": TEST_PASSWORD,
        "password2": TEST_PASSWORD,
    }
    response = requests.post(
        GRAPHQL_URL, json={"query": register_query, "variables": variables}
    )
    response
    # assert response.status_code == 200
    # data = response.json()
    # assert data["data"]["register"]["success"]


def test_verify():
    """Test if account verification works"""
    verify_query = """
            mutation ($token: String!){
                verifyAccount (
                    token: $token
                ) {
                    success
                    errors
                }
            }
    """
    # when test fails, paste the token from the email/command output
    token_from_email = "eyJlbWFpbCI6InRlc3RAcGxlZGdlNGZ1dHVyZS5vcmciLCJhY3Rpb24iOiJhY3RpdmF0aW9uIn0:1n32oh:XYzXouRztx5nXbk8rqlqpVVBP22RFNW0x8CR7jdffdk"
    variables = {"token": token_from_email}
    response = requests.post(
        GRAPHQL_URL, json={"query": verify_query, "variables": variables}
    )
    response
    # assert response.status_code == 200
    # data = response.json()
    # assert data["data"]["verifyAccount"]["success"]


def test_login():
    """Test user login"""
    query = """
            mutation ($email: String!, $password: String!){
            tokenAuth (
            email: $email
            password: $password
          ) {
             success
            errors
            token
            refreshToken
          }
        }
    """
    variables = {"email": "test3@pledge4future.org", "password": "test_password"}
    response = requests.post(GRAPHQL_URL, json={"query": query, "variables": variables})
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["tokenAuth"]["success"]

    global TOKEN
    TOKEN = data["data"]["tokenAuth"]["token"]
    global REFRESH_TOKEN
    REFRESH_TOKEN = data["data"]["tokenAuth"]["refreshToken"]


def test_verify_token():
    """Test if token can be verified"""
    verify_token_query = """
            mutation ($token: String!){
              verifyToken(
                token: $token
              ) {
                success,
                errors,
                payload
              }
            }
    """
    variables = {"token": TOKEN}
    response = requests.post(
        GRAPHQL_URL, json={"query": verify_token_query, "variables": variables}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["verifyToken"]["success"]


def test_me_query():
    """Test whether me query returns the currently logged in user"""
    me_query = """
        query {
          me {
            verified
            workingGroup {
                id
                name
            }
          }
    }
    """
    headers = {"Content-Type": "application/json", "Authorization": f"JWT {TOKEN}"}
    response = requests.post(GRAPHQL_URL, json={"query": me_query}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["me"]["email"] == TEST_EMAIL
    assert data["data"]["me"]["verified"]


def test_update_query():
    """Test whether user data can be updated"""
    update_query = """
        mutation {
        updateAccount (
            firstName: "Louise"
            isRepresentative: "False"
      ) {
        success
        errors
      }
    }
    """
    headers = {"Content-Type": "application/json", "Authorization": f"JWT {TOKEN}"}
    response = requests.post(GRAPHQL_URL, json={"query": update_query}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["updateAccount"]["success"]


def test_refresh_token():
    """Test whether new token can be queried"""
    refresh_token_query = """
        mutation ($refreshtoken: String!) {
      refreshToken(
        refreshToken: $refreshtoken
      ) {
        success,
        errors,
        payload,
        token,
        refreshToken
      }
    }"""
    variables = {"refreshtoken": REFRESH_TOKEN}
    response = requests.post(
        GRAPHQL_URL, json={"query": refresh_token_query, "variables": variables}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["refreshToken"]["success"]
    global TOKEN
    TOKEN = data["data"]["refreshToken"]["token"]


def test_delete_account():
    """Test whether account is deleted (not applied atm)"""
    pass
    # Archive account
    # delete_query = """mutation ($password: String!)
    # {
    #    deleteAccount(
    #        password: $password,
    # ) {
    #    success,
    #    errors
    # }
    # }"""
    # headers = {"Content-Type": "application/json", "Authorization": f"JWT {TOKEN}"}
    # variables = {"password": TEST_PASSWORD}
    # response = requests.post(
    #    GRAPHQL_URL,
    #    json={"query": delete_query, "variables": variables},
    #    headers=headers,
    # )
    # assert response.status_code == 200
    # data = response.json()
    # assert data["data"]["deleteAccount"]["success"]


def test_list_users():
    """Test to query all users"""
    query = """
        query {
      users {
        edges {
          node {
            email
          }
        }
      }
    }
    """
    response = requests.post(GRAPHQL_URL, json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]["users"]["edges"]) > 1


def test_query_dropdown_options():
    """Test if querying dropdown options"""
    query = """
    { __type(name: "ElectricityFuelType") {
          enumValues {
            name
            description
          }
        }
    }
    """
    response = requests.post(GRAPHQL_URL, json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["__type"]["enumValues"][0]["name"] == "GERMAN_ENERGY_MIX"

    query = """
    {__type(name: "Unit") {
        enumValues
    {
        name
    description
    }
    }
    }
    """
    response = requests.post(GRAPHQL_URL, json={"query": query})
    assert response.status_code == 200
    response.json()
