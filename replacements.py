def variableReplace(app, docname, source):
    """
    Takes the source on rst and replaces all the needed variables declared on
    variable_replacements structure
    """
    result = source[0]
    for key in app.config.variable_replacements:
        result = result.replace(key, app.config.variable_replacements[key])
    source[0] = result


# Add the needed variables to be replaced either on code or on text on the next
# dictionary structure.
variable_replacements = {
    "{InstallationVersion}" : "1.2.5",
    "{admindocs}" : "https://apptainer.org/docs/admin/1.2",
    "{version}": "1.2",
    "{adminversion}": "1.2",
    "{Project}": "Apptainer",
    "{AProject}": "An Apptainer",
    "{aProject}": "an Apptainer",
    "{command}": "apptainer",
    "{ENVPREFIX}": "APPTAINER",
    "{orgrepo}": "apptainer/apptainer",
    "{repobranch}": "release-1.2",
}


def setup(app):
    app.add_config_value('variable_replacements', {}, True)
    app.connect('source-read', variableReplace)
