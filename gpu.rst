.. _gpu:

####################################
GPU Support (NVIDIA CUDA & AMD ROCm)
####################################

{Project} natively supports running application containers that use
NVIDIA's CUDA GPU compute framework, or AMD's ROCm solution. This allows
easy access to users of GPU-enabled machine learning frameworks such as
TensorFlow, regardless of the host operating system. As long as the host
has a driver and library installation for CUDA/ROCm, then it's possible
to e.g. run TensorFlow in an up-to-date Ubuntu 24.04 container, from an
older RHEL 8 host. However, note that since the libraries are bound in
from the host, the libc version present in the container and on the host
must not be too far apart or there will be libc mismatch errors.  Errors
happen when the libc in the container is older than on the host and have
sometimes also been seen when the libc in the container is much newer
than on the host.

Applications that support OpenCL for compute acceleration can also be
used easily, with an additional bind option.

{Project} experimental support is provided to use
Nvidia's ``nvidia-container-cli`` tooling for GPU container setup. This
functionality, accessible via the new ``--nvccli`` flag, improves
compatibility with OCI runtimes and exposes additional container
configuration options.

*****************************
NVIDIA GPUs & CUDA (Standard)
*****************************

Commands that ``run``, or otherwise execute containers (``shell``,
``exec``) can take an ``--nv`` option, which will setup the container's
environment to use an NVIDIA GPU and the basic CUDA libraries to run a
CUDA enabled application. The ``--nv`` flag will:

-  Ensure that the ``/dev/nvidiaX`` device entries are available inside
   the container, so that the GPU cards in the host are accessible.

-  Locate and bind the basic CUDA libraries from the host into the
   container, so that they are available to the container, and match the
   kernel GPU driver on the host.

-  Set the ``LD_LIBRARY_PATH`` inside the container so that the bound-in
   version of the CUDA libraries are used by applications run inside the
   container.

Requirements
============

To use the ``--nv`` flag to run a CUDA application inside a container
you must ensure that:

-  The host has a working installation of the NVIDIA GPU driver, and a
   matching version of the basic NVIDIA/CUDA libraries. The host *does
   not* need to have an X server running, unless you want to run
   graphical apps from the container.

-  The NVIDIA libraries are in the system's library search path.

-  The application inside your container was compiled for a CUDA
   version, and device capability level, that is supported by the host
   card and driver.

These requirements are usually satisfied by installing the NVIDIA
drivers and CUDA packages directly from the NVIDIA website. Linux
distributions may provide NVIDIA drivers and CUDA libraries, but they
are often outdated which can lead to problems running applications
compiled for the latest versions of CUDA.

{Project} will find the NVIDIA/CUDA libraries on your host using the
list of libraries in the configuration file
``etc/{command}/nvbliblist``, and resolving paths through the
``ldconfig`` cache. At time of release this list is appropriate for the
latest stable CUDA version. It can be modified by the administrator to
add additional libraries if necessary. See the admin guide for more
details.

Example - tensorflow-gpu
========================

Tensorflow is commonly used for machine learning projects but can be
difficult to install on older systems, and is updated frequently.
Running tensorflow from a container removes installation problems and
makes trying out new versions easy.

The official tensorflow repository on Docker Hub contains NVIDA GPU
supporting containers, that will use CUDA for processing. You can view
the available versions on the `tags page on Docker Hub
<https://hub.docker.com/r/tensorflow/tensorflow/tags>`__

The container is large, so it's best to build or pull the docker image
to a SIF before you start working with it:

.. code::

   $ {command} pull docker://tensorflow/tensorflow:latest-gpu
   ...
   INFO:    Creating SIF file...
   [=====================================================================]
   100 % 0s
   INFO:    Build complete: tensorflow_latest-gpu.sif

Then run the container with GPU support:

.. code::

   $ {command} run --nv tensorflow_latest-gpu.sif

   ________                               _______________
   ___  __/__________________________________  ____/__  /________      __
   __  /  _  _ \_  __ \_  ___/  __ \_  ___/_  /_   __  /_  __ \_ | /| / /
   _  /   /  __/  / / /(__  )/ /_/ /  /   _  __/   _  / / /_/ /_ |/ |/ /
   /_/    \___//_/ /_//____/ \____//_/    /_/      /_/  \____/____/|__/


   You are running this container as user with ID 1000 and group 1000,
   which should map to the ID and group for your user on the Docker host. Great!

   {Project}>

You can verify the GPU is available within the container by using the
tensorflow ``list_local_devices()`` function:

.. code::

   {Project}> python
   Python 2.7.15+ (default, Jul  9 2019, 16:51:35)
   [GCC 7.4.0] on linux2
   Type "help", "copyright", "credits" or "license" for more information.
   >>> from tensorflow.python.client import device_lib
   >>> print(device_lib.list_local_devices())
   2019-11-14 15:32:09.743600: I tensorflow/core/platform/cpu_feature_guard.cc:142] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
   2019-11-14 15:32:09.784482: I tensorflow/core/platform/profile_utils/cpu_utils.cc:94] CPU Frequency: 3292620000 Hz
   2019-11-14 15:32:09.787911: I tensorflow/compiler/xla/service/service.cc:168] XLA service 0x565246634360 executing computations on platform Host. Devices:
   2019-11-14 15:32:09.787939: I tensorflow/compiler/xla/service/service.cc:175]   StreamExecutor device (0): Host, Default Version
   2019-11-14 15:32:09.798428: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library libcuda.so.1
   2019-11-14 15:32:09.842683: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:1006] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
   2019-11-14 15:32:09.843252: I tensorflow/compiler/xla/service/service.cc:168] XLA service 0x5652469263d0 executing computations on platform CUDA. Devices:
   2019-11-14 15:32:09.843265: I tensorflow/compiler/xla/service/service.cc:175]   StreamExecutor device (0): GeForce GT 730, Compute Capability 3.5
   2019-11-14 15:32:09.843380: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:1006] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
   2019-11-14 15:32:09.843984: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1618] Found device 0 with properties:
   name: GeForce GT 730 major: 3 minor: 5 memoryClockRate(GHz): 0.9015
   ...

Multiple GPUs
=============

By default, {Project} makes all host devices available in the
container. When the ``--contain`` option is used a minimal ``/dev`` tree
is created in the container, but the ``--nv`` option will ensure that
all nvidia devices on the host are present in the container.

This behaviour is different to ``nvidia-docker`` where an
``NVIDIA_VISIBLE_DEVICES`` environment variable is used to control
whether some or all host GPUs are visible inside a container. The
``nvidia-container-runtime`` explicitly binds the devices into the
container dependent on the value of ``NVIDIA_VISIBLE_DEVICES``.

To control which GPUs are used in {aProject} container that is run
with ``--nv`` you can set ``{ENVPREFIX}ENV_CUDA_VISIBLE_DEVICES`` before
running the container, or ``CUDA_VISIBLE_DEVICES`` inside the container.
This variable will limit the GPU devices that CUDA programs see.

E.g. to run the tensorflow container, but using only the first GPU in
the host, we could do:

.. code::

   $ {ENVPREFIX}ENV_CUDA_VISIBLE_DEVICES=0 {command} run --nv tensorflow_latest-gpu.sif

   # or

   $ export {ENVPREFIX}ENV_CUDA_VISIBLE_DEVICES=0
   $ {command} run tensorflow_latest-gpu.sif

Troubleshooting
===============

If the host installation of the NVIDIA / CUDA driver and libraries is
working and up-to-date there are rarely issues running CUDA programs
inside of {Project} containers. The most common issue seen is:

CUDA_ERROR_UNKNOWN when everything seems to be correctly configured
-------------------------------------------------------------------

CUDA depends on multiple kernel modules being loaded. Not all of the
modules are loaded at system startup. Some portions of the NVIDA driver
stack are initialized when first needed. This is done using a setuid
root binary, so initializing can be triggered by any user on the host.
In {Project} containers, privilege escalation is blocked, so the
setuid root binary cannot initialize the driver stack fully.

If you experience ``CUDA_ERROR_UNKNOWN`` in a container, initialize the
driver stack on the host first, by running a CUDA program there or
``modprobe nvidia_uvm`` as root, and using ``nvidia-persistenced`` to
avoid driver unload.

*****************************************
NVIDIA GPUs & CUDA (nvidia-container-cli)
*****************************************

The ``--nvccli`` option instructs
{Project} to perform GPU container setup using the
``nvidia-container-cli`` utility. This utility must be installed
separately from {Project}. It is available in the repositories of
some distributions, and at:
https://nvidia.github.io/libnvidia-container/

.. warning::

   This feature is considered experimental in {Project} as of now. It
   cannot not replace the legacy NVIDIA support in all situations, and
   should be tested carefully before use in production workflows.

Using ``nvidia-container-cli`` to configure a container for GPU
operation has a number of advantages, including:

-  The tool is maintained by NVIDIA, and will track new features /
   libraries in new CUDA releases closely.
-  Support for passing only specific GPUs / MIG devices into the
   container.
-  Support for providing different classes of GPU capability to the
   container, e.g. compute, graphics, and display functionality.
-  Configuration via the same environment variables that are in use with
   OCI containers.

Requirements & Limitations
==========================

-  ``nvidia-container-cli`` must be installed on your host.
   It must be able to be found by the ``binary path`` set in
   ``{command}.conf`` which by default includes the user's PATH.

-  For security reasons, ``--nvccli`` cannot be used with
   privileged mode in a setuid install of {Project}.
   ``nvidia-container-cli`` also requires writing to the image, so
   either the ``--writable`` (``-w``) or ``--writable-tmpfs`` option
   is also required; if neither is given, ``--writable-tmpfs`` is
   implied.
   That also means that the permissions on system directories such as
   ``/usr/bin`` have to be writable, so either use a sandbox image that
   has that directory writable by the user (for example built with
   the ``--fix-perms`` option) or use ``--fakeroot``.

-  There are known problems with library discovery for the current
   ``nvidia-container-cli`` in recent Debian distributions. See `this
   GitHub issue <https://github.com/NVIDIA/nvidia-docker/issues/1399>`__

Example - tensorflow-gpu
========================

Tensorflow can be run using ``--nvccli`` in a similar manner as the
standard ``--nv`` binding approach when run unprivleged. Build the
large container into a sandbox:

.. code::

   $ {command} build --sandbox tensorflow_latest-gpu docker://tensorflow/tensorflow:latest-gpu
   INFO:    Starting build...
   ...
   INFO:    Creating sandbox directory...
   INFO:    Build complete: tensorflow_latest-gpu

Then run the container with ``nvidia-container-cli`` GPU support:

.. code::

   $ {command} run --nvccli tensorflow_latest-gpu

   ________                               _______________
   ___  __/__________________________________  ____/__  /________      __
   __  /  _  _ \_  __ \_  ___/  __ \_  ___/_  /_   __  /_  __ \_ | /| / /
   _  /   /  __/  / / /(__  )/ /_/ /  /   _  __/   _  / / /_/ /_ |/ |/ /
   /_/    \___//_/ /_//____/ \____//_/    /_/      /_/  \____/____/|__/


   You are running this container as user with ID 1000 and group 1000,
   which should map to the ID and group for your user on the Docker host. Great!

   {Project}>

You can verify the GPU is available within the container by using the
tensorflow ``list_local_devices()`` function:

.. code::

   {Project}> python
   Python 2.7.15+ (default, Jul  9 2019, 16:51:35)
   [GCC 7.4.0] on linux2
   Type "help", "copyright", "credits" or "license" for more information.
   >>> from tensorflow.python.client import device_lib
   >>> print(device_lib.list_local_devices())
   ...
   device_type: "GPU"
   memory_limit: 14474280960
   locality {
     bus_id: 1
     links {
     }
   }
   incarnation: 13349913758992036690
   physical_device_desc: "device: 0, name: Tesla T4, pci bus id: 0000:00:1e.0, compute capability: 7.5"
   ...

GPU Selection
=============

When running with ``--nvccli``, by default {Project} will expose all
GPUs on the host inside the container. This mirrors the functionality of
the standard GPU support for the most common use-case.

Setting the ``{ENVPREFIX}_CUDA_VISIBLE_DEVICES`` environment variable
before running a container is still supported, to control which GPUs are
used by CUDA programs that honor ``CUDA_VISIBLE_DEVICES``. However, more
powerful GPU isolation is possible using the ``--contain`` (or ``-c``) flag and
``NVIDIA_VISIBLE_DEVICES`` environment variable. This controls which GPU
devices are bound into the ``/dev`` tree in the container.

For example, to pass only the 2nd and 3rd GPU into a container running
on a system with 4 GPUs, run the following:

.. code::

   $ export NVIDIA_VISIBLE_DEVICES=1,2
   $ {command} run -uwc --nvccli tensorflow_latest-gpu

Note that:

-  ``NVIDIA_VISIBLE_DEVICES`` is not prepended with ``{ENVPREFIX}_`` as
   this variable controls container setup, and is not passed into the
   container.

-  The GPU device identifiers start at 0, so 1,2 refers to the 2nd and
   3rd GPU.

-  You can use GPU UUIDs in place of numeric identifiers. Use
   ``nvidia-smi -L`` to list both numeric IDs and UUIDs available on the
   system.

-  ``all`` can be used to pass all available GPUs into the container.

If you use ``--contain`` without setting ``NVIDIA_VISIBLE_DEVICES``, no
GPUs will be available in the container, and a warning will be shown:

.. code::

   $ {command} run -uwc --nvccli tensorflow_latest-gpu
   WARNING: When using nvidia-container-cli with --contain NVIDIA_VISIBLE_DEVICES
   must be set or no GPUs will be available in container.

To restore the behaviour of the standard GPU handling, set
``NVIDIA_VISIBLE_DEVICES=0`` when running with ``--contain``.

If your system contains Ampere or newer GPUs that support virtual MIG
devices, you can specify MIG identifiers / UUIDs.

.. code::

   $ export NVIDIA_VISIBLE_DEVICES=MIG-GPU-5c89852c-d268-c3f3-1b07-005d5ae1dc3f/7/0

{Project} does not configure MIG partitions. It is expected that
these would be statically configured by the system administrator, or
setup dynamically by a job scheduler / workflow system according to the
requirements of the job.

Other GPU Options
=================

In ``--nvccli`` mode, {Project} understands the following additional
environment variables. Note that these environment variables are read
from the environment where ``{command}`` is run. {Project} does
not currently read these settings from the container environment.

-  ``NVIDIA_DRIVER_CAPABILITIES`` controls which libraries and utilities
   are mounted in the container, to support different requirements. The
   default value under {Project} is ``compute,utility``, which will
   provide CUDA functionality and basic utilities such as
   ``nvidia-smi``. Other options include ``graphics`` for OpenGL/Vulkan
   support, ``video`` for the codecs SDK, and ``display`` to use X11
   from a container.

-  ``NVIDIA_REQUIRE_*`` variables allow specifying requirements, which
   will be checked by ``nvidia-container-cli`` prior to starting the
   container. Constraints can be set on ``cuda``, ``driver``, ``arch``,
   and ``brand`` values. Docker/OCI images may set these variables
   inside the container, to indicate runtime requirements. However,
   these container variables are not yet interpreted by {Project}.

-  ``NVIDIA_DISABLE_REQUIRE`` will disable the enforcement of any
   ``NVIDIA_REQUIRE_*`` requirements that are set.

Full details of the supported values for these environment variables can
be found in the container-toolkit guide:

https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/user-guide.html#environment-variables-oci-spec

***************
AMD GPUs & ROCm
***************

{Project} has a ``--rocm`` flag to support GPU compute with the
ROCm framework using AMD Radeon GPU cards.

Commands that ``run``, or otherwise execute containers (``shell``,
``exec``) can take an ``--rocm`` option, which will setup the
container's environment to use a Radeon GPU and the basic ROCm libraries
to run a ROCm enabled application. The ``--rocm`` flag will:

-  Ensure that the ``/dev/dri/`` device entries are available inside the
   container, so that the GPU cards in the host are accessible.

-  Locate and bind the basic ROCm libraries from the host into the
   container, so that they are available to the container, and match the
   kernel GPU driver on the host.

-  Set the ``LD_LIBRARY_PATH`` inside the container so that the bound-in
   version of the ROCm libraries are used by application run inside the
   container.

Requirements
============

To use the ``--rocm`` flag to run a CUDA application inside a container
you must ensure that:

-  The host has a working installation of the ``amdgpu`` driver, and a
   compatible version of the basic ROCm libraries. The host *does not*
   need to have an X server running, unless you want to run graphical
   apps from the container.

-  The ROCm libraries are in the system's library search path.

-  The application inside your container was compiled for a ROCm version
   that is compatible with the ROCm version on your host.

These requirements can be satisfied by following the requirements on the
`ROCm web site <https://rocm.github.io/ROCmInstall.html>`__

Example - tensorflow-rocm
=========================

Tensorflow is commonly used for machine learning projects, but can be
difficult to install on older systems, and is updated frequently.
Running tensorflow from a container removes installation problems and
makes trying out new versions easy.

The rocm tensorflow repository on Docker Hub contains Radeon GPU
supporting containers, that will use ROCm for processing. You can view
the available versions on the `tags page on Docker Hub
<https://hub.docker.com/r/rocm/tensorflow/tags>`__

The container is large, so it's best to build or pull the docker image
to a SIF before you start working with it:

.. code::

   $ {command} pull docker://rocm/tensorflow:latest
   ...
   INFO:    Creating SIF file...
   [=====================================================================]
   100 % 0s
   INFO:    Build complete: tensorflow_latest.sif

Then run the container with GPU support:

.. code::

   $ {command} run --rocm tensorflow_latest.sif

You can verify the GPU is available within the container by using the
tensorflow ``list_local_devices()`` function:

.. code::

   {Project}> ipython
   Python 3.5.2 (default, Jul 10 2019, 11:58:48)
   Type 'copyright', 'credits' or 'license' for more information
   IPython 7.8.0 -- An enhanced Interactive Python. Type '?' for help.
   >>> from tensorflow.python.client import device_lib
   ...
   >>> print(device_lib.list_local_devices())
   ...
   2019-11-14 16:33:42.750509: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1651] Found device 0 with properties:
   name: Lexa PRO [Radeon RX 550/550X]
   AMDGPU ISA: gfx803
   memoryClockRate (GHz) 1.183
   pciBusID 0000:09:00.0
   ...

*******************
OpenCL Applications
*******************

Both the ``--rocm`` and ``--nv`` flags will bind the vendor OpenCL
implementation libraries into a container that is being run. However,
these libraries will not be used by OpenCL applications unless a vendor
icd file is available under ``/etc/OpenCL/vendors`` that directs OpenCL
to use the vendor library.

The simplest way to use OpenCL in a container is to ``--bind
/etc/OpenCL`` so that the icd files from the host (which match the
bound-in libraries) are present in the container.

Example - Blender OpenCL
========================

The `Sylabs examples repository <https://github.com/sylabs/examples>`__
contains an example container definition for the 3D modelling
application 'Blender'.

The latest versions of Blender supports OpenCL rendering. You can run
Blender as a graphical application that will make use of a local Radeon
GPU for OpenCL compute using the container that has been published to
the Sylabs library:

.. code::

   $ {command} exec --rocm --bind /etc/OpenCL library://sylabs/examples/blender blender

Note the *exec* used as the *runscript* for this container is setup for
batch rendering (which can also use OpenCL).
