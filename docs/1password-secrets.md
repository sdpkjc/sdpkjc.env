# 1Password CLI for Environment Variables

## Reference Syntax

```
op://<vault-name>/<item-name>/<section-name>/<field-name>
```

## Common Commands

```bash
# Sign in
eval $(op signin)

# Create item with sections
op item create \
  --category=api-credential \
  --title=APIKeys \
  --vault=Dev \
  'section.FIELD_NAME=value'

# Read value
op read "op://Dev/APIKeys/section/FIELD_NAME"

# Edit/add fields
op item edit APIKeys --vault=Dev 'section.NEW_FIELD=value'

# List items
op item list --vault=Dev
```

## Shell Integration

See `shell/.env_presets` for preset functions:

```bash
use_env wukong192    # Load Anthropic preset
load_gitlab          # Load GitLab credentials
show_env             # Show current env
clear_env            # Clear env
```

## Docs

- https://developer.1password.com/docs/cli/
- https://developer.1password.com/docs/cli/secret-references/
