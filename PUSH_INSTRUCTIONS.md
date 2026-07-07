# Push Instructions

Extract this ZIP into the root of your AIMS repository.

```powershell
cd C:\Git\AIMS
git checkout -b genesis-v0.0.0
# copy/extract files here
git status
git add .
git commit -m "chore(genesis): bootstrap AIMS Genesis v0.0.0"
git push -u origin genesis-v0.0.0
git tag -a v0.0.0-genesis -m "AIMS Genesis baseline"
git push origin v0.0.0-genesis
```

If you want to merge into main:

```powershell
git checkout main
git merge genesis-v0.0.0
git push
```
