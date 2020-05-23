import requests


def client():
    token_h = "Token 4a734e02d006d01c8ccc1dff06f6fa66638f1874"
    # creadentials = {"username": "masakis", "password": "Ma45450721"}

    # response = requests.post(
    #     "http://127.0.0.1:8000/api/rest-auth/login/", data=creadentials)
    headers = {"Authorization": token_h}

    response = requests.get(
        "http://127.0.0.1:8000/api/profiles/", headers=headers)

    print("Status Code: ", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    client()
