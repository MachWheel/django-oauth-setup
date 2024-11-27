import jwt


class GoogleLoginServiceCredentials:
    client_id: str
    client_secret: str
    project_id: str

    def __init__(self, client_id: str, client_secret: str, project_id: str):
        self.client_id = client_id
        self.project_id = project_id
        self.client_secret = client_secret


class GoogleAccessTokens:
    id_token: str
    access_token: str

    def __init__(self, response_data: dict):
        self.id_token = str(response_data["id_token"])
        self.access_token = str(response_data["access_token"])


class GoogleUserData:
    email: str
    first_name: str
    last_name: str

    def __init__(self, access_tokens: GoogleAccessTokens):
        decoded_token_data = jwt.decode(
            jwt=access_tokens.id_token,
            options={"verify_signature": False}
        )
        self.email = decoded_token_data["email"]
        self.first_name = decoded_token_data["given_name"]
        try:
            self.last_name = decoded_token_data["family_name"]
        except KeyError:
            self.last_name = ""

