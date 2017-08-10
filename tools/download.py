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
      associatedVcfs:
        type: array
"""
donor = task_dict.get('input').get('donor')
#vcflist = task_dict.get('input').get('vcflist')
object_id = task_dict.get('input').get('object_id')
tumor_id = task_dict.get('input').get('tumor_id')
vcf = task_dict.get('input').get('vcflist')

#temp hard code (obj ids may not line up correctly just for test)
objid = {'6a40a6df68474d9357bacc988ea3e30e.bam':'0a84c77a-510c-5d5e-904b-723464025c76',
        '7676725d9976424c98f7a92075e65554.bam':'85fbc8e4-382c-5e1f-9430-7c68ed490207',
        "f8f0136b-09ec-d079-e040-11ac0c4842e7.broad-mutect-v3.20160222.somatic.snv_mnv.vcf.gz":'6963fa25-5037-50d8-bb15-4e3e9e891d86',
        "f8f0136b-09ec-d079-e040-11ac0c4842e7.broad-dRanger_snowman-10.20160101.somatic.sv.vcf.gz":'79286996-7da5-52b6-a21e-392e7d8489fa',
        "f8f0136b-09ec-d079-e040-11ac0c4842e7.broad-snowman-10.20160101.somatic.indel.vcf.gz":'400f343a-149c-54c5-aeef-d649ea3a6577',
        "f8f0136b-09ec-d079-e040-11ac0c4842e7.dkfz-snvCalling_1-0-132-1-hpc.1602051320.somatic.snv_mnv.vcf.gz":'100c52c6-d5cf-5720-91fb-c5d4a7ae165e',
        "f8f0136b-09ec-d079-e040-11ac0c4842e7.dkfz-indelCalling_1-0-132-1-hpc.1602051320.somatic.indel.vcf.gz":'b669398b-e461-5359-8e83-fff07e391c5e',
        "f8f0136b-09ec-d079-e040-11ac0c4842e7.embl-delly_1-0-0-preFilter-hpc.150901.somatic.sv.vcf.gz":'cff611fb-96dd-5fd9-9b50-43083177e828',
        "f8f0136b-09ec-d079-e040-11ac0c4842e7.MUSE_1-0rc-b391201-vcf.20160101.somatic.snv_mnv.vcf.gz":'acad417a-20d1-5a94-89a3-fc4bd9c3b863',
        "f8f0136b-09ec-d079-e040-11ac0c4842e7.svcp_1-0-5.20150306.somatic.snv_mnv.vcf.gz":'595c7ddb-dcde-5867-9b63-74bb1b23cfe4',
        "f8f0136b-09ec-d079-e040-11ac0c4842e7.svcp_1-0-5.20150306.somatic.indel.vcf.gz":'6508ab98-9733-5cf3-90be-45aac84de77b',
        "f8f0136b-09ec-d079-e040-11ac0c4842e7.svfix2_4-0-12.20160213.somatic.sv.vcf.gz":'08bccc42-4a01-5a76-a911-ea5544d1c725'}

task_start = int(time.time())

try:
    os.mkdir(donor)

    if object_id:
        r = subprocess.check_output(['icgc-storage-client', '--profile', 'collab', 'download', '--object-id', objid[object_id], '--output-dir', donor])
    else:
        json_input["tumours"] = {}
        json_input["tumours"].append({
            "tumourId": tumour_id,
            "bamFileName": tumour_id
        })
        for i in vcf:
            k = subprocess.check_output(['icgc-storage-client', '--profile', 'collab', 'download', '--object-id', objid[i], '--output-dir', donor])
            json_input["bamFileName"].append({i})

        f = subprocess.check_output(['icgc-storage-client', '--profile', 'collab', 'download', '--object-id', objid[tumor_id], '--output-dir', donor])

except Exception, e:
    with open('jt.log', 'w') as f: f.write(str(e))
    sys.exit(1)  # task failed


# complete the task

task_stop = int(time.time())

output_json = {
    'file': os.path.join(cwd, file_name)
    'json_in': json_input
}

save_output_json(output_json)
