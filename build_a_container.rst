.. _build-a-container:


=================
Build a Container
=================

.. _sec:build_a_container:

``build`` is the “Swiss army knife” of container creation. You can use it to
download and assemble existing containers from external resources like the
`Container Library <https://cloud.sylabs.io/library>`_ and
`Docker Hub <https://hub.docker.com/>`_. You can use it to convert containers
between the formats supported by apptainer. And you can use it in conjunction
with a :ref:`apptainer definition <definition-files>` file to create a
container from scratch and customized it to fit your needs.

--------
Overview
--------


The ``build`` command accepts a target as input and produces a container as
output.

The target defines the method that ``build`` uses to create the container. It
can be one of the following:


-  URI beginning with **library://** to build from the Container Library

-  URI beginning with **docker://** to build from Docker Hub

-  URI beginning with **shub://** to build from apptainer Hub

-  path to a **existing container** on your local machine

-  path to a **directory** to build from a sandbox

-  path to a :ref:`apptainer definition file <definition-files>`

``build`` can produce containers in two different formats that can be specified
as follows.

-  compressed read-only **apptainer Image File (SIF)** format suitable for
   production (default)

-  writable **(ch)root directory** called a sandbox for interactive development
   ( ``--sandbox`` option)

Because ``build`` can accept an existing container as a target and create a
container in either supported format you can convert existing containers from
one format to another.

------------------------------------------------------------
Downloading an existing container from the Container Library
------------------------------------------------------------

You can use the build command to download a container from the Container
Library.


.. code-block:: none

    $ sudo apptainer build lolcow.sif library://sylabs-jms/testing/lolcow

The first argument (``lolcow.sif``) specifies a path and name for your
container. The second argument (``library://sylabs-jms/testing/lolcow``) gives
the Container Library URI from which to download. By default the container will
be converted to a compressed, read-only SIF. If you want your container in a
writable format use the ``--sandbox`` option.

-------------------------------------------------
Downloading an existing container from Docker Hub
-------------------------------------------------

You can use ``build`` to download layers from Docker Hub and assemble them into
apptainer containers.

.. code-block:: none

    $ sudo apptainer build lolcow.sif docker://godlovedc/lolcow

.. _create_a_writable_container:

-------------------------------------------
Creating writable ``--sandbox`` directories
-------------------------------------------

If you wanted to create a container within a writable directory (called a
sandbox) you can do so with the ``--sandbox`` option. It’s possible to create a
sandbox without root privileges, but to ensure proper file permissions it is
recommended to do so as root.

.. code-block:: none

    $ sudo apptainer build --sandbox lolcow/ library://sylabs-jms/testing/lolcow

The resulting directory operates just like a container in a SIF file. To make
changes within the container, use the ``--writable`` flag when you invoke your
container.  It’s a good idea to do this as root to ensure you have permission to
access the files and directories that you want to change.

.. code-block:: none

    $ sudo apptainer shell --writable lolcow/

------------------------------------------------
Converting containers from one format to another
------------------------------------------------

If you already have a container saved locally, you can use it as a target to
build a new container. This allows you convert containers from one format to
another. For example if you had a sandbox container called ``development/`` and
you wanted to convert it to SIF container called ``production.sif`` you could:

.. code-block:: none

    $ sudo apptainer build production.sif development/

Use care when converting a sandbox directory to the default SIF format. If
changes were made to the writable container before conversion, there is no
record of those changes in the apptainer definition file rendering your
container non-reproducible. It is a best practice to build your immutable
production containers directly from a apptainer definition file instead.

-----------------------------------------------------
Building containers from apptainer definition files
-----------------------------------------------------

Of course, apptainer definition files can be used as the target when building
a container. For detailed information on writing apptainer definition files,
please see the :doc:`Container Definition docs <definition_files>`. Let’s say
you already have the following container definition file called ``lolcow.def``,
and you want to use it to build a SIF container.

.. code-block:: apptainer

    Bootstrap: docker
    From: ubuntu:16.04

    %post
        apt-get -y update
        apt-get -y install fortune cowsay lolcat

    %environment
        export LC_ALL=C
        export PATH=/usr/games:$PATH

    %runscript
        fortune | cowsay | lolcat

You can do so with the following command.

.. code-block:: none

    $ sudo apptainer build lolcow.sif lolcow.def

The command requires ``sudo`` just as installing software on your local machine
requires root privileges.


.. note::
    Beware that it is possible to build an image on a host and have the image not work on a different host. This could be because of
    the default compressor supported by the host. For example, when building an image on a host in which the default compressor
    is ``xz`` and then trying to run that image on a CentOS 6 node, where the only compressor available is ``gzip``.

-----------------------------
Building encrypted containers
-----------------------------
Beginning in apptainer 3.4.0 it is possible to build and run encrypted
containers.  The containers are decrypted at runtime entirely in kernel space, 
meaning that no intermediate decrypted data is ever present on disk or in 
memory.  See :ref:`encrypted containers <encryption>` for more details.

-------------
Build options
-------------

``--builder``
=============

apptainer 3.0 introduces the option to perform a remote build. The
``--builder`` option allows you to specify a URL to a different build service.
For instance, you may need to specify a URL to build to an on premises
installation of the remote builder.  This option must be used in conjunction
with ``--remote``.

``--detached``
==============

When used in combination with the ``--remote`` option, the ``--detached`` option
will detach the build from your terminal and allow it to build in the background
without echoing any output to your terminal.

``--encrypt``
==============

Specifies that apptainer should use a secret saved in either the 
``apptainer_ENCRYPTION_PASSPHRASE`` or ``apptainer_ENCRYPTION_PEM_PATH``
environment variable to build an encrypted container.  See :ref:`encrypted 
containers <encryption>` for more details.   

``--fakeroot``
==============

Gives users a way to build containers completely unprivileged.  See :ref:`the 
fakeroot feature <fakeroot>` for details. 

``--force``
===========

The ``--force`` option will delete and overwrite an existing apptainer image
without presenting the normal interactive prompt.

``--json``
==========

The ``--json`` option will force apptainer to interpret a given definition
file as a json.

``--library``
=============

This command allows you to set a different library.  (The default library is
"https://library.sylabs.io")

``--notest``
============

If you don’t want to run the ``%test`` section during the container build, you 
can skip it with the ``--notest`` option. For instance, maybe you are building a
container intended to run in a production environment with GPUs. But perhaps 
your local build resource does not have GPUs. You want to include a ``%test`` 
section that runs a short validation but you don’t want your build to exit with 
an error because it cannot find a GPU on your system.

``--passphrase``
================

This flag allows you to pass a plaintext passphrase to encrypt the container 
file system at build time. See :ref:`encrypted containers <encryption>` for more 
details.   

``--pem-path``
==============

This flag allows you to pass the location of a public key to encrypt the 
container file system at build time. See :ref:`encrypted containers 
<encryption>` for more details.  

``--remote``
============

apptainer 3.0 introduces the ability to build a container on an external
resource running a remote builder.  (The default remote builder is located at
"https://cloud.sylabs.io/builder".)

``--sandbox``
=============

Build a sandbox (chroot directory) instead of the default SIF format.

``--section``
=============

Instead of running the entire definition file, only run a specific section or
sections.  This option accepts a comma delimited string of definition file
sections.  Acceptable arguments include ``all``, ``none`` or any combination of
the following: ``setup``, ``post``, ``files``, ``environment``, ``test``,
``labels``.

Under normal build conditions, the apptainer definition file is saved into
a container’s meta-data so that there is a record showing how the container was
built. Using the ``--section`` option may render this meta-data useless, so use
care if you value reproducibility.

``--update``
============

You can build into the same sandbox container multiple times (though the results
may be unpredictable and it is generally better to delete your container and
start from scratch).

By default if you build into an existing sandbox container, the  ``build``
command will prompt you to decide whether or not to overwrite the container.
Instead of this behavior you can use the ``--update`` option to build _into_ an
existing container. This will cause apptainer to skip the header and build
any sections that are in the definition file into the existing container.

The ``--update`` option is only valid when used with sandbox containers.

``--nv``
========

This flag allows you to mount the Nvidia CUDA libraries of your host into your build
environment. Libraries are mounted during the execution of ``post`` and ``test`` sections.

``--rocm``
==========

This flag allows you to mount the AMD Rocm libraries of your host into your build
environment. Libraries are mounted during the execution of ``post`` and ``test`` sections.

``--bind``
==========

This flag allows you to mount a directory, a file or an image during build, it works
the same way as ``--bind`` for ``shell``, ``exec`` and ``run`` and can be specified
multiple times, see :ref:`user defined bind paths <user-defined-bind-paths>`.
Bind mount occurs during the execution of ``post`` and ``test`` sections.

-----------------
More Build topics
-----------------

-  If you want to **customize the cache location** (where Docker layers are
   downloaded on your system), specify Docker credentials, or any custom tweaks
   to your build environment, see :ref:`build environment <build-environment>`.

-  If you want to make internally **modular containers**, check out the getting
   started guide `here <https://sci-f.github.io/tutorials>`_

-  If you want to **build your containers** on the Remote Builder, (because you
   don’t have root access on a Linux machine or want to host your container on
   the cloud) check out `this site <https://cloud.sylabs.io/builder>`_

-  If you want to **build a container with an encrypted file system** look 
   :ref:`here <encryption>`.
