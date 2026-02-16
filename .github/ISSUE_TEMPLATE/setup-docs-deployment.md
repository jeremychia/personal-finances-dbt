---
name: 🚀 Setup dbt Docs Deployment
about: Checklist for setting up automated dbt documentation deployment to GitHub Pages
title: 'Setup: Enable dbt Docs Deployment to GitHub Pages'
labels: ['documentation', 'setup', 'github-pages']
assignees: ''
---

## 📋 Setup Checklist

### 1. Enable GitHub Pages
- [ ] Go to **Settings** → **Pages**
- [ ] Under **Source**, select **"GitHub Actions"**
- [ ] Save the settings

### 2. Configure BigQuery Service Account Secret
- [ ] Ensure you have a valid service account key file (`keys/keyfile.json`)
- [ ] Encode the service account key:
  ```bash
  cat keys/keyfile.json | base64 > keyfile_base64.txt
  ```
- [ ] Go to **Settings** → **Secrets and variables** → **Actions**
- [ ] Click **"New repository secret"**
- [ ] Name: `DBT_SERVICE_ACCOUNT_KEY`
- [ ] Value: Paste the base64 encoded content from `keyfile_base64.txt`
- [ ] Click **"Add secret"**
- [ ] Delete the temporary `keyfile_base64.txt` file

### 3. Verify Permissions
Ensure the repository has these permissions configured:
- [ ] **Contents**: Read ✓
- [ ] **Pages**: Write ✓
- [ ] **id-token**: Write ✓

*(These should be automatically configured by the workflow file)*

### 4. Test the Workflow
- [ ] Push changes to the `main` branch
- [ ] Go to **Actions** tab and verify the "Deploy dbt Docs to GitHub Pages" workflow runs successfully
- [ ] Check that the documentation is available at: `https://jeremychia.github.io/personal-finances-dbt/`

### 5. Verify Documentation Content
Once deployed, verify the documentation includes:
- [ ] Model lineage graphs
- [ ] Model descriptions and column documentation
- [ ] Source documentation
- [ ] Test documentation

---

## 🔍 Troubleshooting

### Common Issues:

**Issue**: Authentication failure with BigQuery
- Verify the service account key is correctly base64 encoded
- Check that the service account has necessary BigQuery permissions
- Ensure the `DBT_SERVICE_ACCOUNT_KEY` secret is properly set

**Issue**: GitHub Pages deployment fails
- Verify GitHub Pages is enabled with "GitHub Actions" source
- Check repository permissions for Pages deployment

**Issue**: dbt docs generation fails
- Check that `dbt_project.yml` configuration is valid
- Verify all required dbt packages are listed in `packages.yml`
- Ensure the target database/dataset exists and is accessible

---

## 📚 Additional Resources
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [dbt Documentation](https://docs.getdbt.com/docs/building-a-dbt-project/documentation)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
