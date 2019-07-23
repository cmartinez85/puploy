from config import Config
from optparse import OptionParser
from transfer import TransferPackages
import sys
import os


def main():
    parser = OptionParser()
    parser.add_option("-s", "--Sources", dest="sources", type="string")
    parser.add_option("-c", "--configFiles", dest="configFiles", default="environments.cfg")
    parser.add_option("-n", "--buildNumber", dest="buildNumber", default="1.0.0.0", type="string")
    parser.add_option("-t", "--TargetNode", dest="targetNode", default=None, type="string")
    parser.add_option("-S", "--SecureMode", dest="secureMode", default=True, type="string")

    (options, args) = parser.parse_args(sys.argv)

    cfg = Config(options.configFiles)
    # print cfg
    print "Destination node:", options.targetNode
    if options.targetNode is None:
        print "Invalid deploy, target host not defined in build parameters"
        exit(1)
    print "Parsing configs..."
    cfg.Server[0].addMapping("host", options.targetNode, "Add target node to config")
    cfg.Server[0].addMapping("location", os.path.join(cfg.Server[0].Baselocation,
                                                      options.buildNumber).replace("\\", "/"),
                             "add buildNumber as final location dir")

    cfg.addMapping("Secure", options.secureMode, "Add secure mode to deploy")
    cfg.Server[0].addMapping("Sources", options.sources, "Add path puppet manifests")
    filename = "%s_last" % options.configFiles
    # cfg.save(filename)
    print "Configs parsed saved in %s_last " % options.configFiles
    print cfg

    TransferPackages(cfg)

if __name__ == '__main__':
    print "this is for tests"
    main()
