import streamlit as st
import utils

mails, profiles, users = utils.extract_data("perm")
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

date_end = st.sidebar.date_input(
    "Fecha de fin (hasta)",
    max_date
)
if date_end > max_date:
    st.error(f"Error: La fecha máxima es {max_date}")

if st.sidebar.button("Aplicar cambios"):
    if show_general == "Mostrar":
        st.subheader("Información general sobre API")
        joined_by_date = utils.overview_info(users)
        st.plotly_chart(joined_by_date)
    elif show_general == "No Mostrar":
        pass
    initial = False
    if len(user_choice) == 0:
        st.write("vistazo general")
        fig = utils.general_view(mails, profiles)
        st.subheader("Histograma de Largo de Mails")
        st.plotly_chart(fig)
    else:
        st.write("usuarios seleccionados")
        st.write(f"Mostrando resultados para usuario {user_choice}")
        fig = utils.user_view(mails, profiles, user_choice)
        st.plotly_chart(fig)
else:
    # gráficos default al entrar
    st.subheader("Información general sobre API")
    joined_by_date = utils.overview_info(users)
    st.plotly_chart(joined_by_date)
    fig = utils.general_view(mails, profiles)
    st.subheader("Histograma de Largo de Mails")
    st.plotly_chart(fig)
