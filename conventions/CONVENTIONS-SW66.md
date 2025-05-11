# Conventions Shopware 6.6 plugin

- always use constructor property promotion
- use autowiring whenever possible
- the "special repository" `sales_channel.product.repository` get injected with named parameter injection:
```
        <service id="MyCompany\MyPluginSW6\Service\MyService"  autowire="true">
            <argument type="service" key="$productRepository" id="sales_channel.product.repository"/>
        </service>
```
- use attributes, not annotations
