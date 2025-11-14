# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python CLI tool that generates AWS SSO configuration and directory structures. It automates the creation of AWS CLI config files with SSO profiles and optionally creates directory structures that mirror AWS Organization Unit (OU) hierarchies.

## Development Commands

### Required AWS Profile Baseline
Always ensure local workspaces have the following profile in `~/.aws/config` before running commands or tests:

```
[profile sso-browser]
sso_session = sso
region = eu-west-1
output = json
```

Most examples assume `aws sso login --profile sso-browser` has been executed and that cached credentials exist for subsequent CLI calls.

### Package Management
- **Install in development mode**: `pip install -e .`
- **Build package**: `pip install build && python -m build`
- **Test installation**: `uvx sso-config-generator --help`

### Testing
- **Run test script**: `./test_sso_config.sh` (comprehensive test of all CLI options)
- **Manual testing**: `uvx sso-config-generator --no-create-directories` (dry run mode)

### Versioning and Release
- Uses semantic-release for automated versioning based on commit messages
- Version is managed in `src/sso_config_generator/version.py`
- Use conventional commit messages: `feat:` for minor, `fix:` for patch increments
- Release workflow automatically publishes to PyPI on main branch pushes

## Code Architecture

### Core Components

**CLI Layer (`cli.py`)**:
- Click-based command-line interface
- Handles all command-line options and flags
- Delegates to `SSOConfigGenerator` class for core functionality

**Core Logic (`core.py`)**:
- `SSOConfigGenerator` class contains all business logic
- Key methods:
  - `generate()`: Main orchestration method
  - `_get_sso_info()`: Extracts SSO configuration from AWS config
  - `_get_accounts()`: Retrieves account information with OU caching
  - `_generate_aws_config()`: Creates/updates AWS CLI config file
  - `_create_directory_structure()`: Creates directory hierarchy

**Version Management (`version.py`)**:
- Single source of truth for version number
- Imported by `__init__.py` and used by CLI

### Key Architecture Patterns

**Caching Strategy**:
- OU structure cached in `.ou` file (same directory as AWS config)
- Cache includes account info, roles, and OU hierarchy
- Use `--rebuild-cache` to force refresh

**Configuration Management**:
- Managed block approach in AWS config file using markers
- Preserves existing configuration outside managed blocks
- SSO session configuration handled separately from profiles

**Environment Detection**:
- Auto-detects Cloud9/CloudX environments
- Changes working directory to `environment` subdirectory if present
- Automatically skips SSO name directory creation in Cloud9/CloudX

**Directory Structure Logic**:
- Base path can be customized with `--unified-root`
- SSO name directory creation controlled by `--skip-sso-name`
- OU structure mirroring optional with `--use-ou-structure`

### AWS Integration

**Authentication Flow**:
- Relies on existing AWS SSO setup (`aws configure sso`)
- Reads SSO tokens from `~/.aws/sso/cache/`
- Falls back to prompting for re-authentication

**Organizations API Usage**:
- Only used when `--use-ou-structure` is enabled
- Builds complete OU tree recursively
- Maps accounts to their OU paths for directory structure

### File Generation

**AWS Config Files**:
- Creates profiles in format: `{role}@{sanitized_account_name}`
- Uses SSO session configuration for token sharing
- Preserves existing non-SSO configuration

**Directory Files**:
- `.envrc`: Sets `AWS_PROFILE` environment variable for direnv
- `repos.md`: Placeholder file (populated by external tools)
- `.generate-sso-config`: YAML config for regeneration

## Special Considerations

- Path sanitization replaces spaces with underscores but preserves case
- Cloud9/CloudX auto-detection based on home directory structure
- OU cache stored alongside AWS config file for consistency
- Profile naming uses sanitized account names for filesystem compatibility