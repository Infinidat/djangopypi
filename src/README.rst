DjangoPyPI
==========

DjangoPyPI is a Django application that provides a re-implementation of the
`Python Package Index <http://pypi.python.org>`_.

Installation
------------

Path
____

The first step is to get ``djangopypi`` into your Python path.

Buildout
++++++++

Simply add ``djangopypi`` to your list of ``eggs`` and run buildout again it
should downloaded and installed properly.

EasyInstall/Setuptools
++++++++++++++++++++++

If you have setuptools installed, you can use ``easy_install djangopypi``

Manual
++++++

Download and unpack the source then run::

    $ python setup.py install

Django Settings
_______________

Add ``djangopypi`` to your ``INSTALLED_APPS`` setting and run ``syncdb`` again
to get the database tables [#]_.

Then add an include in your url config for ``djangopypi.urls``::

    urlpatterns = patterns("",
        ...
        url(r'', include("djangopypi.urls"))
    )

This will make the repository interface be accessible at ``/pypi/``.



Uploading to your PyPI
----------------------

Assuming you are running your Django site locally for now, add the following to
your ``~/.pypirc`` file::

    [distutils]
    index-servers =
        pypi
        local

    [pypi]
    username:user
    password:secret

    [local]
    username:user
    password:secret
    repository:http://localhost:8000/pypi/

Uploading a package: Python >=2.6
_________________________________

To push the package to the local pypi::

    $ python setup.py register -r local sdist upload -r local


Uploading a package: Python <2.6
________________________________

If you don't have Python 2.6 please run the command below to install the
backport of the extension for multiple repositories::

     $ easy_install -U collective.dist

Instead of using register and dist command, you can use ``mregister`` and
``mupload`` which are a backport of python 2.6 register and upload commands
that supports multiple servers.

To push the package to the local pypi::

    $ python setup.py mregister -r local sdist mupload -r local

