.. _plugins:

#########
 Plugins
#########

**********
 Overview
**********

{AProject} plugin is a package that can be dynamically loaded by
the {Project} runtime, augmenting {Project} with experimental,
non-standard and/or vendor-specific functionality. Currently, plugins
are able to add commands and flags to {Project}. In the future,
plugins will also be able to interface with more complex subsystems of
the {Project} runtime.

***************
 Using Plugins
***************

The ``list`` command prints the currently installed plugins.

.. code::

   $ {command} plugin list
   There are no plugins installed.

Plugins are packaged and distributed as binaries encoded with the
versatile Singularity Image Format (SIF). However, plugin authors may
also distribute the source code of their plugins. A plugin can be
compiled from its source code with the ``compile`` command. A sample
plugin ``test-plugin`` is included with the {Project} source code.

.. code::

   $ {command} plugin compile examples/plugins/test-plugin/

Upon successful compilation, a SIF file will appear in the directory of
the plugin's source code.

.. code::

   $ ls examples/plugins/test-plugin/ | grep sif
   test-plugin.sif

.. note::

   Currently, **all** plugins must be compiled from the {Project}
   source code tree.

   Also, the plugins mechanism for the Go language that {Project} is
   written in is quite restrictive - it requires extremely close version
   matching of packages used in a plugin to the ones used in the program
   the plugin is built for. Additionally {Project} is using build
   time config to get the source tree location for ``{command} plugin
   compile`` so that you don't need to export environment variables etc,
   and there isn't mismatch between package path information that Go
   uses. This means that at present you must:

   -  Build plugins using the exact same version of the source code, in
      the same location, as was used to build the {Project}
      executable.

   -  Use the exact same version of Go that was used to build the
      executable when compiling a plugin for it.

Every plugin encapsulates various information such as the plugin's
author, the plugin's version, etc. To view this information about a
plugin, use the ``inspect`` command.

.. code::

   $ {command} plugin inspect examples/plugins/test-plugin/test-plugin.sif
   Name: sylabs.io/test-plugin
   Description: This is a short test plugin for {Project}
   Author: Michael Bauer
   Version: 0.0.1

To install a plugin, use the ``install`` command. This operation
requires root privilege.

.. code::

   $ sudo {command} plugin install examples/plugins/test-plugin/test-plugin.sif
   $ {command} plugin list
   ENABLED  NAME
       yes  sylabs.io/test-plugin

After successful installation, the plugin will automatically be enabled.
Any plugin can be disabled with the ``disable`` command and re-enabled
with the ``enable`` command. Both of these operations require root
privilege.

.. code::

   $ sudo {command} plugin disable sylabs.io/test-plugin
   $ {command} plugin list
   ENABLED  NAME
        no  sylabs.io/test-plugin
   $ sudo {command} plugin enable sylabs.io/test-plugin
   $ {command} plugin list
   ENABLED  NAME
       yes  sylabs.io/test-plugin

Finally, to uninstall a plugin, use the ``uninstall`` command. This
operation requires root privilege.

.. code::

   $ sudo {command} plugin uninstall sylabs.io/test-plugin
   Uninstalled plugin "sylabs.io/test-plugin".
   $ {command} plugin list
   There are no plugins installed.

******************
 Writing a Plugin
******************

Developers interested in writing {Project} plugins can get started
by reading the `Go documentation
<https://godoc.org/github.com/{orgrepo}/pkg/plugin>`_ for the
plugin package. Furthermore, reading through the `source code
<https://github.com/{orgrepo}/tree/master/examples/plugins>`_
for the example plugins will prove valuable. More detailed plugin
development documentation is in the works and will be released at a
future date.
