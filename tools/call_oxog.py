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

task_start = int(time.time())

try:
        r = subprocess.check_output(['cwltool', '--non-strict', 'oxog_varbam_annotate_wf.cwl', 'dockstore_test.json'])
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
