import os

import requests
from dotenv import load_dotenv


def get_access_token(auth_url, client_id, secret):
    response = requests.post(auth_url,
                             data={
                                 'grant_type': 'client_credentials',
                                 'client_id': client_id,
                                 'client_secret': secret
                             })

    return response.json()['access_token']


class AtomicApi:
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.clientId = os.getenv('CLIENT_ID')
        self.secret = os.getenv('SECRET')
        self.dest_secret = os.getenv('DEST_SECRET')
        self.dest_client_id = os.getenv('DEST_CLIENT_ID')
        self.dest_auth_url = os.getenv('DEST_AUTH_URL')
        self.token = ''
        self.dest_token = ''

    def get_flow_config(self, flow_id):
        if self.token == '':
            self.token = get_access_token(auth_url=os.getenv('SOURCE_AUTH_URL'),
                                          client_id=self.clientId,
                                          secret=self.secret)

        url = os.getenv('GET_FLOW_URL')
        get_flow_endpoint = url.format(environment=os.getenv('SOURCE_ENV'), action_flow=flow_id)
        response = requests.get(get_flow_endpoint, headers={'Authorization': f'Bearer {self.token}'})
        return response.json()['data']['config']

    def post_flow_config(self, flow_id, flow_config):
        if self.dest_token == '':
            self.dest_token = get_access_token(auth_url=self.dest_auth_url,
                                               client_id=self.dest_client_id,
                                               secret=self.dest_secret)

        post_flow_endpoint = os.getenv('POST_FLOW_URL').format(environment=os.getenv('DEST_ENV'), action_flow=flow_id)
        response = requests.post(post_flow_endpoint, headers={'Authorization': f'Bearer {self.dest_token}'},
                                 json={'config': flow_config})
        return response.json()

    def update_action_flow(self, flow_id, name):
        if self.dest_token == '':
            self.dest_token = get_access_token(auth_url=self.dest_auth_url,
                                               client_id=self.dest_client_id,
                                               secret=self.dest_secret)

        update_flow_endpoint = os.getenv('UPDATE_FLOW_URL').format(environment=os.getenv('DEST_ENV'),
                                                                   action_flow=flow_id)
        response = requests.put(update_flow_endpoint, headers={'Authorization': f'Bearer {self.dest_token}'},
                                json={'actionFlow': {'name': name}})
        return response.json()
