import streamlit as st
import utils
from datetime import timedelta, datetime
from pytz import UTC

mails, profiles, users_joined, mails_date = utils.extract_data()
st.title("Dashboard API Procesamiento de Mails")

st.sidebar.header("Parámetros para visualizar")

st.sidebar.subheader("Parámetros generales")

show_general = st.sidebar.selectbox(
    "Mostrar información general?",
    ["Mostrar", "No Mostrar", ]
)

st.sidebar.subheader("Parámetros para filtrar usuarios")

user_choice = st.sidebar.multiselect(
    "Elija uno o más usuarios para visualizar",
    profiles.username
)

type_choice = st.sidebar.selectbox(
    "Elegir resultado de clasificación",
    ["Todos", "Spam", "Ham", ]
)

min_date = mails["created_at"].min().date()
max_date = mails["created_at"].max().date()

date_start = st.sidebar.date_input(
    "Fecha de inicio (desde)",
    min_date
)
if date_start < min_date:
    st.error(f"Error: La fecha mínima es {min_date}")
else:
    date_start = UTC.localize(
        datetime.combine(date_start, datetime.min.time())
    )

date_end = st.sidebar.date_input(
    "Fecha de fin (hasta, inclusive)",
    max_date
)
if date_end > max_date:
    st.error(f"Error: La fecha máxima es {max_date}")
else:
    date_end = UTC.localize(
        datetime.combine(date_end, datetime.min.time())
    ) + timedelta(days=1)

if st.sidebar.button("Aplicar cambios"):
    if show_general == "Mostrar":
        utils.overview_info(users_joined)
    elif show_general == "No Mostrar":
        pass
    if len(user_choice) == 0:
        utils.general_view(
            mails, profiles, mails_date, type_choice, date_start, date_end
        )
    else:
        utils.user_view(
            mails, profiles, mails_date, user_choice, type_choice,
            date_start, date_end
        )
else:
    # ejecución default al entrar
    utils.overview_info(users_joined)
    utils.entrypoint_view(mails, profiles, mails_date)
