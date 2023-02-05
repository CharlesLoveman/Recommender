from mal_api import MAL_API

user = input()

x = MAL_API.extract_user_entries(user)
print("break")
print(type(x))
print(x)