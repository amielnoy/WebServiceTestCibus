import json
from flask import Flask
from flask.testing import FlaskClient
import pytest

from app import app

global current_user_token


@pytest.fixture()
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
    assert response.json == {'UserMessage': 'OK'}


@pytest.mark.first
def test_login(client):
    global current_user_token
    data = {
        'UserName': 'test_user',
        'Password': 'test_password'
    }
    response = client.post('/login', json=data)
    assert response.status_code == 200
    assert str(response.json).__contains__("access_token")
    response_dictionary = response.json
    current_user_token = response_dictionary['access_token']


def test_logout(client):
    global current_user_token
    headers = {'Authorization': f'Bearer {current_user_token}'}
    response = client.post('/logout', headers=headers)
    assert response.status_code == 200
    assert response.json == {'UserMessage': 'logged OUT SUCCESFULY', 'user': 'test_user'}


def test_get_all_messages(client):
    response = client.get('/messages')
    assert response.status_code == 200
    response_dictionary = response.json
    message_data = response_dictionary['message2']
    assert message_data['UserName'] == "liad", "error in message username expected liad but got=" + message_data[
        'UserName']
    assert message_data['Message'] == "liad Message4", "error in user message expected liad Message4 but got=" + \
                                                       message_data['Message']
    assert message_data['Votes'] == '5', "error in Votes expected 5 Message4 but got=" + \
                                         message_data['Votes']
    # Add assertions for the expected response


def test_add_message_for_loggedin_user(client):
    headers = {'Authorization': f'Bearer {current_user_token}'}
    message_text = "adding message for user"
    data = {"MessageText": message_text}
    response = client.post('/messages', json=data, headers=headers)
    assert response.status_code == 200

    response_dictionary = response.json
    assert response_dictionary['Message'] == message_text
    assert response_dictionary['UserMessage'] == " ADDED SUCCESFULY MESSAGE TO THE BOARD!"
    assert response_dictionary['Username'] == "test_user"


def test_vote_for_message(client):
    global current_user_token
    data = {
        'Vote': 'vote_up'
    }
    headers = {'Authorization': f'Bearer {current_user_token}'}
    response = client.post('/messages/10/vote', json=data, headers=headers)
    assert response.status_code == 200
    response_dictionary = response.json
    assert response_dictionary['Messageid'] == '10', "error expected Messageid 10 got=" + response_dictionary[
        'MessageId']


def test_delete_user_message(client):
    global current_user_token
    # add message to delete later
    headers = {'Authorization': f'Bearer {current_user_token}'}
    message_text = "adding message for user"
    data = {"MessageText": message_text}
    response = client.post('/messages', json=data, headers=headers)
    assert response.status_code == 200
    response_dictionary=response.json
    MessageID=response_dictionary['MessageID']
    #delet it
    response = client.delete('/messages/'+str(MessageID), headers=headers)
    assert response.status_code == 200
    # Add assertions for the expected response
    response_dictionary = response.json
    assert response_dictionary['MessageId'] == str(MessageID), "error expected Messageid "+MessageID+ "got=" + response_dictionary[
        'MessageId']
    assert response_dictionary['UserMessage'] == "DELETED SUCCESFULY By User=test_user"\
        ,"Error in User message! expected="+"DELETED SUCCESFULY By User=test_user but got"+response_dictionary['UserMessage']
def test_get_all_user_messages(client):
    global current_user_token
    headers = {'Authorization': f'Bearer {current_user_token}'}
    response = client.get('/user/messages', headers=headers)
    assert response.status_code == 200
    # Add assertions for the expected response
