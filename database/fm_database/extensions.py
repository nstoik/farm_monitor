# -*- coding: utf-8 -*-
"""Extensions."""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
