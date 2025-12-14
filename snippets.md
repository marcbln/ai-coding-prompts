
---
description: "CODE SNIPPETS TEMPLATES"
createdAt: 2025-12-14
createdBy: Cascade
tags: [snippets, templates, code, plans]
documentType: PROMPT_TEMPLATE
---

## --------------- CREATE PLAN V3 -----------------

<instruction>
Please create a **detailed** multi phased implementation plan in markdown format. 

## Plan Structure
- Include YAML frontmatter with the following fields:
```yaml
---
filename: "ai-plans/{YYMMDD}__PLAN__{name-of-the-plan}.md"
title: "Descriptive title of the plan"
date: YYYY-MM-DD
status: draft|in-progress|completed
priority: low|medium|high|critical
tags: [tag1, tag2, tag3]
estimated_complexity: simple|moderate|complex
---
```
- The first section of the plan briefly describes the problem to be solved.
- The plan will be implemented by an AI coding agent. 
- Include source code in the plan, mark each code block as [NEW FILE], [MODIFY], or [DELETE] to show the type of change
- The plan should also include an update of the user documentation, if needed.
- Please follow SOLID principles

## Report Structure
The last phase of the plan should be to write a report to `ai-plans/{YYMMDD}__IMPLEMENTATION-REPORT__{name-of-the-plan}.md`

Include YAML frontmatter with the following fields:
```yaml
---
filename: "ai-plans/{YYMMDD}__IMPLEMENTATION-REPORT__{name-of-the-plan}.md"
title: "Report: {plan title}"
date: YYYY-MM-DD
plan_file: "ai-plans/{YYMMDD}__PLAN__{name-of-the-plan}.md"
status: completed|partial|blocked
files_created: 0
files_modified: 0
files_deleted: 0
tags: [tag1, tag2, tag3]
documentType: IMPLEMENTATION_REPORT
---
```

The report content should include:
1. **Summary**: Brief overview of what was accomplished (2-3 sentences)
2. **Files Changed**: 
   - List of new files created with brief descriptions
   - List of modified files with summary of changes
   - List of deleted files (if any)
3. **Key Changes**: Bullet points of the main technical changes made
4. **Technical Decisions**: Important design decisions or trade-offs made during implementation
5. **Testing Notes**: How the changes can be verified or tested
6. **Documentation Updates**: Summary of any documentation changes made
7. **Next Steps** (optional): Any follow-up work or improvements that could be made
</instruction>








## --------------- CREATE PLAN V2 -----------------




<instruction>
Please create a **detailed** multi phased implementation plan in markdown format. 

## Plan Structure
- The First line of the plan should be the filename of the plan in format `ai-plans/{YYMMDD}__PLAN__{name-of-the-plan}.md`
- Include YAML frontmatter with the following fields:
```yaml
  ---
  title: "Descriptive title of the plan"
  date: YYYY-MM-DD
  status: draft|in-progress|completed
  priority: low|medium|high|critical
  tags: [tag1, tag2, tag3]
  estimated_complexity: simple|moderate|complex
  ---
```
- The first section of the plan briefly describes the problem to be solved.
- The plan will be implemented by an AI coding agent. 
- Include source code in the plan, mark each code block as [NEW FILE], [MODIFY], or [DELETE] to show the type of change
- The plan should also include an update of the user documentation, if needed.
- Please follow SOLID principles

## Report Structure
The last phase of the plan should be to write a report to `ai-plans/{YYMMDD}__IMPLEMENTATION-REPORT__{name-of-the-plan}.md`

Include YAML frontmatter with the following fields:
```yaml
---
title: "Report: {plan title}"
date: YYYY-MM-DD
plan_file: "ai-plans/{YYMMDD}__PLAN__{name-of-the-plan}.md"
status: completed|partial|blocked
files_created: 0
files_modified: 0
files_deleted: 0
tags: [tag1, tag2, tag3]
---
```

The report content should include:
1. **Summary**: Brief overview of what was accomplished (2-3 sentences)
2. **Files Changed**: 
   - List of new files created with brief descriptions
   - List of modified files with summary of changes
   - List of deleted files (if any)
3. **Key Changes**: Bullet points of the main technical changes made
4. **Technical Decisions**: Important design decisions or trade-offs made during implementation
5. **Testing Notes**: How the changes can be verified or tested
6. **Documentation Updates**: Summary of any documentation changes made
7. **Next Steps** (optional): Any follow-up work or improvements that could be made
</instruction>



## --------------- CREATE PLAN V1 -----------------
<instruction>
Please create a **detailed** multi phased implementation plan in markdown format. 
- The First line of the plan should be the filename of the plan in format `ai-plans/{YYMMDD}__PLAN__{name-of-the-plan}.md`
- The first section of the plan briefly describes the problem to be solved.
- The plan will be implemented by an AI coding agent. 
- Include source code in the plan, mark each code block as [NEW FILE], [MODIFY], or [DELETE] to show the type of change
- The plan should also include an update of the user documentation, if needed.
- The last phase of the plan should be to write a report of the changes that were made to a file in the `ai-plans/{YYMMDD}__IMPLEMENTATION-REPORT__{name-of-the-plan}.md` directory.
- Please follow SOLID principles
</instruction>








## --------------- CREATE PLAN TRASH-01 -----------------

<instruction>
Please create a detailed multi phased implementation plan in markdown format. 
The plan will be implemented by an AI coding agent. 
Before writing the plan please check @ai-docs if anything is unclear.  or ask me. Do not make bold assumptions! 
</instruction>


<instruction>
Create a detailed multi-phased implementation plan in markdown format for execution by an AI coding agent. Before drafting the plan:
1. Thoroughly review all relevant @ai-docs sections (including CONVENTIONS-PHP.md, CONVENTIONS-VUE.md, PROJECT_SUMMARY.md, and HOWTO/) to ensure alignment with current standards
2. Explicitly identify any outdated/incomplete documentation sections requiring updates
3. Flag all uncertainties or missing information that need user clarification before proceeding
4. Verify technical constraints and dependencies through existing documentation
5. Never assume unspecified requirements - explicitly request user input for ambiguous elements

The plan must include:
- Phase-wise breakdown with clear objectives and success criteria
- Documentation validation tasks referencing specific @ai-docs sections
- User clarification checkpoints for unresolved questions
- Risk assessment of outdated documentation impacts
- Version-controlled deliverable artifacts
- Fallback procedures for missing documentation scenarios
- Compatibility checks with existing project structure from PROJECT_SUMMARY.md
- Audit trail of all documentation references and assumptions

Format each phase with:
### Phase [X]: [Title]
**Objective**:  
**Documentation Dependencies**:  
**Pre-Implementation Checks**:  
**Tasks**:
- [ ] Actionable step with @ai-docs reference
- [ ] Uncertainty flagging mechanism  
  **Deliverables**:  
  **User Clarification Points**:
  </instruction>



<instruction>
Please create a detailed multi phased implementation plan in markdown format. 
The plan should also include an update of the user documentation.
The plan will be implemented by an AI coding agent. 
</instruction>



Note:
- all commands need to be executed inside the docker container named `cm-www`
- the app root is in `./vol/www/` outside the container and `/www/` inside the container




<instruction>
Please create a detailed multi phased implementation plan in markdown format in @ai-docs/plans. The last phase pf the plan should be to write a report of the changes that were made in @ai-docs/plans.
The plan will be implemented by an AI coding agent.
</instruction>
<hints>
Please Note:
- create database migration with:
```bash
docker exec cm-www     php /www/bin/console app:mt:tenant-database:migrations:diff  2
```

- execute database migration with:
```bash
docker exec cm-www     /www/scripts/migrate-all-tenant-dbs.sh  -x 1
```

</hints>

