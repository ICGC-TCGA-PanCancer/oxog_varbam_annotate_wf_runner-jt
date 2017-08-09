import urllib
import subprocess

json_input= {}
json_input["refFile"].append({
    "path": "Homo_sapiens_assembly19.fasta" ,
    "class": "File"
})
urllib.urlretrieve('https://personal.broadinstitute.org/gsaksena/public_full9.tar.gz','public_full9.tar.gz')
print(subprocess.check_output(['tar', 'xf', 'public_full9.tar.gz']))
