.. _encryption:

######################
 Encrypted Containers
######################

Users can build a secure, confidential container environment by
encrypting the root file system.

**********
 Overview
**********

{Project} provides a feature to build and run encrypted
containers to allow users to encrypt the file system
image within a SIF. This encryption can be performed using either a
passphrase or asymmetrically via an RSA key pair in Privacy Enhanced
Mail (PEM/PKCS1) format. The container is encrypted in transit, at rest,
and even while running. In other words, there is no intermediate,
decrypted version of the container on disk. Container decryption occurs
at runtime completely within kernel space.

.. note::

   This feature utilizes the Linux ``dm-crypt`` library and
   ``cryptsetup`` utility and requires cryptsetup version of >= 2.0.0.
   This version should be standard with recent Linux versions such as
   Ubuntu 18.04, Debian 10 and CentOS/RHEL 7, but users of older Linux
   versions may have to update.

************************
 Encrypting a container
************************

A container can be encrypted either by supplying a plaintext passphrase
or a PEM file containing an asymmetric RSA public key. Of these two
methods the PEM file is more secure and is therefore recommended for
production use.

An ``-e|--encrypt`` flag to ``{command} build`` is used to indicate
that the container needs to be encrypted.

A passphrase or a key-file used to perform the encryption is supplied at
build time via an environment variable or a command line option.

+------------------------+-------------------------------------------+--------------------------+
| **Encryption Method**  | **Environment Variable**                  | **Commandline Option**   |
+------------------------+-------------------------------------------+--------------------------+
| Passphrase             | ``{ENVPREFIX}_ENCRYPTION_PASSPHRASE``       | ``--passphrase``         |
+------------------------+-------------------------------------------+--------------------------+
| Asymmetric Key (PEM)   | ``{ENVPREFIX}_ENCRYPTION_PEM_PATH``         | ``--pem-path``           |
+------------------------+-------------------------------------------+--------------------------+

The ``-e|--encrypt`` flag is implicitly set when the ``--passphrase`` or
``--pem-path`` flags are passed with the build command. If multiple
encryption related flags and/or environment variables are set, the
following precedence is respected.

#. ``--pem-path``
#. ``--passphrase``
#. ``{ENVPREFIX}_ENCRYPTION_PEM_PATH``
#. ``{ENVPREFIX}_ENCRYPTION_PASSPHRASE``

Passphrase Encryption
=====================

.. note::

   Passphrase encryption is less secure than encrypting containers using
   an RSA key pair (detailed below). Passphrase encryption is provided
   as a convenience, and as a way for users to familiarize themselves
   with the encrypted container workflow, but users running encrypted
   containers in production are encouraged to use asymmetric keys.

In case of plaintext passphrase encryption, a passphrase is supplied by
one of the following methods.

Encrypting with a passphrase interactively
------------------------------------------

.. code::

   $ sudo {command} build --passphrase encrypted.sif encrypted.def
   Enter encryption passphrase: <secret>
   INFO:    Starting build...

Using an environment variable
-----------------------------

.. code::

   $ sudo {ENVPREFIX}_ENCRYPTION_PASSPHRASE=<secret> {command} build --encrypt encrypted.sif encrypted.def
   Starting build...

In this case it is necessary to use the ``--encrypt`` flag since the
presence of an environment variable alone will not trigger the encrypted
build workflow.

While this example shows how an environment variable can be used to set
a passphrase, you should set the environment variable in a way that will
not record your passphrase on the command line. For instance, you could
save a plain text passphrase in a file (e.g. ``secret.txt``) and use it
like so.

.. code::

   $ export {ENVPREFIX}_ENCRYPTION_PASSPHRASE=$(cat secret.txt)

   $ sudo -E {command} build --encrypt encrypted.sif encrypted.def
   Starting build...

PEM File Encryption
===================

{Project} currently supports RSA encryption using a public/private
key-pair. Keys are supplied in PEM format. The public key is used to
encrypt containers that can be decrypted on a host that has access to
the secret private key.

You can create a pair of RSA keys suitable for encrypting your container
with the ``ssh-keygen`` command, and then create a PEM file with a few
specific flags like so:

.. code::

   # Generate a key pair
   $ ssh-keygen -t rsa -b 4096 -m pem -N ''
   Generating public/private rsa key pair.
   Enter file in which to save the key (/home/vagrant/.ssh/id_rsa): rsa
   [snip...]

   # Convert the public key to PEM PKCS1 format
   $ ssh-keygen -f ./rsa.pub -e -m pem >rsa_pub.pem

   # Rename the private key (already PEM PKCS1) to a nice name
   $ mv rsa rsa_pri.pem

You would use the ``rsa_pub.pem`` file to encrypt your container and the
``rsa_pri.pem`` file to run it.

Encrypting with a command line option
-------------------------------------

.. code::

   $ sudo {command} build --pem-path=rsa_pub.pem encrypted.sif encrypted.def
   Starting build...

Encrypting with an environment variable
---------------------------------------

.. code::

   $ sudo {ENVPREFIX}_ENCRYPTION_PEM_PATH=rsa_pub.pem {command} build --encrypt encrypted.sif encrypted.def
   Starting build...

In this case it is necessary to use the ``--encrypt`` flag since the
presence of an environment variable alone will not trigger the encrypted
build workflow.

********************************
 Running an encrypted container
********************************

To ``run``, ``shell``, or ``exec`` an encrypted image, credentials to
decrypt the image need to be supplied at runtime either in a key-file or
a plaintext passphrase.

Running a container encrypted with a passphrase
===============================================

A passphrase can be supplied at runtime by either of the ways listed in
the sections above.

Running with a passphrase interactively
---------------------------------------

.. code::

   $ {command} run --passphrase encrypted.sif
   Enter passphrase for encrypted container: <secret>

Running with a passphrase in an environment variable
----------------------------------------------------

.. code::

   $ {ENVPREFIX}_ENCRYPTION_PASSPHRASE="secret" {command} run encrypted.sif

While this example shows how an environment variable can be used to set
a passphrase, you should set the environment variable in a way that will
not record your passphrase on the command line. For instance, you could
save a plain text passphrase in a file (e.g. ``secret.txt``) and use it
like so.

.. code::

   $ export {ENVPREFIX}_ENCRYPTION_PASSPHRASE=$(cat secret.txt)

   $ {command} run encrypted.sif

Running a container encrypted with a PEM file
=============================================

A private key is supplied using either of the methods listed in the
Encryption section above.

Running using a command line option
-----------------------------------

.. code::

   $ {command} run --pem-path=rsa_pri.pem encrypted.sif

Running using an environment variable
-------------------------------------

.. code::

   $ {ENVPREFIX}_ENCRYPTION_PEM_PATH=rsa_pri.pem {command} run encrypted.sif
