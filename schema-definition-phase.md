---
description: "SCHEMA DEFINITION PHASE"
createdAt: 2025-12-14
createdBy: Cascade
tags: [schema, definition, typescript, phase]
documentType: INSTRUCTIONS
---
# Phase 1.75: Schema Definition

## Purpose
Define all data structures, types, and relationships in a machine-readable format that subsequent phases can validate against.

## Format
```typescript
// schemas.d.ts template
interface Schema {
  models: {
    [modelName: string]: {
      fields: {
        [fieldName: string]: {
          type: string;
          required: boolean;
          constraints?: {
            min?: number;
            max?: number;
            pattern?: string;
            enum?: string[];
          };
          references?: string; // For relationships
        };
      };
      relations: {
        [relationName: string]: {
          type: "one-to-one" | "one-to-many" | "many-to-many";
          model: string;
          inverse?: string;
        };
      };
    };
  };
  
  apis: {
    [endpointName: string]: {
      method: "GET" | "POST" | "PUT" | "DELETE";
      path: string;
      input?: string; // References a model
      output?: string; // References a model
      authentication?: boolean;
    };
  };
}
```

## Usage
- Phase 2 (stubbing) validates file structure against schema
- Phase 3 (implementation) validates code against schema
- Serves as source of truth for data types and relationships
