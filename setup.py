from setuptools import setup


version = '0.1.0'


with open("./keystoneauthenticator/__init__.py", 'a') as f:
    f.write("\n__version__ = '{}'\n".format(version))


setup(
    name='jupyterhub-keystoneauthenticator',
    version=version,
    description='Keystone Authenticator for JupyterHub',
    url='https://github.com/jtopjian/jupyterhub-keystoneauthenticator',
    author='Joe Topjian',
    author_email='joe@topjian.net',
    license='3 Clause BSD',
    packages=['keystoneauthenticator'],
    install_requires=[
        'jupyterhub',
        'openstacksdk',
        'tornado',
        'traitlets',
    ]
)
