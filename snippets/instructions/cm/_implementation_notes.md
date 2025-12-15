---
description: CM Project Specific Context
---
- Frontend root is vol/www/assets
- Backend root is vol/www/src
- the app runs in container `cm-www`, you need to consider this when running commands (use `docker exec -it cm-www /www/bin/console`)
- migrations for the main database are created with `bin/console make:migration` (inside the container)
- migrations for the tenant database are created with `bin/console app:sys:mt:migrations:diff 2` (inside the container)
