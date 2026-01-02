# Prompt Categories

This directory contains 51 prompts organized into 7 categories based on their primary use case.

---

## 🔄 Workflow (10 files)

**Workflow and process prompts** for managing complex tasks, thinking processes, and systematic approaches.

### Examples:
- `Clarifying-Questions.md` - Ask targeted questions to refine specifications
- `Context-Harvesting.md` - Thoroughly understand codebases before making changes
- `Think-Command-(Claude-Code).md` - Deep thinking approach for complex problems
- `Sequential-Thinking-Process-(MCP-→-Prompt).md` - Structured step-by-step reasoning

---

## 📣 Marketing (6 files)

**Marketing and copywriting prompts** for creating compelling content and promotional materials.

### Examples:
- `PAS-Framework-(Marketing).md` - Problem-Agitate-Solution copywriting framework
- `FAB-Framework-(Marketing).md` - Features-Advantages-Benefits framework
- `BAB-Framework-(Marketing).md` - Before-After-Bridge framework
- `Generate-ASO.md.md` - App Store Optimization generation

---

## 💻 Development (7 files)

**Development and coding prompts** for code reviews, testing, and technical workflows.

### Examples:
- `Code-Review.md` - Comprehensive code review process
- `🟢-Integration-Test-Green-Phase-Prompt.md` - TDD green phase for integration tests
- `🔴-Integration-Test-Red-Phase-Prompt.md.md` - TDD red phase for integration tests
- `Transform-Prompt-to-Code.md` - Convert natural language to code

---

## 🎨 Design (2 files)

**Design and architecture prompts** for user experience and system design.

### Examples:
- `Double-Diamond-Framework.md` - Design thinking framework for product discovery
- `UX-Delight-Framework.md` - Creating delightful user experiences

---

## 🚀 Product (5 files)

**Product and idea prompts** for product development, evaluation, and planning.

### Examples:
- `Generate-App-Name.md` - Generate app names based on descriptions
- `Idea-Evaluation-Matrix.md` - Evaluate product ideas systematically
- `Generate-Task.md` - Break down work into actionable tasks
- `High-Experimental-Roadmap.md-for-Parallel-Task-Execution.md` - Parallel task execution planning

---

## 🧠 Consulting (13 files)

**Expert and consulting prompts** for specialized knowledge and expert advice.

### Examples:
- `AI-Therapist.md` - CBT/ACT/psychodynamic therapy assistant
- `Technical-Clarity-Wizard.md` - Clarify technical concepts
- `System-Architecture-Design-Assistant.md` - Software architecture guidance
- `Prompt-Enhancer.md` - Improve and refine existing prompts
- `Parenting-Experts.md` - Parenting advice and strategies

---

## 📚 Documentation (8 files)

**Documentation and template prompts** for creating structured documents and templates.

### Examples:
- `Software-Design-Document-Template.md` - Complete SDD template
- `Apple-Review-Notes-Template.md` - App Store review notes structure
- `Bug-Reproduce-Template.md` - Systematic bug reporting template
- `Yes-Chef-Privacy-Policy.md` - Privacy policy example
- `Yes-Chef-Terms-and-Conditions.md` - Terms of service example

---

## Integration Notes

All prompts include YAML frontmatter compatible with:
- **Windsurf** - Place in `~/.codeium/windsurf/global_workflows/`
- **Cursor** - Add to custom modes via `cline_custom_modes.json`
- **OpenCode** - Add to custom modes directory

Each prompt defines:
- `slug`: Unique identifier
- `name`: Display name with emoji
- `category`: One of the 7 categories above
- `version`: Semantic version number
- `groups`: Permissions (read, edit, command)
- `source`: Always "global"
