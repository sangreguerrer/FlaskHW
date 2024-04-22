import requests
#
# response = requests.post(
#     "http://127.0.0.1:5000/user",
#     json={"name": "user_sa", "email": "ws@ient.ru", "password": "12345FsG3"},
# )
# print(response.status_code)
# print(response.json())

# response = requests.get(
#     'http://127.0.0.1:5000/user',
#         headers={"Authorization": "2609a10a-307f-4740-9f91-f9f0fa882e2d"},
# )
# print(response.status_code)
# print(response.json())

# response = requests.get(
#     'http://127.0.0.1:5000/article',
#         headers={"Authorization": "2609a10a-307f-4740-9f91-f9f0fa882e2d"},
#         json={"id":"1"}
# )
# print(response.status_code)
# print(response.json())

# response = requests.post(
#     "http://127.0.0.1:5000/article",
#     headers={"Authorization": "2609a10a-307f-4740-9f91-f9f0fa882e2d"},
#     json={"title": "user_sa's first article", "description": "Усатая собака и как быть в этой ситуации"}
# )
# print(response.status_code)
# print(response.json())


# response = requests.patch(
#     'http://127.0.0.1:5000/user',
#     headers={"Authorization": "2609a10a-307f-4740-9f91-f9f0fa882e2d"},
#     json={"id": "1", "email": "newman@mail.ru"},
# )
# print(response.status_code)
# print(response.json())
#
# response = requests.patch(
#     'http://127.0.0.1:5000/article/1',
#     headers={"Authorization": "2609a10a-307f-4740-9f91-f9f0fa882e2d"},
#     json={"title": "Mustachioed dog", "description": "Усатая мордастая, носатая,зубастая"},
# )
# print(response.status_code)
# print(response.json())


# response = requests.get(
#     'http://127.0.0.1:5000/user/5',
# )
# print(response.status_code)
# print(response.json())

# response = requests.delete(
#     "http://127.0.0.1:5000/user",
#         headers={"Authorization": "dc5ce184-8605-492c-96f4-6ec27647600f"},
#         json={"id": "4"}
# )
# print(response.status_code)
# print(response.json())

# response = requests.delete(
#     "http://127.0.0.1:5000/article/2",
#         headers={"Authorization": "2609a10a-307f-4740-9f91-f9f0fa882e2d"},
#         json={"id": 2}
# )
# print(response.status_code)
# print(response)

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