---
description: "API CONTRACT TEMPLATE"
createdAt: 2025-12-14
createdBy: Cascade
tags: [api, contract, template, documentation]
documentType: TEMPLATE
---
# API Contract Documentation

## Endpoint Template
```yaml
endpoint:
  path: /api/resource
  method: POST
  authentication: required | optional | none
  
  request:
    contentType: application/json
    schema: # References schema definition
    required_fields: []
    optional_fields: []
    
  response:
    success:
      status: 200
      schema: # References schema definition
    errors:
      - status: 400
        conditions: [] # When this error occurs
        schema: # Error response structure
      
  rate_limiting:
    requests: number
    period: timeframe
    
  caching:
    strategy: none | client | server
    duration: timeframe
```
