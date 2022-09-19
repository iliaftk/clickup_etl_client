from io import BufferedReader
from base.apiitem import APIClass
from oauth.service import OAuth, OAuthUtils
from config import ClickUpCreateTask
from settings import click_up_settings


class Users(APIClass):

    async def get_user_by_token(self) -> dict:
        url = 'https://api.clickup.com/api/v2/user'

        r_json = await self.make_request("GET", url)
        return r_json['user']

    async def get_user_by_team_id_and_user_id(self, team_id: int, user_id: int) -> dict:
        url = f'https://api.clickup.com/api/v2/team/{team_id}/user/{user_id}'

        r_json = await self.make_request("GET", url)
        return r_json['member']['user']

    async def get_users_by_task(self, task_id: str) -> dict:
        url = f'https://api.clickup.com/api/v2/task/{task_id}/member'

        r_json = await self.make_request("GET", url)
        return r_json['members']


class Teams(APIClass):

    async def get_teams(self) -> list:
        url = 'https://api.clickup.com/api/v2/team'

        r_json = await self.make_request("GET", url)
        return r_json['teams']


class Spaces(APIClass):

    async def get_spaces(self, team_id: int) -> list:
        url = f"https://api.clickup.com/api/v2/team/{team_id}/space?archived=false"
        r_json = await self.make_request("GET", url)
        return r_json['spaces']


class Folders(APIClass):

    async def get_folders(self, space_id: int) -> list:
        url = f"https://api.clickup.com/api/v2/space/{space_id}/folder?archived=false"
        r_json = await self.make_request("GET", url)
        return r_json['folders']

    async def get_folder(self, folder_id: int) -> list:
        url = f"https://api.clickup.com/api/v2/folder/{folder_id}"
        r_json = await self.make_request("GET", url)
        return r_json


class Lists(APIClass):

    async def get_lists(self, folder_id: int):
        url = f"https://api.clickup.com/api/v2/folder/{folder_id}/list?archived=false"
        r_json = await self.make_request("GET", url)
        return r_json['lists']


class Tasks(APIClass):

    async def get_tasks(self, team_id: int, click_user_id: int):
        url = f"https://api.clickup.com/api/v2/team/{team_id}/task?assignees%5B%5D={click_user_id}"

        r_json = await self.make_request("GET", url)
        return r_json['tasks']

    async def create_task(self, list_id: int, task: ClickUpCreateTask):
        url = f"https://api.clickup.com/api/v2/list/{list_id}/task/"
        r_json = await self.make_request("POST", url, task.dict())
        return r_json

    async def get_task(self, task_id: str):
        url = f"https://api.clickup.com/api/v2/task/{task_id}/"

        r_json = await self.make_request("GET", url)
        return r_json

    async def get_tasks_by_list(self, list_id: int):
        url = f"https://api.clickup.com/api/v2/list/{list_id}/task"

        r_json = await self.make_request("GET", url)
        return r_json['tasks']

    async def get_task_comments(self, task_id: str):
        url = f"https://api.clickup.com/api/v2/task/{task_id}/comment/"

        r_json = await self.make_request("GET", url)
        return r_json['comments']

    async def add_task_comment(self, task_id: str, payload: dict):
        url = f"https://api.clickup.com/api/v2/task/{task_id}/comment/"

        r_json = await self.make_request("POST", url, payload)
        return r_json

    async def add_task_attachment(self, task_id: str, file_io: BufferedReader):
        url = f'https://api.clickup.com/api/v2/task/{task_id}/attachment'
        files = [
            (
                'attachment',
                (
                    file_io.name,
                    file_io,
                    'application/octet-stream'
                )
            )
        ]

        r_json = await self.make_request_send_file(url, files)
        return r_json


class ClickUpOAuth(OAuth):
    client_id = click_up_settings.CLICKUP_CLIENT_ID
    client_secret = click_up_settings.CLICKUP_SECRET_KEY

    @staticmethod
    def get_code_url(redirect_uri: str, state: dict) -> str:
        return f"https://app.clickup.com/api" \
               f"?client_id={click_up_settings.CLICKUP_CLIENT_ID}" \
               f"&state={OAuthUtils.encode_state_to_base64(state)}" \
               f"&redirect_uri={redirect_uri}"

    @classmethod
    def get_token_url(cls, code: str, redirect_uri: str = None):
        return f'https://api.clickup.com/api/v2/oauth/token?' \
               f'client_id={click_up_settings.CLICKUP_CLIENT_ID}&' \
               f'client_secret={click_up_settings.CLICKUP_SECRET_KEY}&' \
               f'code={code}'
