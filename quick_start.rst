.. _quick-start:

#############
 Quick Start
#############

.. _sec:quickstart:

This guide is intended for running {Project} on a computer where you
have root (administrative) privileges, and will install {Project}
from source code. Other installation options, including building an RPM
package and installing {Project} without root privileges are
discussed in the `installation section of the admin guide
<{admindocs}/installation.html>`__.

If you need to request an installation on your shared resource, see the
:ref:`requesting an installation section <installation-request>` for
information to send to your system administrator.

For any additional help or support contact the {Project} Community:
https://apptainer.org/help

.. _quick-installation:

**************************
 Quick Installation Steps
**************************

You will need a Linux system to run {Project} natively. Options for
using {Project} on Mac and Windows machines, along with alternate
Linux installation options are discussed in the `installation section of
the admin guide
<{admindocs}/installation.html>`__.

Install system dependencies
===========================

You must first install development tools and libraries to your host.

On Debian-based systems, including Ubuntu:

.. code::

   # Ensure repositories are up-to-date
   sudo apt-get update
   # Install debian packages for dependencies
   sudo apt-get install -y \
      build-essential \
      libseccomp-dev \
      pkg-config \
      squashfs-tools \
      cryptsetup \
      curl wget git

On CentOS/RHEL:

.. code::

   # Install basic tools for compiling
   sudo yum groupinstall -y 'Development Tools'
   # Ensure EPEL repository is available
   sudo yum install -y epel-release
   # Install RPM packages for dependencies
   sudo yum install -y \
      libseccomp-devel \
      squashfs-tools \
      cryptsetup \
      wget git

There are 3 broad steps to installing {Project}:

#. :ref:`Installing Go <install>`
#. :ref:`Downloading {Project} <download>`
#. :ref:`Compiling {Project} Source Code <compile>`

.. _install:

Install Go
==========

{Project} is written in Go, and may require a newer version of Go than is
available in the repositories of your distribution. We recommend installing the
latest version of Go from the [official binaries](https://golang.org/dl/).

{Project} aims to maintain support for the two most recent stable versions
of Go. This corresponds to the Go Release Maintenance Policy and Security
Policy, ensuring critical bug fixes and security patches are available for all
supported language versions.

If you are building rpm or debian packages using the packaging supplied
in the ``dist`` directory, and the operating system distribution of Go
is below the minimum required by {Project}, the packages can make
use of the native Go to compile a newer version of Go whose source
tarball is included with the package source.  That capability is
supplied so packages can be built on systems with no access to the
internet.  If you are not building a package or don't want to incur the
overhead of compiling the Go toolchain from source, install a local
binary copy of Go as follows.

.. note::

   If you have previously installed Go from a download, rather than an
   operating system package, you should remove your ``go`` directory,
   e.g. ``rm -r /usr/local/go`` before installing a newer version.
   Extracting a new version of Go over an existing installation can lead
   to errors when building Go programs, as it may leave old files, which
   have been removed or replaced in newer versions.

Visit the `Go Downloads page <https://golang.org/dl/>`_ and pick a
package archive suitable to the environment you are in. Once the
Download is complete, extract the archive to ``/usr/local`` (or use
other instructions on go installation page). Alternatively, follow the
commands here:

.. code::

   $ export VERSION=1.17.5 OS=linux ARCH=amd64 && \  # Replace the values as needed
     wget https://dl.google.com/go/go$VERSION.$OS-$ARCH.tar.gz && \ # Downloads the required Go package
     sudo tar -C /usr/local -xzvf go$VERSION.$OS-$ARCH.tar.gz && \ # Extracts the archive
     rm go$VERSION.$OS-$ARCH.tar.gz    # Deletes the ``tar`` file

Set the Environment variable ``PATH`` to point to Go:

.. code::

   $ echo 'export PATH=/usr/local/go/bin:$PATH' >> ~/.bashrc && \
     source ~/.bashrc

.. _download:

Download {Project} from a release
=====================================

You can download {Project} from one of the releases. To see a full
list, visit `the GitHub release page
<https://github.com/{orgrepo}/releases>`_. After deciding on a
release to install, you can run the following commands to proceed with
the installation.

.. code::

   $ export VERSION={InstallationVersion} && # adjust this as necessary \
       wget https://github.com/{orgrepo}/releases/download/v${VERSION}/{command}-${VERSION}.tar.gz && \
       tar -xzf {command}-${VERSION}.tar.gz && \
       cd {command}-${VERSION}

.. _compile:

Compile the {Project} source code
=====================================

Now you are ready to build {Project}. Dependencies will be
automatically downloaded. You can build {Project} using the
following commands:

.. code::

   $ ./mconfig && \
       make -C builddir && \
       sudo make -C builddir install

{Project} must be installed as root to function properly.

*****************************************
 Overview of the {Project} Interface
*****************************************

{Project}’s :ref:`command line interface <cli>` allows you to build
and interact with containers transparently. You can run programs inside
a container as if they were running on your host system. You can easily
redirect IO, use pipes, pass arguments, and access files, sockets, and
ports on the host system from within a container.

The ``help`` command gives an overview of {Project} options and
subcommands as follows:

.. code::

   $ {command} help

   Linux container platform optimized for High Performance Computing (HPC) and
   Enterprise Performance Computing (EPC)

   Usage:
     {command} [global options...]

   Description:
     {Project} containers provide an application virtualization layer enabling
     mobility of compute via both application and environment portability. With
     {Project} one is capable of building a root file system that runs on any
     other Linux system where {Project} is installed.

   Options:
     -d, --debug     print debugging information (highest verbosity)
     -h, --help      help for {command}
         --nocolor   print without color output (default False)
     -q, --quiet     suppress normal output
     -s, --silent    only print errors
     -v, --verbose   print additional information

   Available Commands:
     build       Build a {Project} image
     cache       Manage the local cache
     capability  Manage Linux capabilities for users and groups
     exec        Run a command within a container
     help        Help about any command
     inspect     Show metadata for an image
     instance    Manage containers running as services
     key         Manage OpenPGP keys
     oci         Manage OCI containers
     plugin      Manage {command} plugins
     pull        Pull an image from a URI
     push        Upload image to the provided library (default is "cloud.sylabs.io")
     remote      Manage {command} remote endpoints
     run         Run the user-defined default command within a container
     run-help    Show the user-defined help for an image
     search      Search a Container Library for images
     shell       Run a shell within a container
     sif         siftool is a program for Singularity Image Format (SIF) file manipulation
     sign        Attach a cryptographic signature to an image
     test        Run the user-defined tests within a container
     verify      Verify cryptographic signatures attached to an image
     version     Show the version for {Project}

   Examples:
     $ {command} help <command> [<subcommand>]
     $ {command} help build
     $ {command} help instance start


   For additional help or support, please visit https://www.apptainer.org/docs/

Information about subcommand can also be viewed with the ``help``
command.

.. code::

   $ {command} help verify
   Verify cryptographic signatures attached to an image

   Usage:
     {command} verify [verify options...] <image path>

   Description:
     The verify command allows a user to verify cryptographic signatures on SIF
     container files. There may be multiple signatures for data objects and
     multiple data objects signed. By default the command searches for the primary
     partition signature. If found, a list of all verification blocks applied on
     the primary partition is gathered so that data integrity (hashing) and
     signature verification is done for all those blocks.

   Options:
     -a, --all               verify all objects
     -g, --group-id uint32   verify objects with the specified group ID
     -h, --help              help for verify
     -j, --json              output json
         --legacy-insecure   enable verification of (insecure) legacy signatures
     -l, --local             only verify with local keys
     -i, --sif-id uint32     verify object with the specified ID
     -u, --url string        key server URL (default "https://keys.openpgp.org")


   Examples:
     $ {command} verify container.sif


   For additional help or support, please visit https://www.apptainer.org/docs/

{Project} uses positional syntax (i.e. the order of commands and
options matters). Global options affecting the behavior of all commands
follow the main ``{command}`` command. Then sub commands are followed
by their options and arguments.

For example, to pass the ``--debug`` option to the main ``{command}``
command and run {Project} with debugging messages on:

.. code::

   $ {command} --debug run library://lolcow

To pass the ``--containall`` option to the ``run`` command and run a
{Project} image in an isolated manner:

.. code::

   $ {command} run --containall library://lolcow

{Project} has the concept of command groups. For
instance, to list Linux capabilities for a particular user, you would
use the ``list`` command in the ``capability`` command group like so:

.. code::

   $ {command} capability list dave

Container authors might also write help docs specific to a container or
for an internal module called an ``app``. If those help docs exist for a
particular container, you can view them like so.

.. code::

   $ {command} inspect --helpfile container.sif  # See the container's help, if provided

   $ {command} inspect --helpfile --app=foo foo.sif  # See the help for foo, if provided

***************************
 Download pre-built images
***************************

You can use the ``search`` command to locate groups, collections, and
containers of interest on the `Container Library
<https://cloud.sylabs.io/library>`_ .

.. code::

   {command} search tensorflow
   Found 22 container images for amd64 matching "tensorflow":

       library://ajgreen/default/tensorflow2-gpu-py3-r-jupyter:latest
               Current software: tensorflow2; py3.7; r; jupyterlab1.2.6
               Signed by: 1B8565093D80FA393BC2BD73EA4711C01D881FCB

       library://bensonyang/collection/tensorflow-rdma_v4.sif:latest

       library://dxtr/default/hpc-tensorflow:0.1

       library://emmeff/tensorflow/tensorflow:latest

       library://husi253/default/tensorflow:20.01-tf1-py3-mrcnn-2020.10.07

       library://husi253/default/tensorflow:20.01-tf1-py3-mrcnn-20201014

       library://husi253/default/tensorflow:20.01-tf2-py3-lhx-20201007

       library://irinaespejo/default/tensorflow-gan:sha256.0c1b6026ba2d6989242f418835d76cd02fc4cfc8115682986395a71ef015af18

       library://jon/default/tensorflow:1.12-gpu
               Signed by: D0E30822F7F4B229B1454388597B8AFA69C8EE9F

       ...

You can use the `pull
<cli/{command}_pull.html>`_
and `build
<cli/{command}_build.html>`_
commands to download pre-built images from an external resource like the
`Container Library <https://cloud.sylabs.io/library>`_ or `Docker Hub
<https://hub.docker.com/>`_.

When called on a native {Project} image like those provided on the
Container Library, ``pull`` simply downloads the image file to your
system.

.. code::

   $ {command} pull library://lolcow

You can also use ``pull`` with the ``docker://`` uri to reference Docker
images served from a registry. In this case ``pull`` does not just
download an image file. Docker images are stored in layers, so ``pull``
must also combine those layers into a usable {Project} file.

.. code::

   $ {command} pull docker://sylabsio/lolcow

Pulling Docker images reduces reproducibility. If you were to pull a
Docker image today and then wait six months and pull again, you are not
guaranteed to get the same image. If any of the source layers has
changed the image will be altered. If reproducibility is a priority for
you, try building your images from the Container Library.

You can also use the ``build`` command to download pre-built images from
an external resource. When using ``build`` you must specify a name for
your container like so:

.. code::

   $ {command} build ubuntu.sif library://ubuntu

   $ {command} build lolcow.sif docker://sylabsio/lolcow

Unlike ``pull``, ``build`` will convert your image to the latest
{Project} image format after downloading it. ``build`` is like a
“Swiss Army knife” for container creation. In addition to downloading
images, you can use ``build`` to create images from other images or from
scratch using a :ref:`definition file <definition-files>`. You can also
use ``build`` to convert an image between the container formats
supported by {Project}. To see a comparison of {Project}
definition file with Dockerfile, please see: :ref:`this section
<sec:deffile-vs-dockerfile>`.

.. _cowimage:

**********************
 Interact with images
**********************

You can interact with images in several ways, each of which can accept
image URIs in addition to a local image path.

For demonstration, we will use a ``lolcow_latest.sif`` image that can be
pulled from the Container Library:

.. code::

   $ {command} pull library://lolcow

Shell
=====

The `shell
<cli/{command}_shell.html>`_
command allows you to spawn a new shell within your container and
interact with it as though it were a small virtual machine.

.. code::

   $ {command} shell lolcow_latest.sif

   {Project} lolcow_latest.sif:~>

The change in prompt indicates that you have entered the container
(though you should not rely on that to determine whether you are in
container or not).

Once inside of a {Project} container, you are the same user as you
are on the host system.

.. code::

   {Project} lolcow_latest.sif:~> whoami
   david

   {Project} lolcow_latest.sif:~> id
   uid=1000(david) gid=1000(david) groups=1000(david),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare)

``shell`` also works with the ``library://``, ``docker://``, and
``shub://`` URIs. This creates an ephemeral container that disappears
when the shell is exited.

.. code::

   $ {command} shell library://lolcow

Executing Commands
==================

The `exec
<cli/{command}_exec.html>`_
command allows you to execute a custom command within a container by
specifying the image file. For instance, to execute the ``cowsay``
program within the ``lolcow_latest.sif`` container:

.. code::

   $ {command} exec lolcow_latest.sif cowsay moo
    _____
   < moo >
    -----
           \   ^__^
            \  (oo)\_______
               (__)\       )\/\
                   ||----w |
                   ||     ||

``exec`` also works with the ``library://``, ``docker://``, and
``shub://`` URIs. This creates an ephemeral container that executes a
command and disappears.

.. code::

   $ {command} exec library://lolcow cowsay "Fresh from the library!"
    _________________________
   < Fresh from the library! >
    -------------------------
           \   ^__^
            \  (oo)\_______
               (__)\       )\/\
                   ||----w |
                   ||     ||

.. _runcontainer:

Running a container
===================

{Project} containers contain :ref:`runscripts <runscript>`. These
are user defined scripts that define the actions a container should
perform when someone runs it. The runscript can be triggered with the
`run
<cli/{command}_run.html>`_
command, or simply by calling the container as though it were an
executable.

.. code::

   $ {command} run lolcow_latest.sif
   ______________________________
   < Mon Aug 16 13:01:55 CDT 2021 >
    ------------------------------
           \   ^__^
            \  (oo)\_______
               (__)\       )\/\
                   ||----w |
                   ||     ||

   $ ./lolcow_latest.sif
   ______________________________
   < Mon Aug 16 13:12:50 CDT 2021 >
    ------------------------------
           \   ^__^
            \  (oo)\_______
               (__)\       )\/\
                   ||----w |
                   ||     ||

``run`` also works with the ``library://``, ``docker://``, and
``shub://`` URIs. This creates an ephemeral container that runs and then
disappears.

.. code::

   $ {command} run library://lolcow
   ______________________________
   < Mon Aug 16 13:12:33 CDT 2021 >
    ------------------------------
           \   ^__^
            \  (oo)\_______
               (__)\       )\/\
                   ||----w |
                   ||     ||


Arguments to ``run``
--------------------

You can pass arguments to the runscript of a container, if it accepts
them. For example, the default runscript of the ``library://alpine``
container passes any arguments to a shell. We can ask the container
to run ``echo`` command in this shell:

.. code::

   $ {command} run library://alpine echo "hello"

   hello

Because {Project} runscripts are evaluated shell scripts
arguments can behave slightly differently than in Docker/OCI
runtimes, if they contain shell code that may be evaluated. To
replicate Docker/OCI behaviour you may need additional escaping or
quoting of arguments.

.. code::

   $ docker run -it --rm alpine echo "\$HOSTNAME"
   $HOSTNAME

   $ {command} run docker://alpine echo "\$HOSTNAME"
   p700

   $ {command} run docker://alpine echo "\\\$HOSTNAME"
   $HOSTNAME

The ``exec`` command replicates the Docker/OCI behavior as it calls
the specified executable directly.

********************
 Working with Files
********************

Files on the host are reachable from within the container.

.. code::

   $ echo "Hello from inside the container" > $HOME/hostfile.txt

   $ {command} exec lolcow_latest.sif cat $HOME/hostfile.txt

   Hello from inside the container

This example works because ``hostfile.txt`` exists in the user’s home
directory. By default {Project} bind mounts ``/home/$USER``,
``/tmp``, and ``$PWD`` into your container at runtime.

You can specify additional directories to bind mount into your container
with the ``--bind`` option. In this example, the ``data`` directory on
the host system is bind mounted to the ``/mnt`` directory inside the
container.

.. code::

   $ echo "Drink milk (and never eat hamburgers)." > /data/cow_advice.txt

   $ {command} exec --bind /data:/mnt lolcow_latest.sif cat /mnt/cow_advice.txt
   Drink milk (and never eat hamburgers).

Pipes and redirects also work with {Project} commands just like they
do with normal Linux commands.

.. code::

   $ cat /data/cow_advice.txt | {command} exec lolcow_latest.sif cowsay
    ________________________________________
   < Drink milk (and never eat hamburgers). >
    ----------------------------------------
           \   ^__^
            \  (oo)\_______
               (__)\       )\/\
                   ||----w |
                   ||     ||

.. _build-images-from-scratch:

***************************
 Build images from scratch
***************************

.. _sec:buildimagesfromscratch:

{Project} produces immutable images in the
Singularity Image File (SIF) format. This ensures reproducible and
verifiable images and allows for many extra benefits such as the ability
to sign and verify your containers.

However, during testing and debugging you may want an image format that
is writable. This way you can ``shell`` into the image and install
software and dependencies until you are satisfied that your container
will fulfill your needs. For these scenarios, {Project} also
supports the ``sandbox`` format (which is really just a directory).

Sandbox Directories
===================

To build into a ``sandbox`` (container in a directory) use the ``build
--sandbox`` command and option:

.. code::

   $ sudo {command} build --sandbox ubuntu/ library://ubuntu

This command creates a directory called ``ubuntu/`` with an entire
Ubuntu Operating System and some {Project} metadata in your current
working directory.

You can use commands like ``shell``, ``exec`` , and ``run`` with this
directory just as you would with a {Project} image. If you pass the
``--writable`` option when you use your container you can also write
files within the sandbox directory (provided you have the permissions to
do so).

.. code::

   $ sudo {command} exec --writable ubuntu touch /foo

   $ {command} exec ubuntu/ ls /foo
   /foo

Converting images from one format to another
============================================

The ``build`` command allows you to build a container from an existing
container. This means that you can use it to convert a container from
one format to another. For instance, if you have already created a
sandbox (directory) and want to convert it to the default immutable
image format (squashfs) you can do so:

.. code::

   $ {command} build new-sif sandbox

Doing so may break reproducibility if you have altered your sandbox
outside of the context of a definition file, so you are advised to
exercise care.

{Project} Definition Files
==============================

For a reproducible, verifiable and production-quality container you
should build a SIF file using a {Project} definition file. This also
makes it easy to add files, environment variables, and install custom
software, and still start from your base of choice (e.g., the Container
Library).

A definition file has a header and a body. The header determines the
base container to begin with, and the body is further divided into
sections that perform things like software installation, environment
setup, and copying files into the container from host system, etc.

Here is an example of a definition file:

.. code:: {command}

   BootStrap: library
   From: ubuntu:16.04

   %post
       apt-get -y update
       apt-get -y install date cowsay lolcat

   %environment
       export LC_ALL=C
       export PATH=/usr/games:$PATH

   %runscript
       date | cowsay | lolcat

   %labels
       Author Sylabs

To build a container from this definition file (assuming it is a file
named lolcow.def), you would call build like so:

.. code::

   $ sudo {command} build lolcow.sif lolcow.def

In this example, the header tells {Project} to use a base Ubuntu
16.04 image from the Container Library.

-  The ``%post`` section executes within the container at build time
   after the base OS has been installed. The ``%post`` section is
   therefore the place to perform installations of new applications.

-  The ``%environment`` section defines some environment variables that
   will be available to the container at runtime.

-  The ``%runscript`` section defines actions for the container to take
   when it is executed.

-  And finally, the ``%labels`` section allows for custom metadata to be
   added to the container.

This is a very small example of the things that you can do with a
:ref:`definition file <definition-files>`. In addition to building a
container from the Container Library, you can start with base images
from Docker Hub and use images directly from official repositories such
as Ubuntu, Debian, CentOS, Arch, and BusyBox. You can also use an
existing container on your host system as a base.

This quickstart document just scratches the surface of all of the things
you can do with {Project}!

If you need additional help or support, see https://apptainer.org/help.

.. _installation-request:

{Project} on a shared resource
----------------------------------

Perhaps you are a user who wants a few talking points and background to
share with your administrator. Or maybe you are an administrator who
needs to decide whether to install {Project}.

This document, and the accompanying administrator documentation provides
answers to many common questions.

If you need to request an installation you may decide to draft a message
similar to this:

.. code::

   Dear shared resource administrator,

   We are interested in having {Project} (https://apptainer.org)
   installed on our shared resource. {Project} containers will allow us to
   build encapsulated environments, meaning that our work is reproducible and
   we are empowered to choose all dependencies including libraries, operating
   system, and custom software. {Project} is already in use on many of the
   top HPC centers around the world. Examples include:

       Texas Advanced Computing Center
       GSI Helmholtz Center for Heavy Ion Research
       Oak Ridge Leadership Computing Facility
       Purdue University
       National Institutes of Health HPC
       UFIT Research Computing at the University of Florida
       San Diego Supercomputing Center
       Lawrence Berkeley National Laboratory
       University of Chicago
       McGill HPC Centre/Calcul Québec
       Barcelona Supercomputing Center
       Sandia National Lab
       Argonne National Lab

   Importantly, it has a vibrant team of developers, scientists, and HPC
   administrators that invest heavily in the security and development of the
   software, and are quick to respond to the needs of the community. To help
   learn more about {Project}, I thought these items might be of interest:

       - Security: A discussion of security concerns is discussed at
       {admindocs}/admin_quickstart.html

       - Installation:
       {admindocs}/installation.html

   If you have questions about any of the above, you can contact one of the
   sources listed at https://apptainer.org/help. I can do my best
   to facilitate this interaction if help is needed.

   Thank you kindly for considering this request!

   Best,

   User
