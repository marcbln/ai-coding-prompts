# Shopware 6 Plugin Development Conventions

## PHP Standards
- Always use constructor property promotion
- Always use PHP 8 attributes (not annotations)
- Use `Symfony\Component\Console\Attribute\AsCommand` for console commands

## Console Commands
- Commands MUST extend `\Topdata\TopdataFoundationSW6\TopdataFoundationSW6`
- For CLI output, use `\Topdata\TopdataFoundationSW6\Util\CliLogger` everywhere
- If `SymfonyStyle` is needed, use `\Topdata\TopdataFoundationSW6\Util\CliLogger::getCliStyle()` to get an instance

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

