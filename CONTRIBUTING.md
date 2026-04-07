# Contributing to ResearchClawBench

Thank you for your interest in contributing! ResearchClawBench welcomes contributions in three main areas:

1. **New Research Tasks** — Expand our benchmark with tasks from new domains or papers
2. **New Agents** — Add support for additional AI coding agents
3. **Bug Fixes & Features** — Improve the evaluation framework itself

---

## 1. Contributing New Research Tasks

Each task is a curated research challenge derived from a real published paper. To contribute a task, create a directory under `tasks/` following the naming convention `{Domain}_{NNN}` (e.g., `Biology_000`).

### Directory Structure

```
tasks/YourDomain_000/
├── task_info.json         # Task description + data file manifest
├── data/                  # Input datasets (read-only for agents)
│   ├── dataset1.csv
│   └── dataset2.json
├── related_work/          # Reference papers (PDF)
│   ├── paper_000.pdf
│   ├── paper_001.pdf
│   └── ...
└── target_study/          # Ground truth for evaluation
    ├── paper.pdf          # The original published paper
    ├── checklist.json     # Expert-annotated evaluation checklist
    └── images/            # Target figures referenced in checklist
        ├── figure1.png
        └── ...
```

### task_info.json Format

```json
{
  "task": "A detailed description of the research task the agent should complete...",
  "data": [
    {
      "name": "Dataset Name",
      "path": "./data/dataset1.csv",
      "type": "CSV",
      "description": "What this dataset contains and how it should be used."
    }
  ]
}
```

**Requirements:**
- `task`: Clear research task description grounded in the provided workspace. The agent receives this task text together with the workspace contents.
- `data[].path`: Must start with `./data/` (workspace-relative path).
- `data[].type`: File format (e.g., CSV, JSON, TXT, PDF, HDF5).

### checklist.json Format

The evaluation checklist defines what the judge scores. Each item represents a key finding or analysis from the original paper:

```json
[
  {
    "type": "text",
    "content": "Description of the expected finding or analysis...",
    "path": null,
    "keywords": [
      "Technical keyword 1 the judge should verify",
      "Technical keyword 2..."
    ],
    "weight": 0.3
  },
  {
    "type": "image",
    "content": "Description of the expected figure...",
    "path": "images/figure1.png",
    "keywords": [
      "Visual element 1 to verify",
      "Visual element 2..."
    ],
    "weight": 0.2
  }
]
```

**Item types:**
- `text`: Methodology, findings, or analysis that should appear in the report
- `image`: A figure the agent should generate, compared against the target image

**Guidelines:**
- Weights should sum to 1.0 across all items
- Keywords should be specific and technical, not generic
- Each item should correspond to a distinct, verifiable contribution of the paper
- Include a mix of text and image items where appropriate

### related_work/ Naming

PDFs should be named `paper_000.pdf`, `paper_001.pdf`, etc. These are reference papers the agent can read for context. No duplicate files (identical content) are allowed.

### Validation Checklist

Before submitting:

- [ ] `task_info.json` is valid JSON with all `data[].path` starting with `./data/`
- [ ] All referenced data files exist in `data/`
- [ ] `related_work/` contains at least one reference paper
- [ ] `target_study/checklist.json` is valid JSON with weights summing to ~1.0
- [ ] `target_study/paper.pdf` is the original published paper
- [ ] Image items in checklist have corresponding files in `target_study/images/`
- [ ] A human researcher can reproduce the paper's key results from the provided workspace and instructions

---

## 2. Contributing a New Agent

Agent configuration is stored in `evaluation/agents.json`. Adding a new agent requires:

### Step 1: Add the Agent Preset

Edit `evaluation/agents.json` to add your agent:

```json
{
  "my_agent": {
    "label": "My Agent",
    "icon": "A",
    "logo": "/static/logos/my_agent.svg",
    "cmd": "my-agent run -m <PROMPT> -w <WORKSPACE>"
  }
}
```

**Fields:**
- `label`: Display name in the UI
- `icon`: Single character fallback icon (used when logo is unavailable)
- `logo`: Path to an SVG logo file (place in `evaluation/static/logos/`)
- `cmd`: Shell command to run the agent, with placeholders:
  - `<PROMPT>` — Replaced with the prompt content. For `-p` style flags (file path), replaced with `"path"`. For other flags, replaced with `"$(cat 'path')"` to pass file content.
  - `<WORKSPACE>` — Replaced with the absolute workspace directory path (optional).

### Step 2: Add a Logo (Optional)

Place an SVG logo file at `evaluation/static/logos/my_agent.svg`. Recommended size: 16-20px square, monochrome or simple colors.

### Step 3: Test

```bash
python -m evaluation
# Select your agent in the UI → Start Run → verify output streams correctly
```

### Agent Requirements

Your agent must:
- Accept a prompt/instruction (via file path or stdin)
- Work within a given directory (cwd is set to the workspace)
- Write output to stdout (captured as `_agent_output.jsonl`)
- Be fully autonomous — no interactive prompts or confirmation dialogs
- Generate `report/report.md` and `report/images/` as deliverables

### Existing Agent References

| Agent | Repository | Notes |
|:------|:-----------|:------|
| Claude Code | [Anthropic](https://docs.anthropic.com/en/docs/claude-code) | Stream-JSON output |
| Codex CLI | [OpenAI](https://github.com/openai/codex) | Full-auto mode |
| OpenClaw | [OpenClaw](https://github.com/openclaw/openclaw) | Self-hosted, 3600s timeout |
| Nanobot | [HKUDS/nanobot](https://github.com/HKUDS/nanobot) | Lightweight, reliable tool execution |

---

## 3. Bug Fixes & New Features

### Getting Started

```bash
git clone https://github.com/InternScience/ResearchClawBench.git
cd ResearchClawBench
pip install -r evaluation/requirements.txt
cp evaluation/.env.example evaluation/.env
# Edit .env with your API credentials
python -m evaluation
```

### Project Structure

```
evaluation/
├── server.py              # Flask API + SSE streaming
├── run_task.py            # Workspace setup + agent subprocess
├── score.py               # LLM scoring engine (dual-mode rubric)
├── config.py              # Configuration loader
├── agents.json            # Agent presets
├── instructions_tmpl.py   # Prompt template
├── utils.py               # Utilities (file tree, path safety)
├── static/app.js          # Frontend (single file)
├── static/style.css       # Styles (4 themes)
└── templates/index.html   # HTML shell
```

### Submitting a Pull Request

1. **Fork** the repository and create a feature branch
2. **Make changes** — keep PRs focused on a single concern
3. **Test locally** — verify the UI works, agents can run, scoring produces valid results
4. **Submit PR** with a clear description of what changed and why

### Code Style

- **Python**: Follow existing patterns. No additional linters required.
- **JavaScript**: Single-file `app.js`, vanilla JS (no frameworks). Use `esc()` for user content to prevent XSS.
- **CSS**: Use CSS variables (`var(--text)`, `var(--accent)`, etc.) for theme compatibility. Test in all 4 themes.

### Key Architecture Notes

- **STATIC_MODE**: `app.js` serves both the local Flask UI and GitHub Pages static site. Code guarded by `if (STATIC_MODE)` only runs on GitHub Pages.
- **Stale guards**: All async functions that write to the DOM must check if the current task/run has changed before rendering (see `_selectEpoch` and `isStale()` patterns).
- **File tree limits**: `build_file_tree()` supports `max_per_dir` and `max_depth` to prevent browser freezes from large workspaces.

---

## Code of Conduct

Be respectful, constructive, and collaborative. We're all working toward the same goal: advancing AI's ability to do real science.

---

## Questions?

- Open a [GitHub Issue](https://github.com/InternScience/ResearchClawBench/issues)
- Email: [xu_wanghan@sjtu.edu.cn](https://black-yt.github.io/)
