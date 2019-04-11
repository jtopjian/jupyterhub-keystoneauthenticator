# keystoneauthenticator

Authenticate to JupyterHub using OpenStack Keystone

## Installation ##

You can install it from pip with:

```
pip install git+https://github.com/jtopjian/jupyterhub-keystoneauthenticator
pip3 install git+https://github.com/jtopjian/jupyterhub-keystoneauthenticator
```

## Usage ##

You can enable this authenticator with the following lines in your
`jupyter_config.py`:

```python
c.JupyterHub.authenticator_class = 'keystoneauthenticator.KeystoneAuthenticator'
```

> Note: This will only work if the user is part of a project with the same name
> as their username (ie a personal project). For example, the user "jdoe" is also
> part of a project called "jdoe".

### Required configuration ###

At minimum, the following two configuration options must be set before
the Keystone Authenticator can be used:


#### `KeystoneAuthenticator.auth_url` ####

The Auth URL of your Keystone service. ex: `https://keystone.example.com:5000/v3`

```python
c.KeystoneAuthenticator.auth_url = 'https://keystone.example.com:5000/v3'
```

### Optional configuration ###

#### `KeystoneAuthenticator.valid_role` ####

The name of a role that the user must have on their personal project
in order to access the JupyterHub environment.

```python
c.KeystoneAuthenticator.valid_role = 'jupyterhub_user'
```

## Compatibility ##

This has been tested against OpenStack Keystone 11 (Ocata) and JupyterHub
0.9.6 running Python 3.6. Verifications of this code working well with
other setups are welcome, as are bug reports and patches.


## Configuration note on local user creation

Currently, local user creation by the KeystoneAuthenticator is unsupported as
this is insecure since there's no cleanup method for these created users. As a
result, users who are disabled in Keystone will have access to this for far longer.

For now, you must use a different type of Spawner.

## Credits

The [LDAPAuthenticator](https://github.com/jupyterhub/ldapauthenticator) was
used as a template for this.
