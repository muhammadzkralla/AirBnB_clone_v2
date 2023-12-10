#!/usr/bin/python3
# Pack n Deploy!

from datetime import datetime
from fabric.api import local
import os

env.hosts = ["54.236.44.9", "3.90.65.191"]

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""

    # Create the versions folder if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Generate the archive filename using the current date and time
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_" + now + ".tgz"

    # Compress the web_static folder into the archive
    result = local("tar -czvf versions/{} web_static".format(archive_name))

    # Check if the archive was created successfully
    if result.succeeded:
        archive_path = "versions/{}".format(archive_name)
        print("web_static packed: {} -> {}Bytes".format(archive_path,
              os.path.getsize(archive_path)))
        return archive_path
    else:
        return None

def do_deploy(archive_path):
    """Deploys some arhived folder to two servers..

    Args:
        archive_path (str): The archive file to be uploaded.
    Returns:
        True if success, false if not
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True
