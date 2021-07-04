# AWS-SDK_setEbsTagsFromEC2TagsInfo

## 概要
- [AWS SDK for Python (Boto3)] EC2のタグ情報でEBSのタグ情報を設定する

## オプション

`-f`,`-d` の2つのオプションを使用します。

|オプション|概要|
|---|---|
|-f|EC2のNameタグに含まれる文字列を設定します。文字列は前方一致|
|-d|`False`を指定するとEBSのタグ情報を設定します|


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

実行例３）`-d` オプションを指定しない場合は dry-run になり、実行対象の情報の表示のみ行います。

```powershell
PS C:\> python test.py -f {EC2 Nameタグのフィルタ文字列(前方一致)}
```
