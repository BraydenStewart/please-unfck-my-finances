**What this changes**

**Why**

**Checks**
- [ ] `bash -n run.sh` passes
- [ ] `python -m json.tool` passes on both `config/*.example.json`
- [ ] `git ls-files | grep -Ev '\.example\.|README|spec' | grep -E 'config/|data/|reports/|state/|logs/'` prints nothing
- [ ] Nothing here lets the agent log in, move money, or invent a figure