# Modus Migration Agentic Workflow Tool

## Purpose
Guide the user or agent through the migration process step by step, ensuring confirmation at each stage.

## Rules
- Always start with analysis.
- After each step, present the result and prompt the user to confirm before proceeding.
- Only proceed to migration, verification, or logging if the user explicitly confirms.
- Summarize the workflow in Markdown at each step.

## Output Format
- Use Markdown headings for each step.
- Present prompts and results as bullet points or tables.
- Clearly indicate the current step and next available actions.

## Example
```
# Migration Workflow

## Step 1: Analysis
- Found 2 v1 tags: modus-button, modus-foo
- Reply 'proceed' to continue to migration.

## Step 2: Migration
- Replaced modus-button with modus-wc-button
- Could not migrate modus-foo (no v2 equivalent)
- Reply 'verify' to verify the migration.

## Step 3: Verification
- [x] All v1 tags replaced
- [ ] Accessibility: aria-label missing
- Reply 'log' to log the migration summary.

## Step 4: Logging
- Migration summary logged.
- Workflow complete. 