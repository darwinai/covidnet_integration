from os import system, path
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--imageDir', dest='imageDir', help='location of image directory')
args = parser.parse_args()
print(path.abspath(args.imageDir))
system("px-push " + "--swiftIP 127.0.0.1 " + "--swiftPort 8080 " +
        "--swiftLogin chris:chris1234 " + "--swiftServicesPACS covidnet " +
        "--swiftPackEachDICOM " + f"--xcrdir {path.abspath(args.imageDir)} " + 
        "--parseAllFilesWithSubStr dcm " +"--json > push.json")
system("px-register " + 
        "--CUBEURL http://localhost:8000/api/v1/ " + "--CUBEusername chris " +
        "--CUBEuserpasswd chris1234 " + "--swiftServicesPACS covidnet " +
        "--verbosity 1 " + "--json " + " --logdir /tmp/log " + "--upstreamFile push.json")
