##################
Overlay Containers
##################

.. _overlay-containers:

An *overlay* (or *thin*) image is built from a :ref:`definition file
<definition-files>` with the ``{command} build --overlay`` option. It
contains only the files added, changed, or removed relative to a base
image, rather than a full copy of it. Because the resulting image is small,
many thin images can be derived from one shared base.

This page describes how to build such an image with ``build --overlay``, and
how to combine it with its base image at run time with the ``--basepath``
action option (or the ``{ENVPREFIX}_BASEPATH`` environment variable). It is a
separate feature to :ref:`persistent overlays <persistent-overlays>`, which
attach a user-managed ext3 image to any container.

***********************************
Building with ``build --overlay``
***********************************

Build an overlay image, containing only the files added, changed, or
removed relative to a base image. It requires a :ref:`definition file
<definition-files>` that uses a ``localimage``, ``docker``, or ``oras``
bootstrap as its base.

.. code:: console

   $ {command} build --overlay my-overlay.sif my-def.def

When the image is built, a hash of the base image and its original
reference are stored in the overlay image's metadata. These are used at
run time by the ``--basepath`` action option to find the base image and
combine it with the overlay automatically.

By default the result is a SIF file with an overlay partition in it; add the
``--sandbox`` option to build a sandbox instead. The base image itself cannot
be a sandbox, because a sandbox has no hash of its own.  (It may have
been the case that a base image sandbox came from a source with a hash
and that hash is stored in the sandbox metadata, but there's no way to
know whether or not it had been modified afterward.)

An overlay SIF file can be converted to a sandbox the same way as an
ordinary SIF file, using `{command} build --sandbox`.

.. code:: console

   $ {command} build --sandbox my-overlay-sandbox my-overlay.sif

There is, however, a limitation not present when a sandbox is built
directly from a definition file: if the definition file changed the
owner or group of any file, then ``/etc/subuid`` and ``/etc/subgid``
fakeroot mode needs to be enabled.  That's because the fakeroot
command mode interferes with some special files that overlayfs uses,
so it is disallowed during the extraction.

Using ``--writable`` with an overlay image is not supported, even if it
is a sandbox.

.. _sec:basepath:

************************************
Finding the base with ``--basepath``
************************************

Use the ``--basepath`` exec/run/shell option (or the ``{ENVPREFIX}_BASEPATH``
environment variable) to tell {Project} where to find the base image of an
overlay image built with ``{command} build --overlay``, so it can be
combined with the overlay.  The option takes a comma-separated list of
paths to search.  Base images may be local, or the last entry may
be an ``oras://`` or ``docker://`` image reference; if so it must use
the same transport as the original base.  The two different types are
described in more detail below.

The behaviour depends on the bootstrap of the base image used when the overlay
was built:

* If the base was a ``localimage``, then ``--basepath`` is required.
* If the base was an ``oras`` image, then the default is ``oras://``
  (which means "the same registry and image the original base came from").
* If the base was a ``docker`` image, then the default is ``docker://``.

Local base images
=================

If an entry in the basepath list is a SIF file or a sandbox directory,
it is used directly, regardless of its name, although the hash must match.
Otherwise, if the entry is a directory, it is searched for a base image
matching the hash recorded in the overlay's metadata. Within that
directory {Project} looks for:

* a file or directory directly named after the hash, and
* a file or directory named after the hash, within a subdirectory named with
  the first two characters of the hash (a *fan-out* layout, useful for
  distributing a large number of base images),

It also tries each hash with and without the hash type prefix (typically
``sha256:``), for example:

.. code:: console

   $ {command} build --overlay my-overlay.sif my-def.def
   $ ls /srv/overlay-bases
   1a  sha256:1a2b3c4d...
   $ ls /srv/overlay-bases/1a
   2b3c4d...
   $ {command} run --basepath /srv/overlay-bases my-overlay.sif

Remote base images
==================

When the last entry in the basepath list is an ``oras://`` or ``docker://``
image reference, it must use the same transport as the original base.
Each part of the reference may be left to its default, taken from the
overlay's metadata, or given a new value. A missing registry and/or
image name is taken from the default, and the version is inferred from
the hash recorded in the overlay's metadata.

.. code:: console

   # Use the default registry, image, and hash (same source as the build)
   $ {command} run --basepath oras://ghcr.io/someuser/mybase my-overlay.sif

   # Use multiple search paths -- local first, then original registry
   $ {command} run --basepath /opt/bases,oras:// my-overlay.sif

Placeholders
============

Within the remote reference you may use placeholder values in place of the
default registry name or image name.  Substituting the placeholder for a
part causes that part to be taken from the default recorded in the
overlay's metadata:

* A registry of ``-.-`` refers to the original registry.
* A image name of ``-`` refers to the original image name.
  (Note that image names usually include a slash in them; if they don't,
  a ``library/`` prefix is implied.)

So for example ``oras://`` is equivalent to ``oras://-.-/-``:

.. code:: console

   # These are all equivalent, using the default registry, image, and hash
   $ {command} run my-overlay.sif
   $ {command} run --basepath oras:// my-overlay.sif
   $ {command} run --basepath oras://-.-/- my-overlay.sif

To override only the registry and keep the default image name by using ``-``:

.. code:: console

   $ {command} run --basepath oras://other.registry/- my-overlay.sif

To override only the image name and leave the registry at its default:

.. code:: console

   $ {command} run --basepath oras://-.-/someuser/someimage my-overlay.sif
