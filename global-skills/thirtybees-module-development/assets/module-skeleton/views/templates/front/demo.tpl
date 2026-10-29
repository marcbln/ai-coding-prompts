{* __DISPLAY_NAME__ front controller template. *}
<h1>{l s='__DISPLAY_NAME__' mod='__MODULE__'}</h1>
<p>{$module_text|escape:'htmlall':'UTF-8'}</p>
<p>
  <a href="{$link->getPageLink('index', true)|escape:'htmlall':'UTF-8'}">
    {l s='Back to the shop' mod='__MODULE__'}
  </a>
</p>
