.. _plugins:

=======
Plugins
=======

--------
Overview
--------

<<<<<<< HEAD
A apptainer plugin is a package that can be dynamically loaded by the
apptainer runtime, augmenting apptainer with experimental, non-standard
and/or vendor-specific functionality. Currently, plugins are able to add
commands and flags to apptainer. In the future, plugins will also be able to
interface with more complex subsystems of the apptainer runtime.
=======
A {Singularity} plugin is a package that can be dynamically loaded by the
{Singularity} runtime, augmenting {Singularity} with experimental, non-standard
and/or vendor-specific functionality. Currently, plugins are able to add
commands and flags to {Singularity}. In the future, plugins will also be able to
interface with more complex subsystems of the {Singularity} runtime.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543

-------------
Using Plugins
-------------

The ``list`` command prints the currently installed plugins.

.. code-block:: none

    $ apptainer plugin list
    There are no plugins installed.

Plugins are packaged and distributed as binaries encoded with the versatile
apptainer Image Format (SIF). However, plugin authors may also distribute the
source code of their plugins. A plugin can be compiled from its source code
with the ``compile`` command. A sample plugin ``test-plugin`` is included with
<<<<<<< HEAD
the apptainer source code.
=======
the {Singularity} source code.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543

.. code-block:: none

    $ apptainer plugin compile examples/plugins/test-plugin/

Upon successful compilation, a SIF file will appear in the directory of the
plugin's source code.

.. code-block:: none

    $ ls examples/plugins/test-plugin/ | grep sif
    test-plugin.sif

.. note::

<<<<<<< HEAD
    Currently, **all** plugins must be compiled from the apptainer source
    code tree.

    Also, the plugins mechanism for the Go language that apptainer is written
    in is quite restrictive - it requires extremely close version matching of
    packages used in a plugin to the ones used in the program the plugin is
    built for. Additionally apptainer is using build time config to get the
    source tree location for ``apptainer plugin compile`` so that you don't
=======
    Currently, **all** plugins must be compiled from the {Singularity} source
    code tree.

    Also, the plugins mechanism for the Go language that {Singularity} is written
    in is quite restrictive - it requires extremely close version matching of
    packages used in a plugin to the ones used in the program the plugin is
    built for. Additionally {Singularity} is using build time config to get the
    source tree location for ``singularity plugin compile`` so that you don't
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543
    need to export environment variables etc, and there isn't mismatch between
    package path information that Go uses.  This means that at present you must:

    * Build plugins using the exact same version of the source code, in the
<<<<<<< HEAD
      same location, as was used to build the apptainer executable.
=======
      same location, as was used to build the {Singularity} executable.
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543
    * Use the exact same version of Go that was used to build the executable
      when compiling a plugin for it.

Every plugin encapsulates various information such as the plugin's author, the
plugin's version, etc. To view this information about a plugin, use the
``inspect`` command.

.. code-block:: none

    $ apptainer plugin inspect examples/plugins/test-plugin/test-plugin.sif
    Name: sylabs.io/test-plugin
<<<<<<< HEAD
    Description: This is a short test plugin for apptainer
=======
    Description: This is a short test plugin for {Singularity}
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543
    Author: Michael Bauer
    Version: 0.0.1

To install a plugin, use the ``install`` command. This operation requires root
privilege.

.. code-block:: none

    $ sudo apptainer plugin install examples/plugins/test-plugin/test-plugin.sif
    $ apptainer plugin list
    ENABLED  NAME
        yes  sylabs.io/test-plugin

After successful installation, the plugin will automatically be enabled. Any
plugin can be disabled with the ``disable`` command and re-enabled with the
``enable`` command. Both of these operations require root privilege.

.. code-block:: none

    $ sudo apptainer plugin disable sylabs.io/test-plugin
    $ apptainer plugin list
    ENABLED  NAME
         no  sylabs.io/test-plugin
    $ sudo apptainer plugin enable sylabs.io/test-plugin
    $ apptainer plugin list
    ENABLED  NAME
        yes  sylabs.io/test-plugin

Finally, to uninstall a plugin, use the ``uninstall`` command. This operation
requires root privilege.

.. code-block:: none

    $ sudo apptainer plugin uninstall sylabs.io/test-plugin
    Uninstalled plugin "sylabs.io/test-plugin".
    $ apptainer plugin list
    There are no plugins installed.

----------------
Writing a Plugin
----------------

<<<<<<< HEAD
Developers interested in writing apptainer plugins can get started by reading
=======
Developers interested in writing {Singularity} plugins can get started by reading
>>>>>>> 6910ee5cb0bbe15b17c418636870ad46bae27543
the `Go documentation
<https://godoc.org/github.com/sylabs/apptainer/pkg/plugin>`_ for the plugin
package. Furthermore, reading through the `source code
<https://github.com/apptainer/tree/master/examples/plugins>`_
for the example plugins will prove valuable. More detailed plugin
development documentation is in the works and will be released at a future
date.
