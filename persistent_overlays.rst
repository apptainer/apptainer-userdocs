#####################
 Persistent Overlays
#####################

Persistent overlay directories allow you to overlay a writable file
system on an immutable read-only container for the illusion of
read-write access. You can run a container and make changes, and these
changes are kept separately from the base container image.

**********
 Overview
**********

A persistent overlay is a directory or file system image that “sits on
top” of your immutable SIF container. When you install new software or
create and modify files the overlay will store the changes.

If you want to use a SIF container as though it were writable, you can
create a directory, an ext3 file system image, or embed an ext3 file
system image in SIF to use as a persistent overlay. Then you can specify
that you want to use the directory or image as an overlay at runtime
with the ``--overlay`` option, or ``--writable`` if you want to use the
overlay embedded in SIF.

If you want to make changes to the image, but do not want them to
persist, use the ``--writable-tmpfs`` option. This stores all changes in
an in-memory temporary filesystem which is discarded as soon as the
container finishes executing.

You can use persistent overlays with the following commands:

-  ``run``
-  ``exec``
-  ``shell``
-  ``instance.start``

*******
 Usage
*******

To use a persistent overlay, you must first have a container.

.. code::

   $ sudo singularity build ubuntu.sif library://ubuntu

File system image overlay
=========================

{Project} provides a command ``singularity overlay
create`` to create persistent overlay images. You can create a single
EXT3 overlay image or adding a EXT3 writable overlay partition to an
existing SIF image.

.. note::

   ``dd`` and ``mkfs.ext3`` must be installed on your system.
   Additionally ``mkfs.ext3`` must support ``-d`` option in order to
   create an overlay directory tree usable by a regular user.

For example, to create a 1 GiB overlay image:

.. code::

   $ singularity overlay create --size 1024 /tmp/ext3_overlay.img

To add a 1 GiB writable overlay partition to an existing SIF image:

.. code::

   $ singularity overlay create --size 1024 ubuntu.sif

.. warning::

   It is not possible to add a writable overlay partition to a
   **signed**, **encrypted** SIF image or if the SIF image already
   contain a writable overlay partition.

``singularity overlay create`` also provides an option ``--create-dir``
to create additional directories owned by the calling user, it can be
specified multiple times to create many directories. This is
particularly useful when you need to make a directory writable by your
user.

So for example:

.. code::

   $ singularity build /tmp/nginx.sif docker://nginx
   $ singularity overlay create --size 1024 --create-dir /var/cache/nginx /tmp/nginx.sif
   $ echo "test" | singularity exec /tmp/nginx.sif sh -c "cat > /var/cache/nginx/test"

Directory overlay
=================

A directory overlay is simpler to use than a filesystem image overlay,
but a directory of modifications to a base container image cannot be
transported or shared as easily as a single overlay file.

.. note::

   For security reasons, you must be root to use a bare directory as an
   overlay. ext3 file system images can be used as overlays without root
   privileges.

Create a directory as usual:

.. code::

   $ mkdir my_overlay

The example below shows the directory overlay in action.

.. code::

   $ sudo singularity shell --overlay my_overlay/ ubuntu.sif

   {Project} ubuntu.sif:~> mkdir /data

   {Project} ubuntu.sif:~> chown user /data

   {Project} ubuntu.sif:~> apt-get update && apt-get install -y vim

   {Project} ubuntu.sif:~> which vim
   /usr/bin/vim

   {Project} ubuntu.sif:~> exit

.. _overlay-sif:

Overlay embedded in SIF
=======================

It is possible to embed an overlay image in the SIF file that holds a
container. This allows the read-only container image and your
modifications to it to be managed as a single file. In order to do this,
you must first create a file system image:

.. code::

   $ dd if=/dev/zero of=overlay.img bs=1M count=500 && \
       mkfs.ext3 overlay.img

Then, you can add the overlay to the SIF image using the ``sif``
functionality of {Project}.

.. code::

   $ singularity sif add --datatype 4 --partfs 2 --parttype 4 --partarch 2 --groupid 1 ubuntu_latest.sif overlay.img

Below is the explanation what each parameter means, and how it can
possibly affect the operation:

-  ``datatype`` determines what kind of an object we attach, e.g. a
   definition file, environment variable, signature.
-  ``partfs`` should be set according to the partition type, e.g.
   SquashFS, ext3, raw.
-  ``parttype`` determines the type of partition. In our case it is
   being set to overlay.
-  ``partarch`` must be set to the architecture against you're building.
   In this case it's ``amd64``.
-  ``groupid`` is the ID of the container image group. In most cases
   there's no more than one group, therefore we can assume it is 1.

All of these options are documented within the CLI help. Access it by
running ``singularity sif add --help``.

After you've completed the steps above, you can shell into your
container with the ``--writable`` option.

.. code::

   $ sudo singularity shell --writable ubuntu_latest.sif

Final note
==========

You will find that your changes persist across sessions as though you
were using a writable container.

.. code::

   $ singularity shell --overlay my_overlay/ ubuntu.sif

   {Project} ubuntu.sif:~> ls -lasd /data
   4 drwxr-xr-x 2 user root 4096 Apr  9 10:21 /data

   {Project} ubuntu.sif:~> which vim
   /usr/bin/vim

   {Project} ubuntu.sif:~> exit

If you mount your container without the ``--overlay`` directory, your
changes will be gone.

.. code::

   $ singularity shell ubuntu.sif

   {Project} ubuntu.sif:~> ls /data
   ls: cannot access 'data': No such file or directory

   {Project} ubuntu.sif:~> which vim

   {Project} ubuntu.sif:~> exit

To resize an overlay, standard Linux tools which manipulate ext3 images
can be used. For instance, to resize the 500MB file created above to
700MB one could use the ``e2fsck`` and ``resize2fs`` utilities like so:

.. code::

   $ e2fsck -f my_overlay && \
       resize2fs my_overlay 700M

Hints for creating and manipulating ext3 images on your distribution are
readily available online and are not treated further in this manual.
