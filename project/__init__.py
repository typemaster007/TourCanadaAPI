from flask import *
import os

template_dir = os.path.abspath('./project/view/templates')
static_dir = os.path.abspath('./project/view/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key='abc'

import project.controller
import project.model
