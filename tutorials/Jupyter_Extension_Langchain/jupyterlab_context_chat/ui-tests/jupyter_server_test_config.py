"""Server configuration for integration tests.

!! Never use this configuration in production because it
opens the server to the world and provide access to JupyterLab
JavaScript objects through the global window variable.

Import as:

import tutorials.Jupyter_Extension_Langchain.jupyterlab_context_chat.ui-tests.jupyter_server_test_config as tjeljccujstc
"""

from jupyterlab.galata import configure_jupyter_server

configure_jupyter_server(c)

# Uncomment to set server log level to debug level
# c.ServerApp.log_level = "DEBUG"
