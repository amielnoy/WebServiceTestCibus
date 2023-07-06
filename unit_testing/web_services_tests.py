import json
from flask import Flask
from flask.testing import FlaskClient
import pytest
from unittest.mock import patch

from Utils.users_login_sessions import UsersLoginSessions
from app import app


@pytest.fixture
def client() -> FlaskClient:
    app.testing = True
    with app.test_client() as client:
        yield client


def test_register_user(client):
    data = {
        'UserName': 'test_user',
        'Password': 'test_password'
    }
    response = client.post('/register', json=data)
    assert response.status_code == 200
    assert response.json == "Wrote to Users table: user_name=test_user Password=test_password"


def test_login(client):
    data = {
        'UserName': 'test_user',
        'Password': 'test_password'
    }
    response = client.post('/login', json=data)
    assert response.status_code == 200
    assert response.json == 'user=test_user logged in SUCCESFULY'


def test_logout(client):
    data = {
        'UserName': 'test_user',
        'Password': 'test_password'
    }
    response = client.post('/logout', json=data)
    assert response.status_code == 200
    assert response.json == 'user=test_user logged out succesfuly!'

def test_get_all_messages(client):
    response = client.get('/messages')
    assert response.status_code == 200
    # Add assertions for the expected response


def test_vote_for_message(client):
    data = {
        'UserName': 'test_user',
        'Vote': 'vote_up'
    }
    response = client.post('/messages/1/vote', json=data)
    assert response.status_code == 200
    # Add assertions for the expected response


def test_delete_user_message(client):
    data = {
        'UserName': 'test_user'
    }
    response = client.delete('/messages/1', json=data)
    assert response.status_code == 200
    # Add assertions for the expected response


def test_get_all_user_messages(client):
    response = client.get('/user/messages')
    assert response.status_code == 200
    # Add assertions for the expected response
