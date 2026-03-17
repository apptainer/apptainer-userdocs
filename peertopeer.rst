.. _peertopeer:

################################
IPFS Peer-To-Peer (P2P) Clusters
################################

It is possible for users of {Project} to use `IPFS
<https://ipfs.tech/>`__ clusters as sources for their container
images. This is done through an IPFS HTTP Gateway that
fetches data from the IPFS network.

There are both private and public IPFS Gateways. Check with your
IPFS Cluster administrator to find out which gateway to use.

.. code:: console

   $ export IPFS_GATEWAY=http://127.0.0.1:8080

   $ export IPFS_GATEWAY=https://ipfs.io

It can be configured in ``~/.ipfs/gateway`` or ``/etc/ipfs/gateway``.

A daemon on localhost will *automatically* be detected as a gateway.

******************
Content addressing
******************

In IPFS, data is chunked into blocks, which are assigned a
unique identifier called a **Content Identifier (CID)**.
This means that the content is addressable by *what* it is,
and not *where* it is stored like with a regular HTTP URL.

A CID (version 1) is a long string in "`multiformat <https://multiformats.io/>`__":

``bafkreihdwdcefgh4dqkjv67uzcmw7ojee6xedzdetojuzjevtenxquvyku``

The parts of a CID can be inspected with the `CID Inspector
<https://cid.ipfs.tech/#bafkreihdwdcefgh4dqkjv67uzcmw7ojee6xedzdetojuzjevtenxquvyku>`__:

.. code:: text

   base32 - cidv1 - raw - (sha2-256 : 256 : E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855)``

Note: There is an older CID version 0 as well,
it is **not** supported by {Project}.

*************
IPFS Kubo CLI
*************

To upload an image to IPFS, use ``ipfs``:

.. code:: console

   $ ipfs add --cid-version 1 lolcow.sif
   added bafybeice667c6gxovimsb6gnk6vex7vhzluhkl5hjv4ac4lhilxn52c43m lolcow.sif

You can download as well, with ``ipfs``:

.. code:: console

   $ ipfs get bafybeice667c6gxovimsb6gnk6vex7vhzluhkl5hjv4ac4lhilxn52c43m -o lolcow.sif

**********
Using IPFS
**********

Running an image from IPFS is done like:

.. code:: console

   $ {command} run ipfs://bafybeice667c6gxovimsb6gnk6vex7vhzluhkl5hjv4ac4lhilxn52c43m

Or you can pull it to a regular file first:

.. code:: console

   $ {command} pull lolcow.sif ipfs://bafybeice667c6gxovimsb6gnk6vex7vhzluhkl5hjv4ac4lhilxn52c43m

********
Advanced
********

To make version 1 the default, instead of having to use a flag, you can run:

.. code:: shell

   ipfs config --json Import.CidVersion 1

You can wrap the image with a directory, to record the filename and details:

.. code:: console

   $ ipfs add -w lolcow.sif
   added bafybeice667c6gxovimsb6gnk6vex7vhzluhkl5hjv4ac4lhilxn52c43m lolcow.sif
   added bafybeiacfjtqrksxw5udplhs3rpvd7dyeqe7thzompdip635ps7o6sbp4q
   $ {command} run ipfs://bafybeiacfjtqrksxw5udplhs3rpvd7dyeqe7thzompdip635ps7o6sbp4q/lolcow.sif

For testing purposes, you can run a local-only IPFS daemon without connecting it:

.. code:: console

   $ ipfs daemon --offline
   ...
   Swarm not listening, running in offline mode.
   RPC API server listening on /ip4/127.0.0.1/tcp/5001
   WebUI: http://127.0.0.1:5001/webui
   Gateway server listening on /ip4/127.0.0.1/tcp/8080
   Daemon is ready

********
Archives
********

If you need to back up or transport content-addressed data using a non-IPFS
medium, CID can be preserved with CAR files (similar to TAR, for data).

.. code:: console

   $ ipfs dag export bafybeice667c6gxovimsb6gnk6vex7vhzluhkl5hjv4ac4lhilxn52c43m >lolcow.car

   $ ipfs dag import <lolcow.car
   Pinned root	bafybeice667c6gxovimsb6gnk6vex7vhzluhkl5hjv4ac4lhilxn52c43m	success
