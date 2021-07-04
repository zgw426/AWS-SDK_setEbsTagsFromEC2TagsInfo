# AWS-SDK_setEbsTagsFromEC2TagsInfo

## 概要
- [AWS SDK for Python (Boto3)] EC2のタグ情報でEBSのタグ情報を設定する

## オプション

`-f`,`-d` の2つのオプションを使用します。

|オプション|概要|
|---|---|
|-f|EC2のNameタグに含まれる文字列を設定します。文字列は前方一致|
|-d|`False`を指定するとdry-runが **無効** になり、EBSのタグ情報を設定します|


スクリプト実行方法

```powershell
PS C:\> python test.py -f {EC2 Nameタグのフィルタ文字列(前方一致)} -d False
```

実行例１）EC2のNameタグの文字列が `aws` で始まるEC2に紐づくEBSをタグ更新の対象にする

```powershell
PS C:\> python test.py -f aws -d False
```

実行例２）EC2のNameタグの文字列が `aws-test` で始まるEC2に紐づくEBSをタグ更新の対象にする

```powershell
PS C:\> python test.py -f aws-test -d False
```

実行例３）`-d` オプションを指定しない場合は dry-runが **有効** になり、処理対象の情報表示のみ行います。

```powershell
PS C:\> python test.py -f {EC2 Nameタグのフィルタ文字列(前方一致)}
```


## スクリプト実行結果サンプル

スクリプトを実行したときの出力サンプルです。

```powershell
PS C:\Users\usr01\test> python setEbsTags.py -f aws-test -d False
Python Version Check [OK] : sys.version_info(major=3, minor=9, micro=5, releaselevel='final', serial=0)
==========================================================
[1]     ---------------------------
        EC2 InstanceID = i-00000000000000001
        タグ名= Name,   値= aws-testかきくけこ
        タグ名= project,        値= projectかきくけこ
        タグ名= cost,   値= costかきくけこ
        EBS IDs= ['vol-000000000000001', 'vol-000000000000002']
==========================================================
----------------------------------------------------------
[Dry-run:OFF] EBSのタグ情報を更新->開始
[1](EBSタグ更新) ---------------------------
        EC2-ID=i-00000000000000001
        EBS=['vol-000000000000001', 'vol-000000000000002']
        Tags=[{'Key': 'Name', 'Value': 'aws-testかきくけこ'}, {'Key': 'project', 'Value': 'projectかきくけこ'}, {'Key': 'cost', 'Value': 'costかきくけこ'}]
[Dry-run:OFF] EBSのタグ情報を更新->終了
----------------------------------------------------------
PS C:\Users\usr01\test> 
```
