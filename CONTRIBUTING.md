# **Contributing to SSH Config Auditor**

Thank you for taking the time to contribute! This document outlines the process and guidelines to ensure smooth collaboration while maintaining code quality, consistency, and stability in the SSH Config Auditor project.

---

## **Table of Contents**
1. [Code of Conduct](#code-of-conduct)  
2. [Ways to Contribute](#ways-to-contribute)  
3. [Getting Started](#getting-started)  
4. [Branching & Workflow](#branching--workflow)  
5. [Coding Standards & Style](#coding-standards--style)  
6. [Testing](#testing)  
7. [Commit Messages](#commit-messages)  
8. [Pull Request Guidelines](#pull-request-guidelines)  
9. [Issue Guidelines](#issue-guidelines)  
10. [Security Vulnerabilities](#security-vulnerabilities)  
11. [Contact](#contact)

---

## **1. Code of Conduct**

Please follow our [Code of Conduct](#) (if you have one in a separate file) to ensure a respectful and harassment-free environment for all project contributors and users.

---

## **2. Ways to Contribute**

1. **Reporting Bugs**: Create an [issue](#issue-guidelines) if you encounter a problem.  
2. **Submitting Enhancements**: Propose features or improvements that would benefit users.  
3. **Fixing Bugs or Adding Features**: Contribute code via [Pull Requests](#pull-request-guidelines).  
4. **Improving Documentation**: Provide clear, concise docs to help users get started and understand the project.  
5. **Writing Tests**: Strengthen code reliability by adding or expanding tests.

---

## **3. Getting Started**

1. **Fork the Repository**: Click the “Fork” button on GitHub and clone your fork locally:
   ```bash
   git clone git@github.com:<YOUR_USERNAME>/ssh-config-auditor.git
   cd ssh-config-auditor
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Run Tests** to verify everything is working:
   ```bash
   pytest --maxfail=1 --disable-warnings
   ```

---

## **4. Branching & Workflow**

We use a **branching strategy** to keep code organized:
1. **main**: Production-ready branch; only merge tested, stable code here.  
2. **develop**: Active development branch; pull requests for new features and bug fixes should go here first.  

**Recommended Workflow**:
1. **Create a feature branch** from `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```
2. **Implement** your changes.  
3. **Commit** and **Push** to your feature branch:
   ```bash
   git push -u origin feature/your-feature-name
   ```
4. **Create a Pull Request** into `develop`.

---

## **5. Coding Standards & Style**

Our code should follow **SOLID** principles, **DRY** (Don’t Repeat Yourself), and **KISS** (Keep It Simple, Stupid). We recommend:

- **PEP 8** for Python style (indentation, naming, etc.).  
- **Type hints** for function parameters and return types where feasible.  
- Use **docstrings** with concise explanations in your modules and functions.
- Keep **imports** organized (standard library, then third-party, then local modules).

You can use tools like **black**, **flake8**, or **isort** to automatically check and format your code.

---

## **6. Testing**

1. **Unit Tests**: Place them in the `tests/` directory.  
2. **Integration Tests**: If you need to test an entire SSH pipeline, consider using Docker/Podman-based test environments.  
3. **Run Tests** before pushing:
   ```bash
   pytest --maxfail=1 --disable-warnings
   ```
4. **Coverage**: We encourage using `pytest-cov` to ensure comprehensive tests:
   ```bash
   pip install pytest-cov
   pytest --cov=auditor tests/
   ```

---

## **7. Commit Messages**

Use a **clear, consistent** format for commit messages (e.g., [Conventional Commits](https://www.conventionalcommits.org/)):

```
feat: add support for PDF report generation
fix: resolve crash on missing sshd_config
docs: update README with new usage examples
refactor: rename parser module to config_parser
test: add unit test for SSHConfigAuditor
```

Good commit messages help maintainers understand your changes at a glance.

---

## **8. Pull Request Guidelines**

1. **Create a Pull Request** against the `develop` branch.  
2. **Describe** the changes in detail, referencing any related issues.  
3. **Ensure** tests pass and the code follows style guidelines.  
4. **Request Reviews**: Tag relevant maintainers or project owners.  
5. **Update Documentation**: If you add a feature, update the README or related docs.

If a reviewer requests changes, address them in new commits pushed to the same branch. Once approved, a maintainer will merge the PR.

---

## **9. Issue Guidelines**

When creating an issue:
1. **Search** to see if the issue already exists.  
2. **Clearly describe** the problem or feature request.  
3. **Include** steps to reproduce (if a bug) and environment details.  
4. **Attach logs or error messages** if relevant.  
5. **Use labels** (bug, enhancement, question, etc.) if available.

---

## **10. Security Vulnerabilities**

If you discover a security issue in SSH Config Auditor:
1. **Do not create a public issue**.  
2. **Contact** the maintainers privately (e.g., via email).  
3. Provide steps to replicate the vulnerability and any relevant details.

We will coordinate a fix and release a security advisory as soon as possible.

---

## **11. Contact**

For questions, suggestions, or anything else:
- **Issues**: [GitHub Issues](https://github.com/dkrizhanovskyi/ssh-config-auditor/issues)  
- **Email**: [dk.arecibo@pm.me](mailto:dk.arecibo@pm.me)
- **Pull Requests**: [GitHub Pull Requests](https://github.com/dkrizhanovskyi/ssh-config-auditor/pulls)

---

Thank you for contributing and making SSH Config Auditor a better, more secure tool for everyone!  
