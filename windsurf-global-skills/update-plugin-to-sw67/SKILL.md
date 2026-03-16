---
name: update-plugin-to-sw67
description: Upgrades a Shopware 6 plugin from an older version (like 6.4/6.5) to be fully compatible with Shopware 6.7 by refactoring deprecated code, updating routing attributes, replacing removed interfaces, and modernizing PHP features. Use this skill when asked to make a Shopware plugin compatible with version 6.7.
---

# Upgrading a Shopware Plugin to 6.7

This skill outlines the critical tasks required to upgrade a Shopware 6 plugin for compatibility with Shopware 6.7. Shopware 6.6 and 6.7 introduce significant breaking changes, especially regarding Symfony updates and removed core interfaces.

## 1. Routing: Migrating from Annotations to Attributes
Shopware 6.6 (via Symfony 6/7) completely removed support for `@Route` annotations in favor of PHP 8 `#[Route(...)]` attributes.

**Action Required:**
- Replace `use Symfony\Component\Routing\Annotation\Route;` with `use Symfony\Component\Routing\Attribute\Route;` in all controller files.
- Convert all class-level and method-level doctrine annotations to PHP 8 attributes.

*Example Before:*
```php
/**
 * @Route(defaults={"_routeScope"={"storefront"}})
 */
class MyAjaxController extends StorefrontController {
    /**
     * @Route("/my-route", name="frontend.my.route", methods={"GET"})
     */
    public function myAction() {}
}
```

*Example After:*
```php
#[Route(defaults: ['_routeScope' => ['storefront']])]
class MyAjaxController extends StorefrontController {
    #[Route(path: '/my-route', name: 'frontend.my.route', methods: ['GET'])]
    public function myAction() {}
}
```

## 2. Replacing Removed Interfaces
Certain interfaces heavily used in previous Shopware versions have been deprecated and removed.

**Action Required:**
- **EntityRepositoryInterface:** Replace `use Shopware\Core\Framework\DataAbstractionLayer\EntityRepositoryInterface;` with the concrete class `use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;`.

*Example:*
Change `private EntityRepositoryInterface $repository;` to `private EntityRepository $repository;`.

## 3. Modernizing Dependency Injection (Constructor Property Promotion)
To adhere to modern PHP 8 standards and typical Shopware repository guidelines (like `AGENTS.md`), dependency injection should be refactored to use constructor property promotion.

**Action Required:**
- Refactor all `__construct` methods in controllers, services, and subscribers.
- Use `private readonly` for injected dependencies.

*Example Before:*
```php
class MyService {
    private EntityRepository $repo;
    
    public function __construct(EntityRepository $repo) {
        $this->repo = $repo;
    }
}
```

*Example After:*
```php
class MyService {
    public function __construct(
        private readonly EntityRepository $repo
    ) {}
}
```

## 4. `composer.json` Updates
Ensure the plugin requires the correct Shopware core version.

**Action Required:**
- Update `composer.json` to require `"shopware/core": "6.7.*"`.

## 5. Clean Up Codebase
- Run `phpstan` and `php-cs-fixer` if available in the project to verify type safety and formatting.
- Ensure no backward compatibility code remains if the user specifies no backward compatibility is needed.

Follow these steps meticulously to ensure the upgraded plugin performs seamlessly in Shopware 6.7 environments.
