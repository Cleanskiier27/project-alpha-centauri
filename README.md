# 🌌 Project Alpha Centauri: Interstellar Maturation Registry

A comprehensive, 30-phase SBIR- and TRL-aligned maturation pipeline for deep-space technology development and interstellar infrastructure staging.

---

## 🛰️ Live Preview & Portals

*   **Interactive Dashboard:** [https://cleanskiier27.github.io/project-alpha-centauri/](https://cleanskiier27.github.io/project-alpha-centauri/)
*   **Stitched Master Document:** [https://cleanskiier27.github.io/project-alpha-centauri/master_doc.html](https://cleanskiier27.github.io/project-alpha-centauri/master_doc.html)
*   **Robotic Swarm Bid Proposal:** [https://cleanskiier27.github.io/project-alpha-centauri/nasa_robotic_bid.html](https://cleanskiier27.github.io/project-alpha-centauri/nasa_robotic_bid.html)

---

## 🏗️ Mission Architecture

Project Alpha Centauri is segmented into **six distinct vector phases**, each delivering 5 distinct CIS technology maturation artifacts:

```
🔭 Origin Vector (TRL 1–2)  ->  🌱 Seed Vector (TRL 2–4)   ->  🔥 Ignition Vector (TRL 3–4)
                                                                       |
🌕 Translunar Vector (TRL 7–9) <- 🛸 Orbit Vector (TRL 6–7) <- 🚀 Ascent Vector (TRL 4–6)
```

1.  **Origin Vector (A1–A5)**: Establishes foundations, matrices, scanned principles, and early drafts.
2.  **Seed Vector (B1–B5)**: Focuses on architectural blueprints, physical lattices, and prototype reports.
3.  **Ignition Vector (C1–C5)**: Drives experimental validation logs, interface definitions, and TRL audits.
4.  **Ascent Vector (D1–D5)**: Systems engineering plans, environmental qualification, and simulation trials.
5.  **Orbit Vector (E1–E5)**: Beta prototype validation, infrastructure mapping, and lunar ops readiness reviews.
6.  **Translunar Vector (F1–F5)**: Gamma prototype validation, final flight certifications, and scale engines.

---

## 🛠️ Repository Assets

*   `/docs/centauri/`: Core Markdown catalog for the 30 maturation artifacts.
*   `/docs/NASA-ROBOTIC-BID-SUBMISSION.md`: Formally submitted SBIR Galactic Proposal for the Alpha Centauri robotic construction swarm ($5B contract value).
*   `/viz/`: Interactive simulations including the Galactic Navigation System and the Proxima B Exohub console.
*   `build_site.py`: Fast Python site compiler that parses Markdown files and compiles a responsive space-themed catalog.

---

## ⚙️ CI/CD Workflows

The registry is verified by automated pipelines:
*   **CI - Device Registration Tests**: Runs Mocha/Chai integration test suites for status queuing.
*   **Deploy Centauri Docs**: Automates site compiling and publishes it to GitHub Pages.
*   **Sync Branches**: Synchronizes the main branch with the active `bigtree` branch.
*   **Dependabot Integration**: Automatically tracks and updates Node.js dependencies and GitHub Actions packages.
