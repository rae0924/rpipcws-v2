from flask import Flask

app = Flask(__name__)

from rpipcws_v2 import main