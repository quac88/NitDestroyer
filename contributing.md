# Rule for contributing

Feature Development: Developers should create new branches off the development branch for individual features or fixes.
## Format for branch names:
your-name/type-of-commit/few-words-about-what-you-did

## Example:
```
git checkout -b quac/feat/add-player-class
```

After completing the feature, a pull request (PR) is made against the development branch. After the review process, it gets merged.

## Example:
```
git add .
```
```
git commit -m "feat: add player class"
```
```
git push origin quac/feat/add-player-class
```

Release Process: Once the development branch has reached a stable point and is ready for release:
```
git checkout main
```
```
git merge development
```
```
git push origin main
```

# PR Template

## Description of what you changed

## Did you add any new dependencies ex (using a new library, python version, etc)?

## How did you test your changes?

## What issue (if any) does this fix?

## Checklist:
- [ ] I have read the [contributing.md](contributing.md) rules
- [ ] I am follwoing the [branch naming rules](contributing.md#format-for-branch-names)
- [ ] I am using symantic release and angular style commits (see [commits.md](docs/commits.md))
- [ ] I have tested my changes
- [ ] I have added any new dependencies to the [README.md](README.md)
- [ ] I have added any new dependencies to the [requirements.txt](requirements.txt)