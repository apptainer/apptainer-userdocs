.. _signnverify:

################################
Signing and Verifying Containers
################################

.. _sec:signnverify:

{Project}'s SIF images can be signed, and subsequently verified, so that a
user can be confident that an image they have obtained is a bit-for-bit
reproduction of the original container as the author intended it. The signature,
over the metadata and content of the container, is created using a private key,
and directly added to the SIF file. This means that a signed container carries
it's signature with it, avoiding the need for extra infrastructure to distribute
signatures to end users of the container.

A user verifies the container has not been modified since signing using a public
key or certificate. By default, {Project} uses PGP keys to sign and verify
containers. Signing and verifying containers with X.509 key material
/ certificates is also supported.

PGP Public keys for verification can be distributed manually, or can be uploaded
to and automatically retrieved from a keyserver.

As well as indicating a container has not been modified, a valid signature may
be used to indicate a container has undergone testing or review, and is approved
for execution. Multiple signatures can be added to a container, to document its
progress through an approval process. {Project}'s Execution Control List
(ECL) feature can be enable by administrators of privileged installations to
restrict execution of containers based on their signatures (see the admin guide
for more information).

.. note::

   To verify containers signed with Singularity versions older than
   3.6.0 the ``--legacy-insecure`` flag must be provided to the
   ``{command} verify`` command.

.. _verify_container_from_remote_sources:

****************************************
Verifying containers from remote sources
****************************************

The ``verify`` command will allow you to verify that a SIF container image has
been signed using a PGP key. This ensures that the container image on your disk
is a bit-for-bit reproduction of the original image.


.. code::

   $ {command} verify alpine_latest.sif

   [REMOTE]  Signing entity: Ian Kaneshiro (example key) <ikaneshiro@apptainer.org>
   [REMOTE]  Fingerprint: 8232570480B868E1473AEEB03DBCBA1EE9D661E5
   Objects verified:
   ID  |GROUP   |LINK    |TYPE
   ------------------------------------------------
   1   |1       |NONE    |Def.FILE
   2   |1       |NONE    |JSON.Generic
   3   |1       |NONE    |JSON.Generic
   4   |1       |NONE    |FS
   Container verified: my_container.sif

In this example you can see that **Ian Kaneshiro** has signed the
container.

This feature is available with SIF images like those you can pull from container
libraries or OCI registries via `oras://`.

.. _sign_your_own_containers:

***************************
Signing your own containers
***************************

Generating and managing PGP keys
================================

To sign your own containers you first need to generate one or more keys.

If you attempt to sign a container before you have generated any keys,
{Project} will guide you through the interactive process of creating
a new key. Or you can use the ``newpair`` subcommand in the ``key``
command group like so:

.. code::

   $ {command} key newpair

   Enter your name (e.g., John Doe) : Ian Kaneshiro
   Enter your email address (e.g., john.doe@example.com) : ikaneshiro@apptainer.org
   Enter optional comment (e.g., development keys) : example key
   Enter a passphrase :
   Retype your passphrase :
   Generating Entity and OpenPGP Key Pair... done

The ``list`` subcommand will show you all of the keys you have created
or saved locally.`

.. code::

   $ {command} key list

   Public key listing (/home/ian/.{command}/keys/pgp-public):

   0) U: Ian Kaneshiro (example key) <ikaneshiro@apptainer.org>
      C: 2022-02-23 15:12:19 -0800 PST
      F: 8232570480B868E1473AEEB03DBCBA1EE9D661E5
      L: 4096
      --------

In the output above the index of my key is ``0`` and the letters stand
for the following:

   -  U: User
   -  C: Creation date and time
   -  F: Fingerprint
   -  L: Key length

If you would like others in the community to easily be able to fetch your
public key for image verification, you can push your key to a public keyserver.

First we can check which key server we have configured using:

.. code::

   $ {command} remote list

   Cloud Services Endpoints
   ========================

   NAME           URI                  ACTIVE  GLOBAL  EXCLUSIVE
   DefaultRemote  cloud.apptainer.org  YES     YES     NO

   Keyservers
   ==========

   URI                       GLOBAL  INSECURE  ORDER
   https://keys.openpgp.org  YES     NO        1*

   * Active cloud services keyserver

   Authenticated Logins
   =================================

   URI             INSECURE
   oras://ghcr.io  NO

Here we can see that we will be pushing to `https://keys.openpgp.org`. Now
we can use the following command to push our key:

.. code::

   $ {command} key push 8232570480B868E1473AEEB03DBCBA1EE9D661E5

   public key `8232570480B868E1473AEEB03DBCBA1EE9D661E5' pushed to server successfully

If you delete your local public PGP key, you can always locate and
download it again like so.

.. code::

   $ {command} key search --long-list ikaneshiro@apptainer.org

   Showing 1 results

   FINGERPRINT                               ALGORITHM  BITS  CREATION DATE                  EXPIRATION DATE  STATUS     NAME/EMAIL
   8232570480B868E1473AEEB03DBCBA1EE9D661E5  RSA        4096  2022-02-23 15:12:19 -0800 PST                   [enabled]  Ian Kaneshiro (example key) <ikaneshiro@apptainer.org>

   $ {command} key pull 8232570480B868E1473AEEB03DBCBA1EE9D661E5
   1 key(s) added to keyring of trust /home/ian/.{command}/keys/pgp-public

But note that this only restores the *public* key (used for verifying)
to your local machine and does not restore the *private* key (used for
signing).

.. _searching_for_keys:

Searching for keys
==================

{Project} allows you to search the keystore for public keys. You can
search for names, emails, and fingerprints (key IDs). When searching for
a fingerprint, you need to use ``0x`` before the fingerprint, check the
example:

.. code::

   # search for key ID:
   $ {command} key search 0x8883491F4268F173C6E5DC49EDECE4F3F38D871E

   # search for the sort ID:
   $ {command} key search 0xF38D871E

   # search for user:
   $ {command} key search Godlove

   # search for email:
   $ {command} key search @gmail.com

Signing and validating your own containers
==========================================

Now that you have a key generated, you can use it to sign images like
so:

.. code::

   $ {command} sign my_container.sif

   Signing image: my_container.sif
   Enter key passphrase :
   Signature created and applied to my_container.sif

Because your public PGP key is saved locally you can verify the image
without needing to contact the key server.

.. code::

   $ {command} verify my_container.sif

   Verifying image: my_container.sif
   [LOCAL]   Signing entity: Ian Kaneshiro (example key) <ikaneshiro@apptainer.org>
   [LOCAL]   Fingerprint: 8232570480B868E1473AEEB03DBCBA1EE9D661E5
   Objects verified:
   ID  |GROUP   |LINK    |TYPE
   ------------------------------------------------
   1   |1       |NONE    |Def.FILE
   2   |1       |NONE    |JSON.Generic
   3   |1       |NONE    |JSON.Generic
   4   |1       |NONE    |FS
   Container verified: my_container.sif

If you've pushed your key to a key server you can also verify this image
in the absence of a local public key. To demonstrate this, first
``remove`` your local public key, and then try to use the ``verify``
command again.

.. code::

   $ {command} key remove 8232570480B868E1473AEEB03DBCBA1EE9D661E5

   $ {command} verify my_container.sif

   Verifying image: my_container.sif
   [REMOTE]  Signing entity: Ian Kaneshiro (example key) <ikaneshiro@apptainer.org>
   [REMOTE]  Fingerprint: 8232570480B868E1473AEEB03DBCBA1EE9D661E5
   Objects verified:
   ID  |GROUP   |LINK    |TYPE
   ------------------------------------------------
   1   |1       |NONE    |Def.FILE
   2   |1       |NONE    |JSON.Generic
   3   |1       |NONE    |JSON.Generic
   4   |1       |NONE    |FS
   Container verified: my_container.sif

Note that the ``[REMOTE]`` message shows the key used for verification
was obtained from a key server, and is not present on your local
computer. You can retrieve it, so that you can verify even if you are
offline with ``{command} key pull``

.. code::

   $ {command} key pull 8232570480B868E1473AEEB03DBCBA1EE9D661E5

   1 key(s) added to keyring of trust /home/ian/.{command}/keys/pgp-public

Advanced Signing - SIF IDs and Groups
=====================================

As well as the default behaviour, which signs all objects, fine-grained
control of signing is possible.

If you ``sif list`` a SIF file you will see it is comprised of a number
of objects. Each object has an ``ID``, and belongs to a ``GROUP``.

.. code::

   $ {command} sif list my_container.sif

   ------------------------------------------------------------------------------
   ID   |GROUP   |LINK    |SIF POSITION (start-end)  |TYPE
   ------------------------------------------------------------------------------
   1    |1       |NONE    |32768-32800               |Def.FILE
   2    |1       |NONE    |36864-39751               |JSON.Generic
   3    |1       |NONE    |40960-41055               |JSON.Generic
   4    |1       |NONE    |45056-2781184             |FS (Squashfs/*System/amd64)
   5    |NONE    |1   (G) |2781184-2782981           |Signature (SHA-256)

I can choose to sign and verify a specific object with the ``--sif-id``
option to ``sign`` and ``verify``.

.. code::

   $ {command} sign --sif-id 1 my_container.sif

   Signing image: my_container.sif
   Enter key passphrase :
   Signature created and applied to my_container.sif

   $ {command} verify --sif-id 1 my_container.sif

   Verifying image: my_container.sif
   [LOCAL]   Signing entity: Ian Kaneshiro (example key) <ikaneshiro@apptainer.org>
   [LOCAL]   Fingerprint: 8232570480B868E1473AEEB03DBCBA1EE9D661E5
   Objects verified:
   ID  |GROUP   |LINK    |TYPE
   ------------------------------------------------
   1   |1       |NONE    |Def.FILE
   Container verified: my_container.sif

Note that running the ``verify`` command without specifying the specific
sif-id gives a fatal error. The container is not considered verified as
whole because other objects could have been changed without my
knowledge.

.. code::

   $ {command} verify my_container.sif

   Verifying image: my_container.sif
   [LOCAL]   Signing entity: Ian Kaneshiro (example key) <ikaneshiro@apptainer.org>
   [LOCAL]   Fingerprint: 8232570480B868E1473AEEB03DBCBA1EE9D661E5

   Error encountered during signature verification: object 2: object not signed
   FATAL:   Failed to verify container: integrity: object 2: object not signed

I can sign a group of objects with the ``--group-id`` option to
``sign``.

.. code::

   $ {command} sign --group-id 1 my_container.sif
   Signing image: my_container.sif
   Enter key passphrase :
   Signature created and applied to my_container.sif

This creates one signature over all objects in the group. I can verify
that nothing in the group has been modified by running ``verify`` with
the same ``--group-id`` option.

.. code::

   $ {command} verify --group-id 1 my_container.sif

   Verifying image: my_container.sif
   [LOCAL]   Signing entity: Ian Kaneshiro (example key) <ikaneshiro@apptainer.org>
   [LOCAL]   Fingerprint: 8232570480B868E1473AEEB03DBCBA1EE9D661E5
   Objects verified:
   ID  |GROUP   |LINK    |TYPE
   ------------------------------------------------
   1   |1       |NONE    |Def.FILE
   2   |1       |NONE    |JSON.Generic
   3   |1       |NONE    |JSON.Generic
   4   |1       |NONE    |FS
   Container verified: my_container.sif

Because every object in the SIF file is within the signed group 1 the
entire container is signed, and the default ``verify`` behavior without
specifying ``--group-id`` can also verify the container:

.. code::

   $ {command} verify my_container.sif

   Verifying image: my_container.sif
   [LOCAL]   Signing entity: Ian Kaneshiro (example key) <ikaneshiro@apptainer.org>
   [LOCAL]   Fingerprint: 8232570480B868E1473AEEB03DBCBA1EE9D661E5
   Objects verified:
   ID  |GROUP   |LINK    |TYPE
   ------------------------------------------------
   1   |1       |NONE    |Def.FILE
   2   |1       |NONE    |JSON.Generic
   3   |1       |NONE    |JSON.Generic
   4   |1       |NONE    |FS
   Container verified: my_container.sif

***********************************
PEM Key / X.509 Certificate Support
***********************************

{Project} also supports signing SIF container images
using a PEM format private key, and verifying with a PEM format public key, or
X.509 certificate. Non-PGP signatures are implemented using the `Dead Simple
Signing Envelope <https://github.com/secure-systems-lab/dsse>`__ (DSSE)
standard.

Signing with a PEM key
======================

To sign a container using a private key in PEM format, provide the key material
to the ``sign`` command using the ``--key`` flag:

.. code:: 

   $ {command} sign --key mykey.pem lolcow.sif 
   INFO:    Signing image with key material from 'mykey.pem'
   INFO:    Signature created and applied to image 'lolcow.sif'

The DSSE signature descriptor can now be seen by inspecting the SIF file:

.. code:: 

   $ {command} sif list lolcow.sif 
   ------------------------------------------------------------------------------
   ID   |GROUP   |LINK    |SIF POSITION (start-end)  |TYPE
   ------------------------------------------------------------------------------
   1    |1       |NONE    |32176-32393               |Def.FILE
   2    |1       |NONE    |32393-33522               |JSON.Generic
   3    |1       |NONE    |33522-33718               |JSON.Generic
   4    |1       |NONE    |36864-84656128            |FS (Squashfs/*System/amd64)
   5    |NONE    |1   (G) |84656128-84658191         |Signature (SHA-256)

   $ {command} sif dump 5 lolcow.sif | jq
   {
   "payloadType": "application/vnd.{command}.sif-metadata+json",
   ...

Attempting to ``verify`` the image without options will fail, as it is not signed with a PGP key:

.. code:: 

   $ {command} verify lolcow.sif 
   INFO:    Verifying image with PGP key material
   FATAL:   Failed to verify container: integrity: key material not provided for DSSE envelope signature

Note that the error message shows that the container image has a DSSE signature present.

Verifying with a PEM key
========================

To verify a container using a PEM public key directly, provide the key material
to the ``verify`` command using the ``key`` flag:

.. code:: 

   $ {command} verify --key mypublic.pem lolcow.sif 
   INFO:    Verifying image with key material from 'mypublic.pem'
   Objects verified:
   ID  |GROUP   |LINK    |TYPE
   ------------------------------------------------
   1   |1       |NONE    |Def.FILE
   2   |1       |NONE    |JSON.Generic
   3   |1       |NONE    |JSON.Generic
   4   |1       |NONE    |FS
   INFO:    Verified signature(s) from image 'lolcow.sif'

Verifying with an X.509 certificate
===================================

To verify a container that was signed with a PEM private key, using an X.509 certificate,
pass the certificate to the ``verify`` command using the ``--certificate`` flag.
If the certificate is part of a chain, provide intermediate and valid root
certificates with the ``--certificate-intermediates`` and
``--certificate-roots`` flags:

.. code::

   $ {command} verify \
      --certificate leaf.pem \
      --certificate-intermediates intermediate.pem \
      --certificate-roots root.pem \
      lolcow.sif 

.. note:: 

   The certificate must have a usage field that allows code signing in order to
   verify container images.

OSCP Certificate Revocation Checks
==================================

When verifying a container using X.509 certificates, {Project} can perform
online revocation checks using the Online Certificate Status Protocol (OCSP). To
enable OCSP checks, add the ``--ocsp-verify`` flag to your ``verify`` command:

.. code:: 

   $ {command} verify \
      --certificate leaf.pem \
      --certificate-intermediates intermediate.pem \
      --certificate-roots root.pem \
      --ocsp-verify
      lolcow.sif 

{Project} will then attempt to contact the prescribed OCSP responder for
each certificate in the chain, in order to check that the relevant certificate
has not been revoked. In the event that an OCSP responder cannot be contacted,
or a certificate has been revoked, verification will fail with a validation
error:

.. code:: 

   INFO:    Validate: cert:leaf  issuer:intermediate
   FATAL:   Failed to verify container: OCSP verification has failed
