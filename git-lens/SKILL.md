---
name: git-lens
description: Advanced git repository analysis, including line-by-line authorship (blame), file history, and cross-commit content searching. Use when the user asks about who wrote specific code, when a file was changed, or for repository-wide history insights.
---

# Git Lens

## Overview
The `git-lens` skill provides specialized workflows and tools for deep repository analysis. It enables Gemini CLI to act as a "Lens" into the git history, identifying authors of specific lines and tracking the evolution of files over time.

## Core Capabilities

### 1. Authorship Analysis (Blame)
Identify who changed specific lines to understand context or find the right person for questions.
- **Tool**: `git blame -L <start>,<end> <file_path>`
- **Workflow**: If a bug is found in a specific block of code, use blame to find the original PR or author for context.

### 2. File Evolution Tracking
See the full history of a file, even through renames.
- **Script**: `python scripts/get_file_history.py <file_path>`
- **Pattern**: `git log --follow --patch <file_path>`

### 3. Historical Content Search
Search for deleted code or the introduction of specific strings across all branches and history.
- **Pattern**: `git log -S "<string>"`

## Workflow: Investigating a Code Block
1. **Locate**: Identify the file and line range of interest.
2. **Blame**: Run `git blame` to find the commit hash and author.
3. **Inspect**: Use `git show <hash>` to see the full context of that change.
4. **Contextualize**: Read the commit message to understand the *why* behind the change.

## Reference Material
For more advanced commands and patterns, see [git_patterns.md](references/git_patterns.md).
