


<instruction>
Please create a detailed multi phased implementation plan in markdown format. 
The plan should also include an update of the user documentation.
The plan will be implemented by an AI coding agent. 
</instruction>


Note: 
- all commands need to be executed inside the docker container named `cm-www`
- the app root is in `./vol/www/` outside the container and `/www/` inside the container




<instruction>
Please create a detailed multi phased implementation plan in markdown format in @ai_docs/plans. The last phase pf the plan should be to write a report of the changes that were made in @ai_docs/plans.
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




