import subprocess
from os import path
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--imageDir', dest='imageDir', help='location of image directory')
args = parser.parse_args()
print(path.abspath(args.imageDir))
push_json = open("push.json", "w")
subprocess.run(["px-push", "--swiftIP", "127.0.0.1", "--swiftPort", "8080",
        "--swiftLogin", "chris:chris1234", "--swiftServicesPACS", "covidnet",
        "--swiftPackEachDICOM", "--xcrdir", path.abspath(args.imageDir), 
        "--parseAllFilesWithSubStr", "dcm", "--json"], stdout=push_json)
subprocess.run(["px-register","--CUBEURL", "http://localhost:8000/api/v1/", "--CUBEusername", "chris",
 "--CUBEuserpasswd","chris1234", "--swiftServicesPACS", "covidnet",
 "--verbosity", "1", "--json", "--logdir", "/tmp/log", "--upstreamFile", "push.json"])
subprocess.run(["rm", "push.json"])