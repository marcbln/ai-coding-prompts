---
name: sw67-scheduled-tasks
description: Patterns and gotchas for Shopware 6.7 scheduled tasks. Use when creating a ScheduledTask/ScheduledTaskHandler, debugging messenger.CRITICAL "Too few arguments" errors for task handlers, auditing plugins after a 6.6/6.7 upgrade, or when scheduled tasks don't run. Covers the constructor breaking change, task registration/lifecycle, dynamic rescheduling (6.7.13+), and running/debugging tasks.
---

# Shopware 6.7 Scheduled Task Patterns

## 1. Breaking Change: `ScheduledTaskHandler` Constructor (6.6+)

Since Shopware 6.6, the abstract base class signature is:

```php
public function __construct(
    protected EntityRepository $scheduledTaskRepository,
    protected readonly LoggerInterface $exceptionLogger,
)
```

**Symptom:** Handler crashes at runtime with `ArgumentCountError`, visible only as a messenger log entry:

```
messenger.CRITICAL: Error thrown while handling message ...ScheduledTask...
Removing from transport after 0 retries.
Error: "Too few arguments to function ...ScheduledTaskHandler::__construct(), 1 passed ... and exactly 2 expected"
```

**Root cause:** The handler calls `parent::__construct($scheduledTaskRepository)` with only one argument (the pre-6.6 signature). This is NOT caught at compile time — it only explodes when the message is consumed.

**Fix (handler):**

```php
use Psr\Log\LoggerInterface;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\MessageQueue\ScheduledTask\ScheduledTaskHandler;
use Symfony\Component\Messenger\Attribute\AsMessageHandler;
use Topdata\TopdataEnhancedSearchSW6\Service\SearchAnalyticsService;

#[AsMessageHandler(handles: ConsolidateSearchLogsTask::class)]
class ConsolidateSearchLogsTaskHandler extends ScheduledTaskHandler
{
    public function __construct(
        EntityRepository $scheduledTaskRepository,
        LoggerInterface $exceptionLogger,
        private readonly SearchAnalyticsService $analyticsService,
        private readonly SystemConfigService $systemConfigService
    ) {
        parent::__construct($scheduledTaskRepository, $exceptionLogger);
    }
}
```

**Fix (services.xml):** Task handlers are usually registered with explicit (non-autowired) arguments — the new logger must be injected there too, using the exact parameter name as `key`:

```xml
<service id="Plugin\ScheduledTask\MyTaskHandler">
    <argument type="service" id="scheduled_task.repository"/>
    <argument type="service" id="Psr\Log\LoggerInterface" key="$exceptionLogger"/>
    <argument type="service" id="..." key="$myService"/>
    <tag name="messenger.message_handler"/>
</service>
```

No plugin reinstall needed — `services.xml` is re-read per request; only the failed/queued message needs to be retried or cleared.

## 2. Audit Existing Plugins After an Upgrade

Scan all plugins for handlers with the old one-arg parent call:

```bash
for f in $(rg -ln "extends ScheduledTaskHandler" custom/plugins/*/src/); do
    echo "=== $f"; rg -n "parent::__construct" "$f"
done
```

- All non-topdata/older plugins (SwagPayPal, MoorlFoundation, etc.) already pass 2 args — they were updated in 6.6.
- Only plugins last touched before 6.6 (e.g. merged/legacy plugin sources) still have the bug.
- Always fix PHP handler + `services.xml` **together** in the same edit, then verify: `php -l` on the handler and `xmllint --noout` on the services.xml.

## 3. Task Registration & Lifecycle

A `ScheduledTask` + handler pair is wired up as:

```xml
<service id="Plugin\ScheduledTask\MyTask">
    <tag name="shopware.scheduled.task"/>
</service>
```

- The task class extends `ScheduledTask`, implements `getTaskName()` (use a vendor-prefixed name to avoid collisions) and `getDefaultInterval()` (constants: `MINUTELY` 60, `HOURLY` 3600, `DAILY` 86400, `WEEKLY` 604800).
- `TaskRegistry` (runs on `scheduled-task:register` / plugin install) upserts tasks into the `scheduled_task` table. It syncs `runInterval` with `defaultRunInterval` — if a plugin changes `getDefaultInterval()`, the DB interval is updated only when it still matches the default; otherwise the shop's customized interval is preserved.
- `shouldRun()` — return false to register the task as `STATUS_SKIPPED` (e.g. gated on a config flag).
- `shouldRescheduleOnFailure()` — return true to silently retry on the next run instead of throwing/marking failed.
- Handler wiring: `#[AsMessageHandler(handles: MyTask::class)]` attribute on the handler subclass plus a `messenger.message_handler` tag in services.xml.
- `run()` is the abstract method the task executes; the parent `__invoke` handles status transitions (queued → running → scheduled/failed), rescheduling into `nextExecutionTime + runInterval`, and logs failures through the injected `exceptionLogger`.

## 4. Dynamic Rescheduling (6.7.13+)

Since Shopware 6.7.13, a handler can implement `Shopware\Core\Framework\MessageQueue\ScheduledTask\DynamicallyScheduledTaskHandler` (in addition to extending `ScheduledTaskHandler`) to compute the next execution time per-run instead of using the fixed `runInterval`:

```php
use Shopware\Core\Framework\MessageQueue\ScheduledTask\DynamicallyScheduledTaskHandler;
use Shopware\Core\Framework\MessageQueue\ScheduledTask\ScheduledTask;
use Shopware\Core\Framework\MessageQueue\ScheduledTask\ScheduledTaskEntity;

class MyTaskHandler extends ScheduledTaskHandler implements DynamicallyScheduledTaskHandler
{
    public function getNextExecutionTime(ScheduledTask $task, ScheduledTaskEntity $taskEntity): ?\DateTimeImmutable
    {
        // return null to keep the default runInterval-based rescheduling
        return new \DateTimeImmutable('+5 minutes');
    }
}
```

## 5. Running & Debugging Tasks

Console commands (all prefixed `scheduled-task:*`):

- `bin/console scheduled-task:list` — show registered tasks + status
- `bin/console scheduled-task:register` — (re)register tasks from tagged services (runs automatically on plugin install/update)
- `bin/console scheduled-task:schedule <name> [--immediately] [--force]` — schedule a task manually
- `bin/console scheduled-task:run-single <name>` — run one task regardless of schedule (great for testing)
- `bin/console scheduled-task:deactivate <name>` — set status inactive
- `bin/console messenger:consume` — run the message worker (in prod, needs a supervisor daemon; the AdminWorker only polls while the admin UI is open and can be disabled)

Debug flow when a task "doesn't run":
1. `scheduled-task:list` → is the status `queued`/`scheduled` (not `failed`/`skipped`/`inactive`)?
2. If `failed`, the handler crashed (e.g. the constructor break from section 1) — check `var/log/messenger-*.log` for `messenger.CRITICAL`.
3. Fix, then `scheduled-task:schedule <name> --immediately --force` and `messenger:consume` (or wait for the admin worker).
4. Check the DB row in `scheduled_task` for the expected `nextExecutionTime`.

## 6. Related

- Full upgrade workflow: see `update-plugin-to-sw67` skill (routing attributes, removed interfaces, fetching UPGRADE-6.x docs).