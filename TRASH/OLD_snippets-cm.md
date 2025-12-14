"---
description: "OLD SNIPPETS CM"
createdAt: 2025-12-14
createdBy: Cascade
tags: [snippets, old, trash, cm]
documentType: PROMPT_TEMPLATE
---
"Please follow SOLID principles""



## --------------- CREATE PLAN V3 -----------------

<instruction>
Create a **detailed** multi phased implementation plan in markdown format. 

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
- The second section contains generic implementation notes:
```
  - Frontend root is vol/www/assets
  - Backend root is vol/www/src
  - the app runs in container `cm-www`, you need to consider this when running commands (use `docker exec -it cm-www /www/bin/console`)
  - migrations for the main database are created with `bin/console make:migration` (inside the container)
  - migrations for the tenant database are created with `bin/console app:sys:mt:migrations:diff 2` (inside the container)
```
- The plan will be implemented by an AI coding agent. Include source code in the plan.
- Include source code in the plan, mark each code block as [NEW FILE], [MODIFY], or [DELETE] to show the type of change
- Follow SOLID principles

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
<Instruction>
Create A **Detailed** Multi Phased Implementation Plan In Markdown Format. 

## Plan Structure
- The First Line Of The Plan Should Be The Filename Of The Plan In Format `Ai-Plans/{Yymmdd}__Plan__{Name-Of-The-Plan}.Md`
- Include Yaml Frontmatter With The Following Fields:
```Yaml
  ---
  Title: "Descriptive Title Of The Plan"
  Date: Yyyy-Mm-Dd
  Status: Draft|In-Progress|Completed
  Priority: Low|Medium|High|Critical
  Tags: [Tag1, Tag2, Tag3]
  Estimated_Complexity: Simple|Moderate|Complex
  ---
```
- The First Section Of The Plan Briefly Describes The Problem To Be Solved.
- The Second Section Contains Generic Implementation Notes:
```
  - Frontend Root Is Vol/Www/Assets
  - Backend Root Is Vol/Www/Src
  - The App Runs In Container `Cm-Www`, You Need To Consider This When Running Commands (Use `Docker Exec -It Cm-Www /Www/Bin/Console`)
  - Migrations For The Main Database Are Created With `Bin/Console Make:Migration` (Inside The Container)
  - Migrations For The Tenant Database Are Created With `Bin/Console App:Sys:Mt:Migrations:Diff 2` (Inside The Container)
```
- The Plan Will Be Implemented By An Ai Coding Agent. Include Source Code In The Plan.
- Include Source Code In The Plan, Mark Each Code Block As [New File], [Modify], Or [Delete] To Show The Type Of Change
- Follow Solid Principles

## Report Structure
The Last Phase Of The Plan Should Be To Write A Report To `Ai-Plans/{Yymmdd}__IMPLEMENTATION-REPORT__{Name-Of-The-Plan}.Md`

Include Yaml Frontmatter With The Following Fields:
```Yaml
---
Title: "Report: {Plan Title}"
Date: Yyyy-Mm-Dd
Plan_File: "Ai-Plans/{Yymmdd}__Plan__{Name-Of-The-Plan}.Md"
Status: Completed|Partial|Blocked
Files_Created: 0
Files_Modified: 0
Files_Deleted: 0
Tags: [Tag1, Tag2, Tag3]
---
```

The Report Content Should Include:
1. **Summary**: Brief Overview Of What Was Accomplished (2-3 Sentences)
2. **Files Changed**: 
   - List Of New Files Created With Brief Descriptions
   - List Of Modified Files With Summary Of Changes
   - List Of Deleted Files (If Any)
3. **Key Changes**: Bullet Points Of The Main Technical Changes Made
4. **Technical Decisions**: Important Design Decisions Or Trade-Offs Made During Implementation
5. **Testing Notes**: How The Changes Can Be Verified Or Tested
6. **Documentation Updates**: Summary Of Any Documentation Changes Made
7. **Next Steps** (Optional): Any Follow-Up Work Or Improvements That Could Be Made
</Instruction>





## --------------- CREATE PLAN V1 -----------------
<instruction>
- Create a **detailed** multi phased implementation plan in markdown format. 
- The first line of the plan should be the filename of the plan in format `ai-plans/{YYMMDD}__PLAN__{name-of-the-plan}.md`
- The first section of the plan briefly describes the problem to be solved.
- The second section contains generic implementation notes:
```
- Frontend root is vol/www/assets
- Backend root is vol/www/src
- the app runs in container `cm-www`, you need to consider this when running commands (use `docker exec -it cm-www /www/bin/console`)
- migrations for the main database are created with `bin/console make:migration` (inside the container)
- migrations for the tenant database are created with `bin/console app:sys:mt:migrations:diff 2` (inside the container)
```
- The last phase of the plan should be to write a report of the changes that were made to a file in the `ai-plans/{YYMMDD}__IMPLEMENTATION-REPORT__{name-of-the-plan}.md` directory.
- The plan will be implemented by an AI coding agent. Include source code in the plan.
- Include source code in the plan, mark each code block as [NEW FILE], [MODIFY], or [DELETE] to show the type of change
- follow SOLID principles
</instruction>














<instruction>
Please create a detailed multi phased implementation plan in markdown format. 
The plan will be implemented by an AI coding agent. 
Before writing the plan please check @ai-docs if anything is unclear.  or ask me. Do not make bold assumptions! 
</instruction>




<instruction>
Create a detailed multi-phased implementation plan in markdown format for execution by an AI coding agent. Before drafting the plan:
- Thoroughly review all relevant @ai-docs sections (including CONVENTIONS-PHP.md, CONVENTIONS-VUE.md, PROJECT_SUMMARY.md, and HOWTO/) to ensure alignment with current standards
- Explicitly identify any outdated/incomplete documentation sections requiring updates
- Flag all uncertainties or missing information that need user clarification before proceeding
- Verify technical constraints and dependencies through existing documentation
- Never assume unspecified requirements - explicitly request user input for ambiguous elements

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




