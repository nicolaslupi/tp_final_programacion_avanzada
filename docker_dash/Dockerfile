FROM python:3.7.3

EXPOSE 8501

WORKDIR /dashboard

COPY req.txt utils.py dash_app.py ./dashboard/

RUN pip install -r ./dashboard/req.txt

COPY . .

CMD streamlit run dash_app.py

#ENTRYPOINT ["streamlit", "run", "./dashboard/dash_app.py", "--port=8231", "--ip=0.0.0.0", "--allow-root"]
