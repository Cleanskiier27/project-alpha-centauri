import re

with open("README.md", "r") as f:
    content = f.read()

replacement = """## ⚙️ CI/CD Workflows & GitHub Actions (Competition Accelerator)

To rapidly accelerate our competition submissions (such as the NASA SBIR Galactic Proposal), we leverage **GitHub Actions** as a primary tool and force multiplier. It provides robust automation to ensure high-velocity, error-free iterations:

*   **Continuous Deployment:** Automates site compiling and publishes it to GitHub Pages via `Deploy Centauri Docs`.
*   **Automated Testing:** `CI - Device Registration Tests` runs Mocha/Chai integration test suites.
*   **Branch Synchronization:** `Sync Branches` synchronizes the `main` branch with the active `bigtree` branch.
*   **Security & Dependency Management:** `Dependabot Integration` automatically tracks and updates Node.js dependencies and GitHub Actions packages."""

content = re.sub(r'## ⚙️ CI/CD Workflows.*', replacement, content, flags=re.DOTALL)

with open("README.md", "w") as f:
    f.write(content)
