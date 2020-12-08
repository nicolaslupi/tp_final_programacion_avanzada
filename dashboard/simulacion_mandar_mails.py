# %%
import requests
import json

usuarios = ["usuario_01", "usuario_02", "usuario_03", "ezeray"]
contrasenas = ["prueba_01", "prueba_02", "prueba_03", "ezequiel01"]

mails = [
    [
        "special offer for viagra, only 9.99, lowest price in the market!!!!",
        "hello mary, does 1 o'clock work for the meeting? I have to run "
        "some errands before that. best regards, johanne",
        "Cash your inheritance following three easy steps! Contact us "
        "or you'll regret not taking this chance!!!"
    ],
    [
        "I'm the prince of nigeria and can help you make lots of money!!!",
        "Hi Barry, I'm sorry to say but there's no way in which the plan"
        " will work",
        "Cash your inheritance following three easy steps! Contact us "
        "or you'll regret not taking this chance!!!"
    ],
    [
        "Buy viagra at the super low price of 99.99 for a lifetime supply!!!",
        "Hi Tom, Does sunday sound good for the barbeque? Love, Dad",
        "hello mary, does 1 o'clock work for the meeting? I have to run "
        "some errands before that. best regards, johanne",
    ],
    [
        "Cash your inheritance following three easy steps! Contact us "
        "or you'll regret not taking this chance!!!",
        "Hello Barry, What do you think of monday at noon for a quick "
        "meeting about the new process? Best regards, John",
        "hi nico, what do you think about friday night for the movies?"
        " can you buy the tickets? talk to you later, ezequiel"
    ]
]

login_url = "http://localhost:8000/api-token-auth/"
base_url = "http://localhost:8000/"
for i in range(4):
    print(usuarios[i])
    auth_data = {
        "username": usuarios[i],
        "password": contrasenas[i]
    }
    res = requests.post(login_url, auth_data)
    token = json.loads(res.content.decode("utf-8"))["token"]
    headers = {"Authorization": f"JWT {token}"}
    for m in mails[i]:
        print(m)
        requests.post(
            f"{base_url}process_email/",
            json={"text": m},
            headers=headers,
        )


# %%
