#!/usr/bin/env python3

import logging

from app import Config
from ldaploginprovider import LDAPLoginProvider

LOGFORMAT = "[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)"
logging.basicConfig(level=logging.INFO, format=LOGFORMAT)

config = Config()
logging.info("Building ldap_provider")
ldap_provider = LDAPLoginProvider(config.ldap_server, config.ldap_base_dn, config.ldap_user_prefix)
ldap_provider.build_connection()

logging.info("Attempting to login")
user = ldap_provider.login(config.known_user, config.known_pass)
logging.info("Login: " + str(user.__dict__))
