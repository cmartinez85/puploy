import os
import StringIO
from paramiko import SSHClient, AutoAddPolicy, RSAKey, util
from ConfigNode import ConfigNode

class TransferPackages:

    def __init__(self, cfg):


        for server in cfg.Server:
            conn = self.stablishConnection(server)
            self.transferFiles(conn, server.Sources, server.location, base=server.Baselocation)
            self.changeLinks(conn, server.location)
            ConfigNode(conn, noop=cfg.Secure)
            conn.close()
        return
    def launchConfigs(self,connection):
        config = ConfigNode()
    def stablishConnection(self, cfg):
        util.log_to_file("stablishCon.log")
        ssh = SSHClient()
        # la priv-key esta en local en un path del servidor.
        print "Selecting Auth method..."
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        if cfg.key:
            print "ssh-key-rsa method selected."
            try:
                pr_key=open(cfg.key, 'r').read()
                p_key = StringIO.StringIO(pr_key)
            except:
                print "Error reading private ssh key"
            try:
                pr_key = RSAKey.from_private_key(p_key)
                ssh.connect(cfg.host, username=cfg.user, pkey=pr_key)
            except Exception, e:
                print "Error connecting to the host %s, maybe the host is down " \
                      "or private key is invalid" % cfg.host, e

        else:
            print "Password auth method selected."
            try:
                ssh.connect(cfg.host, username=cfg.user, password=cfg.password)
                print "Connected to ", cfg.host
            except Exception, e:
                print "Error connecting, maybe the password is incorrect or the host is down, ", e
        return ssh

    def transferFiles(self, connection, source, dest, base):
        util.log_to_file("transferfiles.log")
        print "Openning sFTP tunnel..."
        sftp = connection.open_sftp()
        print "Starting transfer to %s" % dest
        try:

            os.chdir(os.path.split(source)[0])
            print "source: ", source
            parent = os.path.split(source)[1]
            print "parent:", parent
            for release in sftp.listdir(base):
                if release == os.path.split(dest)[1]:
                    print "Error: Seems like we are deploying the same release!"
                    exit(1)
            sftp.mkdir(dest)

            print "Creating remote dir ", dest
            for walker in os.walk(parent):
                try:
                    sftp.mkdir(os.path.join(dest, walker[0]).replace("\\", "/"))
                    print "Copying directory  ", os.path.join(dest, walker[0]).replace("\\", "/")
                except Exception, e:
                    pass
                for file in walker[2]:
                    destpath = "/".join([dest, walker[0]])
                    sftp.put(os.path.join(walker[0], file), os.path.join(destpath.replace("\\", "/"), file).replace("\\", "/"))
                    print "Copying file ", "/".join([dest, walker[0], file]).replace("\\", "/")

            # print "%s - %s" % source, dest
            sftp.close()
        except Exception, e:
            print "Error in transfer: ", e
            exit(1)
        return

    def changeLinks(self, connection, buildLocation):
        print "BuildPath:", buildLocation
        manifests = os.path.join(buildLocation, "Puppet", "manifests").replace("\\", "/")
        modules = os.path.join(buildLocation, "Puppet", "modules").replace("\\", "/")
        cmd_unlink_manifests = 'if [ -L "/etc/puppet/manifests" ]; then unlink /etc/puppet/manifests;fi'
        cmd_unlink_modules = 'if [ -L "/etc/puppet/modules" ]; then unlink /etc/puppet/modules;fi'
        cmd_link_manifests = "ln -s %s /etc/puppet/manifests" % manifests
        cmd_link_modules = "ln -s %s /etc/puppet/modules" % modules

        try:
            for cmd in [cmd_unlink_modules, cmd_unlink_manifests, cmd_link_manifests, cmd_link_modules]:
                print "moving links: ", cmd
                connection.exec_command(cmd)

        except Exception as e:
            print "Error: Fail to link new manifests", e
        return
