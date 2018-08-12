import ldap
import logging

class UserDataModel:
    pass

class LoginProviderInterface:
    def login(self, username, password):
        pass

class LDAPLoginProvider(LoginProviderInterface):
    def __init__(self, ldap_server, ldap_base, ldap_user_prefix):
        self.ldap_user_prefix = ldap_user_prefix
        self.ldap_server = ldap_server
        self.ldap_base = ldap_base
        self.scope = ldap.SCOPE_SUBTREE
        self.conn = None

    def build_connection(self):
        self.conn = ldap.initialize('ldap://%s' % self.ldap_server)
        self.conn.protocol_version = 3
        self.conn.set_option(ldap.OPT_REFERRALS, 0)

    def search(self, username):
        filter = "(&(objectClass=user)(sAMAccountName=" + username + "))"
        logging.info("searching with filter: " + filter)

        attrs = ["*"]
        r = self.conn.search(self.ldap_base, self.scope, filter, attrs)
        logging.info("enumerating results")
        type, user = self.conn.result(r, 60)
        return user

    def login(self, username, password):
        try:
            logging.debug("pre_bind")
            status = self.conn.simple_bind_s(self.ldap_user_prefix + username, password )
            logging.debug("Simple bind: " + str(self.conn) + "status: " + str(status))
            u = self.search(username)
            user = UserDataModel()
            user.displayName = u[0][1]['displayName'][0]
            return user

        except ldap.INVALID_CREDENTIALS, e:
            self.log(e)
            raise ValueError(e)

    def log(self, msg):
        print "LDAPLoginProvider: %s" % msg
