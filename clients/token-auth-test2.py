import requests


def client():
    token_h = "Token f09494d45aff651e6b3d32b2258b95c4622cfba1"
    # data = {"username": "rest",
    #         "email": "rest@rest.com",
    #         "password1": "rest12399847",
    #         "password2": "rest12399847",
    #         }

    # response = requests.post(
    #     "http://127.0.0.1:8000/api/rest-auth/registration/", data=data)
    headers = {"Authorization": token_h}

    response = requests.get(
        "http://127.0.0.1:8000/api/profiles/", headers=headers)

    print("Status Code: ", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    client()
