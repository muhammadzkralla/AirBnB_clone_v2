#!/usr/bin/python3
# Deploy archived files with Fabric.
import os.path
from fabric.api import *

env.hosts = ["54.236.44.9", "3.90.65.191"]

def do_deploy(archive_path):
    if os.path.isfile(archive_path) is False:
        return False

    try :
        archive_filename  = archive_path.split("/")[-1]
        archive_no_ext  = archive_filename.split(".")[0]

        put(archive_path, "/tmp/{}".format(archive_filename))
        run("rm -rf /data/web_static/releases/{}/".format(archive_no_ext))
        run("mkdir -p /data/web_static/releases/{}/".format(archive_no_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(archive_filename, archive_no_ext))
        run("rm /tmp/{}".format(archive_filename))
        run("mv /data/web_static/releases/{}/web_static/* "
                "/data/web_static/releases/{}/".format(archive_no_ext, archive_no_ext))
        run("rm -rf /data/web_static/releases/{}/web_static".format(archive_no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(archive_filename))
    
        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False
