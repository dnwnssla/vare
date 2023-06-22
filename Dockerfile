FROM registry.access.redhat.com/ubi8/python-311:1-8.1686736783

RUN git clone https://github.com/dnwnssla/vare.git
RUN pip install flask \ pip install mysqlclient \ pip install sqlalchemy \ pip install Flask-Migrate

EXPOSE 5000
WORKDIR vare/proj/
CMD [ "python", "start_flask.py" ]
