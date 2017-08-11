import urllib
import subprocess
import os

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

refFile = task_dict.get('input').get('refFile')

json_input= {}
json_input["vcfdir"] = {}
json_input["vcfdir"].append({
    "path": donor,
    "class": "Directory"
})
json_input["refFile"] = {}
json_input["refFile"].append({
    "path": "Homo_sapiens_assembly19.fasta" ,
    "class": "File"
})
if os.isfile("public_full9.tar.gz") = False
    urllib.urlretrieve('https://personal.broadinstitute.org/gsaksena/public_full9.tar.gz','public_full9.tar.gz')
    print(subprocess.check_output(['tar', 'xvzf', 'public_full9.tar.gz', '--directory', '/ref']))

output_json = {
    'file': os.path.join(cwd, file_name),
    'json_in': json_input
}

save_output_json(output_json)
