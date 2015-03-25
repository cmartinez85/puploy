import os
import StringIO
from paramiko import SSHClient, AutoAddPolicy, RSAKey, util
import paramiko
class transferPackages:

    def __init__(self, cfg):
        for server in cfg.Server:
            conn = self.stablishConnection(server)
            self.transferFiles(conn, server.localfiles, server.location)
            conn.close()

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



    def transferFiles(self, connection, source, dest):
        util.log_to_file("transferfiles.log")
        print "Openning sFTP tunnel..."
        sftp = connection.open_sftp()
        # print "Starting transfer to %s" % dest
        try:

            os.chdir(os.path.split(source)[0])

            parent = os.path.split(source)[1]

            for walker in os.walk(parent):
                try:

                    sftp.mkdir(os.path.join(dest, walker[0]).replace("\\", "/"))
                    print "Copying directory  ", os.path.join(dest, walker[0])
                except Exception, e:
                    pass
                for file in walker[2]:
                    destpath = "/".join([dest, walker[0]])
                    sftp.put(os.path.join(walker[0], file), os.path.join(destpath.replace("\\", "/"), file).replace("\\", "/"))
                    print "Copying directory  ", "/".join([dest, walker[0], file])
#            sftp.put_all(source, dest)
            print "%s - %s" % source, dest
            sftp.close()
        except Exception, e:
            print "Error: No se han podido copiar los ficheros", e
        return
