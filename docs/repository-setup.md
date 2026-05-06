# Repository Setup

Recommended GitHub repository name:

```text
bridgeworld-mailerlite-newsletter
```

Recommended description:

```text
Bridgeworld newsletter planning, MailerLite setup notes, campaign assets, and publishing workflow documentation.
```

## Create The Repository

When Git and GitHub CLI are available locally, run these commands from this folder:

```powershell
git init
git add README.md .gitignore docs/repository-setup.md
git commit -m "Initial repository setup"
gh repo create bridgeworld-mailerlite-newsletter --private --source . --remote origin --push --description "Bridgeworld newsletter planning, MailerLite setup notes, campaign assets, and publishing workflow documentation."
```

Use `--public` instead of `--private` only if the project will not contain private campaign planning, subscriber-related exports, or business-sensitive material.

## Data Safety

Do not commit MailerLite API keys, contact lists, subscriber exports, private analytics exports, or credentials. Keep those in MailerLite, a password manager, or another approved secure store.
