from src.requestx import RequestX


class ApiClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = self.get_token()
        self.header = self.get_header()

    def get_token(self):
        # 设置身份验证端点URL
        auth_endpoint = f"{self.base_url}/api/token/"

        # 设置用户凭据
        credentials = {
            "username": self.username,
            "password": self.password
        }
        headers = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
        res = RequestX.post(url=auth_endpoint, data=credentials, headers=headers)
        import json
        jwt_token = json.loads(res)["data"]["access"]
        return jwt_token

    def get_header(self):
        header = {
            "Authorization": f"JWT {self.token}",
            "Content-Type": "application/json"
        }
        return header

    def post(self, url, data=None, json=None):
        response = RequestX.post(url, headers=self.header, data=data, json=json)
        return response


if __name__ == "__main__":
    ApiClient(
        base_url="http://10.7.55.191:8000",
        username="",
        password="",
    )
