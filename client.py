import requests


# response = requests.post(
#     "http://127.0.0.1:8080/user",
#     json={"name": "user_sa", "email": "ws@ient.ru", "password": "12345FsG3"},
# )
# print(response.status_code)
# print(response.json())
# #
# response = requests.post(
#     "http://127.0.0.1:8080/login",
#     json={"name": "user_sa", "password": "12345FsG3"},
# )
# print(response.status_code)
# print(response.json())

response = requests.get(
    'http://127.0.0.1:8080/user/1',
        headers={"Authorization": "02890bc0-b80b-4caa-9c9f-1e15e068e8bb"},
)
print(response.status_code)
print(response.json())

response = requests.get(
    'http://127.0.0.1:8080/article',
        headers={"Authorization": "02890bc0-b80b-4caa-9c9f-1e15e068e8bb"},
        json={"id":"1"}
)
print(response.status_code)
print(response.json())

response = requests.post(
    "http://127.0.0.1:8080/article",
    headers={"Authorization": "02890bc0-b80b-4caa-9c9f-1e15e068e8bb"},
    json={"title": "user_sa's first article", "description": "Усатая собака и как быть в этой ситуации"}
)
print(response.status_code)
print(response.json())


response = requests.patch(
    'http://127.0.0.1:8080/user',
    headers={"Authorization": "02890bc0-b80b-4caa-9c9f-1e15e068e8bb"},
    json={"id": "1", "email": "newman@mail.ru"},
)
print(response.status_code)
print(response.json())

response = requests.patch(
    'http://127.0.0.1:8080/article/1',
    headers={"Authorization": "02890bc0-b80b-4caa-9c9f-1e15e068e8bb"},
    json={"title": "Mustachioed dog", "description": "Усатая мордастая, носатая,зубастая"},
)
print(response.status_code)
print(response.json())


response = requests.get(
    'http://127.0.0.1:8080/user/1',
    headers={"Authorization": "02890bc0-b80b-4caa-9c9f-1e15e068e8bb"},
)
print(response.status_code)
print(response.json())

# response = requests.delete(
#     "http://127.0.0.1:8080/user",
#         headers={"Authorization": "c99ae8c7-99d3-429b-9cd8-1530d19223f2"},
#         json={"id": "1"}
# )
# print(response.status_code)
# print(response.json())

# response = requests.delete(
#     "http://127.0.0.1:8080/article/3",
#         headers={"Authorization": "1d47dcfc-9f42-49c0-8190-46286943b6c5"},
#         json={"id": 2}
# )
# print(response.status_code)
# print(response.json())

# response = requests.get(
#     "http://127.0.0.1:5000/user/5",
# )
# print(response.status_code)
# print(response.json())
#
# response = requests.post(
#     "http://127.0.0.1:5000/login",
#     json={"name": "user_sa", "password": "12345FsG3"},
# )
# print(response.status_code)
# print(response.json())