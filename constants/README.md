# Constants

The `constants` module provides standard enumerations used across the ETL process.

## Modules

### Audit Fields

`audit_fields.AuditField` defines standard audit field values.

- `CREATED_BY_SYSTEM`: "system"
- `UPDATED_BY_SYSTEM`: "system"

### Environments

`environments.Environment` defines the supported deployment environments.

- `LOCAL`
- `DEVELOPMENT`
- `UAT`
- `PREPRODUCTION`
- `PRODUCTION`

## Usage

```python
from etl_core.constants import AuditField
from etl_core.constants import Environment

print(AuditField.CREATED_BY_SYSTEM)
# Output: system

print(Environment.UPDATED_BY_SYSTEM)
# Output: production
```
