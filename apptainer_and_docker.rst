.. _apptainer-and-docker:

=====================================
Support for Docker and OCI Containers
=====================================

The Open Containers Initiative (OCI) container format, which grew out
of Docker, is the dominant standard for cloud-focused containerized
deployments of software. Although {Singularity}'s own container format
has many unique advantages, it's likely you will need to work with
Docker/OCI containers at some point.

{Singularity} aims for maximum compatibility with Docker, within the
constraints on a runtime that is well suited for use on shared systems
and especially in HPC environments.

Using {Singularity} you can:

<<<<<<< HEAD:apptainer_and_docker.rst
Effort has been expended in developing `Docker <https://www.docker.com/>`_ containers. Deconstructed into one or more compressed archives 
(typically split across multiple segments, or **layers** as they are known in Docker parlance) plus some metadata, images for these containers
are built from specifications known as ``Dockerfiles``. The public `Docker Hub <https://hub.docker.com/>`_, as well as various private registries, 
host images for use as Docker containers. Apptainer has from the outset emphasized the importance of interoperability with Docker. As a consequence, 
this section of the Apptainer User Docs first makes its sole focus interoperabilty with Docker. In so doing, the following topics receive attention here:
- Application of Apptainer action commands on ephemeral containers derived from public Docker images
- Converting public Docker images into Apptainer's native format for containerization, namely the Singularilty Image Format (SIF)
- Authenticated application of Apptainer commands to containers derived from private Docker images
- Authenticated application of Apptainer commands to containers derived from private Docker images originating from private registries
- Building SIF containers for Apptainer via the command line or definition files from a variety of sources for Docker images and image archives

The second part of this section places emphasis upon Apptainer's interoperability with open standards emerging from the `Open Containers Initiative <https://www.opencontainers.org/>`_ (OCI). 
Specifically, in documenting Apptainer interoperability as it relates to the OCI Image Specification, the following topics are covered:
- Compliance with the OCI Image Layout Specification
- OCI-compliant caching in Apptainer
- Acquiring OCI images and image archives via Apptainer
- Building SIF containers for Apptainer via the command line or definition files from a variety of sources for OCI images and image archives

The section closes with a brief enumeration of emerging best practices plus consideration of troubleshooting common issues.


.. _sec:action_commands_prebuilt_public_docker_images:

--------------------------------------------------------
Running action commands on public images from Docker Hub
--------------------------------------------------------

``godlovedc/lolcow`` is a whimsical example of a publicly accessible image hosted via `Docker Hub <https://hub.docker.com/>`_. Apptainer can execute this image as follows:

.. code-block:: none

    $ apptainer run docker://godlovedc/lolcow
=======
* Pull, run, and build from most containers on Docker Hub, without
  changes.

* Pull, run, and build from containers hosted on other registries,
  including private registries deployed on premise, or in the cloud.

* Pull and build from OCI containers in archive formats, or cached in
  a local Docker daemon.

This section will highlight these workflows, and discuss the
limitations and best practices to keep in mind when creating
containers targeting both Docker and {Singularity}.

--------------------------
Containers From Docker Hub
--------------------------

Docker Hub is the most common place that projects publish public
container images. At some point, it's likely that you will want to run
or build from containers that are hosted there.

Public Containers
=================

It's easy to run a public Docker Hub container with
{Singularity}. Just put ``docker://`` in front of the container
repository and tag. To run the container that's called
``sylabsio/lolcow:latest``:

.. code-block:: none

    $ singularity run docker://sylabsio/lolcow:latest
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst
    INFO:    Converting OCI blobs to SIF format
    INFO:    Starting build...
    Getting image source signatures
    Copying blob 16ec32c2132b done
    Copying blob 5ca731fc36c2 done
    Copying config fd0daa4d89 done
    Writing manifest to image destination
    Storing signatures
    2021/10/04 14:50:21  info unpack layer: sha256:16ec32c2132b43494832a05f2b02f7a822479f8250c173d0ab27b3de78b2f058
    2021/10/04 14:50:23  info unpack layer: sha256:5ca731fc36c28789c5ddc3216563e8bfca2ab3ea10347e07554ebba1c953242e
    INFO:    Creating SIF file...
<<<<<<< HEAD:apptainer_and_docker.rst
    INFO:    Build complete: /home/vagrant/.apptainer/cache/oci-tmp/a692b57abc43035b197b10390ea2c12855d21649f2ea2cc28094d18b93360eeb/lolcow_latest.sif
    INFO:    Image cached as SIF at /home/vagrant/.apptainer/cache/oci-tmp/a692b57abc43035b197b10390ea2c12855d21649f2ea2cc28094d18b93360eeb/lolcow_latest.sif
     ___________________________________
    / Repartee is something we think of \
    | twenty-four hours too late.       |
    |                                   |
    \ -- Mark Twain                     /
     -----------------------------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||

Here ``docker`` is prepended to ensure that the ``run`` command of Apptainer is instructed to bootstrap container creation based upon this Docker image, thus creating a complete URI for Apptainer. Apptainer subsequently downloads :ref:`all the OCI blobs that comprise this image <sec:oci_overview>`, and converts them into a *single* SIF file - the native format for Apptainer containers. Because this image from Docker Hub is cached locally in the ``$HOME/.apptainer/cache/oci-tmp/<org.opencontainers.image.ref.name>/lolcow_latest.sif`` directory, where ``<org.opencontainers.image.ref.name>`` will be replaced by the appropriate hash for the container, the image does not need to be downloaded again (from Docker Hub) the next time a Apptainer ``run`` is executed. In other words, the cached copy is sensibly reused:

.. code-block:: none

    $ apptainer run docker://godlovedc/lolcow
     _________________________________________
    / Soap and education are not as sudden as \
    | a massacre, but they are more deadly in |
    | the long run.                           |
    |                                         |
    \ -- Mark Twain                           /
     -----------------------------------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
=======
     _____________________________
    < Mon Oct 4 14:50:30 CDT 2021 >
     -----------------------------
	    \   ^__^
	     \  (oo)\_______
		(__)\       )\/\
		    ||----w |
		    ||     ||


Note that {Singularity} retrieves blobs and configuration data from
Docker Hub, extracts the layers that make up the Docker container, and
creates a SIF file from them. This SIF file is kept in your
{Singularity} :ref:`cache directory <sec:cache>`, so if you run the
same Docker container again the downloads and conversion aren't
required.

To obtain the Docker container as a SIF file in a specific location,
which you can move, share, and keep for later, ``singularity pull``
it:

.. code-block:: none

    $ singularity pull docker://sylabsio/lolcow
    INFO:    Using cached SIF image
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

    $ ls -l lolcow_latest.sif
    -rwxr-xr-x 1 myuser myuser 74993664 Oct  4 14:55 lolcow_latest.sif

If it's the first time you pull the container it'll be downloaded and
translated. If you have pulled the container before, it will be copied
from the cache.

.. note::

<<<<<<< HEAD:apptainer_and_docker.rst
    Use is made of the ``$HOME/.apptainer`` directory by default to :ref:`cache images <sec:cache>`. To cache images elsewhere, use of the environment variable ``APPTAINER_CACHEDIR`` can be made.
=======
   ``singularity pull`` of a Docker container actually runs a
   ``singularity build`` behind the scenes, since we are translating
   from OCI to SIF. If you ``singularity pull`` a Docker container
   twice, the output file isn't identical because metadata such as
   dates from the conversion will vary. This differs from pulling a
   SIF container (e.g. from a ``library://`` URI), which always give
   you an exact copy of the image.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst


Docker Hub Limits
=================

<<<<<<< HEAD:apptainer_and_docker.rst
    cd /home/vagrant/.apptainer/cache/oci-tmp/a692b57abc43035b197b10390ea2c12855d21649f2ea2cc28094d18b93360eeb/
=======
Docker Hub introduced limits on anonymous access to its API in
November 2020. Every time you use a ``docker://`` URI to run, pull
etc. a container {Singularity} will make requests to Docker Hub in
order to check whether the container has been modified there. On
shared systems, and when running containers in parallel, this can
quickly exhaust the Docker Hub API limits.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

We recommend that you ``singularity pull`` a Docker image to a local
SIF, and then always run from the SIF file, rather than using
``singularity run docker://...`` repeatedly.

Alternatively, if you have signed up for a Docker Hub account, make
sure that you authenticate before using ``docker://`` container URIs.

Authentication / Private Containers
===================================

To make use of the API limits under a Docker Hub account, or to access
private containers, you'll need to authenticate to Docker Hub. There
are a number of ways to do this with {Singularity}.

<<<<<<< HEAD:apptainer_and_docker.rst
    SIF files abstract Apptainer containers as a single file. As with any executable, a SIF file can be executed directly.

``fortune | cowsay | lolcat`` is executed by *default* when this container is ``run`` by Apptainer. Apptainer's ``exec`` command allows a different command to be executed; for example:
=======
Singularity CLI Remote Command
------------------------------

The ``singularity remote login`` command supports logging into Docker
Hub and other OCI registries. For Docker Hub, the registry hostname is
``docker.io``, so you will need to login as below, specifying your
username:
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

.. code-block::

<<<<<<< HEAD:apptainer_and_docker.rst
    $ apptainer exec docker://godlovedc/lolcow fortune
    Don't go around saying the world owes you a living.  The world owes you
    nothing.  It was here first.
            -- Mark Twain
=======
    $ singularity remote login --username myuser docker://docker.io
    Password / Token:
    INFO:    Token stored in /home/myuser/.singularity/remote.yaml
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

The Password / Token you enter must be a Docker Hub CLI access token,
which you should generate in the 'Security' section of your account
profile page on Docker Hub.

<<<<<<< HEAD:apptainer_and_docker.rst
    The *same* cached copy of the ``lolcow`` container is reused here by Apptainer ``exec``, and immediately below here by ``shell``.
=======
To check which Docker / OCI registries you are currently logged in to,
use ``singularity remote list``.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

To logout of a registry, so that your credentials are forgotten, use
``singularity remote logout``:

.. code-block::

<<<<<<< HEAD:apptainer_and_docker.rst
In addition to non-interactive execution of an image from Docker Hub, pptainer provides support for an *interactive* ``shell`` session:
=======
   $ singularity remote logout docker://docker.io
   INFO:    Logout succeeded
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

Docker CLI Authentication
-------------------------

<<<<<<< HEAD:apptainer_and_docker.rst
    $ apptainer shell docker://godlovedc/lolcow
    apptainer lolcow_latest.sif:~> cat /etc/os-release
    NAME="Ubuntu"
    VERSION="16.04.3 LTS (Xenial Xerus)"
    ID=ubuntu
    ID_LIKE=debian
    PRETTY_NAME="Ubuntu 16.04.3 LTS"
    VERSION_ID="16.04"
    HOME_URL="http://www.ubuntu.com/"
    SUPPORT_URL="http://help.ubuntu.com/"
    BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
    VERSION_CODENAME=xenial
    UBUNTU_CODENAME=xenial
    apptainer lolcow_latest.sif:~>

From this it is evident that use is being made of Ubuntu 16.04 *within* this container, whereas the shell *external* to the container is running a more recent release of Ubuntu (not illustrated here).

``inspect`` reveals the metadata for a Apptainer container encapsulated via SIF; :ref:`Container Metadata <sec:inspect_container_metadata>` is documented below.

.. note::

    ``apptainer search [search options...] <search query>`` does *not* support Docker registries like `Docker Hub <https://hub.docker.com/>`_. Use the search box at Docker Hub to locate Docker images. Docker ``pull`` commands, e.g., ``docker pull godlovedc/lolcow``, can be easily translated into the corresponding command for apptainer. The Docker ``pull`` command is available under "DETAILS" for a given image on Docker Hub.


.. TODO-ND add content re: apptainer capability - possibly a new section

.. TODO-ND add content re: apptainer instance - possibly a new section ... review first sushma-98's edits for the running services page


.. _sec:use_prebuilt_public_docker_images:

--------------------------------------------
Making use of public images from Docker Hub
--------------------------------------------

Apptainer can make use of public images available from the `Docker Hub <https://hub.docker.com/>`_. By specifying the ``docker://`` URI for an image that has already been located, Apptainer can ``pull``  it - e.g.:

.. code-block:: none

    $ apptainer pull docker://godlovedc/lolcow
    INFO:    Starting build...
    Getting image source signatures
    Copying blob sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
     45.33 MiB / 45.33 MiB [====================================================] 2s
    Copying blob sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
     848 B / 848 B [============================================================] 0s
    Copying blob sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
     621 B / 621 B [============================================================] 0s
    Copying blob sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
     853 B / 853 B [============================================================] 0s
    Copying blob sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
     169 B / 169 B [============================================================] 0s
    Copying blob sha256:8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
     53.75 MiB / 53.75 MiB [====================================================] 3s
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: lolcow_latest.sif

This ``pull`` results in a *local* copy of the Docker image in SIF, the Apptainer Image Format:

.. code-block:: none

    $ file lolcow_latest.sif
    lolcow_latest.sif: a /usr/bin/env run-apptainer script executable (binary data)

In converting to SIF, individual layers of the Docker image have been *combined* into a single, native file for use by Apptainer; there is no need to subsequently ``build`` the image for Apptainer. For example, you can now ``exec``, ``run`` or ``shell`` into the SIF version via apptainer, :ref:`as described above <sec:action_commands_prebuilt_public_docker_images>`.

.. _sec:use_prebuilt_public_docker_images_SUB_inspect:

``inspect`` reveals metadata for the container encapsulated via SIF:

.. code-block:: none

        $ apptainer inspect lolcow_latest.sif

        {
            "org.label-schema.build-date": "Thursday_6_December_2018_17:29:48_UTC",
            "org.label-schema.schema-version": "1.0",
            "org.label-schema.usage.apptainer.deffile.bootstrap": "docker",
            "org.label-schema.usage.apptainer.deffile.from": "godlovedc/lolcow",
            "org.label-schema.usage.apptainer.version": "3.0.1-40.g84083b4f"
        }
=======
If you have the ``docker`` CLI installed on your machine, you can
``docker login`` to your account. This stores authentication
information in ``~/.docker/config.json``. The process that
{Singularity} uses to retrieve Docker / OCI containers will attempt to
use this information to login.

.. note::

   {Singularity} can only read credentials stored directly in
   ``~/.docker/config.json``. It cannot read credentials from external
   Docker credential helpers.

Interactive Login
-----------------
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

To perform a one-off interactive login, which will not store your
credentials, use the ``--docker-login`` flag:

.. code-block::

   $ singularity pull --docker-login docker://sylabsio/private
   Enter Docker Username: myuser
   Enter Docker Password:

Environment Variables
---------------------

<<<<<<< HEAD:apptainer_and_docker.rst
    $ apptainer verify lolcow_latest.sif
    Verifying image: lolcow_latest.sif
    ERROR:   verification failed: error while searching for signature blocks: no signatures found for system partition
=======
When calling {Singularity} in a CI/CD workflow, or other
non-interactive scenario, it may be useful to specify Docker Hub login
credentials using environment variables. These are often the default
way of passing secrets into jobs within CI pipelines.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

Singularity accepts a username, and password / token, as
``SINGULARITY_DOCKER_USERNAME`` and ``SINGULARITY_DOCKER_PASSWORD``
respectively. These environment variables will override any stored
credentials.

.. code-block::

   $ export SINGULARITY_DOCKER_USERNAME=myuser
   $ export SINGULARITY_DOCKER_PASSWORD=mytoken
   $ singularity pull docker://sylabsio/private

--------------------------------
Containers From Other Registries
--------------------------------

You can use ``docker://`` URIs with {Singularity} to pull and run
containers from OCI registries other than Docker Hub. To do this,
you'll need to include the hostname or IP address of the registry in
your ``docker://`` URI. Authentication with other registries is
carried out in the same basic manner, but sometimes you'll need to
retrieve your credentials using a specific tool, especially when
working with Cloud Service Provider environments.

Below are specific examples for some common registries. Most other
registries follow a similar pattern for pulling public images, and
authenticating to access private images.

<<<<<<< HEAD:apptainer_and_docker.rst
---------------------------------------------
Making use of private images from Docker Hub
---------------------------------------------

After successful authentication, Apptainer can also make use of *private* images available from the `Docker Hub <https://hub.docker.com/>`_. The three means available for authentication follow here. Before describing these means, it is instructive to illustrate the error generated when attempting access a private image *without* credentials:
=======
Quay.io
=======

Quay is an OCI container registry used by a large number of projects,
and hosted at ``https://quay.io``. To pull public containers from
Quay, just include the ``quay.io`` hostname in your ``docker://`` URI:
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

.. code-block::

<<<<<<< HEAD:apptainer_and_docker.rst
    $ apptainer pull docker://ilumb/mylolcow
    INFO:    Starting build...
    FATAL:   Unable to pull docker://ilumb/mylolcow: conveyor failed to get: Error reading manifest latest in docker.io/ilumb/mylolcow: errors:
    denied: requested access to the resource is denied
    unauthorized: authentication required

In this case, the ``mylolcow`` repository of user ``ilumb`` **requires** authentication through specification of a valid username and password.


Authentication via Remote Login
===============================

Users are able to supply credentials on a per registry basis with the ``remote`` command group. See :ref:`Managing OCI Registries <sec:managing_oci_registries>`
for detailed instructions.
=======
    $ singularity pull docker://quay.io/bitnami/python:3.7
    INFO:    Converting OCI blobs to SIF format
    INFO:    Starting build...
    ...
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

    $ singularity run python_3.7.sif
    Python 3.7.12 (default, Sep 24 2021, 11:48:27)
    [GCC 8.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

To pull containers from private repositories you will need to generate
a CLI token in the Quay web interface, then use it to login with
{Singularity}. Use the same methods as described for Docker Hub above:

* Run ``singularity remote login --username myuser docker://quay.io``
  to store your credentials for {Singularity}.

* Use ``docker login quay.io`` if ``docker`` is on your machine.

<<<<<<< HEAD:apptainer_and_docker.rst
Interactive login is the first of two means provided for authentication with Docker Hub. It is enabled through use of the ``--docker-login`` option of Apptainer's ``pull`` command; for example:
=======
* Use the ``--docker-login`` flag for a one-time interactive login.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

* Set the ``SINGULARITY_DOCKER_USERNAME`` and
  ``SINGULARITY_DOCKER_PASSWORD`` environment variables.

<<<<<<< HEAD:apptainer_and_docker.rst
    $ apptainer pull --docker-login docker://ilumb/mylolcow
    Enter Docker Username: ilumb
    Enter Docker Password:
    INFO:    Starting build...
    Getting image source signatures
    Skipping fetch of repeat blob sha256:7b8b6451c85f072fd0d7961c97be3fe6e2f772657d471254f6d52ad9f158a580
    Skipping fetch of repeat blob sha256:ab4d1096d9ba178819a3f71f17add95285b393e96d08c8a6bfc3446355bcdc49
    Skipping fetch of repeat blob sha256:e6797d1788acd741d33f4530106586ffee568be513d47e6e20a4c9bc3858822e
    Skipping fetch of repeat blob sha256:e25c5c290bded5267364aa9f59a18dd22a8b776d7658a41ffabbf691d8104e36
    Skipping fetch of repeat blob sha256:258e068bc5e36969d3ba4b47fd3ca0d392c6de465726994f7432b14b0414d23b
    Copying config sha256:8a8f815257182b770d32dffff7f185013b4041d076e065893f9dd1e89ad8a671
     3.12 KiB / 3.12 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: mylolcow_latest.sif
=======
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

NVIDIA NGC
==========

The NVIDIA NGC catalog at https://ngc.nvidia.com contains various GPU
software, packaged in containers. Many of these containers are
specifically documented by NVIDIA as supported by {Singularity}, with
instructions available.

Previously, an account and API token was required to pull NGC
containers. However, they are now available to pull as a guest without
login:

.. code-block::

   $ singularity pull docker://nvcr.io/nvidia/pytorch:21.09-py3
   INFO:    Converting OCI blobs to SIF format
   INFO:    Starting build...

If you do need to pull containers using an NVIDIA account, e.g. if you
have access to an NGC Private Registry, you will need to generate an
API key in the web interface in order to authenticate.

Use one of the following authentication methods (detailed above for
Docker Hub), with the username ``$oauthtoken`` and the password set to
your NGC API key.

* Run ``singularity remote login --username \$oauthtoken
  docker://nvcr.io`` to store your credentials for {Singularity}.

<<<<<<< HEAD:apptainer_and_docker.rst
    export APPTAINER_DOCKER_USERNAME=ilumb
    export APPTAINER_DOCKER_PASSWORD=<redacted>
=======
* Use ``docker login nvcr.io`` if ``docker`` is on your machine.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

* Use the ``--docker-login`` flag for a one-time interactive login.

<<<<<<< HEAD:apptainer_and_docker.rst
Based upon these exports, ``$ apptainer pull docker://ilumb/mylolcow`` allows for the retrieval of this private image.
=======
* Set the ``SINGULARITY_DOCKER_USERNAME="\$oauthtoken"`` and
  ``SINGULARITY_DOCKER_PASSWORD`` environment variables.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

See also: https://docs.nvidia.com/ngc/ngc-private-registry-user-guide/index.html


GitHub Container Registry
=========================

GitHub Container Registry is increasingly used to provide Docker
containers alongside the source code of hosted projects. You can pull
a public container from GitHub Container Registry using a ``ghcr.io``
URI:

.. code-block::

   $ singularity pull docker://ghcr.io/containerd/alpine:latest
   INFO:    Converting OCI blobs to SIF format
   INFO:    Starting build...

<<<<<<< HEAD:apptainer_and_docker.rst
-----------------------------------------------------
Making use of private images from Private Registries
-----------------------------------------------------
=======
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

To pull private containers from GHCR you will need to generate a
personal access token in the GitHub web interface in order to
authenticate. This token must have required scopes. See
`the GitHub documentation here. <https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry>`__

Use one of the following authentication methods (detailed above for
Docker Hub), with your username and personal access token:

* Run ``singularity remote login --username myuser docker://ghcr.io`` to store your
  credentials for {Singularity}.

* Use ``docker login ghcr.io`` if ``docker`` is on your machine.

* Use the ``--docker-login`` flag for a one-time interactive login.

* Set the ``SINGULARITY_DOCKER_USERNAME`` and
  ``SINGULARITY_DOCKER_PASSWORD`` environment variables.

<<<<<<< HEAD:apptainer_and_docker.rst
    $ apptainer pull docker://godlovedc/lolcow
=======
AWS ECR
=======
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

To work with an AWS hosted Elastic Container Registry (ECR) generally
requires authentication. There are various ways to generate
credentials. You should follow one of the approaches in
`the ECR guide <https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html>`__
in order to obtain a username and password.

.. warning::

<<<<<<< HEAD:apptainer_and_docker.rst
    $ apptainer pull docker://index.docker.io/godlovedc/lolcow
=======
    The ECR Docker credential helper cannot be used, as {Singularity}
    does not currently support external credential helpers used with
    Docker, only reading credentials stored directly in the
    ``.docker/config.json`` file.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

The ``get-login-password`` approach is the most straightforward. It
uses the AWS CLI to request a password, which can then be used to
authenticate to an ECR private registry in the specified region. The
username used in conjunction with this password is always ``AWS``.

.. code-block:: none

<<<<<<< HEAD:apptainer_and_docker.rst
    $ apptainer pull docker://nvcr.io/nvidia/pytorch:18.11-py3
    INFO:    Starting build...
    Getting image source signatures
    Skipping fetch of repeat blob sha256:18d680d616571900d78ee1c8fff0310f2a2afe39c6ed0ba2651ff667af406c3e
    <blob fetching details deleted>
    Skipping fetch of repeat blob sha256:c71aeebc266c779eb4e769c98c935356a930b16d881d7dde4db510a09cfa4222
    Copying config sha256:b77551af8073c85588088ab2a39007d04bc830831ba1eef4127b2d39aaf3a6b1
     21.28 KiB / 21.28 KiB [====================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: pytorch_18.11-py3.sif

will retrieve a specific version of the `PyTorch platform <https://pytorch.org/>`_ for Deep Learning from the NVIDIA GPU Cloud (NGC). Because NGC is a private registry, the above ``pull`` assumes :ref:`authentication via environment variables <sec:authentication_via_environment_variables>` when the blobs that collectively comprise the Docker image have not already been cached locally. In the NGC case, the required environment variable are set as follows:

.. code-block:: none

    export APPTAINER_DOCKER_USERNAME='$oauthtoken'
    export APPTAINER_DOCKER_PASSWORD=<redacted>
=======
    $ aws ecr get-login-password --region region

Then login using one of the following methods:
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

* Run ``singularity remote login --username AWS
  docker://<accountid>.dkr.ecr.<region>.amazonaws.com`` to store your
  credentials for {Singularity}.

* Use ``docker login --username AWS
  <accountid>.dkr.ecr.<region>.amazonaws.com`` if ``docker`` is on
  your machine.

* Use the ``--docker-login`` flag for a one-time interactive login.

* Set the ``SINGULARITY_DOCKER_USERNAME=AWS`` and
  ``SINGULARITY_DOCKER_PASSWORD`` environment variables.

You should now be able to pull containers from your ECR URI at
``docker://<accountid>.dkr.ecr.<region>.amazonaws.com``.


Azure ACR
=========

<<<<<<< HEAD:apptainer_and_docker.rst
    $ apptainer pull --docker-login docker://nvcr.io/nvidia/pytorch:18.11-py3
    Enter Docker Username: $oauthtoken
    Enter Docker Password:
    INFO:    Starting build...
    Getting image source signatures
    Skipping fetch of repeat blob sha256:18d680d616571900d78ee1c8fff0310f2a2afe39c6ed0ba2651ff667af406c3e
    <blob fetching details deleted>
    Skipping fetch of repeat blob sha256:c71aeebc266c779eb4e769c98c935356a930b16d881d7dde4db510a09cfa4222
    Copying config sha256:b77551af8073c85588088ab2a39007d04bc830831ba1eef4127b2d39aaf3a6b1
    21.28 KiB / 21.28 KiB [====================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: pytorch_18.11-py3.sif

Authentication aside, the outcome of the ``pull`` command is the Apptainer container ``pytorch_18.11-py3.sif`` - i.e., a locally stored copy, that has been coverted to SIF.
=======
An Azure hosted Azure Container Registry (ACR) will generally hold
private images and require authentication to pull from. There are
several ways to authenticate to ACR, depending on the account type you
use in Azure. See the
`ACR documentation <https://docs.microsoft.com/en-us/azure/container-registry/container-registry-authentication?tabs=azure-cli>`__
for more information on these options.

Generally, for identities, using ``az acr login`` from the Azure
CLI will add credentials to ``.docker/config.json`` which can be read
by {Singularity}.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

Service Principle accounts will have an explicit username and
password, and you should authenticate using one of the following
methods:

<<<<<<< HEAD:apptainer_and_docker.rst
------------------------------------------------------
Building images for Apptainer from Docker Registries
------------------------------------------------------

The ``build`` command is used to **create** Apptainer containers. Because it is documented extensively :ref:`elsewhere in this manual <build-a-container>`, only specifics relevant to Docker are provided here - namely, working with Docker Hub via :ref:`the apptainer command line <sec:apptainer_build_cli>` and through :ref:`apptainer definition files <sec:apptainer_build_def_files>`.
=======
* Run ``singularity remote login --username myuser
  docker://myregistry.azurecr.io`` to store your credentials for
  {Singularity}.

* Use ``docker login --username myuser myregistry.azurecr.io`` if
  ``docker`` is on your machine.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

* Use the ``--docker-login`` flag for a one-time interactive login.

<<<<<<< HEAD:apptainer_and_docker.rst
.. _sec:apptainer_build_cli:

Working from the Apptainer Command Line
=========================================
=======
* Set the ``SINGULARITY_DOCKER_USERNAME`` and
  ``SINGULARITY_DOCKER_PASSWORD`` environment variables.

The recent repository-scoped access token preview may be more
convenient. See the
`preview documentation <https://docs.microsoft.com/en-us/azure/container-registry/container-registry-repository-scoped-permissions>`__
which details how to use ``az acr token create`` to obtain a token
name and password pair that can be used to authenticate with the above
methods.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

-------------------------------------
Building From Docker / OCI Containers
-------------------------------------

If you wish to use an existing Docker or OCI container as the basis
for a new container, you will need to specifiy it as the *bootstrap*
source in a {Singularity} definition file.

Just as you can run or pull containers from different registries using
a ``docker://`` URI, you can use different headers in a definition file
to instruct {Singularity} where to find the container you want to use
as the starting point for your build.

<<<<<<< HEAD:apptainer_and_docker.rst
    $ apptainer build mylolcow_latest.sif docker://godlovedc/lolcow
    INFO:    Starting build...
    Getting image source signatures
    Skipping fetch of repeat blob sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
    Skipping fetch of repeat blob sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
    Skipping fetch of repeat blob sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
    Skipping fetch of repeat blob sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
    Skipping fetch of repeat blob sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
    Skipping fetch of repeat blob sha256:8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: mylolcow_latest.sif

This ``build`` results in a *local* copy of the Docker image in SIF, as did ``pull`` :ref:`above <sec:use_prebuilt_public_docker_images>`. Here, ``build`` has named the Apptainer container ``mylolcow_latest.sif``.
=======

Registries In Definition Files
==============================
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

When you wish to build from a Docker or OCI container that's hosted in
a registry, such as Docker Hub, your definition file should begin with
``Bootstrap: docker``, followed with a ``From:`` line which specifies
the location of the container you wish to pull.

Docker Hub
----------

Docker Hub is the default registry, so when building from Docker Hub
the ``From:`` header only needs to specify the container respository
and tag:

.. code-block:: singularity

<<<<<<< HEAD:apptainer_and_docker.rst
    $ apptainer build --sandbox mylolcow_latest_sandbox docker://godlovedc/lolcow
    INFO:    Starting build...
    Getting image source signatures
    Skipping fetch of repeat blob sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
    Skipping fetch of repeat blob sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
    Skipping fetch of repeat blob sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
    Skipping fetch of repeat blob sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
    Skipping fetch of repeat blob sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
    Skipping fetch of repeat blob sha256:8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating sandbox directory...
    INFO:    Build complete: mylolcow_latest_sandbox
=======
    Bootstrap: docker
    From: ubuntu:20.04
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

If you ``singularity build`` a definition file with these lines,
{Singularity} will fetch the ``ubuntu:20.04`` container image from
Docker Hub, and extract it as the basis for your new container.

Other Registries
----------------

<<<<<<< HEAD:apptainer_and_docker.rst
    bin  boot  core  dev  environment  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  apptainer  srv  sys  tmp  usr  var

The ``build`` command of Apptainer allows (e.g., development) sandbox containers to be converted into (e.g., production) read-only SIF containers, and vice-versa. Consult the :ref:`Build a container <build-a-container>` documentation for the details.

Implicit in the above command-line interactions is use of public images from Docker Hub. To make use of **private** images from Docker Hub, authentication is required. Available means for authentication were described above. Use of environment variables is functionally equivalent for Apptainer ``build`` as it is for ``pull``; see :ref:`Authentication via Environment Variables <sec:authentication_via_environment_variables>` above. For purely interactive use, authentication can be added to the ``build`` command as follows:
=======
To pull from a different Docker registry, you can either specify the
hostname in the ``From:`` header, or use the separate ``Registry:``
header. The following two examples are equivalent:


.. code-block:: singularity
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

    Bootstrap: docker
    From: quay.io/bitnami/python:3.7

<<<<<<< HEAD:apptainer_and_docker.rst
    apptainer build --docker-login mylolcow_latest_il.sif docker://ilumb/mylolcow
=======
.. code-block:: singularity
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

   Bootstrap: docker
   Registry: quay.io
   From: bitnami/python:3.7


Authentication During a Build
-----------------------------

<<<<<<< HEAD:apptainer_and_docker.rst
By making use of the `Sylabs Cloud Remote Builder <https://cloud.sylabs.io/builder>`_, it is possible to build SIF containers *remotely* from images hosted at Docker Hub. The Sylabs Cloud Remote Builder is a **service** that can be used from the Apptainer command line or via its Web interface. Here use of the Apptainer CLI is emphasized.

Once you have an account for Sylabs Cloud, and have logged in to the portal, select `Remote Builder <https://cloud.sylabs.io/builder>`_. The right-hand side of this page is devoted to use of the apptainer CLI. Self-generated API tokens are used to enable authenticated access to the Remote Builder. To create a token, follow the `instructions provided <https://cloud.sylabs.io/auth/tokens>`_. Once the token has been created, run ``apptainer remote login`` and paste it at the prompt.

The above token provides *authenticated* use of the Sylabs Cloud Remote Builder when ``--remote`` is *appended* to the Apptainer ``build`` command. For example, for remotely hosted images:
=======
If you are building from an image in a private registry you will need
to ensure that the credentials needed to access the image are
available to {Singularity}.

A build might be run as the ``root`` user, e.g. via ``sudo``, or under
your own account with ``--fakeroot``.

If you are running the build as ``root``, using ``sudo``, then any
stored credentials or environment variables must be available to the
``root`` user:
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

* Use the ``--docker-login`` flag for a one-time interactive
  login. I.E. run ``sudo singularity build --docker-login myimage.sif
  Singularity``.

<<<<<<< HEAD:apptainer_and_docker.rst
    $ apptainer build --remote lolcow_rb.sif docker://godlovedc/lolcow
    searching for available build agent.........INFO:    Starting build...
    Getting image source signatures
    Copying blob sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
     45.33 MiB / 45.33 MiB  0s
    Copying blob sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
     848 B / 848 B  0s
    Copying blob sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
     621 B / 621 B  0s
    Copying blob sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
     853 B / 853 B  0s
    Copying blob sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
     169 B / 169 B  0s
    Copying blob sha256:8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
     53.75 MiB / 53.75 MiB  0s
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB  0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: /tmp/image-341891107
    INFO:    Now uploading /tmp/image-341891107 to the library
     87.94 MiB / 87.94 MiB  100.00% 38.96 MiB/s 2s
    INFO:    Setting tag latest
     87.94 MiB / 87.94 MiB [===============================================================================] 100.00% 17.23 MiB/s 5s
=======
* Set the ``SINGULARITY_DOCKER_USERNAME`` and
  ``SINGULARITY_DOCKER_PASSWORD`` environment variables. Pass the
  environment variables through sudo to the ``root`` build process by
  running ``sudo -E singularity build ...``.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

* Run ``sudo singularity remote login ...`` to store your credentials
  for the ``root`` user on your system. This is separate from storing
  the credentials under your own account.

* Use ``sudo docker login`` if ``docker`` is on your
  machine. This is separate from storing the credentials under your
  own account.

<<<<<<< HEAD:apptainer_and_docker.rst
During the build process, progress can be monitored in the Sylabs Cloud portal on the Remote Builder page - as illustrated upon completion by the screenshot below. Once complete, this results in a *local* copy of the SIF file ``lolcow_rb.sif``. From the `Sylabs Library <https://cloud.sylabs.io/library>`_ it is evident that the 'original' SIF file remains available via this portal.
=======
If you are running the build under your account via the ``--fakeroot``
feature you do not need to specially set credentials for the root
user.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst


Archives & Docker Daemon
========================

As well as being hosted in a registry, Docker / OCI containers might
be found inside a running Docker daemon, or saved as an
archive. {Singularity} can build from these locations by using
specialised bootstrap agents.

Containers Cached by the Docker Daemon
--------------------------------------

<<<<<<< HEAD:apptainer_and_docker.rst
Apptainer containers can be built at the command line from images cached *locally* by Docker. Suppose, for example:
=======
If you have pulled or run a container on your machine under
``docker``, it will be cached locally by the Docker daemon. The
``docker images`` command will list containers that are available:
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

.. code-block:: none

    $ docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    sylabsio/lolcow     latest              5a15b484bc65        2 hours ago         188MB

This indicates that ``sylabsio/lolcow:latest`` has been cached locally
by Docker. You can directly build it into a SIF file using a
``docker-daemon://`` URI specifying the ``REPOSITORY:TAG`` container
name:

.. code-block:: none

<<<<<<< HEAD:apptainer_and_docker.rst
    $ sudo apptainer build lolcow_from_docker_cache.sif docker-daemon://godlovedc/lolcow:latest
=======
    $ singularity build lolcow_from_docker_cache.sif docker-daemon://sylabsio/lolcow:latest
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst
    INFO:    Starting build...
    Getting image source signatures
    Copying blob sha256:a2022691bf950a72f9d2d84d557183cb9eee07c065a76485f1695784855c5193
     119.83 MiB / 119.83 MiB [==================================================] 6s
    Copying blob sha256:ae620432889d2553535199dbdd8ba5a264ce85fcdcd5a430974d81fc27c02b45
     15.50 KiB / 15.50 KiB [====================================================] 0s
    Copying blob sha256:c561538251751e3685c7c6e7479d488745455ad7f84e842019dcb452c7b6fecc
     14.50 KiB / 14.50 KiB [====================================================] 0s
    Copying blob sha256:f96e6b25195f1b36ad02598b5d4381e41997c93ce6170cab1b81d9c68c514db0
     5.50 KiB / 5.50 KiB [======================================================] 0s
    Copying blob sha256:7f7a065d245a6501a782bf674f4d7e9d0a62fa6bd212edbf1f17bad0d5cd0bfc
     3.00 KiB / 3.00 KiB [======================================================] 0s
    Copying blob sha256:70ca7d49f8e9c44705431e3dade0636a2156300ae646ff4f09c904c138728839
     116.56 MiB / 116.56 MiB [==================================================] 6s
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: lolcow_from_docker_cache.sif

<<<<<<< HEAD:apptainer_and_docker.rst
results in ``lolcow_from_docker_cache.sif`` for native use by Apptainer. There are two important differences in syntax evident in the above ``build`` command:

1. The ``docker`` part of the URI has been appended by ``daemon``. This ensures Apptainer seek an image locally cached by Docker to bootstrap the conversion process to SIF, as opposed to attempting to retrieve an image remotely hosted via Docker Hub.
2. ``sudo`` is prepended to the ``build`` command for Apptainer; this is required as the Docker daemon executes as ``root``. However, if the user issuing the ``build`` command is a member of the ``docker`` Linux group, then ``sudo`` need not be prepended.

.. note::

    The image tag, in this case ``latest``, is **required** when bootstrapping creation of a container for Apptainer from an image locally cached by Docker.

.. note::

    The Sylabs Cloud Remote Builder *does not* interoperate with local Docker daemons; therefore, images cached locally by Docker, *cannot* be used to bootstrap creation of SIF files via the Remote Builder service. Of course, a SIF file could be created locally as detailed above. Then, in a separate, manual step, :ref:`pushed to the Sylabs Cloud apptainer Library <sec:pushing_locally_available_images_to_library>`.
=======
The tag name must be included in the URI. Unlike when pulling from a
registry, the ``docker-daemon`` bootstrap agent will not try to pull a
``latest`` tag automatically.


.. note::

   In the example above, the build was performed without
   ``sudo``. This is possible only when the user is part of the
   ``docker`` group on the host, since {Singularity} must contact the
   Docker daemon through its socket. If you are not part of the
   ``docker`` group you will need to use ``sudo`` for the build to
   complete successfully.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

To build from an image cached by the Docker daemon in a definition
file use ``Bootstrap: docker-daemon``, and a ``From:
<REPOSITORY>:TAG`` line:

.. code-block:: singularity

    Bootstrap: docker-daemon
    From: sylabsio/lolcow:latest


<<<<<<< HEAD:apptainer_and_docker.rst
apptainer containers can also be built at the command line from Docker images stored locally as ``tar`` files.
=======
Containers in Docker Archive Files
----------------------------------
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

Docker allows containers to be exported into single file tar
archives. These cannot be run directly, but are intended to be
imported into Docker to run at a later date, or another
location. {Singularity} can build from (or run) these archive files,
by extracting them as part of the build process.

<<<<<<< HEAD:apptainer_and_docker.rst
1. Obtain a local copy of the image from Docker Hub via ``sudo docker pull godlovedc/lolcow``. Issuing the following command confirms that a copy of the desired image is available locally:
=======
If an image is listed by the ``docker images`` command, then we can
create a tar archive file using ``docker save`` and the image ID:
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

.. code-block:: none

        $ sudo docker images
        REPOSITORY                        TAG               IMAGE ID       CREATED          SIZE
        sylabsio/lolcow                   latest            5a15b484bc65   2 hours ago      188MB

	$ docker save 5a15b484bc65 -o lolcow.tar

If we examine the contents of the tar file we can see that it contains
the layers and metadata that make up a Docker container:

.. code-block:: none

<<<<<<< HEAD:apptainer_and_docker.rst
    $ sudo tar tvf lolcow.tar
    drwxr-xr-x 0/0               0 2017-09-21 19:37 02aefa059d08482d344293d0ad27182a0a9d330ebc73abd92a1f9744844f91e9/
    -rw-r--r-- 0/0               3 2017-09-21 19:37 02aefa059d08482d344293d0ad27182a0a9d330ebc73abd92a1f9744844f91e9/VERSION
    -rw-r--r-- 0/0            1417 2017-09-21 19:37 02aefa059d08482d344293d0ad27182a0a9d330ebc73abd92a1f9744844f91e9/json
    -rw-r--r-- 0/0       122219008 2017-09-21 19:37 02aefa059d08482d344293d0ad27182a0a9d330ebc73abd92a1f9744844f91e9/layer.tar
    drwxr-xr-x 0/0               0 2017-09-21 19:37 3762e087ebbb895fd9c38981c1f7bfc76c9879fd3fdadef64df49e92721bb527/
    -rw-r--r-- 0/0               3 2017-09-21 19:37 3762e087ebbb895fd9c38981c1f7bfc76c9879fd3fdadef64df49e92721bb527/VERSION
    -rw-r--r-- 0/0             482 2017-09-21 19:37 3762e087ebbb895fd9c38981c1f7bfc76c9879fd3fdadef64df49e92721bb527/json
    -rw-r--r-- 0/0           14848 2017-09-21 19:37 3762e087ebbb895fd9c38981c1f7bfc76c9879fd3fdadef64df49e92721bb527/layer.tar
    -rw-r--r-- 0/0            4432 2017-09-21 19:37 577c1fe8e6d84360932b51767b65567550141af0801ff6d24ad10963e40472c5.json
    drwxr-xr-x 0/0               0 2017-09-21 19:37 5bad884501c0e760bc0c9ca3ae3dca3f12c4abeb7d18194c364fec522b91b4f9/
    -rw-r--r-- 0/0               3 2017-09-21 19:37 5bad884501c0e760bc0c9ca3ae3dca3f12c4abeb7d18194c364fec522b91b4f9/VERSION
    -rw-r--r-- 0/0             482 2017-09-21 19:37 5bad884501c0e760bc0c9ca3ae3dca3f12c4abeb7d18194c364fec522b91b4f9/json
    -rw-r--r-- 0/0            3072 2017-09-21 19:37 5bad884501c0e760bc0c9ca3ae3dca3f12c4abeb7d18194c364fec522b91b4f9/layer.tar
    drwxr-xr-x 0/0               0 2017-09-21 19:37 81ce2fd011bc8241ae72eaee9146116b7c289e941467ff276397720171e6c576/
    -rw-r--r-- 0/0               3 2017-09-21 19:37 81ce2fd011bc8241ae72eaee9146116b7c289e941467ff276397720171e6c576/VERSION
    -rw-r--r-- 0/0             406 2017-09-21 19:37 81ce2fd011bc8241ae72eaee9146116b7c289e941467ff276397720171e6c576/json
    -rw-r--r-- 0/0       125649920 2017-09-21 19:37 81ce2fd011bc8241ae72eaee9146116b7c289e941467ff276397720171e6c576/layer.tar
    drwxr-xr-x 0/0               0 2017-09-21 19:37 a10239905b060fd8b17ab31f37957bd126774f52f5280767d3b2639692913499/
    -rw-r--r-- 0/0               3 2017-09-21 19:37 a10239905b060fd8b17ab31f37957bd126774f52f5280767d3b2639692913499/VERSION
    -rw-r--r-- 0/0             482 2017-09-21 19:37 a10239905b060fd8b17ab31f37957bd126774f52f5280767d3b2639692913499/json
    -rw-r--r-- 0/0           15872 2017-09-21 19:37 a10239905b060fd8b17ab31f37957bd126774f52f5280767d3b2639692913499/layer.tar
    drwxr-xr-x 0/0               0 2017-09-21 19:37 ab6e1ca3392b2f4dbb60157cf99434b6975f37a767f530e293704a7348407634/
    -rw-r--r-- 0/0               3 2017-09-21 19:37 ab6e1ca3392b2f4dbb60157cf99434b6975f37a767f530e293704a7348407634/VERSION
    -rw-r--r-- 0/0             482 2017-09-21 19:37 ab6e1ca3392b2f4dbb60157cf99434b6975f37a767f530e293704a7348407634/json
    -rw-r--r-- 0/0            5632 2017-09-21 19:37 ab6e1ca3392b2f4dbb60157cf99434b6975f37a767f530e293704a7348407634/layer.tar
    -rw-r--r-- 0/0             574 1970-01-01 01:00 manifest.json

In other words, it is evident that this 'tarball' is a Docker-format image comprised of multiple layers along with metadata in a JSON manifest.

Through use of the ``docker-archive`` bootstrap agent, a SIF file (``lolcow_tar.sif``) for use by Apptainer can be created via the following ``build`` command:

.. code-block:: none

    $ apptainer build lolcow_tar.sif docker-archive://lolcow.tar
=======
    $ tar tvf lolcow.tar
    drwxr-xr-x  0 0      0           0 Aug 16 11:22 2f0514a4c044af1ff4f47a46e14b6d46143044522fcd7a9901124209d16d6171/
    -rw-r--r--  0 0      0           3 Aug 16 11:22 2f0514a4c044af1ff4f47a46e14b6d46143044522fcd7a9901124209d16d6171/VERSION
    -rw-r--r--  0 0      0         401 Aug 16 11:22 2f0514a4c044af1ff4f47a46e14b6d46143044522fcd7a9901124209d16d6171/json
    -rw-r--r--  0 0      0    75156480 Aug 16 11:22 2f0514a4c044af1ff4f47a46e14b6d46143044522fcd7a9901124209d16d6171/layer.tar
    -rw-r--r--  0 0      0        1499 Aug 16 11:22 5a15b484bc657d2b418f2c20628c29945ec19f1a0c019d004eaf0ca1db9f952b.json
    drwxr-xr-x  0 0      0           0 Aug 16 11:22 af7e389ea6636873dbc5adc17826e8401d96d3d384135b2f9fe990865af202ab/
    -rw-r--r--  0 0      0           3 Aug 16 11:22 af7e389ea6636873dbc5adc17826e8401d96d3d384135b2f9fe990865af202ab/VERSION
    -rw-r--r--  0 0      0         946 Aug 16 11:22 af7e389ea6636873dbc5adc17826e8401d96d3d384135b2f9fe990865af202ab/json
    -rw-r--r--  0 0      0   118356480 Aug 16 11:22 af7e389ea6636873dbc5adc17826e8401d96d3d384135b2f9fe990865af202ab/layer.tar
    -rw-r--r--  0 0      0         266 Dec 31  1969 manifest.json


We can convert this tar file into a singularity container using the
``docker-archive`` bootstrap agent. Because the agent accesses a file,
rather than an object hosted by a service, it uses ``:<filename>``,
not ``://<location>``. To build a tar archive directly to a SIF
container:

.. code-block:: none

    $ singularity build lolcow_tar.sif docker-archive:lolcow.tar
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst
    INFO:    Starting build...
    Getting image source signatures
    Copying blob sha256:2f0514a4c044af1ff4f47a46e14b6d46143044522fcd7a9901124209d16d6171
     119.83 MiB / 119.83 MiB [==================================================] 6s
    Copying blob sha256:af7e389ea6636873dbc5adc17826e8401d96d3d384135b2f9fe990865af202ab
     15.50 KiB / 15.50 KiB [====================================================] 0s
    Copying config sha256:5a15b484bc657d2b418f2c20628c29945ec19f1a0c019d004eaf0ca1db9f952b
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: lolcow_tar.sif

<<<<<<< HEAD:apptainer_and_docker.rst
There are two important differences in syntax evident in the above ``build`` command:

1. The ``docker`` part of the URI has been appended by ``archive``. This ensures Apptainer seek a Docker-format image archive stored locally as ``lolcow.tar`` to bootstrap the conversion process to SIF, as opposed to attempting to retrieve an image remotely hosted via Docker Hub.
2. ``sudo`` is *not* prepended to the ``build`` command for Apptainer. This is *not* required if the executing user has the appropriate access privileges to the stored file.

.. note::

    The ``docker-archive`` bootstrap agent handles archives (``.tar`` files) as well as compressed archives (``.tar.gz``) when containers are built for Apptainer via its ``build`` command.

.. note::

    The Sylabs Cloud Remote Builder *does not* interoperate with locally stored Docker-format images; therefore, images cached locally by Docker, *cannot* be used to bootstrap creation of SIF files via the Remote Builder service. Of course, a SIF file could be created locally as detailed above. Then, in a separate, manual step, :ref:`pushed to the Sylabs Library <sec:pushing_locally_available_images_to_library>`.


.. _sec:pushing_locally_available_images_to_library:
=======

.. note::

    The ``docker-archive`` bootstrap agent can also handle gzipped Docker
    archives (``.tar.gz`` or ``.tgz`` files).
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst


<<<<<<< HEAD:apptainer_and_docker.rst
The outcome of bootstrapping from an image cached locally by Docker, or one stored locally as an archive, is of course a *locally* stored SIF file. As noted above, this is the *only* option available, as the Sylabs Cloud Remote Builder *does not* interoperate with the Docker daemon or locally stored archives in the Docker image format. Once produced, however, it may be desirable to  make the resulting SIF file available through the Sylabs Library; therefore, the procedure to ``push`` a locally available SIF file to the Library is detailed here.

From the `Sylabs Cloud Library <https://library.sylabs.io/>`_, select ``Create a new Project``. In this first of two steps, the publicly accessible project is created as illustrated below:

.. image:: create_project.png
=======
To build an image using a definition file, which starts from a
container in a Docker archive, use ``Bootstrap: docker-archive`` and
specify the filename in the ``From:`` line:

.. code-block:: singularity
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

    Bootstrap: docker-archive
    From: lolcow.tar

.. _sec:optional_headers_def_files:

-------------------------------------
Differences and Limitations vs Docker
-------------------------------------

Though Docker / OCI container compatibility is a goal of
{Singularity}, there are some differences and limitations due to the
way {Singularity} was designed to work well on shared systems and HPC
clusters. If you are having difficulty running a specific Docker
container, check through the list of differences below. There are
workarounds for many of the issues that you are most likely to face.

Read-only by Default
====================

{Singularity}'s container image format (SIF) is generally
read-only. This permits containers to be run in parallel from a shared
location on a network filesystem, support in-built signing and
verification, and offer encryption. A container's filesystem is
mounted directly from the SIF, as SquashFS, so cannot be written to by
default.

When a container is run using Docker its layers are extracted, and the
resulting container filesystem can be written to and modified by
default. If a Docker container expects to write files, you will need
to follow one of the following methods to allow it to run under
{Singularity}.

* A directory from the host can be passed into the container with the
  ``--bind`` or ``--mount`` flags. It needs to be mounted inside the
  container at the location where files will be written.

* The ``--writable-tmpfs`` flag can be used to allow files to be
  created in a special temporary overlay. Any changes are lost when
  the container exits. The SIF file is never modified.

* The container can be converted to a sandbox directory, and executed
  with the ``--writable`` flag, which allows modification of the
  sandbox content.

* A writable overlay partition can be added to the SIF file, and the container
  executed with the ``--writable`` flag. Any changes made are kept
  permanently in the overlay partition.

Of these methods, only ``--writable-tmpfs`` is always safe to run in
parallel. Each time the container is executed, a separate temporary
overlay is used and then discarded.

Binding a directory into a container, or running a writable sandbox
may or may not be safe, depending on the program executed. The program
must use, and the filesystem support, some type of locking in order
that the parallel runs do not interfere.

A writable overlay file in a SIF partition cannot be used in
parallel. {Singularity} will refuse to run concurrently using the same
SIF writable overlay partition.

Dockerfile ``USER``
===================

The ``Dockerfile`` used to build a Docker container may contain a
``USER`` statement. This tells the container runtime that it should
run the container under the specified user account.

Because {Singularity} is designed to provide easy and safe access to
data on the host system, work under batch schedulers, etc., it does
not permit changing the user account the container is run as.

Any ``USER`` statement in a ``Dockerfile`` will be ignored by
{Singularity} when the container is run. In practice, this often does
not affect the execution of the software in the container. Software
that is written in a way that requires execution under a specific user
account will generally require modification for use with {Singularity}.

{Singularity}'s ``--fakeroot`` mode will start a container as a fake
``root`` user, mapped to the user's real account outside of the
container. Inside the container it is possible to change to another
user account, which is mapped to a configured range of sub-uids / gids
belonging to the original user. It may be possible to execute software
expecting a fixed user account manually inside a ``--fakeroot`` shell,
if your adminstrator has configured the system for ``--fakeroot``.

Default Mounts / $HOME
======================

A default installation of {Singularity} will mount the user's home
directory, ``/tmp`` directory, and the current working directory, into
each container that is run. Administrators may also configure e.g. HPC
project directories to automatically bind mount. Docker does not mount
host directories into the container by default.

The home directory mount is the most likely to cause problems when
running Docker containers. Various software will look for packages,
plugins, and configuration files in ``$HOME``. If you have, for
example, installed packages for Python into your home directory (``pip
install --user``) then a Python container may find and attempt to use
them. This can cause conflicts and unexpected behaviour.

If you experience issues, use the ``--contain`` option to stop
{Singularity} automatically binding directories into the
container. You may need to use ``--bind`` or ``--mount`` to then add
back e.g. an HPC project directory that you need access to.

.. code-block::

   # Without --contain, python in the container finds packages
   # in your $HOME directory.
   $ singularity exec docker://python:3.9 pip list
   Package    Version
   ---------- -------
   pip        21.2.4
   rstcheck   3.3.1
   setuptools 57.5.0
   wheel      0.37.0

   # With --contain, python in the container only finds packages
   # installed in the container.
   $ singularity exec --contain docker://python:3.9 pip list
   Package    Version
   ---------- -------
   pip        21.2.4
   setuptools 57.5.0
   wheel      0.37.0


Environment Propagation
=======================

{Singularity} propagates most environment variables set on the host
into the container, by default. Docker does not propagate any host
environment variables into the container. Environment variables may
change the behaviour of software.

To disable automatic propagation of environment variables, the
``--cleanenv / -e`` flag can be specified. When ``--cleanenv`` is
used, only variables on the host that are prefixed with
``SINGULARITYENV_`` are set in the container:

.. code-block:: none

<<<<<<< HEAD:apptainer_and_docker.rst
    $ apptainer push lolcow_tar.sif library://ilumb/default/lolcow_tar
    INFO:    Now uploading lolcow_tar.sif to the library
     87.94 MiB / 87.94 MiB [=============================================================================] 100.00% 1.25 MiB/s 1m10s
    INFO:    Setting tag latest


Finally, from the perspective of the Library, the *hosted* version of the SIF file appears as illustrated below. Directions on how to ``pull`` this file are included from the portal.

.. image:: lolcow_lib_listing.png

.. note::

    The hosted version of the SIF file in the Sylabs Cloud Apptainer Library is maintainable. In other words, if the image is updated locally, the update can be pushed to the Library and tagged appropriately.
=======
    # Set a host variable
    $ export HOST_VAR=123
    # Set a singularity container environment variable
    $ export "SINGULARITYENV_FORCE_VAR="123"

    $ singularity run library://alpine env | grep VAR
    FORCE_VAR=123
    HOST_VAR=ABC
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

    $ singularity run --cleanenv library://alpine env | grep VAR
    FORCE_VAR=123

<<<<<<< HEAD:apptainer_and_docker.rst
.. _sec:apptainer_build_def_files:
=======
Any environment variables set via an ``ENV`` line in a ``Dockerfile``
will be available when the container is run with {Singularity}.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst


Namespace & Device Isolation
============================

Because {Singularity} favors an integration over isolation approach it
does not, by default, use all the methods through which a container
can be isolated from the host system. This makes it much easier to run
a {Singularity} container like any other program, while the unique
security model ensures safety. You can access the host's network, GPUs,
and other devices directly. Processes in the container are not
numbered separately from host processes. Hostnames are not changed,
etc.

<<<<<<< HEAD:apptainer_and_docker.rst
Akin to a set of blueprints that explain how to build a custom container, Apptainer definition files (or "def files") are considered in detail :ref:`elsewhere in this manual <definition-files>`. Therefore, only def file nuances specific to interoperability with Docker receive consideration here.

Apptainer definition files are comprised of two parts - a **header** plus **sections**.
=======
Most containers are not impacted by the differences in isolation. If
you require more isolation, than {Singularity} provides by default, you
can enable some of the extra namespaces that Docker uses, with flags:

* ``--ipc / -i`` creates a separate IPC (inter process communication)
  namespace, for SystemV IPC objects and POSIX message queues.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

* ``--net / -n`` creates a new network namespace, abstracting the container
  networking from the host.

<<<<<<< HEAD:apptainer_and_docker.rst
.. code-block:: apptainer
=======
* ``--userns / -u`` runs the container unprivileged, inside a user
  namespace and avoiding setuid setup code. This prevents executing
  SIF images directly. They will be extracted to a directory sandbox.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

* ``--uts`` creates a new UTS namespace, which allows a different
  hostname and/or NIS domain for the container.

To limit presentation of devices from the host into the container, use
the ``--contain`` flag. As well as preventing automatic binds of host
directories into the container, ``--contain`` sets up a minimal
``/dev`` directory, rather than binding in the entire host ``/dev``
tree.

.. note::

<<<<<<< HEAD:apptainer_and_docker.rst
    sudo Apptainer build lolcow.sif lolcow.def

creates a Apptainer container in SIF by bootstrapping from the public ``godlovedc/lolcow`` image from Docker Hub.
=======
   When using the ``--nv`` or ``--rocm`` flags, GPU devices are
   present in the container even when ``--contain`` is used.

Init Shim Process
=================
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

When a {Singularity} container is run using the ``--pid / p`` option,
or started as an instance (which implies ``--pid``), a shim init
process is executed that will run the container payload itself.

The shim process helps to ensure signals are propagated correctly from
the terminal, or batch schedulers etc. when containers are not
designed for interactive use. Because Docker does not provide an init
process by default, some containers have been designed to run their
own init process, which cannot operate under the control of
{Singularity}'s shim.

For example, a container using the ``tini`` init process will produce
warnings when started as an instance, or if run with ``--pid``. To
work around this, use the ``--no-init`` flag to disable the shim:

<<<<<<< HEAD:apptainer_and_docker.rst
.. code-block:: apptainer
=======
.. code-block::
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

    $ singularity run --pid tini_example.sif
    [WARN  tini (2690)] Tini is not running as PID 1 .
    Zombie processes will not be re-parented to Tini, so zombie reaping won't work.
    To fix the problem, run Tini as PID 1.

    $ singularity run --pid --no-init tini_example.sif
    ...
    # NO WARNINGS

-----------------------------
Docker-like ``--compat`` Flag
-----------------------------

<<<<<<< HEAD:apptainer_and_docker.rst
    sudo apptainer build --docker-login mylolcow.sif mylolcow.def

creates a apptainer container in SIF by bootstrapping from the *private* ``ilumb/mylolcow`` image from Docker Hub after successful :ref:`interactive authentication <sec:authentication_via_docker_login>`.
=======
If Docker-like behavior is important, {Singularity} can be started
with the ``--compat`` flag. This flag is a convenient short-hand
alternative to using all of:

* ``--containall``
* ``--no-init``
* ``--no-umask``
* ``--writable-tmpfs``
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

A container run with ``--compat`` has:

* A writable root filesystem, using a temporary overlay where changes
  are discarded at container exit.

<<<<<<< HEAD:apptainer_and_docker.rst
    $ sudo -E apptainer build mylolcow.sif mylolcow.def
=======
* No automatic bind mounts of ``$HOME`` or other directories from the
  host into the container.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

* Empty temporary ``$HOME`` and ``/tmp`` directories, the contents of
  which will be discarded at container exit.

* A minimal ``/dev`` tree, that does not expose host devices inside
  the container (except GPUs when used with ``--nv`` or ``--rocm``).

<<<<<<< HEAD:apptainer_and_docker.rst
    The ``-E`` option is required to preserve the user's existing environment variables upon ``sudo`` invocation - a priviledge escalation *required* to create apptainer containers via the ``build`` command.
=======
* An clean environment, not including environment variables set on the
  host.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

* Its own PID and IPC namespaces.

* No shim init process.

These options will allow most, but not all, Docker / OCI containers to
execute correctly under {Singularity}. The user namespace and network
namespace are not used, as these negate benefits of SIF and direct
access to high performance cluster networks.

<<<<<<< HEAD:apptainer_and_docker.rst
.. code-block:: apptainer
=======
--------------------------
CMD / ENTRYPOINT Behaviour
--------------------------
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

When a container is run using ``docker``, its default behavior depends
on the ``CMD`` and/or ``ENTRYPOINT`` set in the ``Dockerfile`` that
was used to build it, along with any arguments on the command
line. The ``CMD`` and ``ENTRYPOINT`` can also be overridden by flags.

<<<<<<< HEAD:apptainer_and_docker.rst
With two small adjustments to the apptainer ``build`` command, the Sylabs Cloud Remote Builder can be utilized:
=======
A {Singularity} container has the concept of a *runscript*, which is a
single shell script defining what happens when you ``singularity run``
the container. Because there is no internal concept of ``CMD`` and
``ENTRYPOINT``, {Singularity} must create a runscript from the ``CMD``
and ``ENTRYPOINT`` when converting a Docker container. The behavior of
this script mirrors Docker as closely as possible.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

If the Docker container only has an ``ENTRYPOINT`` - that
``ENTRYPOINT`` is run, with any arguments appended:

.. code-block:: none

<<<<<<< HEAD:apptainer_and_docker.rst
    $ apptainer build --remote lolcow_rb_def.sif lolcow.def
    searching for available build agent......INFO:    Starting build...
    Getting image source signatures
    Copying blob sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
     45.33 MiB / 45.33 MiB  0s
    Copying blob sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
     848 B / 848 B  0s
    Copying blob sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
     621 B / 621 B  0s
    Copying blob sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
     853 B / 853 B  0s
    Copying blob sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
     169 B / 169 B  0s
    Copying blob sha256:8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
     53.75 MiB / 53.75 MiB  0s
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB  0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: /tmp/image-994007654
    INFO:    Now uploading /tmp/image-994007654 to the library
     87.94 MiB / 87.94 MiB  100.00% 41.76 MiB/s 2s
    INFO:    Setting tag latest
     87.94 MiB / 87.94 MiB [===============================================================================] 100.00% 19.08 MiB/s 4s

In the above, ``--remote`` has been added as the ``build`` option that causes use of the Remote Builder service. A much more subtle change, however, is the *absence* of ``sudo`` ahead of ``apptainer build``. Though subtle here, this absence is notable, as users can build containers via the Remote Builder with *escalated privileges*; in other words, steps in container creation that *require* ``root`` access *are* enabled via the Remote Builder even for (DevOps) users *without* admninistrative privileges locally.
=======
   # ENTRYPOINT="date"
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

   # Runs 'date'
   $ singularity run mycontainer.sif
   Wed 06 Oct 2021 02:42:54 PM CDT

   # Runs 'date --utc`
   $ singularity run mycontainer.sif --utc
   Wed 06 Oct 2021 07:44:27 PM UTC

If the Docker container only has a ``CMD`` - the ``CMD`` is run, or is
*replaced* with any arguments:

.. code-block:: none

<<<<<<< HEAD:apptainer_and_docker.rst
A copy of the SIF file created by the service remains in the Sylabs Cloud Apptainer Library as illustrated below.
=======
   # CMD="date"
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

   # Runs 'date'
   $ singularity run mycontainer.sif
   Wed 06 Oct 2021 02:45:39 PM CDT

   # Runs 'echo hello'
   $ singularity run mycontainer.sif echo hello
   hello

<<<<<<< HEAD:apptainer_and_docker.rst
    The Sylabs Cloud is currently available as an Alpha Preview. In addition to the Apptainer Library and Remote Builder, a Keystore service is also available. All three services make use of a *freemium* pricing model in supporting apptainer Community Edition. In contrast, all three services are included in apptainerPRO - an enterprise grade subscription for apptainer that is offered for a fee from Sylabs. For addtional details regarding the different offerings available for apptainer, please `consult the Sylabs website <https://www.sylabs.io/apptainer/>`_.
=======
If the Docker container has a ``CMD`` *and* ``ENTRYPOINT``, then we
run ``ENTRYPOINT`` with either ``CMD`` as default arguments, or
replaced with any user supplied arguments:
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

.. code-block:: none

   # ENTRYPOINT="date"
   # CMD="--utc"

   # Runs 'date --utc'
   $ singularity run mycontainer.sif
   Wed 06 Oct 2021 07:48:43 PM UTC

<<<<<<< HEAD:apptainer_and_docker.rst
When ``docker-daemon`` is the bootstrap agent in a Apptainer definition file, SIF containers can be created from images cached locally by Docker. Suppose the definition file ``lolcow-d.def`` has contents:

.. code-block:: apptainer
=======
   # Runs 'date -R'
   $ singularity run mycontainer.sif -R
   Wed, 06 Oct 2021 14:49:07 -0500

There is no flag to override an ``ENTRYPOINT`` set for a Docker
container. Instead, use ``singularity exec`` to run an arbitrary
program inside a container.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst


.. _sec:best_practices:

<<<<<<< HEAD:apptainer_and_docker.rst
    Again, the image tag ``latest`` is **required** when bootstrapping creation of a container for Apptainer from an image locally cached by Docker.
=======
-------------------------------------------------------
Best Practices for Docker & {Singularity} Compatibility
-------------------------------------------------------
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

As detailed previously, {Singularity} can make use of most Docker and
OCI images without issues, or via simple workarounds. In general,
however, there are some best practices that should be applied when
creating Docker / OCI containers that will also be run using
{Singularity}.


<<<<<<< HEAD:apptainer_and_docker.rst
    $ sudo apptainer build lolcow_from_docker_cache.sif lolcow-d.def
    Build target already exists. Do you want to overwrite? [N/y] y
    INFO:    Starting build...
    Getting image source signatures
    Copying blob sha256:a2022691bf950a72f9d2d84d557183cb9eee07c065a76485f1695784855c5193
     119.83 MiB / 119.83 MiB [==================================================] 6s
    Copying blob sha256:ae620432889d2553535199dbdd8ba5a264ce85fcdcd5a430974d81fc27c02b45
     15.50 KiB / 15.50 KiB [====================================================] 0s
    Copying blob sha256:c561538251751e3685c7c6e7479d488745455ad7f84e842019dcb452c7b6fecc
     14.50 KiB / 14.50 KiB [====================================================] 0s
    Copying blob sha256:f96e6b25195f1b36ad02598b5d4381e41997c93ce6170cab1b81d9c68c514db0
     5.50 KiB / 5.50 KiB [======================================================] 0s
    Copying blob sha256:7f7a065d245a6501a782bf674f4d7e9d0a62fa6bd212edbf1f17bad0d5cd0bfc
     3.00 KiB / 3.00 KiB [======================================================] 0s
    Copying blob sha256:70ca7d49f8e9c44705431e3dade0636a2156300ae646ff4f09c904c138728839
     116.56 MiB / 116.56 MiB [==================================================] 6s
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: lolcow_from_docker_cache.sif
=======
    1. **Don't require execution by a specific user**
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

    Avoid using the ``USER`` instruction in your Docker file, as it is
    ignored by Singularity. Install and configure software inside the
    container so that it can be run by any user.

    2. **Don't install software under /root or in another user's home
       directory**

<<<<<<< HEAD:apptainer_and_docker.rst
    The ``sudo`` requirement in the above ``build`` request originates from Apptainer; it is the standard requirement when use is made of definition files. In other words, membership of the issuing user in the ``docker`` Linux group is of no consequence in this context.
=======
    Because a Docker container builds and runs as the ``root`` user by
    default, it's tempting to install software into root's home
    directory (``/root``). Permissions on ``/root`` are usually set so
    that it is inaccessible to non-root users. When the container is
    run as another user the software may be inaccessible.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

    Software inside another user's home directory,
    e.g. ``/home/myapp``, may be obscured by {Singularity}'s automatic
    mounts onto ``/home``.

<<<<<<< HEAD:apptainer_and_docker.rst
Alternatively when ``docker-archive`` is the bootstrap agent in a Apptainer definition file, SIF containers can be created from images stored locally by Docker. Suppose the definition file ``lolcow-da.def`` has contents:

.. code-block:: apptainer
=======
    Install software into system-wide locations in the container,
    such as under ``/usr`` or ``/opt`` to avoid these issues.

    3. **Support a read-only filesystem**
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

    Because of the immutable nature of the SIF format, a container run
    with {Singularity} is read-only by default.

    Try to ensure your container will run with a read-only
    filesystem. If this is not possible, document exactly where the
    container needs to write, so that a user can bind in a writable
    location, or use ``--writable-tmpfs`` as appropriate.

    You can test read-only execution with Docker using ``docker
    run --read-only --tmpfs /run --tmpfs /tmp sylabsio/lolcow``.

<<<<<<< HEAD:apptainer_and_docker.rst
    $ sudo apptainer build lolcow_tar_def.sif lolcow-da.def
    INFO:    Starting build...
    Getting image source signatures
    Copying blob sha256:a2022691bf950a72f9d2d84d557183cb9eee07c065a76485f1695784855c5193
     119.83 MiB / 119.83 MiB [==================================================] 6s
    Copying blob sha256:ae620432889d2553535199dbdd8ba5a264ce85fcdcd5a430974d81fc27c02b45
     15.50 KiB / 15.50 KiB [====================================================] 0s
    Copying blob sha256:c561538251751e3685c7c6e7479d488745455ad7f84e842019dcb452c7b6fecc
     14.50 KiB / 14.50 KiB [====================================================] 0s
    Copying blob sha256:f96e6b25195f1b36ad02598b5d4381e41997c93ce6170cab1b81d9c68c514db0
     5.50 KiB / 5.50 KiB [======================================================] 0s
    Copying blob sha256:7f7a065d245a6501a782bf674f4d7e9d0a62fa6bd212edbf1f17bad0d5cd0bfc
     3.00 KiB / 3.00 KiB [======================================================] 0s
    Copying blob sha256:70ca7d49f8e9c44705431e3dade0636a2156300ae646ff4f09c904c138728839
     116.56 MiB / 116.56 MiB [==================================================] 6s
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: lolcow_tar_def.sif
=======
    4. **Be careful writing to /tmp**
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

    {Singularity} mounts the *host* ``/tmp`` into the container, by
    default. This means you must be be careful when writing sensitive
    information to ``/tmp``, and should ensure your container cleans
    up files it writes there.

    5. **Consider library caches / ldconfig**

    If your ``Dockerfile`` adds libraries and / or manipulates the ld
    search path in the container (``ld.so.conf`` / ``ld.so.conf.d``),
    you should ensure the library cache is updated during the build.

    Because Singularity runs containers read-only by default, the
    cache and any missing library symlinks may not be able to be
    updated / created at execution time.

    Run ``ldconfig`` toward the *end* of your ``Dockerfile`` to ensure
    symbolic links and the the ``ld.so.cache`` are up-to-date.


<<<<<<< HEAD:apptainer_and_docker.rst
.. code-block:: apptainer
=======
.. _sec:troubleshooting:
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

---------------
Troubleshooting
---------------

Registry Authentication Issues
==============================

If you experience problems pulling containers from a private registry,
check your credentials carefully. You can ``singularity pull`` with
the ``--docker-login`` flag to perform an interactive login. This may
be useful if you are unsure whether you have stored credentials
properly via ``singularity remote login`` or ``docker login``.

OCI registries expect different values for username and password
fields. Some require a token to be generated and used instead of your
account password. Some take a generic username, and rely only on the
token to identify you. Consult the documentation for your registry
carefully. Look for instructions that detail how to login via ``docker
login`` without external helper programs, if possible.

Container Doesn't Start
=======================

If a Docker container fails to start, the most common cause is that it
needs to write files, while {Singularity} runs read-only by default.

Try running with the ``--writable-tmpfs`` option, or the ``--compat``
flag (which enables additional compatibility fixes).

<<<<<<< HEAD:apptainer_and_docker.rst
Thus far, use of Docker Hub has been assumed. To make use of a different repository of Docker images the **optional** ``Registry`` keyword can be added to the Apptainer definition file. For example, to make use of a Docker image from the NVIDIA GPU Cloud (NGC) corresponding definition file is:

.. code-block:: apptainer
=======
You can also look for error messages mentioning 'permission denied' or
'read-only filesystem'. Note where the program is attempting to write,
and use ``--bind`` or ``--mount`` to bind a directory from the host
system into that location. This will allow the container to write the
needed files, which will appear in the directory you bind in.

Unexpected Container Behaviour
==============================
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst

If a Docker container runs, but exhibits unexpected behavior, the most
likely cause is the different level of isolation that Singularity
provides vs Docker.

Try running the container with the ``--contain`` option, or the
``--compat`` option (which is more strict). This disables the
automatic mount of your home directory, which is a common source of
issues where software in the container loads configuration or packages
that may be present there.

Getting Help
============

<<<<<<< HEAD:apptainer_and_docker.rst
    $ sudo apptainer build --docker-login mypytorch.sif ngc_pytorch.def
    Enter Docker Username: $oauthtoken
    Enter Docker Password: <obscured>
    INFO:    Starting build...
    Getting image source signatures
    Copying blob sha256:18d680d616571900d78ee1c8fff0310f2a2afe39c6ed0ba2651ff667af406c3e
     41.34 MiB / 41.34 MiB [====================================================] 2s
    <blob copying details deleted>
    Copying config sha256:b77551af8073c85588088ab2a39007d04bc830831ba1eef4127b2d39aaf3a6b1
    21.28 KiB / 21.28 KiB [====================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: mypytorch.sif
=======
The community Slack channels and mailing list are excellent places to
ask for help with running a specific Docker container. Other users may
have already had success running the same container or
software. Please don't report issues with specific Docker containers
on GitHub, unless you believe they are due to a bug in {Singularity}.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst


.. _sec:deffile-vs-dockerfile:

--------------------------------------------
{Singularity} Definition file vs. Dockerfile
--------------------------------------------

An alternative to running Docker containers with {Singularity} is to
re-write the ``Dockerfile`` as a definition file, and build a native
SIF image.

The table below gives a quick reference comparing Dockerfile and
{Singularity} definition files. For more detail please see :ref:`definition-files`.

================ =========================== ================ =============================
{Singularity} Definition file                Dockerfile
-------------------------------------------- ----------------------------------------------
Section          Description                 Section          Description
================ =========================== ================ =============================
``Bootstrap``    | Defines the source of
                 | the base image to build
                 | your container from.      \-               | Can only bootstrap
                 | Many bootstrap agents                      | from Docker Hub.
                 | are supported, e.g.
                 | ``library``, ``docker``,
                 | ``http``, ``shub``,
                 | ``yum``, ``debootstrap``.

``From:``        | Specifies the base        ``FROM``         | Creates a layer from
                 | image from which to the                    | the specified docker image.
                 | build the container.

``%setup``       | Run setup commands        \-               | Not supported.
                 | outside of the
                 | container (on the host
                 | system) after the base
                 | image bootstrap.

``%files``       | Copy files from           ``COPY``         | Copy files from
                 | your host to                               | your host to
                 | the container, or                          | the container, or
                 | between build stages.                      | between build stages.

``%environment`` | Declare and set           ``ENV``          | Declare and set
                 | container environment                      | a container environment
                 | variables.                                 | variable.

``%help``        | Provide a help
                 | section for your          \-               | Not supported.
                 | container image.

``%post``        | Commands that will                         | Commands that will
                 | be run at                 ``RUN``          | be run at
                 | build-time.                                | build-time.


``%runscript```  | Commands that will
                 | be run when you           ``ENTRYPOINT``   | Commands / arguments
                 | ``singularity run``       ``CMD``          | that will run in the
                 | the container image.                       | container image.

``%startscript`` | Commands that will
                 | be run when               \-               | Not Applicable.
                 | an instance is started.

<<<<<<< HEAD:apptainer_and_docker.rst
The execution-specific part of this ``Dockerfile`` is the ``ENTRYPOINT`` - "... an optional definition for the first part of the command to be run ..." according to `the available documentation <https://docs.docker.com/search/?q=ENTRYPOINT>`_. After conversion to SIF, execution of ``fortune | cowsay | lolcat`` *within* the container produces the output:

.. code-block:: none

    $ ./mylolcow.sif
     ______________________________________
    / Q: How did you get into artificial   \
    | intelligence? A: Seemed logical -- I |
    \ didn't have any real intelligence.   /
     --------------------------------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||



In addition, ``CMD`` allows an arbitrary string to be *appended* to the ``ENTRYPOINT``. Thus, multiple commands or flags can be passed together through combined use.

Suppose now that a Apptainer ``%runscript`` **section** is added to the definition file as follows:

.. code-block:: apptainer

    Bootstrap: docker
    Namespace: godlovedc
    From: lolcow

    %runscript

        fortune

After conversion to SIF via the Apptainer ``build`` command, exection of the resulting container produces the output:

.. code-block:: none

    $ ./lolcow.sif
    This was the most unkindest cut of all.
            -- William Shakespeare, "Julius Caesar"

In other words, introduction of a ``%runscript`` section into the Apptainer definition file causes the ``ENTRYPOINT`` of the ``Dockerfile`` to be *bypassed*. The presence of the ``%runscript`` section would also bypass a ``CMD`` entry in the ``Dockerfile``.

To *preserve* use of ``ENTRYPOINT`` and/or ``CMD`` as defined in the ``Dockerfile``, the ``%runscript`` section must be *absent* from the Apptainer definition. In this case, and to favor execution of ``CMD`` *over* ``ENTRYPOINT``, a non-empty assignment of the *optional* ``IncludeCmd`` should be included in the header section of the apptainer definition file as follows:

.. code-block:: apptainer

    Bootstrap: docker
    Namespace: godlovedc
    From: lolcow
    IncludeCmd: yes

.. note::

    Because only a non-empty ``IncludeCmd`` is required, *either* ``yes`` (as above) or ``no`` results in execution of ``CMD`` *over* ``ENTRYPOINT``.

.. _sec:def_files_execution_SUB_execution_precedence:

To summarize execution precedence:

1. If present, the ``%runscript`` section of the Apptainer definition file is executed
2. If ``IncludeCmd`` is a non-empty keyword entry in the header of the Apptainer definition file, then ``CMD`` from the ``Dockerfile`` is executed
3. If present in the ``Dockerfile``, ``ENTRYPOINT`` appended by ``CMD`` (if present) are executed in sequence
4. Execution of the ``bash`` shell is defaulted to

.. TODO-ND Test CMD vs ENTRYPOINT via a documented example

.. _sec:inspect_container_metadata:

Container Metadata
------------------

Apptainer's ``inspect`` command displays container metadata - data about data that is encapsulated *within* a SIF file. Default output (assumed via the ``--labels`` option) from the command was :ref:`illustrated above <sec:use_prebuilt_public_docker_images_SUB_inspect>`. ``inspect``, however, provides a number of options that are :ref:`detailed elsewhere <environment-and-metadata>`; in the remainder of this section, Docker-specific use to establish execution precedence is emphasized.

As stated above (i.e., :ref:`the first case of execution precedence <sec:def_files_execution_SUB_execution_precedence>`), the very existence of a ``%runscript`` section in a Apptainer definition file *takes precedence* over commands that might exist in the ``Dockerfile``.

When the ``%runscript`` section is *removed* from the Apptainer definition file, the result is (once again):

.. code-block:: none

    $ apptainer inspect --deffile lolcow.sif

    from: lolcow
    bootstrap: docker
    namespace: godlovedc

.. TODO-ND below ... Need to add a CMD to lolcow ...

The runscript 'inherited' from the ``Dockerfile`` is:

.. code-block:: none

    $ apptainer inspect --runscript lolcow.sif

    #!/bin/sh
    OCI_ENTRYPOINT='"/bin/sh" "-c" "fortune | cowsay | lolcat"'
    OCI_CMD=''
    # ENTRYPOINT only - run entrypoint plus args
    if [ -z "$OCI_CMD" ] && [ -n "$OCI_ENTRYPOINT" ]; then
        APPTAINER_OCI_RUN="${OCI_ENTRYPOINT} $@"
    fi

    # CMD only - run CMD or override with args
    if [ -n "$OCI_CMD" ] && [ -z "$OCI_ENTRYPOINT" ]; then
        if [ $# -gt 0 ]; then
            APPTAINER_OCI_RUN="$@"
        else
            APPTAINER_OCI_RUN="${OCI_CMD}"
        fi
    fi

    # ENTRYPOINT and CMD - run ENTRYPOINT with CMD as default args
    # override with user provided args
    if [ $# -gt 0 ]; then
        APPTAINER_OCI_RUN="${OCI_ENTRYPOINT} $@"
    else
        APPTAINER_OCI_RUN="${OCI_ENTRYPOINT} ${OCI_CMD}"
    fi

    eval ${APPTAINER_OCI_RUN}

From this Bourne shell script, it is evident that only an ``ENTRYPOINT`` is detailed in the ``Dockerfile``; thus the ``ENTRYPOINT only - run entrypoint plus args`` conditional block is executed. In this case then, :ref:`the third case of execution precedence <sec:def_files_execution_SUB_execution_precedence>` has been illustrated.

The above Bourne shell script also illustrates how the following scenarios will be handled:

- A ``CMD`` only entry in the ``Dockerfile``
- **Both** ``ENTRYPOINT`` *and* ``CMD`` entries in the ``Dockerfile``

From this level of detail, use of ``ENTRYPOINT`` *and/or* ``CMD`` in a Dockerfile has been made **explicit**. These remain examples within :ref:`the third case of execution precedence <sec:def_files_execution_SUB_execution_precedence>`.


-----------------
OCI Image Support
-----------------

.. _sec:oci_overview:


Overview
========

OCI is an acronym for the `Open Containers Initiative <https://www.opencontainers.org/>`_ - an independent organization whose mandate is to develop open standards relating to containerization. To date, standardization efforts have focused on container formats and runtimes; it is the former that is emphasized here. Stated simply, an **OCI blob** is content that can be addressed; in other words, *each* layer of a Docker image is rendered as an OCI blob as illustrated in the (revisited) ``pull`` example below.

.. note::

    To facilitate interoperation with Docker Hub, the Apptainer core makes use of  the ``containers/image`` `library <https://github.com/containers/image/>`_ - "... a set of Go libraries aimed at working in various way[s] with containers' images and container image registries."


Image Pulls Revisited
---------------------

After describing various :ref:`action commands that could be applied to images hosted remotely via Docker Hub <sec:action_commands_prebuilt_public_docker_images>`, the notion of having :ref:`a local copy in apptainer's native format for containerization (SIF) <sec:use_prebuilt_public_docker_images>` was introduced:

.. code-block:: none

    $ apptainer pull docker://godlovedc/lolcow
    INFO:    Starting build...
    Getting image source signatures
    Copying blob sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
     45.33 MiB / 45.33 MiB [====================================================] 1s
    Copying blob sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
     848 B / 848 B [============================================================] 0s
    Copying blob sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
     621 B / 621 B [============================================================] 0s
    Copying blob sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
     853 B / 853 B [============================================================] 0s
    Copying blob sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
     169 B / 169 B [============================================================] 0s
    Copying blob sha256:8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
     53.75 MiB / 53.75 MiB [====================================================] 2s
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: lolcow_latest.sif

Thus use of Apptainer's ``pull`` command results in the *local* file copy in SIF, namely ``lolcow_latest.sif``. Layers of the image from Docker Hub are copied locally as OCI blobs.

.. TODO minor - fix appearance of above link


Image Caching in Apptainer
----------------------------

If the *same* ``pull`` command is issued a *second* time, the output is different:

.. code-block:: none

    $ apptainer pull docker://godlovedc/lolcow
    INFO:    Starting build...
    Getting image source signatures
    Skipping fetch of repeat blob sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
    Skipping fetch of repeat blob sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
    Skipping fetch of repeat blob sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
    Skipping fetch of repeat blob sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
    Skipping fetch of repeat blob sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
    Skipping fetch of repeat blob sha256:8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: lolcow_latest.sif

As the copy operation has clearly been *skipped*, it is evident that a copy of all OCI blobs **must** be cached locally. Indeed, Apptainer has made an entry in its local cache as follows:

.. code-block:: none

    $ tree .apptainer/
    .apptainer/
    └── cache
        └── oci
            ├── blobs
            │   └── sha256
            │       ├── 3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
            │       ├── 73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
            │       ├── 7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
            │       ├── 8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
            │       ├── 9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
            │       ├── 9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
            │       ├── d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
            │       └── f2a852991b0a36a9f3d6b2a33b98a461e9ede8393482f0deb5287afcbae2ce10
            ├── index.json
            └── oci-layout

    4 directories, 10 files

.. _misc:OCI_Image_Layout_Specification:

Compliance with the OCI Image Layout Specification
--------------------------------------------------

From the perspective of the directory ``$HOME/.apptainer/cache/oci``, this cache implementation in Apptainer complies with the `OCI Image Layout Specification <https://github.com/opencontainers/image-spec/blob/master/image-layout.md>`_:

- ``blobs`` directory - contains content addressable data, that is otherwise considered opaque
- ``oci-layout`` file - a mandatory JSON object file containing both mandatory and optional content
- ``index.json`` file - a mandatory JSON object file containing an index of the images

Because one or more images is 'bundled' here, the directory ``$HOME/.apptainer/cache/oci`` is referred to as the ``$OCI_BUNDLE_DIR``.

For additional details regarding this specification, consult the `OCI Image Format Specification <https://github.com/opencontainers/image-spec>`_.


OCI Compliance and the Apptainer Cache
----------------------------------------

As required by the layout specification, OCI blobs are *uniquely* named by their contents:

.. code-block:: none

    $ shasum -a 256 ./blobs/sha256/9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
    9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118  ./blobs/sha256/9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118

They are also otherwise opaque:

.. code-block:: none

    $ file ./blobs/sha256/9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118 ./blobs/sha256/9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118: gzip compressed data

The content of the ``oci-layout`` file in this example is:

.. code-block:: javascript

    $ cat oci-layout | jq
    {
      "imageLayoutVersion": "1.0.0"
    }

This is as required for compliance with the layout standard.

.. note::

    In rendering the above JSON object files, use has been made of ``jq`` - the command-line JSON processor.

The index of images in this case is:

.. code-block:: javascript

    $ cat index.json | jq
    {
      "schemaVersion": 2,
      "manifests": [
        {
          "mediaType": "application/vnd.oci.image.manifest.v1+json",
          "digest": "sha256:f2a852991b0a36a9f3d6b2a33b98a461e9ede8393482f0deb5287afcbae2ce10",
          "size": 1125,
          "annotations": {
            "org.opencontainers.image.ref.name": "a692b57abc43035b197b10390ea2c12855d21649f2ea2cc28094d18b93360eeb"
          },
          "platform": {
            "architecture": "amd64",
            "os": "linux"
          }
        }
      ]
    }

The ``digest`` blob in this index file includes the details for all of the blobs that collectively comprise the ``godlovedc/lolcow`` image:

.. code-block:: javascript

    $ cat  ./blobs/sha256/f2a852991b0a36a9f3d6b2a33b98a461e9ede8393482f0deb5287afcbae2ce10 | jq
    {
      "schemaVersion": 2,
      "config": {
        "mediaType": "application/vnd.oci.image.config.v1+json",
        "digest": "sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82",
        "size": 3410
      },
      "layers": [
        {
          "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
          "digest": "sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118",
          "size": 47536248
        },
        {
          "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
          "digest": "sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a",
          "size": 848
        },
        {
          "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
          "digest": "sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2",
          "size": 621
        },
        {
          "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
          "digest": "sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e",
          "size": 853
        },
        {
          "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
          "digest": "sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9",
          "size": 169
        },
        {
          "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
          "digest": "sha256:8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945",
          "size": 56355961
        }
      ]
    }

The ``digest`` blob referenced in the ``index.json`` file references the following configuration file:

.. code-block:: javascript

    $ cat ./blobs/sha256/73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82 | jq
    {
      "created": "2017-09-21T18:37:47.278336798Z",
      "architecture": "amd64",
      "os": "linux",
      "config": {
        "Env": [
          "PATH=/usr/games:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
          "LC_ALL=C"
        ],
        "Entrypoint": [
          "/bin/sh",
          "-c",
          "fortune | cowsay | lolcat"
        ]
      },
      "rootfs": {
        "type": "layers",
        "diff_ids": [
          "sha256:a2022691bf950a72f9d2d84d557183cb9eee07c065a76485f1695784855c5193",
          "sha256:ae620432889d2553535199dbdd8ba5a264ce85fcdcd5a430974d81fc27c02b45",
          "sha256:c561538251751e3685c7c6e7479d488745455ad7f84e842019dcb452c7b6fecc",
          "sha256:f96e6b25195f1b36ad02598b5d4381e41997c93ce6170cab1b81d9c68c514db0",
          "sha256:7f7a065d245a6501a782bf674f4d7e9d0a62fa6bd212edbf1f17bad0d5cd0bfc",
          "sha256:70ca7d49f8e9c44705431e3dade0636a2156300ae646ff4f09c904c138728839"
        ]
      },
      "history": [
        {
          "created": "2017-09-18T23:31:37.453092323Z",
          "created_by": "/bin/sh -c #(nop) ADD file:5ed435208da6621b45db657dd6549ee132cde58c4b6763920030794c2f31fbc0 in / "
        },
        {
          "created": "2017-09-18T23:31:38.196268404Z",
          "created_by": "/bin/sh -c set -xe \t\t&& echo '#!/bin/sh' > /usr/sbin/policy-rc.d \t&& echo 'exit 101' >> /usr/sbin/policy-rc.d \t&& chmod +x /usr/sbin/policy-rc.d \t\t&& dpkg-divert --local --rename --add /sbin/initctl \t&& cp -a /usr/sbin/policy-rc.d /sbin/initctl \t&& sed -i 's/^exit.*/exit 0/' /sbin/initctl \t\t&& echo 'force-unsafe-io' > /etc/dpkg/dpkg.cfg.d/docker-apt-speedup \t\t&& echo 'DPkg::Post-Invoke { \"rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true\"; };' > /etc/apt/apt.conf.d/docker-clean \t&& echo 'APT::Update::Post-Invoke { \"rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true\"; };' >> /etc/apt/apt.conf.d/docker-clean \t&& echo 'Dir::Cache::pkgcache \"\"; Dir::Cache::srcpkgcache \"\";' >> /etc/apt/apt.conf.d/docker-clean \t\t&& echo 'Acquire::Languages \"none\";' > /etc/apt/apt.conf.d/docker-no-languages \t\t&& echo 'Acquire::GzipIndexes \"true\"; Acquire::CompressionTypes::Order:: \"gz\";' > /etc/apt/apt.conf.d/docker-gzip-indexes \t\t&& echo 'Apt::AutoRemove::SuggestsImportant \"false\";' > /etc/apt/apt.conf.d/docker-autoremove-suggests"
        },
        {
          "created": "2017-09-18T23:31:38.788043199Z",
          "created_by": "/bin/sh -c rm -rf /var/lib/apt/lists/*"
        },
        {
          "created": "2017-09-18T23:31:39.411670721Z",
          "created_by": "/bin/sh -c sed -i 's/^#\\s*\\(deb.*universe\\)$/\\1/g' /etc/apt/sources.list"
        },
        {
          "created": "2017-09-18T23:31:40.055188541Z",
          "created_by": "/bin/sh -c mkdir -p /run/systemd && echo 'docker' > /run/systemd/container"
        },
        {
          "created": "2017-09-18T23:31:40.215057796Z",
          "created_by": "/bin/sh -c #(nop)  CMD [\"/bin/bash\"]",
          "empty_layer": true
        },
        {
          "created": "2017-09-21T18:37:46.483638061Z",
          "created_by": "/bin/sh -c apt-get update && apt-get install -y fortune cowsay lolcat"
        },
        {
          "created": "2017-09-21T18:37:47.041333952Z",
          "created_by": "/bin/sh -c #(nop)  ENV PATH=/usr/games:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
          "empty_layer": true
        },
        {
          "created": "2017-09-21T18:37:47.170535967Z",
          "created_by": "/bin/sh -c #(nop)  ENV LC_ALL=C",
          "empty_layer": true
        },
        {
          "created": "2017-09-21T18:37:47.278336798Z",
          "created_by": "/bin/sh -c #(nop)  ENTRYPOINT [\"/bin/sh\" \"-c\" \"fortune | cowsay | lolcat\"]",
          "empty_layer": true
        }
      ]
    }

.. TODO Is the above not the config.json file referred to at https://github.com/opencontainers/runtime-spec/blob/master/config.md ???

Even when all OCI blobs are already in Apptainer's local cache, repeated image pulls cause *both* these last-two JSON object files, as well as the ``oci-layout`` and ``index.json`` files, to be updated.


Building Containers for Apptainer from OCI Images
===================================================

.. _cli-oci-bootstrap-agent:

Working Locally from the Apptainer Command Line: ``oci`` Bootstrap Agent
--------------------------------------------------------------------------

The example detailed in the previous section can be used to illustrate how a SIF file for use by Apptainer can be created from the local cache - an albeit contrived example, that works because the Apptainer cache is compliant with the OCI Image Layout Specification.

.. note::

    Of course, the ``oci`` bootstrap agent can be applied to *any* **bundle** that is compliant with the OCI Image Layout Specification - not *just* the Apptainer cache, as created by executing a Apptainer ``pull`` command.

In this local case, the ``build`` command of Apptainer makes use of the ``oci`` bootstrap agent as follows:

.. code-block:: none

    $ apptainer build ~/lolcow_oci_cache.sif oci://$HOME/.apptainer/cache/oci:a692b57abc43035b197b10390ea2c12855d21649f2ea2cc28094d18b93360eeb
    INFO:    Starting build...
    Getting image source signatures
    Skipping fetch of repeat blob sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
    Skipping fetch of repeat blob sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
    Skipping fetch of repeat blob sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
    Skipping fetch of repeat blob sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
    Skipping fetch of repeat blob sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
    Skipping fetch of repeat blob sha256:8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: /home/vagrant/lolcow_oci_cache.sif

As can be seen, this results in the SIF file ``lolcow_oci_cache.sif`` in the user's home directory.

The syntax for the ``oci`` bootstrap agent requires some elaboration, however. In this case, and as illustrated above, ``$HOME/.apptainer/cache/oci`` has content:

.. code-block:: none

    $ ls
    blobs  index.json  oci-layout


In other words, it is the ``$OCI_BUNDLE_DIR`` containing the data and metadata that collectively comprise the image layed out in accordance with the OCI Image Layout Specification :ref:`as discussed previously <misc:OCI_Image_Layout_Specification>` - the same data and metadata that are assembled into a single SIF file through the ``build`` process. However,

.. code-block:: none

    $ apptainer build ~/lolcow_oci_cache.sif oci://$HOME/.apptainer/cache/oci
    INFO:    Starting build...
    FATAL:   While performing build: conveyor failed to get: more than one image in oci, choose an image

does not *uniquely* specify an image from which to bootstrap the ``build`` process. In other words, there are multiple images referenced via ``org.opencontainers.image.ref.name`` in the ``index.json`` file. By appending ``:a692b57abc43035b197b10390ea2c12855d21649f2ea2cc28094d18b93360eeb`` to ``oci`` in this example, the image is uniquely specified, and the container created in SIF (as illustrated previously).

.. note::

    Executing the Apptainer ``pull`` command multiple times on the same image produces multiple ``org.opencontainers.image.ref.name`` entries in the ``index.json`` file. Appending the value of the unique ``org.opencontainers.image.ref.name`` allows for use of the ``oci`` bootstrap agent.


.. _cli-oci-archive-bootstrap-agent:

Working Locally from the Apptainer Command Line: ``oci-archive`` Bootstrap Agent
----------------------------------------------------------------------------------

OCI archives, i.e., ``tar`` files obeying the OCI Image Layout Specification :ref:`as discussed previously <misc:OCI_Image_Layout_Specification>`, can seed creation of a container for Apptainer. In this case, use is made of the ``oci-archive`` bootstrap agent.

To illustrate this agent, it is convenient to build the archive from the Apptainer cache. After a single ``pull`` of the ``godlovedc/lolcow`` image from Docker Hub, a ``tar`` format archive can be generated from the ``$HOME/.apptainer/cache/oci`` directory as follows:

.. code-block:: none

    $ tar cvf $HOME/godlovedc_lolcow.tar *
    blobs/
    blobs/sha256/
    blobs/sha256/73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
    blobs/sha256/8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
    blobs/sha256/9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
    blobs/sha256/3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
    blobs/sha256/9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
    blobs/sha256/d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
    blobs/sha256/f2a852991b0a36a9f3d6b2a33b98a461e9ede8393482f0deb5287afcbae2ce10
    blobs/sha256/7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
    index.json
    oci-layout

The native container ``lolcow_oci_tarfile.sif`` for use by Apptainer can be created by issuing the ``build`` command as follows:

.. code-block:: none

    $ apptainer build lolcow_oci_tarfile.sif oci-archive://godlovedc_lolcow.tar
    Build target already exists. Do you want to overwrite? [N/y] y
    INFO:    Starting build...
    Getting image source signatures
    Skipping fetch of repeat blob sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
    Skipping fetch of repeat blob sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
    Skipping fetch of repeat blob sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
    Skipping fetch of repeat blob sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
    Skipping fetch of repeat blob sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
    Skipping fetch of repeat blob sha256:8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: lolcow_oci_tarfile.sif

This assumes that the ``tar`` file exists in the current working directory.

.. note::

    Cache maintenance is a manual process at the current time. In other words, the cache can be cleared by **carefully** issuing the command ``rm -rf $HOME/.apptainer/cache``. Of course, this will clear the local cache of all downloaded images.

.. TODO-ND: Update owing to intro of new capab???

.. note::

    Because the layers of a Docker image as well as the blobs of an OCI image are already ``gzip`` compressed, there is a minimal advantage to having compressed archives representing OCI images. For this reason, the ``build`` detailed above bootstraps a SIF file for use by apptainer from only a ``tar`` file, and not a ``tar.gz`` file.


Working from the Apptainer Command Line with Remotely Hosted Images
---------------------------------------------------------------------

In the previous section, an OCI archive was created from locally available OCI blobs and metadata; the resulting ``tar`` file served to bootstrap the creation of a container for apptainer in SIF via the ``oci-archive`` agent. Typically, however, OCI archives of interest are remotely hosted. Consider, for example, an Alpine Linux OCI archive stored in Amazon S3 storage. Because such an archive can be retrieved via secure HTTP, the following ``pull`` command results in a local copy as follows:

.. code-block:: none

    $ apptainer pull https://s3.amazonaws.com/apptainer-ci-public/alpine-oci-archive.tar
     1.98 MiB / 1.98 MiB [==================================================================================] 100.00% 7.48 MiB/s 0s

Thus ``https`` (and ``http``) are additional bootstrap agents available to seed development of containers for Apptainer.

It is worth noting that the OCI image specfication compliant contents of this archive are:

.. code-block:: none

    $ tar tvf alpine-oci-archive.tar
    drwxr-xr-x 1000/1000         0 2018-06-25 14:45 blobs/
    drwxr-xr-x 1000/1000         0 2018-06-25 14:45 blobs/sha256/
    -rw-r--r-- 1000/1000       585 2018-06-25 14:45 blobs/sha256/b1a7f144ece0194921befe57ab30ed1fd98c5950db7996719429020986092058
    -rw-r--r-- 1000/1000       348 2018-06-25 14:45 blobs/sha256/d0ff39a54244ba25ac7447f19941765bee97b05f37ceb438a72e80c9ed39854a
    -rw-r--r-- 1000/1000   2065537 2018-06-25 14:45 blobs/sha256/ff3a5c916c92643ff77519ffa742d3ec61b7f591b6b7504599d95a4a41134e28
    -rw-r--r-- 1000/1000       296 2018-06-25 14:45 index.json
    -rw-r--r-- 1000/1000        31 2018-06-25 14:45 oci-layout

Proceeding as before, for a (now) locally available OCI archive, a SIF file can be produced by executing:

.. code-block:: none

    $ apptainer build alpine_oci_archive.sif oci-archive://alpine-oci-archive.tar
    INFO:    Starting build...
    Getting image source signatures
    Copying blob sha256:ff3a5c916c92643ff77519ffa742d3ec61b7f591b6b7504599d95a4a41134e28
     1.97 MiB / 1.97 MiB [======================================================] 0s
    Copying config sha256:b1a7f144ece0194921befe57ab30ed1fd98c5950db7996719429020986092058
     585 B / 585 B [============================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: alpine_oci_archive.sif

The resulting SIF file can be validated as follows, for example:

.. code-block:: none

    $ ./alpine_oci_archive.sif
    apptainer> cat /etc/os-release
    NAME="Alpine Linux"
    ID=alpine
    VERSION_ID=3.7.0
    PRETTY_NAME="Alpine Linux v3.7"
    HOME_URL="http://alpinelinux.org"
    BUG_REPORT_URL="http://bugs.alpinelinux.org"
    apptainer>
    $

.. note::


    The ``http`` and ``https`` bootstrap agents can only be used to ``pull`` OCI archives from where they are hosted.

    In working with remotely hosted OCI image archives then, a two-step workflow is *required* to produce SIF files for native use by Apptainer:

    1. Transfer of the image to local storage via the ``https`` (or ``http``) bootstrap agent. The Apptainer ``pull`` command achieves this.
    2. Creation of a SIF file via the ``oci-archive`` bootstrap agent. The Apptainer ``build`` command achieves this.
    
    Established with nothing more than a Web server then, any individual, group or organization, *could* host OCI archives. This might be particularly appealing, 
    
    for example, for organizations having security requirements that preclude access to public registries such as Docker Hub. Other that having a very basic hosting capability, OCI archives need only comply to the OCI Image Layout Specification :ref:`as discussed previously <misc:OCI_Image_Layout_Specification>`.

Working with Definition Files: Mandatory Header Keywords
--------------------------------------------------------

Three, new bootstrap agents have been introduced as a consequence of compliance with the OCI Image Specification - assuming ``http`` and ``https`` are considered together. In addition to bootstrapping images for apptainer completely from the command line, definition files can be employed.

As :ref:`above <cli-oci-bootstrap-agent>`, the OCI image layout compliant Apptainer cache can be employed to create SIF containers; the definition file, ``lolcow-oci.def``, equivalent is:


.. code-block:: apptainer

    Bootstrap: oci
    From: .apptainer/cache/oci:a692b57abc43035b197b10390ea2c12855d21649f2ea2cc28094d18b93360eeb

Recall that the colon-appended string in this file uniquely specifies the ``org.opencontainers.image.ref.name`` of the desired image, as more than one possibility exists in the ``index.json`` file. The corresponding ``build`` command is:

.. code-block:: none

    $ sudo apptainer build ~/lolcow_oci_cache.sif lolcow-oci.def
    WARNING: Authentication token file not found : Only pulls of public images will succeed
    Build target already exists. Do you want to overwrite? [N/y] y
    INFO:    Starting build...
    Getting image source signatures
    Copying blob sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
     45.33 MiB / 45.33 MiB [====================================================] 0s
    Copying blob sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
     848 B / 848 B [============================================================] 0s
    Copying blob sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
     621 B / 621 B [============================================================] 0s
    Copying blob sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
     853 B / 853 B [============================================================] 0s
    Copying blob sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
     169 B / 169 B [============================================================] 0s
    Copying blob sha256:8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
     53.75 MiB / 53.75 MiB [====================================================] 0s
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: /home/vagrant/lolcow_oci_cache.sif

Required use of ``sudo`` allows Apptainer to ``build`` the SIF container ``lolcow_oci_cache.sif``.

When it comes to OCI archives, the definition file, ``lolcow-ocia.def`` corresponding to the command-line invocation above is:

.. code-block:: apptainer

    Bootstrap: oci-archive
    From: godlovedc_lolcow.tar

Applying ``build`` as follows

.. code-block:: none

    $ sudo apptainer build lolcow_oci_tarfile.sif lolcow-ocia.def
    WARNING: Authentication token file not found : Only pulls of public images will succeed
    INFO:    Starting build...
    Getting image source signatures
    Skipping fetch of repeat blob sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
    Skipping fetch of repeat blob sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
    Skipping fetch of repeat blob sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
    Skipping fetch of repeat blob sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
    Skipping fetch of repeat blob sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
    Skipping fetch of repeat blob sha256:8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: lolcow_oci_tarfile.sif

results in the SIF container ``lolcow_oci_tarfile.sif``.


Working with Definition Files: Additonal Considerations
-------------------------------------------------------

In working with definition files, the following additional considerations arise:

- In addition to the mandatory header keywords documented above, :ref:`optional header keywords <sec:optional_headers_def_files>` are possible additions to OCI bundle and/or archive bootstrap definition files.
- As distribution of OCI bundles and/or archives is out of the Initiative's scope, so is the authentication required to access private images and/or registries.
- The direction of execution follows along the same lines :ref:`as described above <sec:def_files_execution>`. Of course, the SIF container's metadata will make clear the ``runscript`` through application of the ``inspect`` command :ref:`as described previously <sec:inspect_container_metadata>`.
- Container metadata will also reveal whether or not a given SIF file was bootstrapped from an OCI bundle or archive; for example, below it is evident that an OCI archive was employed to bootstrap creation of the SIF file:

.. code-block:: javascript

    $ apptainer inspect --labels lolcow_oci_tarfile.sif | jq
    {
      "org.label-schema.build-date": "Sunday_27_January_2019_0:5:29_UTC",
      "org.label-schema.schema-version": "1.0",
      "org.label-schema.usage.apptainer.deffile.bootstrap": "oci-archive",
      "org.label-schema.usage.apptainer.deffile.from": "godlovedc_lolcow.tar",
      "org.label-schema.usage.apptainer.version": "3.0.3-1"
    }


.. _sec:docker_cache:

-----------------
Container Caching
-----------------

To avoid fetching duplicate docker or OCI layers every time you want to ``run``, ``exec`` etc. a ``docker://`` or ``oci://`` container directly, Apptainer keeps a cache of layer files. The SIF format container that apptainer creates from these layers is also cached. This means that re-running a docker container, e.g. ``apptainer run docker://alpine`` is much faster until the upstream image changes in docker hub, and a new SIF must be built from updated layers.

By default the cache directory is ``.apptainer/cache`` in your ``$HOME`` directory. You can modify the cache directory by setting the ``APPTAINER_CACHEDIR`` environment variable. To disable caching altogether, set the ``apptainer_DISABLE_CACHE`` environment variable.

The ``apptainer cache`` command can be used to see the content of your cache dir, and clean the cache if needed:

.. code-block:: none
                
    $ apptainer cache list
    There are 10 container file(s) using 4.75 GB and 78 oci blob file(s) using 5.03 GB of space
    Total space used: 9.78 GB

    $ apptainer cache clean
    This will delete everything in your cache (containers from all sources and OCI blobs). 
    Hint: You can see exactly what would be deleted by canceling and using the --dry-run option.
    Do you want to continue? [N/y] y
    Removing /home/dave/.apptainer/cache/library
    Removing /home/dave/.apptainer/cache/oci-tmp
    Removing /home/dave/.apptainer/cache/shub
    Removing /home/dave/.apptainer/cache/oci
    Removing /home/dave/.apptainer/cache/net
    Removing /home/dave/.apptainer/cache/oras

For a more complete guide to caching and the ``cache`` command, see the :ref:`build-environment` page.

    
.. _sec:best_practices:

--------------
Best Practices
--------------

Apptainer can make use of most Docker and OCI images without complication. However, there exist  known cases where complications can arise. Thus a brief compilation of best practices follows below.

1. Accounting for trust
Docker containers *allow for* privilege escalation. In a ``Dockerfile``, for example, the ``USER`` instruction allows for user and/or group settings to be made in the Linux operating environment. The trust model in Apptainer is completely different: Apptainer allows untrusted users to run untrusted containers in a trusted way. Because Apptainer containers embodied as SIF files execute in *user* space, there is no possibility for privilege escalation. In other words, those familiar with Docker, should *not* expect access to elevated user permissions; and as a corollary, use of the ``USER`` instruction must be *avoided*.
Apptainer does, however, allow for fine-grained control over the permissions that containers require for execution. Given that Apptainer executes in user space, it is not surprising that permissions need to be externally established *for* the container through use of the ``capability`` command. :ref:`Detailed elsewhere in this documentation <security-options>`, Apptainer allows users and/or groups to be granted/revoked authorized capabilties. Owing to Apptainer's trust model, this fundamental best practice can be stated as follows:

"Employ ``apptainer capability`` to manage execution privileges for containers"
2. Maintaining containers built from Docker and OCI images
SIF files created by bootstrapping from Docker or OCI images are, of course, only as current as the most recent Apptainer ``pull``. Subsequent retrievals *may* result in containers that are built and/or behave differently, owing to changes in the corresponding ``Dockerfile``. A prudent practice then, for maintaining containers of value, is based upon use of apptainer definition files. Styled and implemented after a ``Dockerfile`` retrieved at some point in time, use of ``diff`` on subsequent versions of this same file, can be employed to inform maintenance of the corresponding apptainer definition file. Understanding build specifications at this level of detail places container creators in a much more sensible position prior to signing with an encrypted key. Thus the best practice is:

"Maintain detailed build specifications for containers, rather than opaque runtimes"
3. Working with environment variables

In a ``Dockerfile``, `environment variables are declared <https://docs.docker.com/engine/reference/builder/#env>`_ as key-value pairs through use of the ``ENV`` instruction. Declaration in the build specification for a container is advised, rather than relying upon user
(e.g., ``.bashrc``, ``.profile``) or system-wide configuration files for interactive shells. Should a ``Dockerfile`` be converted into a definition file for Apptainer, as suggested in the container-maintenance best practice above, :ref:`environment variables can be explicitly represented <definition-files>` as ``ENV`` instructions that have been converted into entries in the ``%environment`` section, respectively. This best practice can be stated as follows:
"Define environment variables in container specifications, not interactive shells"
4. Installation to ``/root``
Docker and OCI container's are typically run as the ``root`` user; therefore, ``/root`` (this user's ``$HOME`` directory) will be the installation target when ``$HOME`` is specified. Installation to ``/root`` may prove workable in some circumstances - e.g., while the container is executing, or if read-only access is required to this directory after installation. In general, however, because this is the ``root`` directory conventional wisdom suggests this practice be avoided. Thus the best practice is:
"Avoid installations that make use of ``/root``."
5. Read-only ``/`` filesystem
Apptainer mounts a container's ``/`` filesystem in read-only mode. To ensure a Docker container meets Apptainer's requirements, it may prove useful to execute ``docker run --read-only --tmpfs /run --tmpfs /tmp godlovedc/lolcow``. The best practioce here is:
"Ensure Docker containers meet Apptainer's read-only ``/`` filesystem requirement"
6. Installation to ``$HOME`` or ``$TMP``
In making use of Apptainer, it is common practice for ``$USER`` to be automatically mounted on ``$HOME``, and for ``$TMP`` also to be mounted. To avoid the side effects (e.g., 'missing' or conflicting files) that might arise as a consequence of executing ``mount`` commands then, the best practice is:
"Avoid placing container 'valuables' in ``$HOME`` or ``$TMP``."
A detailed review of the container's build specification (e.g., its ``Dockerfile``) may be required to ensure this best practice is adhered to.
7. Current library caches
Irrespective of containers, `a common runtime error <https://codeyarns.com/2014/01/14/how-to-fix-shared-object-file-error/>`_ stems from failing to locate shared libraries required for execution. Suppose now there exists a requirement for symbolically linked libraries *within* a Apptainer container. If the builld process that creates the container fails to update the cache, then it is quite likely that (read-only) execution of this container will result in the common error of missing libraries. Upon investigation, it is likely revealed that the library exists, just not the required symbolic links. Thus the best practice is:
"Ensure calls to ``ldconfig`` are executed towards the *end* of ``build`` specifications (e.g., ``Dockerfile``), so that the library cache is updated when the container is created."
8. Use of plain-text passwords for authentication
For obvious reasons, it is desireable to completely *avoid* use of plain-text passwords. Therefore, for interactive sessions requiring authentication, use of the ``--docker-login`` option for Apptainer's ``pull`` and ``build`` commands is *recommended*. At the present time, the *only* option available for non-interactive use is to :ref:`embed plain-text passwords into environment variables <sec:authentication_via_environment_variables>`. Because the Sylabs Cloud apptainer Library employs `time-limited API tokens for authentication <https://cloud.sylabs.io/auth>`_, use of SIF containers hosted through this service provides a more secure means for both interactive *and* non-interactive use. This best practice is:
"Avoid use of plain-text passwords"
9. Execution ambiguity
Short of converting an *entire* ``Dockerfile`` into a Apptainer definition file, informed specification of the ``%runscript`` entry in the def file *removes* any ambiguity associated with ``ENTRYPOINT`` :ref:`versus <sec:def_files_execution>` ``CMD`` and ultimately :ref:`execution precedence <sec:def_files_execution>`. Thus the best practice is:
"Employ Apptainer's ``%runscript`` by default to avoid execution ambiguity"
Note that the ``ENTRYPOINT`` can be bypassed completely, e.g., ``docker run -i -t --entrypoint /bin/bash godlovedc/lolcow``. This allows for an interactive session within the container, that may prove useful in validating the built runtime.
Best practices emerge from experience. Contributions that allow additional experiences to be shared as best practices are always encouraged. Please refer to :ref:`Contributing <contributing>` for additional details.


.. _sec:troubleshooting:

---------------
Troubleshooting
---------------

In making use of Docker and OCI images through Apptainer the need to troubleshoot may arise. A brief compilation of issues and their resolution is provided here.

1. Authentication issues
Authentication is required to make use of Docker-style private images and/or private registries. Examples involving private images hosted by the public Docker Hub were :ref:`provided above <sec:using_prebuilt_private_images>`, whereas the NVIDIA GPU Cloud was used to :ref:`illustrate access to a private registry <sec:using_prebuilt_private_images_parivate_registries>`. Even if the intended use of containers is non-interactive, issues in authenticating with these image-hosting services are most easily addressed through use of the ``--docker-login`` option that can be appended to a Apptainer ``pull`` request. As soon as image signatures and blobs start being received, authentication credentials have been validated, and the image ``pull`` can be cancelled.
2. Execution mismatches
Execution intentions are detailed through specification files - i.e., the ``Dockerfile`` in the case of Docker images. However, intentions and precedence aside, the reality of executing a container may not align with expectations. To alleviate this mismatch, use of ``apptainer inspect --runscript <somecontainer>.sif`` details the *effective* runscript - i.e., the one that is actually being executed. Of course, the ultimate solution to this issue is to develop and maintain Apptainer definition files for containers of interest.
3. More than one image in the OCI bundle directory
:ref:`As illustrated above <cli-oci-bootstrap-agent>`, and with respect to the bootstrap agent ``oci://$OCI_BUNDLE_DIR``, a fatal error is generated when *more* than one image is referenced in the ``$OCI_BUNDLE_DIR/index.json`` file. The workaround shared previously was to append the bootstrap directive with the unique reference name for the image of interest - i.e., ``oci://$OCI_BUNDLE_DIR:org.opencontainers.image.ref.name``. Because it may take some effort to locate the reference name for an image of interest, an even simpler solution is to ensure that each ``$OCI_BUNDLE_DIR`` contains at most a single image.
4. Cache maintenance
Maintenance of the Apptainer cache (i.e., ``$HOME/.apptainer/cache``) requires manual intervention at this time. By **carefully** issuing the command ``rm -rf $HOME/.apptainer/cache``, its local cache will be cleared of all downloaded images.
5. The ``http`` and ``https`` are ``pull`` only bootstrap agents
``http`` and ``https`` are the only examples of ``pull`` only bootstrap agents. In other words, when used with Apptainer's ``pull`` command, the result is a local copy of, for example, an OCI archive image. This means that a subsequent step is necessary to actually create a SIF container for use by Apptainer - a step involving the ``oci-archive`` bootstrap agent in the case of an OCI image archive.

Like :ref:`best practices <sec:best_practices>`, troubleshooting scenarios and solutions emerge from experience. Contributions that allow additional experiences to be shared  are always encouraged. Please refer to :ref:`Contributing <contributing>` for additional details.

.. TODO-ND SIFtool - does it have more to offer here???

.. _sec:deffile-vs-dockerfile:

------------------------------------------
Apptainer Definition file vs. Dockerfile
------------------------------------------

On the following table, you can see which are the similarities/differences between a Dockerfile and a Apptainer definition file:

================ ========================== ================ =============================
Apptainer Definition file                   Dockerfile
------------------------------------------- ----------------------------------------------
Section          Description                Section          Description
================ ========================== ================ =============================
``Bootstrap``    | Defines from which
                 | library to build
                 | your container from.      \-              | Can only bootstrap
                 | You are free to choose                    | from Docker Hub.
                 | between ``library``
                 | (Our cloud library)
                 | , ``docker`` , ``shub``
                 | and ``oras``.

``From:``        | To specify the provider   ``FROM``        | Creates a layer from
                 | from which to build the                   | the described docker image.
                 | container.                                | For example, if you got a
                                                             | Dockerfile with the ``FROM``
                                                             | section set like:
                                                             | ``FROM:ubuntu:18.04``,
                                                             | this means that a layer
                                                             | will be created from the
                                                             | ``ubuntu:18.04``
                                                             | **Docker** image.
                                                             | (You cannot choose any
                                                             | other bootstrap provider)

``%setup``       | Commands that run        \-               | Not supported.
                 | outside the
                 | container (in the host
                 | system) after the base
                 | OS has been installed.

``%files``       | To copy files from
                 | your local               ``COPY``         | To copy files from your
                 | to the host.                              | Docker's client current
                                                             | directory.

``%environment`` | To declare and set       ``ENV``          | ``ENV`` will take the name
                 | your environment                          | of the variable and the
                 | variables.                                | value and set it.

``%help``        | To provide a help
                 | section to your          \-               | Not supported on the
                 | container image.                          | Dockerfile.

``%post``        | Commands that will
                 | be run at                ``RUN``          | Commands to build your
                 | build-time.                               | application image
                                                             | with ``make``

``%runscript```  | Commands that will
                 | be run at                ``CMD``          | Commands that run
                 | running your                              | within the Docker
                 | container image.                          | container.

``%startscript`` | Commands that will
                 | be run when                \-             | Not supported.
                 | an instance is started.
                 | This is useful for
                 | container images
                 | using services.

``%test``        | Commands that run
                 | at the very end          ``HEALTHCHECK``  | Commands that verify
                 | of the build process                      | the health status of
                 | to validate the                           | the container.
=======
``%test``        | Commands that run
                 | at the very end           ``HEALTHCHECK``  | Commands that verify
                 | of the build process                       | the health status of
                 | to validate the                            | the container.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543:singularity_and_docker.rst
                 | container using
                 | a method of your
                 | choice. (to verify
                 | distribution or
                 | software versions
                 | installed inside
                 | the container)

``%apps``        | Allows you to install
                 | internal modules           \-              | Not supported.
                 | based on the concept
                 | of SCIF-apps.

``%labels``      | Section to add and
                 | define metadata           ``LABEL``        | Declare container
                 | describing your                            | metadata as a
                 | container.                                 | key-value pair.

================ =========================== ================ =============================
