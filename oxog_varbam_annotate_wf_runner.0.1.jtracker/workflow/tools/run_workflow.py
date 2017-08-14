#!/usr/bin/env python

import os
import sys
import json
import time
from random import randint
import subprocess
from utils import get_task_dict, save_output_json

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

tumours = task_dict.get('input').get('tumours')
donor = task_dict.get('input').get('donor')
oxoQScore = task_dict.get('input').get('oxoQScore')
out_dir = task_dict.get('input').get('out_dir')
snv-padding = task_dict.get('input').get('snv-padding')
sv-padding = task_dict.get('input').get('sv-padding')
indel-padding = task_dict.get('input').get('indel-padding')
minibamName = task_dict.get('input').get('minibamName')

task_start = int(time.time())

try:
    json_input= {}
    json_input["vcfdir"] = {
        "path": donor,
        "class": "Directory"
    }
    json_input["refFile"] = {
        "path": "Homo_sapiens_assembly19.fasta" ,
        "class": "File"
    }


    json_input["tumours"] = []


    for t in tumours:
        json_input["tumours"].append({
            "tumourId": t['tumourId'],
            "bamFileName": t['bamFileName'],
            "associatedVcfs": t['associatedVcfs']
        })

    json_input["oxoQScore"] = oxoQScore
    json_input["out_dir"] = out_dir
    json_input["snv-padding"] = snv-padding
    json_input["sv-padding"] = sv-padding
    json_input["indel-padding"] = indel-padding
    json_input["minibamName"] = minibamName

    json_input["inputFileDirectory"] = {}
    json_input["inputFileDirectory"].append({
        "path": donor,
        "location": donor
        "class": "Directory"
    })
    json_input["refDataDir"] = {}
    json_input["refDataDir"].append({
        "path": '/ref',
        "location": '/ref'
        "class": "Directory"
    })

    with open('run.json', 'w') as rj:
        json.dump(json_input, rj)

    r = subprocess.check_output(['cwltool', '--non-strict', 'oxog_varbam_annotate_wf.cwl', 'run.json'])
except Exception, e:
    with open('jt.log', 'w') as f: f.write(str(e))
    sys.exit(1)  # task failed


# complete the task

task_stop = int(time.time())

output_json = {
    'file': os.path.join(cwd, file_name),
    }
}

save_output_json(output_json)
