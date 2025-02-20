# SSO Config Generator

A Python CLI tool for generating AWS SSO configuration and directory structures.

## Overview

SSO Config Generator is a standalone Python tool that simplifies AWS SSO configuration management by:

1. Generating properly configured AWS CLI config files
2. Creating directory structures that mirror your AWS Organization
3. Setting up environment files for easy role switching using `direnv`

## Installation

You can install SSO Config Generator using pip:

```bash
pip install sso-config-generator
```

### Prerequisites

- Python 3.8 or higher
- AWS CLI v2
- `direnv` (optional, for automatic profile switching)

## Usage

### Basic Usage

Simply run:

```bash
sso-config-generator generate
```

This will:
- Create/update your AWS CLI config file (`~/.aws/config`)
- Generate a directory structure under `~/unified-environment/`
- Create `.envrc` files in each account directory with AdministratorAccess role
- Use OU structure for directory organization (cached for performance)

The tool caches OU structure information in `~/.aws/.ou` to improve performance. When the cache exists, it will be used automatically with a notification. To rebuild the cache:

```bash
sso-config-generator generate --rebuild-cache
```

### Command Options

```
Usage: sso-config-generator [OPTIONS]

Options:
  --create-directories/--no-create-directories  Create a directory for each account (default: True)
  --use-ou-structure/--no-use-ou-structure     Use the OU structure in the unified environment (default: True)
  --developer-role-name NAME                    Create .envrc files for the specified role (default: AdministratorAccess)
  --rebuild-cache                               Force rebuild of OU structure cache
  --sso-name NAME            Use specified SSO name instead of SSO start URL
  --create-repos-md          Run cclist --create-repos-md for each directory
  --skip-sso-name           Do not use the SSO name in the path
  --unified-root PATH       Use different root for unified environment
  --help                    Show this message and exit
```

### Examples

1. Basic config generation (uses defaults):
```bash
sso-config-generator generate
```

2. Disable OU structure:
```bash
sso-config-generator generate --no-use-ou-structure
```

3. Use different role:
```bash
sso-config-generator generate --developer-role-name DevRole
```

4. Force rebuild of OU cache:
```bash
sso-config-generator generate --rebuild-cache
```

## Development

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/easytocloud/sso-config-generator.git
cd sso-config-generator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
make dev-setup
```

### Common Development Tasks

- Build the package: `make build`
- Run tests: `make test`
- Lint code: `make lint`
- Format code: `make format`
- Clean build artifacts: `make clean`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
