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

task_start = int(time.time())

try:
    donor = '/' + donor
    shutil.rmtree(donor)
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
