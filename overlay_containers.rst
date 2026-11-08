##################
Overlay Containers
##################

.. _overlay-containers:

An *overlay-only* (or *thin*) image is built from a :ref:`definition file
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

Build an overlay-only image, containing only the files added, changed, or
removed relative to a base image. It requires a :ref:`definition file
<definition-files>` that uses a ``localimage``, ``docker``, or ``oras``
bootstrap as its base.

.. code:: console

   $ {command} build --overlay my-overlay.sif my-def.def

By default the result is a SIF file with an overlay partition in it; add the
``--sandbox`` option to build a sandbox instead. The base image itself cannot
be a sandbox, because a sandbox has no hash that can be recorded.

When the image is built, a hash of the base image (and, where relevant, its
original reference) is stored in the overlay image's metadata. This is used at
run time by the ``--basepath`` action option to find the base image and
combine it with the overlay automatically.

An overlay-only image cannot be run with ``--writable``, because the base
image must be readable as-is.

.. _sec:basepath:

****************************************
Finding the base with ``--basepath``
****************************************

Use the ``--basepath`` action option (or the ``{ENVPREFIX}_BASEPATH``
environment variable) to tell {Project} where to find the base image of an
overlay-only image built with ``{command} build --overlay``, so it can be
combined with the overlay automatically at run time. It takes a comma-separated
list of paths to search. The last entry may be an ``oras://`` or ``docker://``
image reference; if so it must use the same transport as the original base,
may override the registry name and/or image name (or both), and a missing
version is inferred from the hash recorded in the overlay's metadata.

The behaviour depends on the bootstrap of the base image used when the overlay
was built:

* If the base was a ``localimage``, then ``--basepath`` is required.
* If the base was an ``oras`` image, then the default is ``oras://``
  (which means "the same registry and image the original base came from").
* If the base was a ``docker`` image, then the default is ``docker://``.

Local base images
=================

If an entry in the list is a SIF file or a sandbox directory, it is used
directly, regardless of its name. Otherwise, if the entry is a directory, it
is searched for a base image matching the hash recorded in the overlay's
metadata. Within that directory {Project} looks for:

* a file or directory directly named after the hash, and
* a file or directory named after the hash, within a subdirectory named with
  the first two characters of the hash (a *fan-out* layout, useful for
  distributing a large number of base images),

and tries each with and without a ``sha256:`` prefix, for example:

.. code:: console

   $ {command} build --overlay my-overlay.sif my-def.def
   $ ls /srv/overlay-bases
   1a  sha256:1a2b3c4d...
   $ ls /srv/overlay-bases/1a
   2b3c4d...
   $ {command} run --basepath /srv/overlay-bases my-overlay.sif

Remote base images
==================

When the last entry in the list is an ``oras://`` or ``docker://`` image
reference, it must use the same transport as the original base. Each part of
the reference may be left to its default, taken from the overlay's metadata,
or given a new value. A missing registry and/or image name is taken from the
default, and a missing version is inferred from the hash recorded in the
overlay's metadata.

.. code:: console

   # Use the default registry, image, and hash (same source as the build)
   $ {command} run --basepath oras://ghcr.io/someuser/mybase my-overlay.sif

   # Use multiple search paths -- local first, then a registry
   $ {command} run --basepath /opt/bases,oras://ghcr.io/someuser my-overlay.sif

Placeholders
============

Within the remote reference you may use placeholder values in place of the
default registry name or image name. Omitting a part, or explicitly
substituting the placeholder for it, both cause that part to be taken from
the default recorded in the overlay's metadata:

* The registry and repository of ``-.-`` refer to the default registry and
  image name together.
* A repository of ``-`` refers to just the default repository name.
* An identifier of ``-`` (or ``latest``) refers to the default digest (the
  recorded base hash).

So for example ``oras://`` is equivalent to ``oras://-.-/-``:

.. code:: console

   # These are all equivalent, using the default registry, image, and hash
   $ {command} run --basepath oras:// my-overlay.sif
   $ {command} run --basepath oras://-.-/- my-overlay.sif

To override only the registry, keep the default image name by using a
repository of ``-``:

.. code:: console

   $ {command} run --basepath oras://other-registry/- my-overlay.sif

To override only the image name, leave the registry at its default:

.. code:: console

   $ {command} run --basepath oras://ghcr.io/someuser/other-image my-overlay.sif
