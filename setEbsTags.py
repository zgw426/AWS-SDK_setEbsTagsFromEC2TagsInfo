import re
import boto3
import json
import argparse
import sys

# python バージョン確認
if sys.version_info >= (3,8):
    print('Python Version Check [OK] : {0}'.format(sys.version_info) )
else:
    print('Python Version Check [NG] : {0}'.format(sys.version_info) )
    exit()

# オプション
helpStr = ''
helpStr += '-fオプションでEC2のNameタグをフィルタ(前方一致)'
parser = argparse.ArgumentParser(description=helpStr)
parser.add_argument('-f', '--Filter', required=True)
parser.add_argument('-d', '--DryRun', default=True)

args = parser.parse_args()
filterVal = args.Filter
dryrunFlg = args.DryRun

ec2 = boto3.client('ec2')
ec2_data = ec2.describe_instances()

infVal = ""
infFlg = 0

for ec2_reservation in ec2_data['Reservations']:
    for instance in ec2_reservation['Instances']:
        ec2id = instance['InstanceId']
        tagVal = ""
        tagFlg = 0
        ebsVal = ""
        ebsFlg = 0
        setFlg = 0
        #print("ec2id = {0}".format(ec2id) )
        #print("{0}".format(instance['InstanceId']) )
        #print("{0}".format(instance['InstanceType']) )
        #print("{0}".format(instance['PrivateDnsName']) )
        #print("{0}".format(instance['PrivateIpAddress']) )
        #print("{0}".format(instance['BlockDeviceMappings']) )
        for BlockDevice in instance['BlockDeviceMappings']:
            if ebsFlg == 0:
                ebsFlg = 1
            else:
                ebsVal += ","
            ebsVal += '"' + BlockDevice['Ebs']['VolumeId'] + '"'
        for tag in instance['Tags']:
            if tag['Key'].startswith("aws:") == False:
                if tagFlg == 0:
                    tagFlg = 1
                else:
                    tagVal += ","
                if tag['Key'] == "Name":
                    if tag['Value'].startswith(filterVal) == True:
                        setFlg = 1
                tagVal += '{"Key":"' + tag['Key'] + '", "Value":"' + tag['Value'] + '" }'
        if infFlg == 0:
            infFlg = 1
        else:
            infVal += ","
        if setFlg == 1:
            infVal += '{"ec2id":"'+ ec2id +'", "tags": [' + tagVal + '], "EBS": [' + ebsVal + ']  }'

if infVal == ",":
    print("Not HIT")

# 不要な ,(コロン)を削除
if infVal[0] == ",":
    infVal = infVal[1:]
if infVal[-1] == ",":
    infVal = infVal[:-1]

infVal = '[' + infVal + ']'
# 処理対象の一覧情報をjson形式に変換
infJsn = json.loads(infVal)

# 処理対象の情報(infJsn)を表示する
print("==========================================================" )
for i,inf in enumerate(infJsn):
    print("[{0}]\t---------------------------".format(i+1) )
    print("\tEC2 InstanceID = {0}".format(inf['ec2id']) )
    for tag in inf['tags']:
        print("\tタグ名= {0},\t値= {1}".format(tag['Key'], tag['Value']) )
    print("\tEBS IDs= {0}".format(inf['EBS']) )
print("==========================================================" )

# EC2のタグ情報を元にEBSのタグ情報を設定する
def setEbsTag():
    global infJsn
    ec2 = boto3.client('ec2')
    for i,inf in enumerate(infJsn):
        ec2id = inf['ec2id']
        tags  = inf['tags']
        ebss  = inf['EBS']
        response = ec2.create_tags(
            Resources = ebss,
            Tags = tags
        )
        print("[{0}](EBSタグ更新) ---------------------------".format(i+1) )
        print("\tEC2-ID={0}\n\tEBS={1}\n\tTags={2}".format(ec2id, ebss, tags) )

# Dry-Run
if dryrunFlg == True:
    print("[Dry-run:ON] EBSのタグ情報は更新していません。")
    print("=======\n{0}\n=======\n".format(infJsn) )
else:
    print("----------------------------------------------------------" )
    print("[Dry-run:OFF] EBSのタグ情報を更新->開始")
    setEbsTag()
    print("[Dry-run:OFF] EBSのタグ情報を更新->終了")
    print("----------------------------------------------------------" )
