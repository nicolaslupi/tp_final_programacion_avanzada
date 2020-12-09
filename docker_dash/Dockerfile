FROM python:3.7.3

WORKDIR /dashboard

COPY req.txt utils.py dash_app.py ./dashboard/

RUN pip install -r ./dashboard/req.txt

ENTRYPOINT ["streamlit", "run", "./dashboard/dash_app.py", "--port=8231", "--ip=0.0.0.0", "--allow-root"]
