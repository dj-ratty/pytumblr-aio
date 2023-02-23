import urllib.parse
import httpx
import sys

from authlib.integrations.httpx_client import AsyncOAuth1Client


class TumblrRequest:
    """
    A simple request object that lets us query the Tumblr API
    """

    __version = "0.1.2"

    def __init__(self, consumer_key, consumer_secret="", oauth_token="", oauth_secret="", host="https://api.tumblr.com"):
        self.host = host
        self._oauth_data = {"client_id": consumer_key, "client_secret": consumer_secret,
                            "token": oauth_token, "token_secret": oauth_secret}
        self.consumer_key = consumer_key

        self.headers = {
            "User-Agent": "pytumblr-aio/" + self.__version,
        }

    def _get_client(self) -> AsyncOAuth1Client:
        return AsyncOAuth1Client(**self._oauth_data, headers=self.headers)

    async def get(self, url, params):
        """
        Issues a GET request against the API, properly formatting the params

        :param url: a string, the url you are requesting
        :param params: a dict, the key-value of all the paramaters needed
                       in the request
        :returns: a dict parsed of the JSON response
        """
        url = self.host + url
        if params:
            url = url + "?" + urllib.parse.urlencode(params)

        async with self._get_client() as client:
            resp = await client.get(url)
            return await self.json_parse(resp)

    async def post(self, url, params={}, files=[]):
        """
        Issues a POST request against the API, allows for multipart data uploads

        :param url: a string, the url you are requesting
        :param params: a dict, the key-value of all the parameters needed
                       in the request
        :param files: a list, the list of tuples of files

        :returns: a dict parsed of the JSON response
        """
        url = self.host + url
        if files:
            return await self.post_multipart(url, params, files)
        else:
            data = urllib.parse.urlencode(params)
            async with self._get_client() as client:
                resp = await client.post(url, data=data)
                return await self.json_parse(resp)

    async def delete(self, url, params):
        """
        Issues a DELETE request against the API, properly formatting the params

        :param url: a string, the url you are requesting
        :param params: a dict, the key-value of all the paramaters needed
                       in the request
        :returns: a dict parsed of the JSON response
        """
        url = self.host + url
        if params:
            url = url + "?" + urllib.parse.urlencode(params)

        async with self._get_client() as client:
            resp = await client.delete(url)
            return await self.json_parse(resp)

    @staticmethod
    async def json_parse(response):
        """
        Wraps and abstracts response validation and JSON parsing
        to make sure the user gets the correct response.

        :param response: The response returned to us from the request

        :returns: a dict of the json response
        """
        try:
            data = response.json()
        except ValueError:
            data = {'meta': {'status': 500, 'msg': 'Server Error'},
                    'response': {"error": "Malformed JSON or HTML was returned."}}

        # We only really care about the response if we succeed
        # and the error if we fail
        if 200 <= data['meta']['status'] <= 399:
            return data['response']
        else:
            return data

    async def post_multipart(self, url, params, files):
        """
        Generates and issues a multipart request for data files

        :param url: a string, the url you are requesting
        :param params: a dict, a key-value of all the parameters
        :param files:  a dict, matching the form '{name: file descriptor}'

        :returns: a dict parsed from the JSON response
        """
        async with self._get_client() as client:
            resp = await client.post(
                url,
                data=params,
                params=params,
                files=files
            )
        return await self.json_parse(resp)
