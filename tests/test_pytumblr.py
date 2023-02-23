import unittest
import mock
import json
import aio_pytumblr
from urllib.parse import parse_qs
import aiounittest


def wrap_response(response_text):
    def inner(*args, **kwargs):
        mp = mock.MagicMock()
        mp.json.return_value = json.loads(response_text)
        return mp
    return inner


def wrap_response_storing_data(response_text, store):
    def inner(*args, **kwargs):
        # store data for assertion on input
        store.data = kwargs.get('data')

        mp = mock.MagicMock()
        mp.json.return_value = json.loads(response_text)
        return mp
    return inner


class TumblrRestClientTest(aiounittest.AsyncTestCase):
    """
    """

    def setUp(self):
        with open('tumblr_credentials.json', 'r') as f:
            credentials = json.loads(f.read())
        self.client = aio_pytumblr.TumblrRestClient(credentials['consumer_key'], credentials['consumer_secret'], credentials['oauth_token'], credentials['oauth_token_secret'])

    @mock.patch('httpx.AsyncClient.request')
    async def test_dashboard(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = await self.client.dashboard()
        assert response['posts'] == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_posts(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = await self.client.posts('codingjester.tumblr.com')
        assert response['posts'] == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_posts_with_type(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = await self.client.posts('seejohnrun', 'photo')
        assert response['posts'] == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_posts_with_type_and_arg(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        args = {'limit': 1}
        response = await self.client.posts('seejohnrun', 'photo', **args)
        assert response['posts'] == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_blogInfo(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"blog": {} } }')

        response = await self.client.blog_info('codingjester.tumblr.com')
        assert response['blog'] == {}

    @mock.patch('httpx.AsyncClient.request')
    async def test_avatar_with_301(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 301, "msg": "Moved Permanently"}, "response": {"avatar_url": "" } }')

        response = await self.client.avatar('staff.tumblr.com')
        assert response['avatar_url'] == ''

    @mock.patch('httpx.AsyncClient.request')
    async def test_avatar_with_302(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 302, "msg": "Found"}, "response": {"avatar_url": "" } }')

        response = await self.client.avatar('staff.tumblr.com')
        assert response['avatar_url'] == ''

    @mock.patch('httpx.AsyncClient.request')
    async def test_followers(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"users": [] } }')

        response = await self.client.followers('codingjester.tumblr.com')
        assert response['users'] == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_blog_following(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"blogs": [], "total_blogs": 1}}')

        response = await self.client.blog_following('pytblr.tumblr.com')
        assert response['blogs'] == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_blogLikes(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"liked_posts": [] } }')

        response = await self.client.blog_likes('codingjester.tumblr.com')
        assert response['liked_posts'] == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_blogLikes_with_after(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"liked_posts": [] } }')

        response = await self.client.blog_likes('codingjester.tumblr.com', after=1418684291)
        assert response['liked_posts'] == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_notes(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"notes": [], "total_notes": 1, "can_hide_or_delete_notes": false} }')

        response = await self.client.notes('codingjester.tumblr.com', id='123456789098')
        assert response["notes"] == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_blogLikes_with_before(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"liked_posts": [] } }')

        response = await self.client.blog_likes('codingjester.tumblr.com', before=1418684291)
        assert response['liked_posts'] == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_queue(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = await self.client.queue('codingjester.tumblr.com')
        assert response['posts'] == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_drafts(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = await self.client.drafts('codingjester.tumblr.com')
        assert response['posts'] == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_submissions(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = await self.client.submission('codingjester.tumblr.com')
        assert response['posts'] == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_follow(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = await self.client.follow("codingjester.tumblr.com")
        assert response == []

        assert parse_qs(mock_post.data) == parse_qs('url=codingjester.tumblr.com')

    @mock.patch('httpx.AsyncClient.request')
    async def test_unfollow(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = await self.client.unfollow("codingjester.tumblr.com")
        assert response == []

        assert parse_qs(mock_post.data) == parse_qs('url=codingjester.tumblr.com')

    @mock.patch('httpx.AsyncClient.request')
    async def test_reblog(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = await self.client.reblog('seejohnrun', id='123', reblog_key="adsfsadf", state='coolguy', tags=['hello', 'world'])
        assert response == []

        assert parse_qs(mock_post.data) == parse_qs('state=coolguy&reblog_key=adsfsadf&id=123&tags=hello%2Cworld')

    @mock.patch('httpx.AsyncClient.request')
    async def test_edit_post(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = await self.client.edit_post('seejohnrun', id='123', state='coolguy', tags=['hello', 'world'])
        assert response == []

        assert parse_qs(mock_post.data) == parse_qs('state=coolguy&id=123&tags=hello%2Cworld')

    @mock.patch('httpx.AsyncClient.request')
    async def test_like(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = await self.client.like('123', "adsfsadf")
        assert response == []

        assert parse_qs(mock_post.data) == parse_qs('id=123&reblog_key=adsfsadf')

    @mock.patch('httpx.AsyncClient.request')
    async def test_unlike(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = await self.client.unlike('123', "adsfsadf")
        assert response == []

        assert parse_qs(mock_post.data) == parse_qs('id=123&reblog_key=adsfsadf')

    @mock.patch('httpx.AsyncClient.request')
    async def test_info(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = await self.client.info()
        assert response == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_likes(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = await self.client.likes()
        assert response == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_likes_with_after(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = await self.client.likes(after=1418684291)
        assert response == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_likes_with_before(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = await self.client.likes(before=1418684291)
        assert response == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_following(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = await self.client.following()
        assert response == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_tagged(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = await self.client.tagged('food')
        assert response == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_create_text(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = await self.client.create_text('codingjester.tumblr.com', body="Testing")
        assert response == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_create_link(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 201, "msg": "OK"}, "response": []}',
            mock_post)

        response = await self.client.create_link('codingjester.tumblr.com', url="https://google.com", tags=['omg', 'nice'])
        assert response == []

        assert parse_qs(mock_post.data) == parse_qs('url=https%3A%2F%2Fgoogle.com&type=link&tags=omg%2Cnice')

    @mock.patch('httpx.AsyncClient.request')
    async def test_no_tags(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 201, "msg": "OK"}, "response": []}',
            mock_post)

        await self.client.create_link('seejohnrun.tumblr.com', tags=[])

        assert parse_qs(mock_post.data) == parse_qs('type=link&tags=[]')

    @mock.patch('httpx.AsyncClient.request')
    async def test_create_quote(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = await self.client.create_quote('codingjester.tumblr.com', quote="It's better to love and lost, than never have loved at all.")
        assert response == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_create_chat(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = await self.client.create_chat('codingjester.tumblr.com', conversation="JB: Testing is rad.\nJC: Hell yeah.")
        assert response == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_create_photo(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = await self.client.create_photo('codingjester.tumblr.com', source="https://media.tumblr.com/image.jpg")
        assert response == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_create_audio(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = await self.client.create_audio('codingjester.tumblr.com', external_url="https://media.tumblr.com/audio.mp3")
        assert response == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_create_video(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = await self.client.create_video('codingjester.tumblr.com', embed="blahblahembed")
        assert response == []

    @mock.patch('httpx.AsyncClient.request')
    async def test_api_delete(self, mock_delete):
        mock_delete.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        api_url = '/v2/some/api'
        response = await self.client.send_api_request('delete', api_url, {'param1': 'foo', 'param2': 'bar'}, ['param1', 'param2'], False)
        assert response == []


if __name__ == "__main__":
    unittest.main()
