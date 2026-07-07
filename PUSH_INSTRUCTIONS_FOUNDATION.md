# Push Instructions

Extract this ZIP into your AIMS repository on a new branch.

```powershell
cd C:\Git\AIMS
git checkout genesis-v0.0.0
git checkout -b foundation-v0.1.0

# extract ZIP here

git add .
git commit -m "feat(foundation): implement AIMS v0.1 executable pipeline"
git push -u origin foundation-v0.1.0
git tag -a v0.1.0-foundation -m "AIMS Foundation executable pipeline"
git push origin v0.1.0-foundation
```
