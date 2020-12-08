# %%
import streamlit as st
from requests import post, get
from json import loads
from pandas import DataFrame, to_datetime
import plotly.express as px


@st.cache
def extract_data(boiler):
    login_url = "http://localhost:8000/api-token-auth/"
    user_info = {
        "username": "admin_01",
        "password": "sysadmin1234"
    }
    # get token
    res = post(login_url, user_info)
    token = loads(res.content.decode("utf-8"))["token"]
    headers = {"Authorization": f"JWT {token}"}
    # extract mails
    base_url = "http://localhost:8000/"
    res = get(f"{base_url}get_mails", headers=headers)
    mails = loads(res.content.decode("utf-8"))
    mails = DataFrame(mails)
    mails["created_at"] = to_datetime(mails["created_at"])
    mails["mail_length"] = mails["text"].apply(lambda x: len(x))
    # extract users
    res = get(f"{base_url}get_users", headers=headers)
    users = loads(res.content.decode("utf-8"))
    users = DataFrame(users)
    users["date_joined"] = to_datetime(users["date_joined"])
    # extract profiles
    res = get(f"{base_url}get_profiles", headers=headers)
    profiles = loads(res.content.decode("utf-8"))
    profiles = DataFrame(profiles).merge(
        users.loc[:, ["id", "username"]].rename(columns={"id": "user"}),
        on="user"
    )
    mails = mails.merge(
        profiles.loc[:, ["user", "username"]],
        on="user"
    )
    return mails, profiles, users


def overview_info(users):
    joined = users.date_joined.dt.date\
        .value_counts().reset_index()\
        .rename(
            columns={
                "index": "date_joined",
                "date_joined": "number_of_users"
                }
            )
    fig = px.bar(
        joined,
        title="Nuevos usuarios por fecha",
        x="date_joined",
        y="number_of_users"
    )
    return fig


def general_view(mails, profiles):
    fig = px.histogram(
        mails,
        title="Histograma de Largo de Mails, Todos los Usuarios",
        x="mail_length",
        nbins=10,
        marginal="rug"
        )
    return fig


def user_view(mails, profiles, chosen_users):
    tmp = mails.loc[mails["username"].isin(chosen_users)]
    fig = px.histogram(
        tmp,
        title="Histograma de Largo de Mails, Usuarios Seleccionados",
        x="mail_length",
        color="username",
        nbins=10,
        marginal="rug"
    )
    return fig


def boiler():
    pass


# %%
