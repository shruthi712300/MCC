# Secret key for flask
FLASK_SECRET_KEY = "3aa9212bcfc423faa94573ffd859c1080a801e8527aaf36733f5a1898a648642"

# Used to generate csrf token
WTF_CSRF_SECRET_KEY = "a8f9dc11ea39fc5bf1a094d8498aa38f4e443fb2a01952cd6388a8020150c502"


SECRET_KEY = "37faa3f775ff80685667be197638aa6fc6247f017c2035572fdb119d091d0098"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1  # user can access the page for 10 days
AUTH_TOKEN_COOKIE_NAME = "_AUTH"


# SQL database constants
DATABASE_NAME = "servicecc"
MYSQL_USER = "karthik"
MYSQL_PASSWORD = "password"
MYSQL_PORT = "localhost:3306"
SQLALCHEMY_DATABASE_URL = (
    f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_PORT}/{DATABASE_NAME}"
)
# create a database login first
"""
# see https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04
CREATE USER 'karthik'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'karthik'@'localhost' WITH GRANT OPTION;
"""
