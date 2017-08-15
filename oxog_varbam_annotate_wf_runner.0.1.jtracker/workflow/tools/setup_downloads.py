#!/usr/bin/env python

import urllib
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
        type: array
      normal_id:
        type: string
      tumours:
        type: dict

"""
donor = task_dict.get('input').get('donor')
#vcflist = task_dict.get('input').get('vcflist')
normal_id = task_dict.get('input').get('normal_id')
tumours= task_dict.get('input').get('tumours')


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

def report(block_size, file_size):
    global prog
    prog += block_size
    rate = prog//file_size
    print("Downloaded %i bytes of %i. Progress : %i" % (prog, file_size, rate))

try:

    #ref file download
    os.mkdir("ref")
    if os.path.isfile("public_full9.tar.gz") == False:
        prog = 0

        urllib.urlretrieve('https://personal.broadinstitute.org/gsaksena/public_full9.tar.gz','public_full9.tar.gz', reporthook=report)
        print(subprocess.check_output(['tar', 'xvzf', 'public_full9.tar.gz', '--directory', '/ref']))
    refdir = os.path.abspath("ref")

    out_tumour =[]
    out_vcf = []
    os.mkdir(donor)
    dirpath = os.path.abspath(donor)
    #normalBam
    #r = subprocess.check_output(['icgc-storage-client', '--profile', 'collab', 'download', '--object-id', str(list(normal_id.values())[0]), '--output-dir', donor])
    out_bam = str(list(normal_id.keys())[0])

    #tumour
    for t in tumours:
        bamObjID = str(list(t["bamFileName"].values())[0])
        bamNames = str(list(t["bamFileName"].keys())[0])
        out_tumour.append(bamNames)
        #f = subprocess.check_output(['icgc-storage-client', '--profile', 'collab', 'download', '--object-id', bamObjID, '--output-dir', donor])


        for i in list(t['associatedVcfs'].values()):
            vcfObjID = str(i)
            out_vcf.append(vcfObjID)
            # = subprocess.check_output(['icgc-storage-client', '--profile', 'collab', 'download', '--object-id', vcfObjID, '--output-dir', donor])

    #only for test get rid of
    for t in tumours:
        open(donor + '/' + (str(list(t["bamFileName"].keys())[0])), 'a').close()

        for i in list(t['associatedVcfs'].keys()):
            open(donor + '/' + (str(i)), 'a').close()

except Exception, e:
    with open('jt.log', 'w') as f: f.write(str(e))
    sys.exit(1)  # task failed


# complete the task

task_stop = int(time.time())

output_json = {
    'bam': out_bam,
    'tumour_bam': out_tumour,
    'vcf': out_vcf,
    'dir_path': dirpath,
    'ref_path': refdir
}

save_output_json(output_json)
