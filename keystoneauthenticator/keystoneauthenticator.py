import re
import os

from jupyterhub.auth import Authenticator
from tornado import gen
from traitlets import Unicode, Int, Bool, List, Union

import openstack


class KeystoneAuthenticator(Authenticator):
    auth_url = Unicode(
        config=True,
        help="""
        The Auth URL to your OpenStack environment.
        """
    )

    valid_role = Unicode(
        config=True,
        help="""
        A role the user must have to be able to access the Hub.
        """
    )

    valid_username_regex = Unicode(
        r'^[a-z][.a-z0-9-@]+$',
        config=True,
        help="""
        Regex for validating usernames - those that do not match this regex will be rejected.
        """
    )

    @gen.coroutine
    def authenticate(self, handler, data):
        username = data['username']
        password = data['password']
        auth_url = self.auth_url
        valid_role = self.valid_role

        # Protect against invalid usernames.
        if not re.match(self.valid_username_regex, username):
            self.log.warn(
                'username:%s Illegal characters in username, must match regex %s',
                username, self.valid_username_regex
            )
            return None

        # No empty passwords!
        if password is None or password.strip() == '':
            self.log.warn('username:%s Login denied for blank password', username)
            return None

	# Try to authenticate
        try:
            conn = openstack.connect(
                    auth_url=auth_url,
                    project_name=username,
                    username=username,
                    password=password,
                    domain_id="default",
            )

            conn.authorize()

            if valid_role != "":
                for r in conn.identity.roles():
                    if r.location.project.name == username and r.name == valid_role:
                        return username
                self.log.warn("username:%s Login denied for not being part of %s", username, valid_role)
                return None

            return username
        except Exception as e:
            print(e)
            self.log.warn("username:%s Failed to authenticate: %s", username, e)
            return None



if __name__ == "__main__":
    import getpass
    c = KeystoneAuthenticator()
    c.auth_url = os.environ['AUTH_URL']
    if 'VALID_ROLE' in os.environ:
        c.valid_role = os.environ['VALID_ROLE']

    username = input('Username: ')
    passwd = getpass.getpass()
    data = dict(username=username,password=passwd)
    rs=c.authenticate(None,data)
    print(rs.result())
