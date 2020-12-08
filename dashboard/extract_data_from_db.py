# %%
import requests
import json
import pandas as pd

# user info
login_url = "http://localhost:8000/api-token-auth/"
user_info = {
    "username": "admin_01",
    "password": "sysadmin1234"
}
# get token
res = requests.post(login_url, user_info)
token = json.loads(res.content.decode("utf-8"))["token"]
headers = {"Authorization": f"JWT {token}"}
# extract mails
base_url = "http://localhost:8000/"
res = requests.get(f"{base_url}get_mails", headers=headers)
mails = json.loads(res.content.decode("utf-8"))
mails = pd.DataFrame(mails)
# extract users
res = requests.get(f"{base_url}get_users", headers=headers)
users = json.loads(res.content.decode("utf-8"))
users = pd.DataFrame(users).loc[
    :, ["id", "username"]
    ].rename(
        columns={"id": "user"}
    )
# extract profiles
res = requests.get(f"{base_url}get_profiles", headers=headers)
profiles = json.loads(res.content.decode("utf-8"))
profiles = pd.DataFrame(profiles).merge(users, on="user")
# %%
