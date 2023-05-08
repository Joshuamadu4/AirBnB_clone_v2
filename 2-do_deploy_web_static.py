from fabric.api import *
from os import path

env.hosts = ['34.229.69.144', '3.84.168.74']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not path.exists(archive_path):
        return False

    # Extracting the archive filename without the extension
    archive_filename = archive_path.split("/")[-1]
    archive_basename = archive_filename.split(".")[0]

    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, "/tmp/")

    # Creating the directory where we'll uncompress the archive
    run("mkdir -p /data/web_static/releases/{}/".format(archive_basename))

    # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension> on the web server
    run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(archive_filename, archive_basename))

    # Delete the archive from the web server
    run("rm /tmp/{}".format(archive_filename))

    # Moving the contents of the uncompressed archive to the web server's web_static directory
    run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(archive_basename, archive_basename))

    # Removing the unnecessary web_static directory
    run("rm -rf /data/web_static/releases/{}/web_static".format(archive_basename))

    # Delete the symbolic link /data/web_static/current from the web server
    run("rm -rf /data/web_static/current")

    # Creating the new symbolic link
    run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(archive_basename))

    return True

