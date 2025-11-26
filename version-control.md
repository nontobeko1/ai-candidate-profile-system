# 📌 Version Control Strategy — AI Candidate Profiling System  
**Repository:** nontobeko1/ai-candidate-profile-system  
**Version:** 1.0  
**Created:** 2025-11-26  
**Maintainer:** Nontobeko Dube  

---

# 1. Overview
This document defines the version control standards for the **AI Candidate Profiling System**.  
It ensures consistency, security, clean Git history, and efficient collaboration.

---

# 2. Branch Structure

```
main       → Always stable, production-ready code  
dev        → Integration branch for new features  
feature/*  → Individual features  
fix/*      → Bug fixes  
release/*  → Pre-production release prep  
hotfix/*   → Urgent fixes applied directly on main
```

### Branch Naming Examples:
- `feature/ai-extraction-engine`
- `feature/recruiter-dashboard`
- `fix/ppt-generation-bug`
- `hotfix/security-cleanup`

---

# 3. Commit Message Guidelines

Use the **Conventional Commit Standard**:

```
feat: Added AI extraction workflow 
fix: Corrected SQL write failure  
docs: Updated SRS  
style: Reformatted HTML templates  
refactor: Cleaned processing logic 
test: Added unit tests for OCR  
chore: Updated dependencies 
```

### Rules:
- Present tense  
- No full stop  
- Clear, meaningful changes  
- One topic per commit  

---

# 4. Pull Request Workflow

### PRs MUST:
✔ Target the **dev** branch  
✔ Include description + screenshots if UI changes  
✔ Pass linting & tests  
✔ Contain no secrets or API keys  
✔ Be reviewed & approved before merge  

### PR Naming:
```
[Feature] AI Extraction Pipeline
[Fix] PPT Layout Overlap
[Improvement] Faster Upload Flow
```

---

# 5. Version Tagging (Releases)

Semantic versioning:

```
MAJOR.MINOR.PATCH
```

Examples:
- `v1.0.0` — First stable release  
- `v1.1.0` — Added recruiter dashboard  
- `v1.1.1` — Bug fix for login  

Tags are automatically created on `main` only.

---

# 6. Secret Management Requirements

### ❗ Absolutely forbidden in the repo:
- `.env`
- API keys (Google, Gemini, OpenAI)
- Database credentials
- Certificates

### Allowed files:
- `.env.example` (placeholder only)

### Enforced by:
- GitHub Push Protection  
- git-filter-repo cleanup in case of breach  

---

# 7. Git Ignore Policy

Required `.gitignore`:

```
# Environment variables
.env
*.env

# Python cache
__pycache__/
*.pyc
*.pyo

# Uploaded documents
uploads/
profiles/

# Database files
*.db
*.sqlite

# IDE settings
.vscode/
.idea/

# OS files
.DS_Store
Thumbs.db
```

---

# 8. Branch Protection Rules (Recommended)

### Protect `main` and `dev`:
- ✔ Require pull request  
- ✔ Require 1–2 approvals  
- ✔ Require CI checks to pass  
- ✔ Block force pushes  
- ✔ Block secret scanning violations  

---

# 9. Release Workflow

1. Merge approved features into `dev`  
2. When stable → create `release/x.x.x`  
3. Final testing + docs  
4. Merge release → `main`  
5. Create Git tag  
6. Deploy  

---

# 10. Backup & Rollback Strategy

### Backup:
- GitHub automatically stores full repo history  
- Weekly local backup (recommended)

### Rollback:
Use Git tags or commits:

```
git checkout v1.0.0
git revert <commit>
git reset --hard <commit>
```

No rollbacks allowed on `main` without approval.

---

# 11. Contribution Standards

### Contributors MUST:
✔ Create feature branches  
✔ Follow commit style  
✔ Write documentation for changes  
✔ Pass tests before merging  
✔ Never merge directly to `main`  

---

# 12. Code Review Checklist

Before merging:

- [ ] No secrets  
- [ ] Correct branch target  
- [ ] Linting passes  
- [ ] Unit tests added if needed  
- [ ] No commented-out code  
- [ ] Documentation updated  
- [ ] PR description complete  

---

# 13. Project Versioning (Tracking Changes)

Every major version increases when:
- New pipeline added  
- New AI feature added  
- Dashboard released  

Minor version when:
- UI changes  
- Enhancements  

Patch version when:
- Bugs fixed  

---

# 14. GitHub Automation (Optional Enhancements)

Suggested future improvements:
- GitHub Actions for auto-testing  
- Action to auto-build PDFs/PPT  
- Secrets scanning alerts  
- Automatic linting PR checks  

---

# 15. Ownership

| Responsibility      | Person |
|--------------------|--------|
| Repo Owner         | Nontobeko Dube |
| Technical Lead     | — |
| Reviewer           | — |
| Security Monitor   | GitHub Security Bot |

---

# END OF VERSION CONTROL FILE
