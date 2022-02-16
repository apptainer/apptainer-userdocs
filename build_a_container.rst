.. _build-a-container:

###################
 Build a Container
###################

.. _sec:build_a_container:

``build`` is the “Swiss army knife” of container creation. You can use
it to download and assemble existing containers from external resources
like the `Container Library <https://cloud.sylabs.io/library>`_ and
`Docker Hub <https://hub.docker.com/>`_. You can use it to convert
containers between the formats supported by {Project}. And you can
use it in conjunction with a :ref:`{Project} definition
<definition-files>` file to create a container from scratch and
customized it to fit your needs.

**********
 Overview
**********

The ``build`` command accepts a target as input and produces a container
as output.

The target defines the method that ``build`` uses to create the
container. It can be one of the following:

-  URI beginning with **library://** to build from the Container Library
-  URI beginning with **docker://** to build from Docker Hub
-  URI beginning with **shub://** to build from Singularity Hub
-  path to a **existing container** on your local machine
-  path to a **directory** to build from a sandbox
-  path to a :ref:`{Project} definition file <definition-files>`

``build`` can produce containers in two different formats that can be
specified as follows.

-  compressed read-only **Singularity Image File (SIF)** format suitable
   for production (default)
-  writable **(ch)root directory** called a sandbox for interactive
   development ( ``--sandbox`` option)

Because ``build`` can accept an existing container as a target and
create a container in either supported format you can convert existing
containers from one format to another.

**************************************************************
 Downloading an existing container from the Container Library
**************************************************************

You can use the build command to download a container from the Container
Library.

.. code::

   $ sudo {command} build lolcow.sif library://lolcow

The first argument (``lolcow.sif``) specifies a path and name for your
container. The second argument (``library://lolcow``) gives the
Container Library URI from which to download. By default the container
will be converted to a compressed, read-only SIF. If you want your
container in a writable format use the ``--sandbox`` option.

***************************************************
 Downloading an existing container from Docker Hub
***************************************************

You can use ``build`` to download layers from Docker Hub and assemble
them into {Project} containers.

.. code::

   $ sudo {command} build lolcow.sif docker://sylabsio/lolcow

.. _create_a_writable_container:

*********************************************
 Creating writable ``--sandbox`` directories
*********************************************

If you wanted to create a container within a writable directory (called
a sandbox) you can do so with the ``--sandbox`` option. It’s possible to
create a sandbox without root privileges, but to ensure proper file
permissions it is recommended to do so as root.

.. code::

   $ sudo {command} build --sandbox lolcow/ library://lolcow

The resulting directory operates just like a container in a SIF file. To
make changes within the container, use the ``--writable`` flag when you
invoke your container. It’s a good idea to do this as root to ensure you
have permission to access the files and directories that you want to
change.

.. code::

   $ sudo {command} shell --writable lolcow/

**************************************************
 Converting containers from one format to another
**************************************************

If you already have a container saved locally, you can use it as a
target to build a new container. This allows you convert containers from
one format to another. For example if you had a sandbox container called
``development/`` and you wanted to convert it to SIF container called
``production.sif`` you could:

.. code::

   $ sudo {command} build production.sif development/

Use care when converting a sandbox directory to the default SIF format.
If changes were made to the writable container before conversion, there
is no record of those changes in the {Project} definition file
rendering your container non-reproducible. It is a best practice to
build your immutable production containers directly from a {Project}
definition file instead.

*********************************************************
 Building containers from {Project} definition files
*********************************************************

Of course, {Project} definition files can be used as the target when
building a container. For detailed information on writing {Project}
definition files, please see the :doc:`Container Definition docs
<definition_files>`. Let’s say you already have the following container
definition file called ``lolcow.def``, and you want to use it to build a
SIF container.

.. code:: {command}

   Bootstrap: docker
   From: ubuntu:16.04

   %post
       apt-get -y update
       apt-get -y install cowsay lolcat

   %environment
       export LC_ALL=C
       export PATH=/usr/games:$PATH

   %runscript
       date | cowsay | lolcat

You can do so with the following command.

.. code::

   $ sudo {command} build lolcow.sif lolcow.def

The command requires ``sudo`` just as installing software on your local
machine requires root privileges.

.. note::

   Beware that it is possible to build an image on a host and have the
   image not work on a different host. This could be because of the
   default compressor supported by the host. For example, when building
   an image on a host in which the default compressor is ``xz`` and then
   trying to run that image on a CentOS 6 node, where the only
   compressor available is ``gzip``.

*******************************
 Building encrypted containers
*******************************

With {Project} it is possible to build and run
encrypted containers. The containers are decrypted at runtime entirely
in kernel space, meaning that no intermediate decrypted data is ever
present on disk or in memory. See :ref:`encrypted containers
<encryption>` for more details.

***************
 Build options
***************

``--encrypt``
=============

Specifies that {Project} should use a secret saved in either the
``{ENVPREFIX}_ENCRYPTION_PASSPHRASE`` or
``{ENVPREFIX}_ENCRYPTION_PEM_PATH`` environment variable to build an
encrypted container. See :ref:`encrypted containers <encryption>` for
more details.

``--fakeroot``
==============

Gives users a way to build containers completely unprivileged. See
:ref:`the fakeroot feature <fakeroot>` for details.

``--force``
===========

The ``--force`` option will delete and overwrite an existing
{Project} image without presenting the normal interactive prompt.

``--json``
==========

The ``--json`` option will force {Project} to interpret a given
definition file as a json.

``--library``
=============

This command allows you to set a different library. (The default library
is "https://library.sylabs.io")

``--notest``
============

If you don’t want to run the ``%test`` section during the container
build, you can skip it with the ``--notest`` option. For instance, maybe
you are building a container intended to run in a production environment
with GPUs. But perhaps your local build resource does not have GPUs. You
want to include a ``%test`` section that runs a short validation but you
don’t want your build to exit with an error because it cannot find a GPU
on your system.

``--passphrase``
================

This flag allows you to pass a plaintext passphrase to encrypt the
container file system at build time. See :ref:`encrypted containers
<encryption>` for more details.

``--pem-path``
==============

This flag allows you to pass the location of a public key to encrypt the
container file system at build time. See :ref:`encrypted containers
<encryption>` for more details.

``--sandbox``
=============

Build a sandbox (chroot directory) instead of the default SIF format.

``--section``
=============

Instead of running the entire definition file, only run a specific
section or sections. This option accepts a comma delimited string of
definition file sections. Acceptable arguments include ``all``, ``none``
or any combination of the following: ``setup``, ``post``, ``files``,
``environment``, ``test``, ``labels``.

Under normal build conditions, the {Project} definition file is
saved into a container’s meta-data so that there is a record showing how
the container was built. Using the ``--section`` option may render this
meta-data useless, so use care if you value reproducibility.

``--update``
============

You can build into the same sandbox container multiple times (though the
results may be unpredictable and it is generally better to delete your
container and start from scratch).

By default if you build into an existing sandbox container, the
``build`` command will prompt you to decide whether or not to overwrite
the container. Instead of this behavior you can use the ``--update``
option to build _into_ an existing container. This will cause
{Project} to skip the header and build any sections that are in the
definition file into the existing container.

The ``--update`` option is only valid when used with sandbox containers.

``--nv``
========

This flag allows you to mount the Nvidia CUDA libraries of your host
into your build environment. Libraries are mounted during the execution
of ``post`` and ``test`` sections.

.. note::

    This option can't be set via the environment variable `{ENVPREFIX}_NV`.
    {Project} will attempt to bind binaries listed in {ENVPREFIX}_CONFDIR/nvliblist.conf,
    if the mount destination doesn't exist inside the container, they are ignored.

``--rocm``
==========

This flag allows you to mount the AMD Rocm libraries of your host into
your build environment. Libraries are mounted during the execution of
``post`` and ``test`` sections.

.. note::

    This option can't be set via the environment variable `{ENVPREFIX}_ROCM`.
    {Project} will attempt to bind binaries listed in `{ENVPREFIX}_CONFDIR/rocmliblist.conf`,
    if the mount destination doesn't exist inside the container, they are ignored.

``--bind``
==========

This flag allows you to mount a directory, a file or an image during
build, it works the same way as ``--bind`` for ``shell``, ``exec`` and
``run`` and can be specified multiple times, see :ref:`user defined bind
paths <user-defined-bind-paths>`. Bind mount occurs during the execution
of ``post`` and ``test`` sections.

.. note::

    This option can't be set via the environment variables `{ENVPREFIX}_BIND` and `{ENVPREFIX}_BINDPATH`

**Beware that the mount points must exist in the built image** prior to executing ``post`` and ``test``.
So if you want to bind ``--bind /example`` and it doesn't exist in the bootstrap image, you have to
workaround that by adding a ``setup`` section:

.. code-block:: none

    %setup
      mkdir ${ENVPREFIX}_ROOTFS/example

.. note::

    Binding your directory to `/mnt` is another workaround, as this directory is often present in
    distribution images and is intended for that purpose, you could avoid the directory creation
    in the definition file.

``--writable-tmpfs``
====================

This flag will run the ``%test`` section of the build with a writable
tmpfs overlay filesystem in place. This allows the tests to create
files, which will be discarded at the end of the build. Other portions
of the build do not use this temporary filesystem.

*******************
 More Build topics
*******************

-  If you want to **customize the cache location** (where Docker layers
   are downloaded on your system), specify Docker credentials, or any
   custom tweaks to your build environment, see :ref:`build environment
   <build-environment>`.

-  If you want to make internally **modular containers**, check out the
   getting started guide `here <https://sci-f.github.io/tutorials>`_

-  If you want to **build a container with an encrypted file system**
   look :ref:`here <encryption>`.
