.. _build-environment:

#################
Build Environment
#################

.. _sec:buildenv:

********
Overview
********

You may wish to customize your build environment by doing things such as
specifying a custom cache directory for images, or sending your Docker
Credentials to the registry endpoint. In this section, we will discuss these and
other topics related to the build environment.

.. _sec:cache:

*************
Cache Folders
*************

{Project} will cache SIF container images generated from remote
sources, and any OCI/docker layers used to create them. The cache is
created at ``$HOME/.{command}/cache`` by default. The location of the
cache can be changed by setting the ``{ENVPREFIX}_CACHEDIR`` environment
variable.

If you run builds as root, using ``sudo``, images will be cached in root's home
directory at ``/root``, rather than your user's home directory. If you have set
the ``{ENVPREFIX}_CACHEDIR`` environment variable, you may use ``sudo``'s ``-E``
option to pass the value of ``{ENVPREFIX}_CACHEDIR`` through to the root user's
environment. This allows you to control where images will be cached even when
running builds under ``sudo``.

.. code::

   $ export {ENVPREFIX}_CACHEDIR=/tmp/user/temporary-cache

   # Running a build under your user account
   $ {command} build --fakeroot myimage.sif mydef.def

   # Running a build with sudo, must use -E to pass env var
   $ sudo -E {command} build myimage.sif mydef.def

If you change the value of ``{ENVPREFIX}_CACHEDIR`` be sure to choose a
location that is:

   -  Unique to you. Permissions are set on the cache so that private images
      cached for one user are not exposed to another. This means that
      {Project} cache directories cannot be shared across users.

   -  Located on a filesystem with sufficient space for the number and size of
      container images you anticipate using.

   -  Located on a filesystem that supports atomic rename, if possible.

.. warning::

   If you are not certain that your ``$HOME`` or ``{ENVPREFIX}_CACHEDIR``
   filesystems support atomic rename, do not run {Project} in parallel using
   remote container URLs. Instead, use ``{command} pull`` to create a local
   SIF image, and then run this SIF image in a parallel step. Alternatively, you
   may use the ``--disable-cache`` option, but this will result in each
   {Project} instance independently fetching the container from the remote
   source, into a temporary location.

Inside the cache location you will find separate directories for the
different kinds of data that are cached:

.. code::

   $HOME/.{command}/cache/blob
   $HOME/.{command}/cache/library
   $HOME/.{command}/cache/net
   $HOME/.{command}/cache/oci-tmp
   $HOME/.{command}/cache/shub

You can safely delete these directories, or content within them.
{Project} will re-create any directories and data that are needed in
future runs.

You should not add any additional files, or modify files in the cache, as this
may cause checksum / integrity errors when you run or build containers. If you
experience problems use, ``{command} cache clean`` to reset the cache to a
clean, empty state.

BoltDB Corruption Errors
========================

The library that {Project} uses to retrieve and cache Docker/OCI
layers keeps track of them using a single-file database. If your home
directory is on a network filesystem which experiences interruptions, or
you run out of storage, it is possible for this database to become
inconsistent.

If you observe error messages that mention `github.com/etcd-io/bbolt` when
trying to run {Project}, then you should remove the database file:

.. code::

   rm ~/.local/share/containers/cache/blob-info-cache-v1.boltdb

**************
Cache commands
**************

The ``cache`` command for {Project} allows you to view and clean up your
cache, without needing to manually inspect the cache directories.

.. note::

   If you have built images as root, directly or via ``sudo``, the default cache
   location for those builds is ``/root/.{command}``. You will need to use
   ``sudo`` when running ``cache clean`` or ``cache list`` to manage these cache
   entries.

Listing the Cache
=================

To view a summary of cache usage, use ``{command} cache list``:

.. code::

   $ {command} cache list
   There are 4 container file(s) using 59.45 MB and 23 oci blob file(s) using 379.10 MB of space
   Total space used: 438.55 MB

To view more detailed information, use ``{command} cache list -v``:

.. code::

   $ {command} cache list -v
   NAME                     DATE CREATED           SIZE             TYPE
   0ed5a98249068fe0592edb   2020-05-27 12:57:22    192.21 MB        blob
   1d9cd1b99a7eca56d8f2be   2020-05-28 15:19:07    0.35 kB          blob
   219c332183ec3800bdfda4   2020-05-28 12:22:13    0.35 kB          blob
   2adae3950d4d0f11875568   2020-05-27 12:57:16    51.83 MB         blob
   376057ac6fa17f65688c56   2020-05-27 12:57:12    50.39 MB         blob
   496548a8c952b37bdf149a   2020-05-27 12:57:14    10.00 MB         blob
   5a63a0a859d859478f3046   2020-05-27 12:57:13    7.81 MB          blob
   5efaeecfa72afde779c946   2020-05-27 12:57:25    0.23 kB          blob
   6154df8ff9882934dc5bf2   2020-05-27 08:37:22    0.85 kB          blob
   70d0b3967cd8abe96c9719   2020-05-27 12:57:24    26.61 MB         blob
   8f5af4048c33630473b396   2020-05-28 15:19:07    0.57 kB          blob
   95c3f3755f37380edb2f8f   2020-05-28 14:07:20    2.48 kB          blob
   96878229af8adf91bcbf11   2020-05-28 14:07:20    0.81 kB          blob
   af88fdb253aac46693de78   2020-05-28 12:22:13    0.58 kB          blob
   bb94ffe723890b4d62d742   2020-05-27 12:57:23    6.15 MB          blob
   c080bf936f6a1fdd2045e3   2020-05-27 12:57:25    1.61 kB          blob
   cbdbe7a5bc2a134ca8ec91   2020-05-28 12:22:13    2.81 MB          blob
   d51af753c3d3a984351448   2020-05-27 08:37:21    28.56 MB         blob
   d9cbbca60e5f0fc028b13c   2020-05-28 15:19:06    760.85 kB        blob
   db8816f445487e48e1d614   2020-05-27 12:57:25    1.93 MB          blob
   fc878cd0a91c7bece56f66   2020-05-27 08:37:22    32.30 kB         blob
   fee5db0ff82f7aa5ace634   2020-05-27 08:37:22    0.16 kB          blob
   ff110406d51ca9ea722112   2020-05-27 12:57:25    7.78 kB          blob
   sha256.02ee8bf9dc335c2   2020-05-29 13:45:14    28.11 MB         library
   sha256.5111f59250ac94f   2020-05-28 13:14:39    782.34 kB        library
   747d2dbbaaee995098c979   2020-05-28 14:07:22    27.77 MB         oci-tmp
   9a839e63dad54c3a6d1834   2020-05-28 12:22:13    2.78 MB          oci-tmp

   There are 4 container file(s) using 59.45 MB and 23 oci blob file(s) using 379.10 MB of space
   Total space used: 438.55 MB

All cache entries are named using a content hash, so that identical
layers or images that are pulled from different URIs do not result in
duplication within the cache.

Entries marked ``blob`` are OCI/docker layers and manifests, which are used to
create SIF format images in the ``oci-tmp`` cache. Other caches are named for
the source of the image, e.g. ``library`` or ``oras``.

You can limit the cache list to a specific cache type with the ``--type`` /
``-t`` option.

Cleaning the Cache
==================

To reclaim space used by the {Project} cache, use ``{command}
cache clean``.

By default, ``{command} cache clean`` will remove all cache entries,
after asking you to confirm:

.. code::

   $ {command} cache clean
   This will delete everything in your cache (containers from all sources and OCI blobs).
   Hint: You can see exactly what would be deleted by canceling and using the --dry-run option.
   Do you want to continue? [N/y] n

Use the ``--dry-run`` / ``-n`` option to see the files that would be
deleted, or the ``--force`` / ``-f`` option to clean without asking for
confirmation.

If you want to leave your most recent cached images in place, but remove
images that were cached longer ago, you can use the ``--days`` / ``-d``
option. E.g. to clean cache entries older than 30 days:

.. code::

   $ {command} cache clean --days 30

To remove only a specific kind of cache entry, e.g. only library images,
use the ``--type`` / ``-T`` option:

.. code::

   $ {command} cache clean --type library

.. _sec:temporaryfolders:

*****************
Temporary Folders
*****************

When building a container, or pulling/running {aProject} container from a
Docker/OCI source, a temporary working space is required. The container is
constructed in this temporary space before being packaged into {aProject}
SIF image.

The location for temporary directories defaults to ``/tmp``.
However, {Project} will respect the environment variable ``TMPDIR``, and
both of these locations can be overridden by setting the environment
variable ``{ENVPREFIX}_TMPDIR``.

The temporary directory used during a build must be on a filesystem that has
enough space to hold the entire container image, uncompressed, including any
temporary files that are created and later removed in the course of the build.
You may therefore need to set ``{ENVPREFIX}_TMPDIR`` when building a large
container on a system which has a small ``/tmp`` filesystem.

Remember to use ``-E`` option to pass the value of ``{ENVPREFIX}_TMPDIR``
through to root's environment when executing the ``build`` command with
``sudo``.

.. warning::

   Many modern Linux distributions use an in-memory ``tmpfs`` filesystem
   for ``/tmp`` when installed on a computer with a sufficient amount of
   RAM. This may limit the size of container you can build, as temporary
   directories under ``/tmp`` share RAM with runniing programs etc. A
   ``tmpfs`` also uses default mount options that can interfere with
   some container builds.

   If you experience problems, set ``{ENVPREFIX}_TMPDIR`` to a disk location, or
   disable the ``tmpfs`` ``/tmp`` mount on your system.

********************
Encrypted Containers
********************

With {Project} it is possible to build and run encrypted
containers. The containers are decrypted at runtime entirely in memory,
meaning that no intermediate decrypted data is ever present on disk. See
:ref:`encrypted containers <encryption>` for more details.

*********************
Environment Variables
*********************

You can set environment variables on the host to influence the behaviour of a
build. Note that environment variables are not passed into the build itself, and
cannot be accessed in the ``%post`` section of a definition file. To pass values
into a build, use the :ref:`templating / build-args support <sec:templating>`.

Environment variables that control a build are generally associated with an
equivalent CLI option. The order of precedence is:

#. If a flag is represented by both a CLI option and an environment variable,
   and both are set, the CLI option will take precedence. This is true for all
   environment variables with the exception for ``{ENVPREFIX}_BIND`` and
   ``{ENVPREFIX}_BINDPATH``, which are combined with the ``--bind`` option /
   argument pair, if both are present.

#. Environment variables will override default values of CLI options that have
   not been explicitly set in the command line.

#. Any default values for CLI options that have not been overridden on the
   command line, or by corresponding environment variables, will then take
   effect.

Defaults
========

The following variables have defaults that can be overridden by assigning your
own values to the corresponding environment variables at runtime:

Docker
------

``{ENVPREFIX}_DOCKER_LOGIN`` -
Set this to login to a Docker Repository interactively.

``{ENVPREFIX}_DOCKER_USERNAME`` -
Your Docker username.

``{ENVPREFIX}_DOCKER_PASSWORD`` -
Your Docker password.

``RUNSCRIPT_COMMAND`` -
Is not obtained from the environment, but is a hard coded default
("/bin/bash"). This is the fallback command used in the case that the docker
image does not have a CMD or ENTRYPOINT.

``TAG`` -
Is the default tag, ``latest``.

``{ENVPREFIX}_NOHTTPS`` -
This is relevant if you want to use a registry that doesn't support https. A
typical use-case for this variable is when using local registry, running on
the same machine as {Project} itself.

Library
-------

``{ENVPREFIX}_LIBRARY`` -
Used to specify the library to pull from.
Default is the currently selected :ref:`remote endpoint <endpoint>`.

Encryption
----------

``{ENVPREFIX}_ENCRYPTION_PASSPHRASE`` -
Used to pass a plaintext passphrase to be used to encrypt a container file
system (in conjunction with the ``--encrypt`` flag). The default is empty.

``{ENVPREFIX}_ENCRYPTION_PEM_PATH`` -
Used to specify the location of a public key to use for container encryption
(in conjunction with the ``--encrypt`` flag). The default is empty.
