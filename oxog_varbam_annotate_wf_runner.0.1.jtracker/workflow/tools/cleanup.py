#!/usr/bin/env python

import os
import shutil
import sys
import json
import time
from random import randint
import subprocess
from utils import get_task_dict, save_output_json

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

ref_path = task_dict.get('input').get('ref_path')
dir_path = task_dict.get('input').get('dir_path')
donor = task_dict.get('input').get('donor')

task_start = int(time.time())

try:
    if os.path.isdir(ref_path):
        shutil.rmtree(ref_path)

    shutil.rmtree(dir_path)
    shutil.rmtree("OxoG-Dockstore-Tools")
except Exception, e:
    with open('jt.log', 'w') as f: f.write(str(e))
    sys.exit(1)  # task failed

# complete the task

task_stop = int(time.time())

output_json = {
    '':,
    }
}

save_output_json(output_json)
