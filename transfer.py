import StringIO
from paramiko import SSHClient, AutoAddPolicy, RSAKey


class transferPackages:

    def __init__(self, cfg):
        for server in cfg.Pool:
            conn = self.stablishConnection(server)
            self.transferFiles(conn, cfg.localfiles, cfg.location)
            conn.close()

    def stablishConnection(self, cfg):
        ssh = SSHClient()
        # la priv-key esta en local en un path del servidor.
        if cfg.Server.key is not None:
            try:
                pr_key=open(cfg.Server.key, 'r').read()
                p_key = StringIO.StringIO(pr_key)
                ssh.set_missing_host_key_policy(AutoAddPolicy())
            except:
                print "Error reading private ssh key"
            try:
                pr_key = RSAKey.from_private_key(p_key)
                ssh.connect(cfg.Server.host, username=cfg.Server.user, pkey=pr_key)
            except:
                print "Error connecting to the host %s, maybe the host is down " \
                      "or private key is invalid" % cfg.Server.host

        else:
            try:
                ssh.connect(cfg.Server.host, username=cfg.Server.user, password=cfg.password)
            except:
                print "Error connecting, maybe the password is incorrect or the host is down"
        return ssh

    def transferFiles(self, connection, source, dest):
        sftp = connection.open_sftp()
        print "Starting transfer to %s" % dest
        try:
            sftp.put(source, dest)
            sftp.close()
        except:
            print "Error: No se han podido copiar los ficheros"

        return
