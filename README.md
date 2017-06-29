# fabric-digitalocean-tools - Tools to integrate Fabric with Digital Ocean

Tools to better integrate Fabric with Digital Ocean

- Automagically assign Fabric roles based on tags set on Droplets. For example, deploy code only to web servers (see example below)
- Feel free to send pull request with your own helpers that you use with Fabric and Digital Ocean


## Installation
* `pip install fabric-digitalocean-tools`

## Usage
When running your fab command (in the example below `fab deploy_webserver`), make sure to have an environment variable named `TOKEN` or `DO_TOKEN` with an API token from Digital Ocean. The token only requires read-only rights. You can obtain the token by going to the [API](https://cloud.digitalocean.com/settings/api/tokens) tab.

## Example fabfile
```python
from fabric.api import *
from fabric_digitalocean_tools import *

@roles("webserver")
def deploy_webserver():
    run("do something")

# Set the path to your key file and the default user (usualy root)
env.key_file = "path_to_key_file"
env.user = "root"

# Runs every time you run "fab something".
# Add it at the end of the file to make sure it runs each time.
update_roles_digitalocean()
```
