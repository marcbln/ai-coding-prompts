<?php
/**
 * __DISPLAY_NAME__ front controller.
 *
 * @author    __AUTHOR__
 * @copyright __YEAR__ __AUTHOR__
 * @license   AFL-3.0
 */

if (!defined('_TB_VERSION_')) {
    exit;
}

class __CLASS__DemoModuleFrontController extends ModuleFrontController
{
    /** @var bool Set to true for checkout/account/customer pages. */
    public $ssl = false;

    /** @var bool */
    public $display_column_left = false;

    /** @var bool */
    public $display_column_right = false;

    public function initContent()
    {
        parent::initContent();

        $this->context->smarty->assign([
            'module_text' => Configuration::get('__PREFIX___TEXT'),
        ]);

        $this->setTemplate('demo.tpl');
    }
}
