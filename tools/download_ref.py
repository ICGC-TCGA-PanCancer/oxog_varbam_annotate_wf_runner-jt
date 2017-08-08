import urllib
import subprocess

urllib.urlretrieve('https://personal.broadinstitute.org/gsaksena/public_full9.tar.gz','public_full9.tar.gz')
print(subprocess.check_output(['tar', 'xf', 'public_full9.tar.gz']))
