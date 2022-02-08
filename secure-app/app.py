from fastapi import Depends, FastAPI, HTTPException, Request
from okta_jwt.jwt import validate_token as validate_locally
from fastapi.security import OAuth2PasswordBearer
import uvicorn
import configparser
import httpx
import json

app = FastAPI()

# Define the auth scheme and access token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# Load environment variables
config = configparser.ConfigParser()
config.read('app.env')


def validate(request: Request, token: str = Depends(oauth2_scheme)):
    try:
        # AuthN: Validate JWT token locally
        auth_res = validate_locally(
            token,
            config.get('Okta', 'OKTA_ISSUER'),
            config.get('Okta', 'OKTA_AUDIENCE'),
            config.get('Okta', 'OKTA_CLIENT_ID')
        )

        if bool(auth_res) is False:
            return False

        # AuthZ: Validate with defined policies
        data = {
            "input": {
                "method": request.method,
                "api": request.url.path,
                "jwt": {
                    "tokenValue": token
                }
            }
        }

        opa_url = config.get('Opa', 'OPA_AUTHZ_URL')
        headers = {
            'accept': 'application/json'
        }

        authz_response = httpx.post(opa_url, headers=headers, data=json.dumps(data))

        if authz_response:
            authz_json  = json.loads(authz_response.text)
            return bool(authz_json["result"])
        else:
            return False

    except Exception as e:
        print("Error: " + str(e))
        raise HTTPException(status_code=403)


@app.get("/sayhello")
async def sayhello(valid: bool = Depends(validate)):
    if valid:
        return {"message": "Hello there!!"}
    else:
        raise HTTPException(status_code=403)


@app.get("/saysecret")
async def saysecret(valid: bool = Depends(validate)):
    if valid:
        return {"message": "This is a secret"}
    else:
        raise HTTPException(status_code=403)


if __name__ == '__main__':
    uvicorn.run('app:app',
                host='127.0.0.1',
                port=8086,
                reload=True)
