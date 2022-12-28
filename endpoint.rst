.. _endpoints:

##################
 Remote Endpoints
##################

**********
 Overview
**********

The ``remote`` command group allows users to manage the service
endpoints {Project} will interact with for many common command
flows. This includes managing credentials for image storage services
and key servers used to locate public keys for SIF
image verification. Currently, there are three main types of remote
endpoints managed by this command group: `Library API Registries
<https://singularityhub.github.io/library-api/#/?id=library-api>`_,
OCI registries and keyservers.

You are most likely interacting with remote endpoints on a regular basis using
various {Project} commands:
`pull
<cli/{command}_pull.html>`_,
`push
<cli/{command}_push.html>`_,
`build
<cli/{command}_build.html>`_,
`key
<cli/{command}_key.html>`_,
`search
<cli/{command}_search.html>`_,
`verify
<cli/{command}_verify.html>`_,
`exec
<cli/{command}_exec.html>`_,
`shell
<cli/{command}_shell.html>`_,
`run
<cli/{command}_run.html>`_,
or `instance
<cli/{command}_instance.html>`_.

.. _sec:managing-remote-endpoints:

***************************
 Managing Remote Endpoints
***************************

A fresh installation of {Project} is configured with the ``DefaultRemote``,
which does not support the Library API as it is only configured with a
functioning key server, ``https://keys.openpgp.org``. Users or administrators
should configure one of the Library API implementations listed `here
<https://singularityhub.github.io/library-api/#/?id=library-api>`_ if they would
like to use a Library API registry.

Users can setup and switch between multiple remote endpoints, which are
stored in their ``~/.{command}/remote.yaml`` file. Alternatively,
remote endpoints can be set system-wide by an administrator.

Generally, users and administrators should manage remote endpoints using
the ``{command} remote`` command, and avoid editing ``remote.yaml``
configuration files directly.

List Remotes
============

To ``list`` existing remote endpoints, run this:

.. code::

   $ {command} remote list

   Cloud Services Endpoints
   ========================

   NAME           URI                  ACTIVE  GLOBAL  EXCLUSIVE
   DefaultRemote  cloud.apptainer.org  YES     YES     NO

   Keyservers
   ==========

   URI                       GLOBAL  INSECURE  ORDER
   https://keys.openpgp.org  YES     NO        1*

The ``YES`` in the ``ACTIVE`` column for ``DefaultRemote`` shows that this
is the current default remote endpoint.

.. _remote_add_and_login:

Add & Login To Remotes
======================

To ``add`` a remote endpoint (for the current user only):

.. code::

   $ {command} remote add <remote_name> <remote_uri>

For example, if you have an installation of {Project} enterprise
hosted at enterprise.example.com:

.. code::

   $ {command} remote add myremote https://enterprise.example.com

   INFO:    Remote "myremote" added.
   INFO:    Authenticating with remote: myremote
   Generate an API Key at https://enterprise.example.com/auth/tokens, and paste here:
   API Key:

You will be prompted to setup an API key as the remote is added. The web
address needed to do this will always be given.

To ``add`` a global remote endpoint (available to all users on the
system) an administrative user should run:

.. code::

   $ sudo {command} remote add --global <remote_name> <remote_uri>

   # example..

   $ sudo {command} remote add --global company-remote https://enterprise.example.com
   INFO:    Remote "company-remote" added.
   INFO:    Global option detected. Will not automatically log into remote.

.. note::

   Global remote configurations can only be modified by the root user
   and are stored in the ``etc/{command}/remote.yaml`` file, at the
   {Project} installation location.

To ``login`` to a remote, for the first time or if your token expires or
was revoked:

.. code:: console

   # Login to the default remote endpoint
   $ {command} remote login

   # Login to another remote endpoint
   $ {command} remote login <remote_name>

   # example...
   $ {command} remote login myremote
   {command} remote login myremote
   INFO:    Authenticating with remote: myremote
   Generate an API Key at https://enterprise.example.com/auth/tokens, and paste here:
   API Key:
   INFO:    API Key Verified!

If you ``login`` to a remote that you already have a valid token for,
you will be prompted, and the new token will be verified, before it
replaces your existing credential. If you enter an incorrect token your
existing token will not be replaced:

.. code:: console

   $ {command} remote login
   An access token is already set for this remote. Replace it? [N/y]y
   Generate an access token at https://enterprise.example.com/auth/tokens, and paste it here.
   Token entered will be hidden for security.
   Access Token:
   FATAL:   while verifying token: error response from server: Invalid Credentials

   # Previous token is still in place

.. note::

   It is important for users to be aware that the login command will
   store the supplied credentials or tokens unencrypted in your home
   directory.


Remove Remotes
==============

To ``remove`` an endpoint:

.. code::

   $ {command} remote remove <remote_name>

Use the ``--global`` option as the root user to remove a global
endpoint:

.. code::

   $ sudo {command} remote remove --global <remote_name>


Set the Default Remote
======================

A remote endpoint can be set as the default to use with commands such as
``push``, ``pull`` etc. via ``remote use``:

.. code::

   $ {command} remote use <remote_name>

The default remote shows up with a ``YES`` under the ``ACTIVE`` column
in the output of ``remote list``:

.. code::

   $ {command} remote list
   Cloud Services Endpoints
   ========================

   NAME            URI                     ACTIVE  GLOBAL  EXCLUSIVE
   DefaultRemote   cloud.apptainer.org     YES     YES     NO
   company-remote  enterprise.example.com  NO      YES     NO
   myremote        enterprise.example.com  NO      NO      NO

   Keyservers
   ==========

   URI                       GLOBAL  INSECURE  ORDER
   https://keys.openpgp.org  YES     NO        1*

   * Active cloud services keyserver

   $ {command} remote use myremote
   INFO:    Remote "myremote" now in use.

   $ {command} remote list
   Cloud Services Endpoints
   ========================

   NAME            URI                     ACTIVE  GLOBAL  EXCLUSIVE
   DefaultRemote   cloud.apptainer.org     NO      YES     NO
   company-remote  enterprise.example.com  NO      YES     NO
   myremote        enterprise.example.com  YES     NO      NO

   Keyservers
   ==========

   URI                       GLOBAL  INSECURE  ORDER
   https://keys.example.com  YES     NO        1*

   * Active cloud services keyserver

An administrator can make a
remote the only usable remote for the system by using the
``--exclusive`` flag:

.. code::

   $ sudo {command} remote use --exclusive company-remote
   INFO:    Remote "company-remote" now in use.
   $ {command} remote list
   Cloud Services Endpoints
   ========================

   NAME            URI                     ACTIVE  GLOBAL  EXCLUSIVE
   DefaultRemote   cloud.apptainer.org     NO      YES     NO
   company-remote  enterprise.example.com  YES     YES     YES
   myremote        enterprise.example.com  NO      NO      NO

   Keyservers
   ==========

   URI                       GLOBAL  INSECURE  ORDER
   https://keys.example.com  YES     NO        1*

   * Active cloud services keyserver

This, in turn, prevents users from changing the remote they use:

.. code::

   $ {command} remote use myremote
   FATAL:   could not use myremote: remote company-remote has been set exclusive by the system administrator

If you do not want to switch remote with ``remote use`` you can:

-  Make ``push`` and ``pull`` use an alternative library server with the
   ``--library`` option.
-  Make ``keys`` use an alternative keyserver with the ``-url`` option.

.. _no_default_remote:
.. _restoring_pre-{command}_library_behavior:

Restoring pre-{Project} library behavior
========================================

{Project}'s default remote endpoint configures only a public key
server, it does not support the ``library://`` protocol.
Formerly the default was set to point to Sylabs servers, but the
read/write support of the ``oras://`` protocol by for example the
:ref:`GitHub Container Registry <github_container_registry>`
makes it unnecessary.
The remote endpoint was also formerly used for builds using the 
build ``--remote`` option, but {Project} does not support that.
Instead, it supports :ref:`unprivileged local builds <build>`.

If you would still like to have the previous default,
these are the commands to restore the library
behavior from before {Project}, where using the ``library://`` URI would
download from the Sylabs Cloud anonymously:

.. code::

   $ {command} remote add --no-login SylabsCloud cloud.sycloud.io
   INFO:    Remote "SylabsCloud" added.
   $ {command} remote use SylabsCloud
   INFO:    Remote "SylabsCloud" now in use.
   $ {command} remote list
   Cloud Services Endpoints
   ========================

   NAME           URI                  ACTIVE  GLOBAL  EXCLUSIVE
   DefaultRemote  cloud.apptainer.org  NO      YES     NO
   SylabsCloud    cloud.sycloud.io     YES     NO      NO

   Keyservers
   ==========

   URI                                 GLOBAL  INSECURE  ORDER
   https://keys.production.sycloud.io  YES     NO        1*

   * Active cloud services keyserver

To set the defaults system-wide see the corresponding section in the
`admin guide
<{admindocs}/configfiles.html#restoring-pre-{command}-library-behavior>`_.

**************************
 Keyserver Configurations
**************************

By default, {Project} will use the keyserver correlated to the
active cloud service endpoint. This behavior can be changed or
supplemented via the ``add-keyserver`` and ``remove-keyserver``
commands. These commands allow an administrator to create a global list
of key servers used to verify container signatures by default, where
``order 1`` is the first in the list. Other operations performed by
{Project} that reach out to a keyserver will only use the first
entry, or ``order 1``, keyserver.

When we list our default remotes, we can see that the default keyserver
is ``https://keys.openpgp.org`` and the asterisk next to its order
indicates that it is the keyserver associated to the current remote
endpoint. We can also see the ``INSECURE`` column indicating that
{Project} will use TLS when communicating with the keyserver.

.. code::

   $ {command} remote list
   Cloud Services Endpoints
   ========================

   NAME           URI                  ACTIVE  GLOBAL  EXCLUSIVE
   DefaultRemote  cloud.apptainer.org  YES     YES     NO

   Keyservers
   ==========

   URI                       GLOBAL  INSECURE  ORDER
   https://keys.openpgp.org  YES     NO        1*

   * Active cloud services keyserver

We can add a key server to list of keyservers with:

.. code::

   $ sudo {command} remote add-keyserver https://pgp.example.com
   $ {command} remote list
   Cloud Services Endpoints
   ========================

   NAME           URI                  ACTIVE  GLOBAL  EXCLUSIVE
   DefaultRemote  cloud.apptainer.org  YES     YES     NO

   Keyservers
   ==========

   URI                       GLOBAL  INSECURE  ORDER
   https://keys.openpgp.org  YES     NO        1*
   https://pgp.example.com   YES     NO        2

   * Active cloud services keyserver

Here we can see that the ``https://pgp.example.com`` keyserver was
appended to our list. If we would like to specify the order in the list
that this key is placed, we can use the ``--order`` flag:

.. code::

   $ sudo {command} remote add-keyserver --order 1 https://pgp.example.com
   $ {command} remote list
   Cloud Services Endpoints
   ========================

   NAME           URI                  ACTIVE  GLOBAL  EXCLUSIVE
   DefaultRemote  cloud.apptainer.org  YES     YES     NO

   Keyservers
   ==========

   URI                      GLOBAL  INSECURE  ORDER
   https://pgp.example.com  YES     NO        1
   https://keys.openpgp.org YES     NO        2*

   * Active cloud services keyserver

Since we specified ``--order 1``, the ``https://pgp.example.com``
keyserver was placed as the first entry in the list and the default
keyserver was moved to second in the list. With the keyserver
configuration above, all image default image verification performed by
{Project} will first reach out to ``https://pgp.example.com`` and
then to ``https://keys.openpgp.org`` when searching for public keys.

If a keyserver requires authentication before usage, users can login
before using it:

.. code::

   $ {command} remote login --username ian https://pgp.example.com
   Password (or token when username is empty):
   INFO:    Token stored in /home/ian/.{command}/remote.yaml

Now we can see that ``https://pgp.example.com`` is logged in:

.. code::

   $ {command} remote list
   Cloud Services Endpoints
   ========================

   NAME           URI                  ACTIVE  GLOBAL  EXCLUSIVE
   DefaultRemote  cloud.apptainer.org  YES     YES     NO

   Keyservers
   ==========

   URI                       GLOBAL  INSECURE  ORDER
   https://pgp.example.com   YES     NO        1
   https://keys.openpgp.org  YES     NO        2*

   * Active cloud services keyserver

   Authenticated Logins
   =================================

   URI                     INSECURE
   https://pgp.example.com NO

.. note::

   It is important for users to be aware that the login command will
   store the supplied credentials or tokens unencrypted in your home
   directory.

.. _sec:managing_oci_registries:

*************************
 Managing OCI Registries
*************************

It is common for users of {Project} to use OCI registries as sources
for their container images. Some registries require credentials to
access certain images or the registry itself. Previously, the only
methods in {Project} to supply credentials to registries were to
supply credentials for each command or set environment variables for a
single registry.

{Project} supports the ability for users to supply credentials
on a per registry basis with the ``remote`` command group.

Users can login to an oci registry with the ``remote login`` command by
specifying a ``docker://`` prefix to the registry hostname:

.. code::

   $ {command} remote login --username ian docker://docker.io
   Password (or token when username is empty):
   INFO:    Token stored in /home/ian/.{command}/remote.yaml

   $ {command} remote list
   Cloud Services Endpoints
   ========================

   NAME           URI                  ACTIVE  GLOBAL  EXCLUSIVE
   DefaultRemote  cloud.apptainer.org  YES     YES     NO

   Keyservers
   ==========

   URI                       GLOBAL  INSECURE  ORDER
   https://keys.openpgp.org  YES     NO        1*

   * Active cloud services keyserver

   Authenticated Logins
   =================================

   URI                 INSECURE
   docker://docker.io  NO

Now we can see that ``docker://docker.io`` shows up under
``Authenticated Logins`` and {Project} will automatically supply the
configured credentials when interacting with DockerHub. We can also see
the ``INSECURE`` column indicating that {Project} will use TLS when
communicating with the registry.

We can login to multiple OCI registries at the same time:

.. code::

   $ {command} remote login --username ian docker://registry.example.com
   Password (or token when username is empty):
   INFO:    Token stored in /home/ian/.{command}/remote.yaml

   $ {command} remote list
   Cloud Services Endpoints
   ========================

   NAME           URI                  ACTIVE  GLOBAL  EXCLUSIVE
   DefaultRemote  cloud.apptainer.org  YES     YES     NO

   Keyservers
   ==========

   URI                       GLOBAL  INSECURE  ORDER
   https://keys.openpgp.org  YES     NO        1*

   * Active cloud services keyserver

   Authenticated Logins
   =================================

   URI                            INSECURE
   docker://docker.io             NO
   docker://registry.example.com  NO

{Project} will supply the correct credentials for the registry based
off of the hostname when using the following commands with a
``docker://`` or ``oras://`` URI:
`pull
<cli/{command}_pull.html>`_,
`push
<cli/{command}_push.html>`_,
`build
<cli/{command}_build.html>`_,
`exec
<cli/{command}_exec.html>`_,
`shell
<cli/{command}_shell.html>`_,
`run
<cli/{command}_run.html>`_,
or `instance
<cli/{command}_instance.html>`_.

.. note::

   It is important for users to be aware that the login command will
   store the supplied credentials or tokens unencrypted in your home
   directory.
