---
description: "CREATE PLAN V1"
createdAt: 2025-12-14
updatedAt: 2025-12-14
tags: [cm]
---
<instruction>
- Create a **detailed** multi phased implementation plan in markdown format. 
- The first line of the plan should be the filename of the plan in format `ai-backlog/plans/{YYMMDD_HHmm}__IMPLEMENTATION_PLAN__{name-of-the-plan}.md`
- The first section of the plan briefly describes the problem to be solved.
- The second section contains generic implementation notes:
```
- Frontend root is vol/www/assets
- Backend root is vol/www/src
- the app runs in container `cm-www`, you need to consider this when running commands (use `docker exec -it cm-www /www/bin/console`)
- migrations for the main database are created with `bin/console make:migration` (inside the container)
- migrations for the tenant database are created with `bin/console app:sys:mt:migrations:diff 2` (inside the container)
```
- The last phase of the plan should be to write a report of the changes that were made to a file in the `ai-backlog/reports/{YYMMDD_HHmm}__IMPLEMENTATION_REPORT__{name-of-the-plan}.md` directory.
- The plan will be implemented by an AI coding agent. Include source code in the plan.
- Include source code in the plan, mark each code block as [NEW FILE], [MODIFY], or [DELETE] to show the type of change
- follow SOLID principles
</instruction>














<instruction>
Create a detailed multi phased implementation plan in markdown format. 
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
Create a detailed multi phased implementation plan in markdown format. 
The plan should also include an update of the user documentation.
The plan will be implemented by an AI coding agent. 
</instruction>



Note: 
- all commands need to be executed inside the docker container named `cm-www`
- the app root is in `./vol/www/` outside the container and `/www/` inside the container




<instruction>
Create a detailed multi phased implementation plan in markdown format in @ai-docs/plans. The last phase pf the plan should be to write a report of the changes that were made in @ai-docs/plans.
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
