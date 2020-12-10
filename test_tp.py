# %%
# Cambios realizados para compatibilidad:
# SPAM y HAM ahora son Spam y Ham
# paso de ser 'OK' a ser 'OK'
# Ejemplo:  'http://migrupo.us-west-1.elasticbeanstalk.com/'
HOST = "http://localhost:8000/"

PASSWORD_BIG = 'contrabig01'
PASSWORD_SMALL = 'contrasmall01'
# %%
# #------------------------------
import requests
import json

# El username que nos crearon con cupta chica
USERNAME_SMALL = 'user_small_quota'
# El username que nos crearon con cupta grande
USERNAME_BIG = 'user_big_quota'


# pruebo sin headers
res = requests.get(HOST+'quota_info')
assert(res.status_code == 401)

res = requests.get(HOST+'history/1')
assert(res.status_code == 401)

res = requests.post(HOST+'process_email')
assert(res.status_code == 401)

# ### USERNAME_SMALL

data_login = {'username': USERNAME_SMALL, 'password': PASSWORD_SMALL}
response = requests.post(HOST+'api-token-auth/', data_login)
token = json.loads(response.content.decode('utf-8'))['token']
headers = {'Authorization': f'JWT {token}'}

# usuario con 10 quotas
res = requests.get(HOST+'quota_info', headers=headers)
assert(res.status_code == 200)
res_dic = json.loads(res.content.decode('utf-8'))
assert('procesados' in res_dic)
assert(res_dic['procesados'] == 0)
assert(res_dic['disponible'] == 10)


# usuario con 10 quotas
for i in range(1, 11):
    res = requests.post(
            HOST + 'process_email',
            data={'text': 'Hola como estas?'},
            headers=headers
        )
    assert(res.status_code == 200)
    res_dic = json.loads(res.content.decode('utf-8'))
    assert('status' in res_dic)
    assert('result' in res_dic)
    assert(res_dic['status'] == 'OK')
    assert(res_dic['result'] in ['Ham', 'Spam'])

    print(i, res.content)

    res = requests.get(HOST+'quota_info', headers=headers)
    assert(res.status_code == 200)
    res_dic = json.loads(res.content.decode('utf-8'))
    assert('procesados' in res_dic)
    assert(res_dic['procesados'] == i)
    assert(res_dic['disponible'] == 10-i)

res = requests.post(
        HOST+'process_email',
        data={'text': 'Hola como estas?'},
        headers=headers
    )
assert(res.content == b'{"status":"fail","message":"No quota left"}')

# ###### USERNAME_BIG

data_login = {'username': USERNAME_BIG, 'password': PASSWORD_BIG}
response = requests.post(HOST+'api-token-auth/', data_login)
token = json.loads(response.content.decode('utf-8'))['token']
headers = {'Authorization': f'JWT {token}'}

# usuario con 10 quotas
res = requests.get(HOST+'quota_info', headers=headers)
assert(res.status_code == 200)
res_dic = json.loads(res.content.decode('utf-8'))
assert('procesados' in res_dic)
assert(res_dic['procesados'] == 0)
assert(res_dic['disponible'] == 1000)


# usuario con 1000 quotas
for i in range(1, 100):
    res = requests.post(
        HOST+'process_email',
        data={'text': 'Hola como estas?'},
        headers=headers
    )
    assert(res.status_code == 200)
    res_dic = json.loads(res.content.decode('utf-8'))
    assert('status' in res_dic)
    assert('result' in res_dic)
    assert(res_dic['status'] == 'OK')
    assert(res_dic['result'] in ['Ham', 'Spam'])

    print(i, res.content)

    res = requests.get(HOST+'quota_info', headers=headers)
    assert(res.status_code == 200)
    res_dic = json.loads(res.content.decode('utf-8'))
    assert('procesados' in res_dic)
    assert(res_dic['procesados'] == i)
    assert(res_dic['disponible'] == 1000-i)

print('OK')


# %%
