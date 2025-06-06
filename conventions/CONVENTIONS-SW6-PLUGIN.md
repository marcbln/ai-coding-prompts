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





## Storefront JavaScript Conventions

### Handling Core Libraries (like Bootstrap)

**NEVER** import JavaScript libraries that are already provided globally by the Shopware Storefront.

#### The Reason

The Shopware storefront bundles essential third-party libraries (most notably **Bootstrap**) into its main compiled JavaScript file (`all.js`). If your plugin's JavaScript also `import`s Bootstrap, the build system (webpack) will bundle a **second, conflicting copy** of the library into your plugin's final JS file.

This leads to two versions of Bootstrap running on the same page, causing unpredictable conflicts that are very difficult to debug. Symptoms include:
- Core functionality breaking (e.g., account dropdowns, off-canvas menus).
- Modals or popups not working correctly.
- Increased page load size.

#### The Wrong Way

This code will cause conflicts because it creates a separate, competing instance of Bootstrap's code.

```javascript
// ❌ WRONG: This bundles a second copy of Bootstrap into your plugin's JS file.

import { Modal } from 'bootstrap';
import { Toast } from 'bootstrap';
import Plugin from 'src/plugin-system/plugin.class';

export default class MyPlugin extends Plugin {
    init() {
        // ...
        // This 'Modal' comes from your plugin's bundled copy, not Shopware's.
        this.bsModal = new Modal(this.modalElement);
    }
}
```

#### The Correct Way

Always access the global instance of the library that Shopware provides on the `window` object. This ensures your plugin and the Shopware core are using the exact same code.

```javascript
// ✅ CORRECT: Access the global instance provided by Shopware.

import Plugin from 'src/plugin-system/plugin.class';
// Note: There is NO "import from 'bootstrap'".

export default class MyPlugin extends Plugin {
    showMyModal() {
        // First, check if Bootstrap is available on the window object as a safeguard.
        if (typeof window.bootstrap === 'undefined' || typeof window.bootstrap.Modal === 'undefined') {
            console.error('Bootstrap or its Modal component is not available on the window object!');
            return;
        }

        // Destructure the Modal class from the global `window.bootstrap` object.
        const { Modal } = window.bootstrap;

        // Now, create the instance. This uses Shopware's own version of Bootstrap.
        const myModalInstance = new Modal(this.modalElement);
        myModalInstance.show();
    }
}
```

### Rule of Thumb: `import` vs. `window`

- **Third-Party Libraries (Bootstrap, Popper.js, etc.):**
  - Assume Shopware provides it globally. **Do not `import` it.** Access it via `window.bootstrap`, `window.Popper`, etc.

- **Shopware-Specific Modules (`Plugin`, `HttpClient`, etc.):**
  - These are part of the plugin system's internal structure and are designed to be imported. You **MUST `import` them** from their `src/` path (e.g., `import Plugin from 'src/plugin-system/plugin.class';`).





