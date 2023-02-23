#!/usr/bin/python
import aio_pytumblr
import yaml
import os
import code
from authlib.integrations.httpx_client import OAuth1Client


def new_oauth(yaml_path):
    '''
    Return the consumer and oauth tokens with three-legged OAuth process and
    save in a yaml file in the user's home directory.
    '''

    print('Retrieve consumer key and consumer secret from http://www.tumblr.com/oauth/apps')
    consumer_key = input('Paste the consumer key here: ').strip()
    consumer_secret = input('Paste the consumer secret here: ').strip()

    request_token_url = 'https://www.tumblr.com/oauth/request_token'
    authorize_url = 'https://www.tumblr.com/oauth/authorize'
    access_token_url = 'https://www.tumblr.com/oauth/access_token'

    # STEP 1: Obtain request token
    oauth_session = OAuth1Client(consumer_key, client_secret=consumer_secret)
    fetch_response = oauth_session.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    # STEP 2: Authorize URL + Response
    full_authorize_url = oauth_session.create_authorization_url(authorize_url)

    # Redirect to authentication page
    print('\nPlease go here and authorize:\n{}'.format(full_authorize_url))
    redirect_response = input('Allow then paste the full redirect URL here:\n').strip()

    # Retrieve oauth verifier
    oauth_response = oauth_session.parse_authorization_response(redirect_response)

    verifier = oauth_response.get('oauth_verifier')

    # STEP 3: Request final access token
    oauth_session = OAuth1Client(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier
    )
    oauth_tokens = oauth_session.fetch_access_token(access_token_url)

    tokens = {
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret,
        'oauth_token': oauth_tokens.get('oauth_token'),
        'oauth_token_secret': oauth_tokens.get('oauth_token_secret')
    }

    with open(yaml_path, 'w+') as f:
        yaml.dump(tokens, f, indent=2)

    return tokens


if __name__ == '__main__':
    yaml_path = os.path.expanduser('~') + '/.tumblr'
    alternate_path = os.path.expanduser('~') + '/.pytumblr'

    if os.path.isdir(yaml_path) or os.path.exists(alternate_path):
        yaml_path = alternate_path

    if not os.path.exists(yaml_path):
        tokens = new_oauth(yaml_path)
    else:
        with open(yaml_path, "r") as f:
            tokens = yaml.safe_load(f)

    print('pytumblr tokens initialised. You can find tokens here:.\n' + str(yaml_path))
