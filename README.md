# SSO Config Generator

A Python CLI tool for generating AWS CLI configuration and directory structures.

## The issue it solves

In a large organization with multiple AWS accounts, managing access via AWS SSO can become cumbersome. You may have access to many roles across various accounts, and switching between them manually can be error-prone and time-consuming.

sso-config-generator creates a profile for each AWS Role you have access to via AWS SSO. After logging in to an sso session, you can use the profiles in your AWS CLI commands, SDKs, and tools like Terraform.

```bash
aws sso login --profile sso-browser
```
The login command opens a browser window for authentication. After successful login, you can use the generated profiles like this:

```bash
aws s3 ls --profile my-profile-name
```
or set the `AWS_PROFILE` (or `AWS_DEFAULT_PROFILE`) environment variable:

```bash
export AWS_PROFILE=my-profile-name
aws s3 ls
```

Optionally it also creates a directory structure that mirrors your AWS Organization, making it easy to navigate and manage multiple AWS accounts. When a developer role is configured, each account directory receives a `.envrc` file (for use with `direnv`) that sets the `AWS_PROFILE` environment variable for that account, so that cd-ing into the directory automatically switches to the correct AWS profile.

## Profile Naming Convention
Profiles are named using the following convention:

```
<RoleName>@<AccountName>
```
For example, if you have access to the `AdministratorAccess` role in the `DevAccount`, the profile will be named:

```
AdministratorAccess@DevAccount
```

## Authentication Profile

`sso-config-generator` authenticates through a named AWS profile (default: `sso-browser`, overridable with `--profile`).  That profile must exist in `~/.aws/config` and reference a valid `sso_session`:

```ini
[sso-session sso]
sso_region              = eu-west-1
sso_start_url           = https://my-company.awsapps.com/start
sso_registration_scopes = sso:account:access

[profile sso-browser]
sso_session    = sso
sso_account_id = 123456789012           # Organization Management Account ID
sso_role_name  = OrganizationAccountRole
region         = eu-west-1
output         = json
```

Run `aws sso login --profile sso-browser` before invoking `sso-config-generator` so the CLI can reuse the cached credentials.

### One-Time Setup: Authentication Profile Configuration

The authentication profile is used to retrieve both SSO account information and (when `--use-ou-structure` is active) AWS Organization structure. The SSO role must have the necessary IAM permissions.

**Role Setup:**
1. In your AWS SSO console, assign a role to your user account in your **Organization Management Account** (master account)
2. The role name in SSO should match the `sso_role_name` you configured in the `sso-browser` profile (e.g., `OrganizationAccountRole`)
3. In your Organization Management Account, create or update the IAM role with the following trust relationship (for SSO):
   - Trust the SSO service in your region
4. Attach the following permissions policy to the IAM role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sso:ListAccounts",
        "sso:ListAccountRoles",
        "organizations:ListRoots",
        "organizations:ListOrganizationalUnitsForParent",
        "organizations:DescribeOrganizationalUnit",
        "organizations:ListParents"
      ],
      "Resource": "*"
    }
  ]
}
```

**Alternative:** Instead of creating a custom role, you can use the AWS managed policy `OrganizationsReadOnlyAccess` which includes all the required permissions.

After setting up the role in SSO, run:
```bash
aws sso login --profile sso-browser
```

## Overview

SSO Config Generator is a standalone Python tool that simplifies AWS SSO configuration management by:

1. Generating properly configured AWS CLI config files
2. Creating directory structures that mirror your AWS Organization
3. Setting up environment files for easy role switching using `direnv`

## Installation

You can install sso-config-generator via pip, or use it directly without installation using `uvx`. 

```bash
pip install sso-config-generator
```

### Prerequisites

- Python 3.8 or higher
- AWS CLI v2 configured with:
  - Default region set in `~/.aws/config` or via `AWS_DEFAULT_REGION` environment variable
  - AWS SSO configured via `aws configure sso`
- `direnv` (optional, for automatic profile switching)

### AWS Configuration

Before using the tool, ensure you have:

1. Configure AWS SSO:
   Either run:
   ```bash
   aws configure sso
   # Follow the prompts to enter:
   # - SSO start URL (e.g., https://your-domain.awsapps.com/start)
   # - SSO Region
   # - SSO registration scopes (accept default)
   ```
   or manually edit `~/.aws/config` to look like this (the `[profile sso-browser]` block must match the one described in the **Required SSO Browser Profile** section):
   ```
   [sso-session sso]
   sso_region = eu-west-1
   sso_start_url = https://YOUR_DOMAIN.awsapps.com/start
   sso_registration_scopes = sso:account:access

   [profile sso-browser]
   sso_session = sso
   sso_account_id = 123456789012
   sso_role_name = OrganizationAccountRole
   output = json
   region = eu-west-1
   ```
2. Login to AWS SSO:
   ```bash
   # Login to SSO to create credentials
   aws sso login --profile sso-browser
   ```

### Cloud9/CloudX Integration

When running in AWS Cloud9 or CloudX environments, the tool will automatically:
1. Detect if you're in your home directory with an "environment" subdirectory
2. Change to the "environment" directory
3. Skip the SSO name in the directory structure

This ensures seamless operation in AWS-provided development environments.

### Troubleshooting

1. "Error: You must specify a region"
   - Use the `--region` flag: `uvx sso-config-generator --region us-east-1`
   - Or set AWS_DEFAULT_REGION environment variable
   - Or configure default region in ~/.aws/config

2. "Unable to locate credentials"
   - Run `aws sso login` to refresh your SSO credentials
   - Ensure you've completed AWS SSO configuration with `aws configure sso`
   - Check if your SSO session has expired (sessions typically last 8 hours)

3. "SSO session is expired"
   - Run `aws sso login` to start a new session

## Usage

### Basic Usage

Simply run:

```bash
uvx sso-config-generator
```

This will update `~/.aws/config` with one profile per account/role combination and nothing else.  Directory creation and `.envrc` generation are opt-in (see options below).

The tool caches OU structure and account information in the same directory as the **real** config file (symlinks are resolved, so the cache lands in the environment-specific directory rather than `~/.aws/`).  This works seamlessly with [aws-envs](https://github.com/easytocloud/aws-envs), where `~/.aws/config` is a symlink such as `~/.aws/aws-envs/easytocloud/config` — the cache is then stored as `~/.aws/aws-envs/easytocloud/.ou-cache`.

The cache filename is:
- `.ou-cache` — default (one config file = one environment, no qualifier needed)
- `.ou-cache.<sso-session-name>` — when `--sso-session-name` is explicitly supplied (multiple SSO sessions sharing one config file)

If a cache file is older than 7 days it is ignored and rebuilt automatically.
To force a full cache rebuild:

```bash
uvx sso-config-generator --rebuild-cache
```

### Command Options

| Option | Default | Description |
|--------|---------|-------------|
| `--profile NAME` | `sso-browser` | AWS profile used to authenticate against SSO and AWS Organizations |
| `--region REGION` | `eu-west-1` | AWS region |
| `--sso-session-name NAME` | auto-detected | Name of the `[sso-session …]` section in `~/.aws/config` |
| `--sso-name NAME` | extracted from URL | Override the SSO organisation name |
| `--create-directories` | off | Create a local directory tree with one directory per account |
| `--use-ou-structure` | off | Nest account directories under their OU hierarchy (requires `--create-directories`) |
| `--developer-role-name NAME` | not set | Create a `.envrc` in each account directory exporting `AWS_PROFILE` to this role (requires `--create-directories`; omit to skip `.envrc` creation) |
| `--unified-root PATH` | current directory | Root directory for the account tree |
| `--skip-sso-name` | off | Do not create a top-level directory for the SSO organisation name |
| `--create-repos-md` | off | Create a `repos.md` placeholder in each account directory |
| `--rebuild-cache` | off | Force a full refresh of the OU / account cache |
| `--validate` | off | Validate existing configuration instead of generating |
| `--version` | | Show the version and exit |
| `--help` | | Show help and exit |

### Configuration File

Frequently used options can be stored in `.sso-config-generator.ini` so you do not have to repeat them on every invocation.  The tool reads (in order, later values override earlier ones):

1. `~/.sso-config-generator.ini`
2. `./.sso-config-generator.ini` (current working directory)

Command-line flags always take precedence over both files.

A fully annotated sample file with all options set to their defaults (and `DeveloperAccess` as the example developer role) is provided as [`.sso-config-generator.ini.sample`](.sso-config-generator.ini.sample).  Copy and adjust it:

```bash
# User-wide defaults
cp .sso-config-generator.ini.sample ~/.sso-config-generator.ini

# Or project-specific overrides
cp .sso-config-generator.ini.sample .sso-config-generator.ini
```

Minimal example that enables directory creation with OU nesting and `.envrc` files:

```ini
[sso-config-generator]
create_directories  = true
use_ou_structure    = true
developer_role_name = DeveloperAccess
```

### Examples

1. Update `~/.aws/config` only (default behaviour):
```bash
uvx sso-config-generator
```

2. Create a local directory tree:
```bash
uvx sso-config-generator --create-directories
```

3. Directory tree with OU-based nesting:
```bash
uvx sso-config-generator --create-directories --use-ou-structure
```

4. Directory tree with `.envrc` files for a specific role:
```bash
uvx sso-config-generator --create-directories --developer-role-name DeveloperAccess
```

5. Use a different authentication profile:
```bash
uvx sso-config-generator --profile my-admin-profile
```

6. Use a specific AWS region:
```bash
uvx sso-config-generator --region us-east-1
```

7. Force a cache rebuild:
```bash
uvx sso-config-generator --rebuild-cache
```

8. Specify a custom root directory:
```bash
uvx sso-config-generator --create-directories --unified-root ~/aws-environments
```

9. Working in an `environment` directory (Cloud9 / CloudX):
```bash
cd ~/environment
uvx sso-config-generator
# SSO name directory is automatically skipped in an 'environment' directory
```

10. Validate existing configuration:
```bash
uvx sso-config-generator --validate
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

3. Install the package in development mode:
```bash
pip install -e .
```

### Common Development Tasks

- Build the package: `pip install build && python -m build`
- Run the tool: `uvx sso-config-generator`
- Test changes: `./test_sso_config.sh`

### Versioning

This project uses [semantic-release](https://github.com/semantic-release/semantic-release) for automated versioning and package publishing. The version is stored in a single source of truth:

- `src/sso_config_generator/version.py`: Contains the `__version__` variable
- `__init__.py` imports this version
- `pyproject.toml` is updated automatically by the GitHub workflow

When a commit is pushed to the main branch, the GitHub workflow:
1. Determines the next version based on commit messages
2. Creates a GitHub release and tag
3. Updates the version in version.py and pyproject.toml
4. Publishes the package to PyPI

To trigger specific version increments, use the following commit message prefixes:
- `feat:` - Minor version increment (e.g., 1.1.0 -> 1.2.0)
- `fix:`, `docs:`, `style:`, etc. - Patch version increment (e.g., 1.1.0 -> 1.1.1)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
