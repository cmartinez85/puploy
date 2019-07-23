# puploy

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=cmartinez85_puploy&metric=alert_status)](https://sonarcloud.io/dashboard?id=cmartinez85_puploy)


Application for deploy distributed platform via puppet apply. This script is specially prepared for deploy configurations via Teamcity. 


exec:
python DeployNode.py -n %VersionNumber% -s %SourceCheckOutDir% -c %ConfigFile% -S %SecureMode% -t %TargetNode%


In the config file you need to specify path of RAS key or user/password of the target machine.
