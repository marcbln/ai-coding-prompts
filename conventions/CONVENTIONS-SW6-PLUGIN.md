# Shopware 6 Plugin Development Conventions

## PHP Standards
- Always use constructor property promotion
- Always use PHP 8 attributes (not annotations)
- Use `Symfony\Component\Console\Attribute\AsCommand` for console commands

## Console Commands
- Commands MUST extend `\Topdata\TopdataFoundationSW6\TopdataFoundationSW6`
- **Always use `\Topdata\TopdataFoundationSW6\Util\CliLogger` for ALL CLI output**
- Never use direct console output methods
- Available CliLogger methods:
  - `CliLogger::info($msg)` - for informational messages
  - `CliLogger::notice($msg)` - for notices with blue background
  - `CliLogger::warning($msg)` - for warnings with ⚠️ emoji
  - `CliLogger::error($msg)` - for errors with ❌ emoji
  - `CliLogger::success($msg)` - for success messages with ✅ emoji
  - `CliLogger::debug($msg)` - for debug output (respects verbosity)
  - `CliLogger::writeln($msg)` - for general output
  - `CliLogger::write($msg, $newLine)` - for output without automatic newline
  - `CliLogger::section($msg)` - for section headers
  - `CliLogger::title($msg)` - for titles
  - `CliLogger::progress($current, $total, $label)` - for progress indication
  - `CliLogger::activity($msg, $newLine)` - for activity logging with caller info
  - `CliLogger::red($msg)`, `CliLogger::blue($msg)`, `CliLogger::yellow($msg)` - for colored output
  - `CliLogger::dump()` - for debugging (CLI only)
  - `CliLogger::mem()` - for memory usage output
  - `CliLogger::lap($start)` - for timing measurements
- If `SymfonyStyle` is needed, use `CliLogger::getCliStyle()` to get an instance
- Set CliStyle in command's initialize method: `CliLogger::setCliStyle($cliStyle)`

## Dependency Injection
- Use autowiring whenever possible
- For the "special repository" `sales_channel.product.repository`, use named parameter injection:
```xml
<service id="MyCompany\MyPluginSW6\Service\MyService" autowire="true">
    <argument type="service" key="$productRepository" id="sales_channel.product.repository"/>
</service>
```

## Security
- Never use `csrf_token`

## Twig Templates
- Use `path('some.action-name')` when referencing controller actions
