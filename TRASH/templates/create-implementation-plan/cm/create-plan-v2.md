---
description: "CREATE PLAN V2"
createdAt: 2025-12-14
updatedAt: 2025-12-14
tags: [cm]
---
<Instruction>
Create A **Detailed** Multi Phased Implementation Plan In Markdown Format. 

## Plan Structure
- The First Line Of The Plan Should Be The Filename Of The Plan In Format `Ai-Plans/{Yymmdd}__IMPLEMENTATION_PLAN__{Name-Of-The-Plan}.Md`
- Include Yaml Frontmatter With The Following Fields:
```Yaml
  ---
  Title: "Descriptive Title Of The Plan"
  createdAt: YYYY-MM-DD HH:mm
  Status: Draft|In-Progress|Completed
  Priority: Low|Medium|High|Critical
  Tags: [Tag1, Tag2, Tag3]
  estimatedComplexity: Simple|Moderate|Complex
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
The Last Phase Of The Plan Should Be To Write A Report To `Ai-Plans/{Yymmdd}__IMPLEMENTATION_REPORT__{Name-Of-The-Plan}.Md`

Include Yaml Frontmatter With The Following Fields:
```Yaml
---
Title: "Report: {Plan Title}"
createdAt: YYYY-MM-DD HH:mm
Plan_File: "Ai-Plans/{Yymmdd}__IMPLEMENTATION_PLAN__{Name-Of-The-Plan}.Md"
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
