#!/usr/bin/python3
# Fabrik file to create a .tgz archive from web_static.

from datetime import datetime
from fabric.api import local
import os


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
        print("web_static packed: {} -> {}Bytes".format(archive_path, os.path.getsize(archive_path)))
        return archive_path
    else:
        return None
