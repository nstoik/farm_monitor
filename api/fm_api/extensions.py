# -*- coding: utf-8 -*-
"""Extensions module.

Each extension is initialized in the app factory located
in app.py.
"""
from flask_cors import CORS  # type: ignore
from flask_jwt_extended import JWTManager
from flask_smorest import Api

cors = CORS()
jwt = JWTManager()
smorest_api = Api()
