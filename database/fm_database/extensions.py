# -*- coding: utf-8 -*-
"""Extensions."""
from passlib.context import CryptContext  # type: ignore [import]

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
