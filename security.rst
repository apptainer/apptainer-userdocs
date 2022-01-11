.. _security:

<<<<<<< HEAD
***********************
Security in apptainer
***********************

Containers are popular for many good reasons. They are light weight,
easy to spin-up and require reduced IT management resources as
compared to hardware VM environments. More importantly, container
technology facilitates advanced research computing by granting the
ability to package software in highly portable and reproducible
environments encapsulating all dependencies, including the operating
system. But there are still some challenges to container security.

apptainer addresses some core missions of containers : Mobility of
Compute, Reproducibility, HPC support, and **Security**. This section
gives an overview of security features supported by apptainer,
especially where they differ from other container runtimes.
=======
*************************
Security in {Singularity}
*************************
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543

Security Policy
###############

<<<<<<< HEAD
Security is not a check box that one can tick and forget.  Ensuring
security is a ongoing process that begins with software architecture,
and continues all the way through to ongoing security practices.  In
addition to ensuring that containers are run without elevated
privileges where appropriate, and that containers are produced by
trusted sources, users must monitor their containers for newly
discovered vulnerabilities and update when necessary just as they
would with any other software. The apptainer community is constantly probing to find
and patch vulnerabilities within apptainer, and will continue to do
so.

If you suspect you have found a vulnerability in apptainer, please
follow the steps in our published `Security Policy
<https://apptainer.org/security-policy/>`__.

so that it can be disclosed, investigated, and fixed in an appropriate
manner.

apptainer PRO - Long Term Support & Security Patches
######################################################

Security patches for apptainer are applied to the latest open-source
version, so it is important to follow new releases and upgrade when
neccessary.

apptainerPRO is a professionally curated and licensed version of
apptainer that provides added security, stability, and support
beyond that offered by the open source project. Security and bug-fix
patches are backported to select versions of apptainer PRO, so that
they can be deployed long-term where required. PRO users receive
security fixes (without specific notification or detail) prior to
public disclosure, as detailed in the `apptainer Community Security Policy
<https://apptainer.org/security-policy/>`__.


apptainer Runtime & User Privilege
####################################

The apptainer Runtime enforces a unique security model that makes it
appropriate for *untrusted users* to run *untrusted containers* safely
on multi-tenant resources. When you run a container, the processes in
the container will run as your user account. apptainer dynamically
writes UID and GID information to the appropriate files within the
container, and the user remains the same *inside* and *outside*
the container, i.e., if you're an unprivileged user while entering the
container you'll remain an unprivileged user inside the container.

Additional blocks are in place to prevent users from escalating
privileges once they are inside of a container. The container file
system is mounted using the ``nosuid`` option, and processes are
started with the ``PR_NO_NEW_PRIVS`` flag set. This means that even if
you run `sudo` inside your container, you won't be able to change to
another user, or gain root priveleges by other means. This approach
provides a secure way for users to run containers and greatly
simplifies things like reading and writing data to the host system
with appropriate ownership.

It is also important to note that the philosophy of apptainer is
*Integration* over *Isolation*. Most container run times strive to
isolate your container from the host system and other containers as
much as possible. apptainer, on the other hand, assumes that the
user’s primary goals are portability, reproducibility, and ease of use
and that isolation is often a tertiary concern. Therefore, apptainer
only isolates the mount namespace by default, and will bind mount
several host directories such as ``$HOME`` and ``/tmp`` into the
container at runtime. If needed, additional levels of isolation can be
achieved by passing options causing apptainer to enter any or all of
the other kernel namespaces and to prevent automatic bind mounting.
These measures allow users to interact with the host system from
within the container in sensible ways.
=======
If you suspect you have found a vulnerability in {Singularity} we want
to work with you so that it can be investigated, fixed, and disclosed
in a responsible manner. Please follow the steps in our published
`Security Policy <https://singularity.hpcng.org/security-policy/>`__, which begins
with contacting us privately via singularity‑security@hpcng.org

We disclose vulnerabilities found in {Singularity} through public
CVE reports, and notifications on our community channels. We encourage
all users to monitor new releases of {Singularity} for security
information. Security patches are applied to the latest open-source
release.

Background
##########

{Singularity} grew out of the need to implement a container platform
that was suitable for use on shared systems, such as HPC clusters. In
these environments multiple people access a shared resource. User
accounts, groups, and standard file permissions limit their access to
data, devices, and prevent them from disrupting or accessing others'
work.

To provide security in these environments a container needs to run as
the user who starts it on the system. Before the widepread adoption of
the Linux user namespace, only a privileged user could perform the
operations which are needed to run a container. A default Docker
installation uses a root-owned daemon to start containers. Users can
request that the daemon starts a container on their behalf. However,
co-ordinating a daemon with other schedulers is difficult and, since
the daemon is privileged, users can ask it to carry out actions that
they wouldn't normally have permission to do.

When a user runs a container with {Singularity}, it is started as a
normal process running under the user's account. Standard file
permissions and other security controls based on user accounts,
groups, and processes apply. In a default installation {Singularity}
uses a setuid starter binary to perform only the specific tasks needed
to setup the container.


Setuid & User Namespaces
########################

Using a setuid binary to run container setup operations is essential
to support containers on older Linux distributions, such as CentOS 6,
that were previously common in HPC and enterprise. Newer distributions
have support for 'unprivileged user namespace creation'. This means a
normal user can create a user namespace, in which most setup operations
needed to run a container can be run, unprivileged.

{Singularity} supports running containers without setuid, using user
namespaces. It can be compiled with the ``--without-setuid`` option,
or ``allow setuid = no`` can be set in ``singularity.conf`` to enable
this. In this mode *all* operations run as the user who starts the
``singularity`` program. However, there are some disadvantages:

* SIF and other single file container images cannot be mounted
  directly. The container image must be extracted to a directory on
  disk to run. This impact the speed of execution. Workloads accessing
  large numbers of small files (such as python application startup) do
  not benefit from the reduced metadata load on the filesystem an
  image file provides.

* Replacing direct kernel mounts with a FUSE approach is likely to
  cause a significant reduction in perfomance.

* The effectiveness of signing and verifying container images is
  reduced as, when extracted to a directory, modification is possible
  and verification of the image's original signature cannot be
  performed.

* Encryption is not supported. {Singularity} leverages kernel LUKS2
  mounts to run encrypted containers without decrypting their content
  to disk.

* Some sites hold the opinion that vulnerabilities in kernel user
  namespace code could have greater impact than vulnerabilities
  confined to a single piece of setuid software. Therefore they are
  reluctant to enable unprivileged user namespace creation.

Because of the points above, the default mode of operation of
{Singularity} uses a setuid binary. We aim to reduce the
circumstances that require this as new functionality is developed and
reaches commonly deployed Linux distributions.

Runtime & User Privilege Model
##############################

While other runtimes have aimed to safely sandbox containers executing
as the ``root`` user, so that they cannot affect the host system,
{Singularity} has adopted an alternative security model:

* Containers should be run as an unprivileged user.

* The user should never be able to elevate their privileges inside the
  container to gain control over the host.

* All permission restrictions on the user outside of a container
  should apply inside the container.

* Favor integration over isolation. Allow a user to use host resources
  such as GPUs, network filesystems, high speed interconnects
  easily. The process ID space, network etc. are not isolated in
  separate namespaces by default.

To accomplish this, {Singularity} uses a number of Linux kernel
features. The container file system is mounted using the ``nosuid``
option, and processes are started with the ``PR_NO_NEW_PRIVS`` flag
set. This means that even if you run ``sudo`` inside your container,
you won't be able to change to another user, or gain root privileges
by other means.

If you do require the additional isolation of the network, devices,
PIDs etc. provided by other runtimes, {Singularity} can make use of
additional namespaces and functionality such as seccomp and cgroups.

>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543

apptainer Image Format (SIF)
##############################

<<<<<<< HEAD
Ensuring container security as a continuous process. apptainer
provides ways to ensure integrity throughout the lifecyle of a
container, i.e. at rest, in transit and while running. The SIF
apptainer Image Format has been designed to achieve these goals.

A SIF file is an immutable container image that packages the container
environment into a single file. SIF supports security and integrity
through the ability to cryptographically sign a container, creating a
signature block within the SIF file which can guarantee immutability
and provide accountability as to who signed it. apptainer follows
the `OpenPGP <https://www.openpgp.org/>`_ standard to create and
manage these signatures, and the keys used to create them. After
building an image with apptainer, a user can ``apptainer sign``
the container and push it to the Library along with its public PGP key
(stored in :ref:`Keystore <keystore>`). The signature can be verified
(``apptainer verify``) while pulling or downloading the
image. :ref:`This feature <signNverify>` makes it easy to to establish
trust in collaborations within and between teams.

In apptainer 3.4 and above, the root file system of a container
=======
{Singularity} uses SIF as its default container format. A SIF
container is a single file, which makes it easy to manage and
distribute. Inside the SIF file, the container filesystem is held in a
SquashFS object. By default, we mount the container filesystem
directly using SquashFS. On a network filesytem this means that reads
from the container are data-only. Metadata operations happen locally,
speeding up workloads with many small files.

Holding the container image in a single file also enable unique
security features. The container filesystem is immutable, and can be
signed. The signature travels in the SIF image itself so that it is
always possible to verify that the image has not been tampered with or
corrupted.

We use private PGP keys to create a container signature, and the
public key in order to verify the container. Verification of signed
containers happens automatically in ``singularity pull`` commands
against the Sylabs Cloud Container Library. A Keystore in the Sylabs
Cloud makes it easier to share and obtain public keys for container
verification.

A container may be signed once, by a trusted individual who approves
its use. It could also be signed with multiple keys to signify it has
passed each step in a CI/CD QA & Security process. {Singularity} can
be configured with an execution control list (ECL), which requires the
presence of one or more valid signatures, to limit execution to
approved containers.

In {Singularity} 3.4 and above, the root filesystem of a container
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543
(stored in the squashFS partition of SIF) can be encrypted. As a
result, everything inside the container becomes inaccessible without
the correct key or passphrase. The content of the container is
private, even if the SIF file is shared in public.

<<<<<<< HEAD
Unlike other container platforms where execution requires a number of
layers to be extracted to a rootfs directory on the host, apptainer
executes containers in a single step, directly from the immutable
``.sif``. This reduces the attack surface and allows the container to
be easily verified at runtime, to ensure it has not been tampered with.
=======
Encryption and decryption are performed using the Linux kernel's LUKS2
feature. This is the same technology routinely used for full disk
encryption. The encrypted container is mounted directly through the
kernel. Unlike other container formats, an encrypted container is not
decrypted to disk in order to run it.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543


Configuration & Runtime Options
###############################

<<<<<<< HEAD
System administrators who manage apptainer can use configuration
files, to set security restrictions, grant or revoke a user’s
=======
System administrators who manage {Singularity} can use configuration
files to set security restrictions, grant or revoke a user’s
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543
capabilities, manage resources and authorize containers etc.

For example, the `ecl.toml
<\{admindocs\}/configfiles.html#ecl-toml>`_
file allows blacklisting and whitelisting of containers.

Configuration files and their parameters are documented for
administrators documented `here
<\{admindocs\}/configfiles.html>`__.

<<<<<<< HEAD
cgroups support
****************

Starting with v3.0, apptainer added native support for ``cgroups``,
allowing users to limit the resources their containers consume without
the help of a separate program like a batch scheduling system. This
feature can help to prevent DoS attacks where one container seizes
control of all available system resources in order to stop other
containers from operating properly.  To use this feature, a user first
creates a cgroups configuration file. An example configuration file is
installed by default with apptainer as a guide. At runtime, the
``--apply-cgroups`` option is used to specify the location of the
configuration file to apply to the container and cgroups are
configured accordingly. More about cgroups support `here
<\{admindocs\}/configfiles.html#cgroups-toml>`__.

``--security`` options
***********************

apptainer supports a number of methods for further modifying the
security scope and context when running apptainer containers.  Flags
can be passed to the action commands; ``shell``, ``exec``, and ``run``
allowing fine grained control of security. Details about them are
documented :ref:`here <security-options>`.

Security in the Sylabs Cloud
############################

`Sylabs Cloud <https://cloud.sylabs.io/home>`_ consists of a Remote
Builder, a Container Library, and a Keystore. Together, theses
services provide an end-to-end solution for packaging and distributing
applications in secure and trusted containers.

Remote Builder
**************

As mentioned earlier, the apptainer runtime prevents executing code
with root-level permissions on the host system. However, building a
container requires elevated privileges that most shared environments
do not grant their users. The `Build Service
<https://cloud.sylabs.io/builder>`_ aims to address this by allowing
unprivileged users to build containers remotely, with root level
permissions inside the secured service. System administrators can use
the system to monitor which users are building containers, and the
contents of those containers. The Apptainer CLI has native
integration with the Build Service. In addition, a browser interface
to the Build Service also exists, which allows users to build containers using only a web browser.

.. note::

    Please also see the :ref:`Fakeroot feature <fakeroot>` which is a
    secure option for admins in multi-tenant HPC environments and
    similar use cases where they might want to grant a user special
    privileges inside a container.

    Fakeroot has some limitations, and requires unpriveleged user
    namespace support in the host kernel.

Container Library
*****************

The `Container Library <https://cloud.sylabs.io/library>`_ allows
users to store and share apptainer container images in the
apptainer Image Format (SIF). A web front-end allows users to create
new projects within the Container Library, edit documentation
associated with container images, and discover container images
published by their peers.

.. _keystore:

Key Store
*********

The `Key Store <https://cloud.sylabs.io/keystore>`_ is a key
management system offered by Sylabs that uses an `OpenPGP
implementation <https://gnupg.org/>`_ to permit sharing and discovery
of PGP public keys used to sign and verify apptainer container
images. This service is based on the OpenPGP HTTP Keyserver Protocol
(HKP), with several enhancements:

- The Service requires connections to be secured with Transport Layer
  Security (TLS).
- The Service implements token-based authentication, allowing only
  authenticated users to add or modify PGP keys.
- A web front-end allows users to view and search for PGP keys using a
  web browser.


Authentication and encryption
******************************

1. Communication between users, the authentication service other
   services is secured via TLS encryption.

2. The services support authentication of users via signed and encrypted authentication
   tokens.

3. There is no implicit trust relationship between each service. Each
   request between the services is authenticated using the
   authentication token supplied by the user in the associated
   request.



=======
When running a container as root, Singularity can apply hardening
rules using cgroups, seccomp, apparmor. See :ref:`details of these
options here <security-options>`.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543
