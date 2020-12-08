# %%
import streamlit as st
from requests import post, get
from json import loads
from pandas import DataFrame, to_datetime, pivot_table
import plotly.express as px
from numpy import cumsum


@st.cache
def extract_data():
    login_url = "http://localhost:8000/api-token-auth/"
    # Usuario --> 'admin'
    # Contra --> 'usuario01'
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
    # preprop de perfiles para cuota
    profiles["quota_porcentual"] = (
        (profiles["quota"] / profiles["original_quota"]) * 100
    ).apply(lambda x: f"{x:0.2f}%")
    # preprop de usuarios para tener la suma cumulativa
    users_joined = users.date_joined.dt.date\
        .value_counts().reset_index()\
        .rename(
            columns={
                "index": "date_joined",
                "date_joined": "number_of_users"
                }
        ).sort_values(
            by="date_joined"
        )
    users_joined["number_of_users"] = cumsum(users_joined["number_of_users"])
    # preprop de mails, para tener mails procesados por día
    tmp_mails = mails.loc[
        :,
        ["username", "created_at", "result", "text"]
    ].copy()
    tmp_mails["created_at"] = to_datetime(
        tmp_mails["created_at"].dt.date
    ).dt.tz_localize("UTC")
    mails_per_date = pivot_table(
        data=tmp_mails,
        index=["username", "created_at", "result"],
        aggfunc={
            "text": "count"
        }
    ).reset_index()
    return mails, profiles, users_joined, mails_per_date


def overview_info(users_joined):
    fig = px.line(
        users_joined,
        title="Nuevos usuarios por fecha",
        x="date_joined",
        y="number_of_users"
    )
    # write to gui
    st.subheader("Información general sobre API")
    st.plotly_chart(fig)


def filter_mails(mails, type_choice, date_start, date_end, chosen_users=None):
    if type_choice.lower() == "todos":
        tmp_mails = mails.loc[
                (mails.created_at >= date_start) &
                (mails.created_at <= date_end),
                :
            ]
    else:
        tmp_mails = mails.loc[
                (mails.created_at >= date_start) &
                (mails.created_at <= date_end) &
                (mails.result.isin([type_choice])),
                :
            ]
    if not chosen_users:
        return tmp_mails
    else:
        return tmp_mails.loc[mails["username"].isin(chosen_users)]


def filter_profiles(profiles, chosen_users=None):
    if not chosen_users:
        tmp = profiles.loc[
            :, ["username", "quota", "original_quota", "quota_porcentual"]
        ]
    else:
        tmp = profiles.loc[
            profiles["username"].isin(chosen_users),
            ["username", "quota", "original_quota", "quota_porcentual"]
        ]
    return tmp.rename(
            columns={
                "username": "Usuario",
                "quota": "Quota Restante",
                "original_quota": "Quota Original",
                "quota_porcentual": "Quota Porcentual"
            }
        ).sort_values(
            by="Quota Original",
            ascending=False
        ).reset_index(
            drop=True
        )


def filter_mails_per_date(
    mails_per_date, type_choice, date_start, date_end, chosen_users=None
):
    if type_choice.lower() == "todos":
        tmp = mails_per_date.loc[
            (mails_per_date.created_at >= date_start) &
            (mails_per_date.created_at <= date_end),
            :
        ]
    else:
        tmp = mails_per_date.loc[
            (mails_per_date.created_at >= date_start) &
            (mails_per_date.created_at <= date_end) &
            (mails_per_date.result.isin([type_choice])),
            :
        ]
    if not chosen_users:
        return pivot_table(
            tmp, index="created_at", aggfunc={"text": "sum"}
        ).reset_index()
    else:
        tmp = tmp.loc[
            tmp.username.isin(chosen_users),
            :
        ]
        return pivot_table(
            tmp,
            index=["created_at", "username"],
            aggfunc={"text": "sum"}
        ).reset_index()


def entrypoint_view(mails, profiles, mails_date):
    hist = px.histogram(
        mails,
        title="Histograma de Largo de Mails, Todos los Usuarios",
        x="mail_length",
        nbins=10,
        marginal="rug"
    )
    filtered_profiles = filter_profiles(profiles)
    by_date = pivot_table(
        mails_date,
        index="created_at",
        aggfunc={"text": "sum"}
    ).reset_index().rename(
        columns={
            "created_at": "Fecha",
            "text": "Cantidad de Mails"
        }
    )
    bars = px.bar(
        by_date,
        x="Fecha",
        y="Cantidad de Mails"
    )
    # write to gui
    st.write("Mostrando resultados para todos los usuarios")
    st.subheader("Histograma de Largo de Mails")
    st.plotly_chart(hist)
    st.subheader("Mails Procesados por Fecha")
    st.plotly_chart(bars)
    st.subheader("Quota de Mails, Todos los Usuarios")
    st.table(filtered_profiles)


def general_view(
    mails, profiles, mails_date, type_choice, date_start, date_end
):
    tmp_mails = filter_mails(mails, type_choice, date_start, date_end)
    hist = px.histogram(
        tmp_mails,
        title="Histograma de Largo de Mails, Todos los Usuarios",
        x="mail_length",
        nbins=10,
        marginal="rug"
    )
    filtered_profiles = filter_profiles(profiles)
    mails_processed_date = filter_mails_per_date(
        mails_date, type_choice, date_start, date_end,
    )
    bars = px.bar(
        mails_processed_date,
        x="created_at",
        y="text"
    )
    # write to gui
    st.write("Mostrando resultados para todos los usuarios")
    st.subheader("Histograma de Largo de Mails")
    st.plotly_chart(hist)
    st.subheader("Mails Procesados por Fecha")
    st.plotly_chart(bars)
    st.subheader("Quota de Mails, Todos los Usuarios")
    st.table(filtered_profiles)


def user_view(
    mails, profiles, mails_date, chosen_users,
    type_choice, date_start, date_end
):
    tmp_mails = filter_mails(
        mails, type_choice, date_start, date_end, chosen_users=chosen_users
    )
    hist = px.histogram(
        tmp_mails,
        title="Histograma de Largo de Mails, Usuarios Seleccionados",
        x="mail_length",
        color="username",
        nbins=10,
        marginal="rug"
    )
    filtered_profiles = filter_profiles(profiles, chosen_users=chosen_users)
    mails_processed_date = filter_mails_per_date(
        mails_date, type_choice, date_start, date_end,
        chosen_users=chosen_users
    )
    bars = px.bar(
        mails_processed_date,
        x="created_at",
        y="text",
        color="username"
    )
    # write to gui
    st.write(f"Mostrando resultados para usuario(s) {chosen_users}")
    st.subheader("Histograma de Largo de Mails")
    st.plotly_chart(hist)
    st.subheader("Mails Procesados por Fecha")
    st.plotly_chart(bars)
    st.subheader("Quota de Mails, Todos los Usuarios")
    st.table(filtered_profiles)


def boiler():
    pass


# %%
