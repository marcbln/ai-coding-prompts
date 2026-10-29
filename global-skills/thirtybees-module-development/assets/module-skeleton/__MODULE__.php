<?php
/**
 * __DISPLAY_NAME__ module for thirty bees.
 *
 * @author    __AUTHOR__
 * @copyright __YEAR__ __AUTHOR__
 * @license   AFL-3.0
 */

if (!defined('_TB_VERSION_')) {
    exit;
}

class __CLASS__ extends Module
{
    public function __construct()
    {
        $this->name = '__MODULE__';
        $this->tab = 'front_office_features';
        $this->version = '__VERSION__';
        $this->author = '__AUTHOR__';
        $this->need_instance = 0;
        $this->bootstrap = true;
        $this->controllers = ['demo'];

        parent::__construct();

        $this->displayName = $this->l('__DISPLAY_NAME__');
        $this->description = $this->l('__DESCRIPTION__');
        $this->confirmUninstall = $this->l('Remove this module and its settings?');
        $this->tb_min_version = '1.5.0';
        $this->tb_versions_compliancy = '>= 1.5.0';
    }

    public function install()
    {
        return parent::install()
            && $this->registerHook('displayHome')
            && Configuration::updateValue('__PREFIX___TEXT', $this->l('Hello from __DISPLAY_NAME__.'));
    }

    public function uninstall()
    {
        return Configuration::deleteByName('__PREFIX___TEXT')
            && parent::uninstall();
    }

    public function getContent()
    {
        $output = '';

        if (Tools::isSubmit('submit__CLASS__')) {
            $text = Tools::getValue('__PREFIX___TEXT');

            if (!is_string($text) || trim($text) === '') {
                $output .= $this->displayError($this->l('Text is required.'));
            } else {
                Configuration::updateValue('__PREFIX___TEXT', $text);
                $output .= $this->displayConfirmation($this->l('Settings updated.'));
            }
        }

        return $output.$this->renderForm();
    }

    protected function renderForm()
    {
        $form = [
            'form' => [
                'legend' => [
                    'title' => $this->l('Settings'),
                    'icon'  => 'icon-cogs',
                ],
                'input' => [
                    [
                        'type'     => 'text',
                        'label'    => $this->l('Home block text'),
                        'name'     => '__PREFIX___TEXT',
                        'required' => true,
                    ],
                ],
                'submit' => [
                    'title' => $this->l('Save'),
                ],
            ],
        ];

        $helper = new HelperForm();
        $helper->show_toolbar = false;
        $helper->table = $this->table;
        $helper->default_form_language = (int) Configuration::get('PS_LANG_DEFAULT');
        $helper->allow_employee_form_lang = (int) Configuration::get('PS_BO_ALLOW_EMPLOYEE_FORM_LANG');
        $helper->identifier = $this->identifier;
        $helper->submit_action = 'submit__CLASS__';
        $helper->currentIndex = $this->context->link->getAdminLink('AdminModules', false)
            .'&configure='.$this->name.'&tab_module='.$this->tab.'&module_name='.$this->name;
        $helper->token = Tools::getAdminTokenLite('AdminModules');
        $helper->tpl_vars = [
            'fields_value' => [
                '__PREFIX___TEXT' => Tools::getValue('__PREFIX___TEXT', Configuration::get('__PREFIX___TEXT')),
            ],
            'languages'   => $this->context->controller->getLanguages(),
            'id_language' => $this->context->language->id,
        ];

        return $helper->generateForm([$form]);
    }

    public function hookDisplayHome()
    {
        $this->context->smarty->assign([
            'module_text' => Configuration::get('__PREFIX___TEXT'),
        ]);

        return $this->display(__FILE__, 'display_home.tpl');
    }
}
