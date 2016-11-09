# This is the file to keep all third party apis

import requests


class BaseAPI(object):

    def get(self):
        response = requests.get(
            url=self.base_url,
            params=self.parameters
        )
        if response.status_code != 200:
            return None
        return response.json()


class Facebook(BaseAPI):

    base_url = "https://graph.facebook.com/v2.8/me/"
    parameters = {
        'fields': 'id,name',
    }

    def get_user_info(self, access_token):
        self.parameters['access_token'] = access_token
        return self.get()


Facebook = Facebook()
