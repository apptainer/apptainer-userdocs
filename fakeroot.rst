.. _fakeroot:

################
Fakeroot feature
################

********
Overview
********

The fakeroot feature allows an unprivileged user to run a container with
the appearance of running as root.
{Project} does this in different ways, depending on what is available on
the host:

#. If the host is set up to map the current user via ``/etc/subuid`` and
   ``/etc/subgid`` mapping files, {Project} will use that method first.
   This is also commonly referred to as "rootless mode" and is the
   method used for example by Podman.
   This mode requires user namespaces to be enabled.
   It is the most complete emulation but it requires administrator setup
   as described in the `admin guide
   <{admindocs}/user_namespace.html#rootless-fakeroot-feature>`__.
   It also requires some elevated privilege assistance on the host as described
   there, which means that it will not be able to run nested inside another
   container that disallows elevating privileges, as {Project} does.
   Those elevated privileges on the host come from either a setuid-root
   install of {Project} or via the host ``newuidmap`` and ``newgidmap``
   commands.
#. Otherwise if user namespaces are available without ``/etc/subuid``
   and ``/etc/subguid`` mapping files, {Project} will map only
   the root user id to the original unprivileged user.
   This method is sometimes called a "root-mapped user namespace".
   Since this method is not as complete an emulation as rootless mode,
   an INFO message showing it is happening is displayed.
#. If the "fakeroot" command is available on the host, {Project} will
   use it in addition to a root-mapped user namespace.
   This command fakes root privileges on file manipulation, telling
   programs that operations that would succeed as root have succeeded
   even though they really haven't.
   This is useful for avoiding errors when building containers or when
   adding packages to a writable container, because many package
   installations attempt to do additional setup that only works as root.
   When the fakeroot command is used, an INFO message is displayed.
   The combination of a root-mapped user namespace with the fakeroot command
   allows most package installations to work, but the fakeroot command is
   bound in from the host so if the host libc library is of a very
   different vintage than the corresponding container the
   fakeroot command can fail with errors about a missing GLIBC version.
   If that situation happens the easiest solution is to first run a
   container with an operating system matching the target glibc version,
   `install {Project} unprivileged
   <{admindocs}/installation.html#install-from-pre-built-packages>`__
   there, and do the build nested inside that container.
#. If user namespaces are not available but {Project} has been installed
   with setuid-root and also the "fakeroot" command is available, then
   the fakeroot command will be run by itself.
   This allows some package installations to succeed but others will
   still fail; it is not as complete an emulation because the
   root-mapped user namespace causes the kernel to allow bypassing
   restrictions on files that are actually owned by the original user
   on the host, things that the fakeroot command cannot do by itself.
   Also, this mode requires the container image to be a sandbox.

As mentioned above, the "rootless" fakeroot mode is the most complete
emulation.  That mode has almost the same administrative rights as root
but only **inside the container** and the **requested namespaces**,
which means that this user:

   -  can set different user/group ownership for files or directories
      they own
   -  can change user/group identity with su/sudo commands when starting
      as the fake root user

In addition, the first three modes above may have full privileges inside
the requested network namespace (see below).

*********************
Restrictions/security
*********************

Filesystem
==========

A "fake root" user can never access or modify files and directories for
which they don't already have access or rights on the host filesystem,
so a "fake root" user won't be able to access root-only host files
such as ``/etc/shadow`` or the host ``/root`` directory.

Additionally, all files or directories created by the "fake root"
user are owned by ``root:root`` inside the container but as ``user:group``
outside of the container.

Let's consider the following example.  In this case "user" is authorized
to use the rootless mode fakeroot feature and can use 65536
UIDs starting at 131072 (same thing for GIDs).

+----------------------+-----------------------+
| UID inside container | UID outside container |
+======================+=======================+
| 0 (root)             | 1000 (user)           |
+----------------------+-----------------------+
| 1 (daemon)           | 131072 (non-existent) |
+----------------------+-----------------------+
| 2 (bin)              | 131073 (non-existent) |
+----------------------+-----------------------+
| ...                  | ...                   |
+----------------------+-----------------------+
| 65536                | 196607                |
+----------------------+-----------------------+

This means that if the "fake root" user creates a file under a ``bin``
user in the container, this file will be owned by ``131073:131073``
outside of the container. The responsibility relies on the administrator to
ensure that there is no overlap with any user's UID/GID on the
system.

Network
=======

Normally the kernel prevents unprivileged users from connecting to
ports below 1024, and the ``ping`` command requires a setcap capability in
order to work on the network.
{Project} allows overriding these restrictions when all of the following
conditions are true:

#. {Project} is installed with suid mode enabled
#. Network namespaces are enabled
#. The ``-net`` option is used
#. The user is listed in ``/etc/subuid`` and so can use rootless mode
#. The ``--fakeroot`` option is used

If those conditions are true, the user has full network privileges in a
dedicated container network. Inside the container network they can bind
on privileged ports below 1024, use ping, manage firewall rules, listen
to traffic, etc. Anything done in this dedicated network won't affect
the host network.
The ports inside the dedicated network can be mapped to other ports
on the host with the ``--network-args="portmap"`` option.

.. note::

   Of course an unprivileged user can not map host ports below
   1024 by using for example: ``--network-args="portmap=80:80/tcp"``

*****
Usage
*****

You can work as a fake root user inside a container by using the
``--fakeroot`` or ``-f`` option.

The ``--fakeroot`` option is available with the following {command}
commands:

   -  ``shell``
   -  ``exec``
   -  ``run``
   -  ``instance start``
   -  ``build``

The option is automatically implied when doing a build as an
unprivileged user.

.. _build:

Build
=====

Depending on the method of "fake root" used, an unprivileged user can build
an image from a definition file with few restrictions.
Some bootstrap methods that require creation of block devices (like
``/dev/null``) may not always work correctly with "fake root".
With the rootles mode "fake root", {Project} uses seccomp filters
to give programs the illusion that block device creation succeeded.
This appears to work with ``yum`` bootstraps and *may* work with other
bootstrap methods, although ``debootstrap`` is known to not work.

If only the fakeroot command is used for "fake root" mode (because no
user namespaces are available, in suid mode), then building a container
also implies the ``--fix-perms`` option, because otherwise directories
created may not be writable by the creating user.

Examples
========

Build from a definition file:
-----------------------------

(fakeroot is implied)

.. code::

   {command} build /tmp/test.sif /tmp/test.def

Add package to a writable overlay
---------------------------------

.. code::

   mkdir /tmp/test.overlay
   {command} exec --fakeroot --overlay /tmp/test.overlay /tmp/test.sif yum -y install openssh

Ping from container:
--------------------

(when the Network conditions above are met)

.. code::

   {command} exec --fakeroot --net docker://alpine ping -c1 8.8.8.8

HTTP server:
------------

(when the Network conditions above are met)

.. code::

   {command} run --fakeroot --net --network-args="portmap=8080:80/tcp" -w docker://nginx
