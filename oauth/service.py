from base64_encoder import encode_str_to_base64, encode_dict_to_base64
from base.apiitem import APIClass


class OAuth(APIClass):
    client_id = None
    client_secret = None

    @staticmethod
    def get_code_url(redirect_uri: str, state: dict):
        raise NotImplementedError

    @staticmethod
    def get_token_url(code: str, redirect_uri: str = None):
        raise NotImplementedError

    async def get_token(self, code: str, redirect_uri: str = None, is_basic_token: bool = False) -> dict:
        if is_basic_token:
            access_basic_token = f"Basic {OAuthUtils.get_basic_token_to_base64(self.client_id, self.client_secret)}"
            self._headers['Authorization'] = access_basic_token

        url = self.get_token_url(code, redirect_uri)
        return await self.make_request("POST", url)


class OAuthUtils:

    @staticmethod
    def get_basic_token_to_base64(client_id: str, client_secret: str) -> str:
        return encode_str_to_base64(f"{client_id}:{client_secret}")

    @staticmethod
    def encode_state_to_base64(state: dict) -> str:
        return encode_dict_to_base64(state)
