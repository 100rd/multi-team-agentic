# Hooks Guide - Workflow Automation

## What Are Hooks?

Think of hooks as **automatic helpers** that do things for you at specific moments. You don't need to understand the technical details - just tell us what you want automated!

## Examples for Different Projects

### For Software Projects
- **"I always forget to run tests"** → Hook runs tests automatically after you save code
- **"I want code reviewed before pushing"** → Hook blocks pushes until review is done
- **"Remind me of daily standups"** → Hook sends reminders at 9 AM

### For Writing Projects
- **"Check grammar when I finish writing"** → Hook runs grammar check after each section
- **"Track my daily word count"** → Hook logs progress automatically
- **"Format citations properly"** → Hook ensures consistent citation style

### For Documentation Projects
- **"Keep table of contents updated"** → Hook regenerates TOC after changes
- **"Check for broken links"** → Hook validates all links
- **"Ensure consistent terminology"** → Hook flags inconsistent terms

### For Design Projects
- **"Export assets in multiple formats"** → Hook auto-generates different sizes
- **"Backup my work hourly"** → Hook creates versioned backups
- **"Compress images for web"** → Hook optimizes images automatically

## How We'll Set Up Hooks for You

During project setup, we'll ask questions like:

1. **"What repetitive tasks do you do?"**
   - Running tests
   - Formatting code
   - Updating documentation
   - Sending notifications

2. **"What do you often forget to do?"**
   - Add comments
   - Update changelog
   - Run security scans
   - Backup work

3. **"What checkpoints do you need?"**
   - Review before publishing
   - Approval before deploying
   - Validation before submitting

4. **"When should things happen?"**
   - After saving files
   - Before commits
   - Daily/weekly
   - When certain words appear

## Hook Templates by Project Type

### 📱 Software Development
```toml
# Auto-format code
[[hooks]]
event = "PostToolUse"
[hooks.matcher]
tool_name = "Write"
command = "echo 'Auto-formatting code...' && format-tool $CLAUDE_FILE_PATH"

# Run tests before commit
[[hooks]]
event = "PreToolUse"
[hooks.matcher]
tool_name = "Bash"
args_regex = "git commit"
command = "echo 'Running tests...' && npm test"
```

### 📝 Content Writing
```toml
# Grammar check
[[hooks]]
event = "PostToolUse"
[hooks.matcher]
tool_name = "Write"
file_paths = ["*.md", "*.txt"]
command = "echo 'Checking grammar...' && grammarly-cli check $CLAUDE_FILE_PATH"

# Word count tracking
[[hooks]]
event = "Stop"
command = "wc -w content/*.md | tail -1 >> daily-word-count.log"
```

### 📚 Documentation
```toml
# Update table of contents
[[hooks]]
event = "PostToolUse"
[hooks.matcher]
tool_name = "Write"
file_paths = ["docs/**/*.md"]
command = "echo 'Updating TOC...' && doctoc README.md"

# Check links
[[hooks]]
event = "Notification"
[hooks.matcher]
time = "10:00"
command = "echo 'Checking links...' && markdown-link-check docs/**/*.md"
```

### 🎨 Creative Projects
```toml
# Daily progress snapshot
[[hooks]]
event = "Notification"
[hooks.matcher]
time = "17:00"
command = "echo 'Creating daily snapshot...' && git add -A && git commit -m 'Daily progress: $(date)'"

# Backup reminders
[[hooks]]
event = "Stop"
command = "echo '💾 Remember to backup your work to cloud storage!'"
```

## Flexibility Levels

### Minimal Automation
Just a few key hooks:
- Save work automatically
- Basic reminders
- Simple validations

### Moderate Automation
Helpful workflow enhancements:
- Quality checks
- Progress tracking
- Team notifications

### Full Automation
Complete workflow orchestration:
- Multi-step processes
- Complex validations
- Integration with external tools
- Automated reporting

## Creating Custom Hooks

Tell us what you need in plain English:

**You say:** "I want to make sure I never commit sensitive data"
**We create:** A hook that scans for passwords/keys before commits

**You say:** "Remind me to take breaks every hour"
**We create:** A hook that sends hourly break reminders

**You say:** "Keep my writing consistent with our style guide"
**We create:** A hook that checks against your style rules

## Non-Coding Project Examples

### 📊 Research Projects
- Citation formatting
- Data validation
- Progress reports
- Collaboration syncs

### 📖 Book Writing
- Chapter word counts
- Character consistency
- Plot timeline tracking
- Publishing preparation

### 🎬 Video Projects
- Render queue management
- Asset organization
- Version control
- Review reminders

### 📈 Business Planning
- Metric tracking
- Report generation
- Deadline reminders
- Stakeholder updates

## Best Practices

1. **Start Simple** - Add hooks as you discover needs
2. **Test First** - Try hooks in safe environment
3. **Document Why** - Record what each hook does
4. **Review Regularly** - Adjust hooks as workflow evolves
5. **Share Knowledge** - Tell team about useful hooks

## Common Patterns

### Time-Based
- Daily standups
- Weekly reports
- Monthly reviews
- Deadline reminders

### Action-Based
- After writing code
- Before committing
- When creating files
- On specific commands

### Content-Based
- When mentioning "deploy"
- If file contains "TODO"
- When PR is created
- If tests fail

## Security Note

Hooks run commands on your computer, so:
- Only use hooks you understand
- Test in safe environment first
- Review hook commands regularly
- Don't share sensitive hooks publicly

## Getting Started

When setting up your project, we'll ask:
1. What type of work you're doing
2. What you want automated
3. What you often forget
4. When things should happen

Based on your answers, we'll create appropriate hooks that make your workflow smoother!

Remember: **You don't need to know how hooks work** - just tell us what would make your life easier!