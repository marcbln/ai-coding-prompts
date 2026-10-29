# Payment Modules

Source anchors:

- `classes/module/PaymentModule.php` — `validateOrder()` signature and order logic
- `modules/bankwire/bankwire.php` — complete offline payment example
- `modules/bankwire/controllers/front/payment.php` — checkout confirmation page
- `modules/bankwire/controllers/front/validation.php` — order creation
- `modules/bankwire/views/templates/hook/payment.tpl` — payment option
- `modules/bankwire/views/templates/hook/payment_return.tpl` — confirmation page
- `install-dev/data/xml/hook_alias.xml` — `displayPayment` ↔ `payment`,
  `paymentReturn` ↔ `displayPaymentReturn` aliases

## 1. Main class

Extend `PaymentModule` instead of `Module` and declare the payment contracts.

```php
<?php

if (!defined('_TB_VERSION_')) {
    exit;
}

class Mypayment extends PaymentModule
{
    public function __construct()
    {
        $this->name = 'mypayment';
        $this->tab = 'payments_gateways';
        $this->version = '1.0.0';
        $this->author = 'Your Company';
        $this->need_instance = 1;
        $this->bootstrap = true;

        $this->currencies = true;
        $this->currencies_mode = 'checkbox';
        $this->is_eu_compatible = 1;
        $this->controllers = ['payment', 'validation'];

        parent::__construct();

        $this->displayName = $this->l('My payment');
        $this->description = $this->l('Accept payments with My Provider.');
        $this->confirmUninstall = $this->l('Remove the payment configuration?');
        $this->tb_min_version = '1.5.0';
        $this->tb_versions_compliancy = '>= 1.5.0';
    }

    public function install()
    {
        return parent::install()
            && $this->registerHook('displayPayment')
            && $this->registerHook('displayPaymentEU')
            && $this->registerHook('paymentReturn')
            && Configuration::updateValue('MYP_REQUIRED', 1);
    }

    public function uninstall()
    {
        return Configuration::deleteByName('MYP_REQUIRED')
            && parent::uninstall();
    }
}
```

`PaymentModule` inherits the full `Module` lifecycle. Set `$this->currencies` and
`$this->currencies_mode` (`'checkbox'` or `'radio'`) to let the merchant choose
which currencies the gateway accepts. `$this->is_eu_compatible = 1` enables the
EU payment directive path (`displayPaymentEU`).

## 2. Payment option hook

```php
public function hookPayment()
{
    if (!$this->active) {
        return '';
    }

    $this->context->smarty->assign([
        'this_path'     => $this->getPathUri(),
        'this_path_ssl' => Tools::getShopDomainSsl(true, true).__PS_BASE_URI__.'modules/'.$this->name.'/',
    ]);

    return $this->display(__FILE__, 'payment.tpl');
}

public function hookDisplayPaymentEU()
{
    if (!$this->active) {
        return '';
    }

    return [
        'cta_text' => $this->l('Pay with My Provider'),
        'logo'     => Media::getMediaPath(_PS_MODULE_DIR_.$this->name.'/logo.png'),
        'action'   => $this->context->link->getModuleLink($this->name, 'payment', [], true),
    ];
}
```

`registerHook('displayPayment')` resolves to the legacy alias `payment`, so the
handler method is `hookPayment()`. Likewise `registerHook('paymentReturn')`
resolves to `displayPaymentReturn` and the handler is `hookPaymentReturn($params)`.
Registering both the modern and legacy name is unnecessary; use the 1.6-era
names for compatibility (as native `bankwire` does).

`payment.tpl` renders the selectable option and links to the module's front
controller:

```smarty
<p class="payment_module">
  <a href="{$link->getModuleLink('mypayment', 'payment', [], true)|escape:'htmlall':'UTF-8'}"
     title="{l s='Pay with My Provider' mod='mypayment'}">
    <img src="{$module_dir|escape:'htmlall':'UTF-8'}logo.png" alt="" width="86" height="49"/>
    {l s='Pay with My Provider' mod='mypayment'}
  </a>
</p>
```

## 3. Checkout page controller

`controllers/front/payment.php` shows the order summary / redirects to the
provider. Set `$ssl = true`.

```php
class MypaymentPaymentModuleFrontController extends ModuleFrontController
{
    /** @var bool */
    public $ssl = true;

    /** @var bool */
    public $display_column_left = false;

    public function initContent()
    {
        parent::initContent();

        $cart = $this->context->cart;

        if (!Validate::isLoadedObject($cart) || $cart->nbProducts() <= 0) {
            Tools::redirect('index.php?controller=order');
        }

        $this->context->smarty->assign([
            'nbProducts' => $cart->nbProducts(),
            'total'      => $cart->getOrderTotal(true, Cart::BOTH),
            'this_path'  => $this->module->getPathUri(),
        ]);

        $this->setTemplate('payment_execution.tpl');
    }
}
```

For a hosted gateway, this is also where you create the provider session/order
and redirect to its payment page. Build the return/callback URLs with
`getModuleLink(..., true)` and persist the cart/order correlation server-side.

## 4. Validation controller (create the order)

`controllers/front/validation.php` runs after the customer confirms (offline) or
after the provider returns (online). This is the security-critical part.

```php
class MypaymentValidationModuleFrontController extends ModuleFrontController
{
    /** @var bool */
    public $ssl = true;

    public function postProcess()
    {
        $cart = $this->context->cart;

        if (!Validate::isLoadedObject($cart)
            || (int) $cart->id_customer === 0
            || (int) $cart->id_address_delivery === 0
            || (int) $cart->id_address_invoice === 0
            || !$this->module->active
        ) {
            Tools::redirect('index.php?controller=order&step=1');
        }

        $customer = new Customer((int) $cart->id_customer);
        if (!Validate::isLoadedObject($customer)) {
            Tools::redirect('index.php?controller=order&step=1');
        }

        $currency = $this->context->currency;
        $total    = (float) $cart->getOrderTotal(true, Cart::BOTH);

        $this->module->validateOrder(
            (int) $cart->id,
            (int) Configuration::get('PS_OS_PAYMENT'),
            $total,
            $this->module->displayName,
            null,
            [],
            (int) $currency->id,
            false,
            $cart->secure_key
        );

        Tools::redirect(
            'index.php?controller=order-confirmation'
            .'&id_cart='.(int) $cart->id
            .'&id_module='.(int) $this->module->id
            .'&id_order='.(int) $this->module->currentOrder
            .'&key='.$customer->secure_key
        );
    }
}
```

`PaymentModule::validateOrder()` signature in TB 1.7:

```php
validateOrder(
    $idCart,
    $idOrderState,
    $amountPaid,
    $paymentMethod = 'Unknown',
    $message = null,
    $extraVars = [],
    $currencySpecial = null,
    $dontTouchAmount = false,
    $secureKey = false,
    ?Shop $shop = null
)
```

It creates the order from the cart, applies the order state, sends emails, and
sets `$this->currentOrder`. It throws `PrestaShopException` on invalid cart,
order state, inactive module, or secure-key mismatch.

After `validateOrder()`, redirect to `order-confirmation` exactly as above. Do
not render content after order creation.

## 5. Provider callbacks / webhooks / IPN

Use a dedicated front controller (e.g. `controllers/front/callback.php`) with:

- `$ssl = true`.
- No reliance on the customer session: load the cart/order by the provider's
  reference or `id_cart`.
- Signature verification against the raw request body before parsing (use the
  provider's documented algorithm and constant-time comparison).
- Re-check amount, currency, and order state; never trust the provider's
  "paid" flag alone.
- Idempotency: if the order already exists for the cart, update/return instead
  of calling `validateOrder()` again. `Cart::orderExists()` is available.
- Respond with the provider's expected body (plain text, JSON, or 200), not an
  HTML page, and log failures with `Logger::addLog()`.

For redirect-based flows, the customer-facing return controller can be the
validation controller, but only after verifying the provider response.

## 6. Payment return template

```php
public function hookPaymentReturn($params)
{
    if (!isset($params['objOrder']) || !$params['objOrder'] instanceof Order || !$this->active) {
        return '';
    }

    $state = $params['objOrder']->getCurrentState();
    $ok = in_array($state, [
        (int) Configuration::get('PS_OS_PAYMENT'),
        (int) Configuration::get('PS_OS_OUTOFSTOCK'),
        (int) Configuration::get('PS_OS_OUTOFSTOCK_UNPAID'),
    ], true);

    $this->context->smarty->assign([
        'status'       => $ok ? 'ok' : 'failed',
        'total_to_pay' => Tools::displayPrice($params['total_to_pay'], $params['currencyObj'], false),
        'id_order'     => $params['objOrder']->id,
        'reference'    => $params['objOrder']->reference,
    ]);

    return $this->display(__FILE__, 'payment_return.tpl');
}
```

Use `payment_return.tpl` to show the bank details or the provider result. Escape
all order-derived output.

## 7. Checklist

- [ ] Main class extends `PaymentModule`.
- [ ] `$this->controllers = ['payment', 'validation', 'callback']` matches actual
      controller files.
- [ ] `install()` registers `displayPayment`, `displayPaymentEU`,
      `paymentReturn`.
- [ ] Payment/validation/callback controllers force `$ssl = true`.
- [ ] Cart, customer, currency, and module active state validated.
- [ ] `validateOrder()` called once per cart; duplicate guard in place.
- [ ] Provider signature, amount, currency, and state verified before order
      creation.
- [ ] Redirects to `order-confirmation` with cart/module/order/key.
- [ ] Configuration values deleted on uninstall.
- [ ] Tested with the module disabled, an empty cart, an invalid currency, a
      failed provider response, and a replayed callback.
