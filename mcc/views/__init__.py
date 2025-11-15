from .. import app, crud, util
from flask import Flask, request, render_template, session

from . import admin
from . import technician
from . import auth
from . import instore