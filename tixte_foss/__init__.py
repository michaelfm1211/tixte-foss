from config import Config
from flask import Flask
from os import environ

if environ['APP_SETTINGS'] == None:
    print("$APP_SETTINGS is not defined. Ensure it is set to config.ProductionConfig, config.StagingConfig, config.DevelopmentConfig, or config.TestingConfig")

app = Flask(__name__)
app.config.from_object(environ['APP_SETTINGS'])

from tixte_foss import routes  # nopep8

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=environ['PORT'])
