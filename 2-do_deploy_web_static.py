#!/usr/bin/python3
# Deploy archived files with Fabric.
import os.path
from fabric.api import *

env.hosts = ["54.236.44.9", "3.90.65.191"]
env.user = 'ubuntu'
env.key_filename = '/home/zkrallah/rsa'


def do_deploy(archive_path):
    if not exists(archive_path):
        return False

    try:
        archive_filename = archive_path.split('/')[-1]
        archive_no_ext = archive_filename.split('.')[0]

        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress the archive.
        run('mkdir -p /data/web_static/releases/{}'.format(archive_no_ext))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(archive_filename, archive_no_ext))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move the content of the uncompressed folder to a new location
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(
            archive_no_ext, archive_no_ext))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(archive_no_ext))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current on the web server
        # linked to the new version of your code (/data/web_static/releases/<archive filename without extension>)
        run('ln -s /data/web_static/releases/{} /data/web_static/current'.format(archive_no_ext))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False
