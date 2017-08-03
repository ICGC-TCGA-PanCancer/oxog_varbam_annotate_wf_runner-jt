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

"""
    input:
      donor:
        type: string
      vcflist:
        type: string
      normal_id:
        type: string
      tumor_id:
        type: string
"""
donor = task_dict.get('input').get('donor')
vcflist = task_dict.get('input').get('vcflist')
object_id = task_dict.get('input').get('object_id')
tumor_id = task_dict.get('input').get('tumor_id')

task_start = int(time.time())

try:
    os.mkdir(donor)
    os.remove(normalBam)
    os.remove(tumorBam)
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
