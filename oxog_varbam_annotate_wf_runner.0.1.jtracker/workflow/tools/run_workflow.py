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

refFile = task_dict.get('input').get('refFile')
normalBam = task_dict.get('input').get('normalBam')
ref_path = task_dict.get('input').get('ref_path')
dir_path = task_dict.get('input').get('dir_path')
snv_padding = task_dict.get('input').get('snv-padding')
tumours = task_dict.get('input').get('tumours')
donor = task_dict.get('input').get('donor')
oxoQScore = task_dict.get('input').get('oxoQScore')
out_dir = task_dict.get('input').get('out_dir')
sv_padding = task_dict.get('input').get('sv-padding')
indel_padding = task_dict.get('input').get('indel-padding')
minibamName = task_dict.get('input').get('minibamName')

task_start = int(time.time())

try:
    #convert jtracker json to oxog json
    json_input= {}
    json_input["vcfdir"] = {
        "path": dir_path,
        "class": "Directory"
    }
    json_input["refFile"] = {
        "path": ref_path + "/public/" + refFile,
        "class": "File"
    }

    json_input["normalBam"] = {
        "path": dir_path + '/' + normalBam.keys()[0],
        "class": "File"
    }

    json_input["tumours"] = []


    for t in tumours:
        json_input["tumours"].append({
            "tumourId": t['tumourId'],
            "bamFileName": str(t['bamFileName'].keys()[0]),
            "associatedVcfs": t['associatedVcfs'].keys()
        })

    json_input["oxoQScore"] = oxoQScore
    json_input["out_dir"] = out_dir
    json_input["snv-padding"] = snv_padding
    json_input["sv-padding"] = sv_padding
    json_input["indel-padding"] = indel_padding
    json_input["minibamName"] = minibamName

    json_input["inputFileDirectory"] = {
        "path": dir_path,
        "location": dir_path,
        "class": "Directory"
    }
    json_input["refDataDir"] = {
        "path": ref_path,
        "location": ref_path,
        "class": "Directory"
    }

    # dump as json file
    with open('run.json', 'w') as rj:
        json.dump(json_input, rj, indent=4)
    rj.close()

    #clone oxog and call using cwltool. change this to dockstore as soon as its available
    cwd = os.getcwd()
    print(subprocess.check_output(['git', 'clone', 'https://github.com/ICGC-TCGA-PanCancer/OxoG-Dockstore-Tools.git']))
    os.chdir(os.path.join(cwd,'OxoG-Dockstore-Tools'))
    print(subprocess.check_output(['git', 'submodule', 'update', '--init', '--recursive']))
    os.chdir(cwd)
    print(subprocess.check_output(['cwltool', '--non-strict', '--relax-path-checks', 'OxoG-Dockstore-Tools/oxog_varbam_annotate_wf.cwl', 'run.json']))
    #cwltool --non-strict --relax-path-checks OxoG-Dockstore-Tools/oxog_varbam_annotate_wf.cwl run.json

    # r = subprocess.check_output(['dockstore', '--script', '--debug', 'workflow', 'launch', '--descriptor', 'cwl', '--local-entry', '--entry', './oxog_varbam_annotate_wf.cwl', '--json', 'run.json'])
except Exception, e:
    with open('jt.log', 'w') as f: f.write(str(e))
    sys.exit(1)  # task failed


# complete the task

task_stop = int(time.time())

output_json = {
    'run_workflow_dir': cwd
}

save_output_json(output_json)
