import sys
import os
import configparser
from typing import Optional
import click
from .version import __version__
from .core import SSOConfigGenerator


def _read_ini_defaults() -> dict:
    """Read layered .sso-config-generator.ini files and return a default_map for Click.

    Reads ~/.sso-config-generator.ini first, then ./.sso-config-generator.ini so that
    the CWD file overrides the home file.  CLI flags always take precedence over both.
    """
    config = configparser.ConfigParser()
    home_ini = os.path.expanduser('~/.sso-config-generator.ini')
    cwd_ini = os.path.join(os.getcwd(), '.sso-config-generator.ini')
    config.read([home_ini, cwd_ini])

    section = 'sso-config-generator'
    if not config.has_section(section):
        return {}

    bool_keys = {
        'create_directories', 'use_ou_structure', 'create_repos_md',
        'skip_sso_name', 'rebuild_cache', 'validate',
    }
    defaults = {}
    for key, value in config.items(section):
        param = key.replace('-', '_')
        if param in bool_keys:
            defaults[param] = value.lower() in ('true', 'yes', '1')
        else:
            defaults[param] = value
    return defaults


class _IniConfigCommand(click.Command):
    """Click Command subclass that injects .sso-config-generator.ini values as defaults."""

    def make_context(self, info_name, args, parent=None, **extra):
        extra['default_map'] = _read_ini_defaults()
        return super().make_context(info_name, args, parent=parent, **extra)


@click.command(cls=_IniConfigCommand)
@click.version_option(version=__version__)
@click.option('--create-directories', is_flag=True, default=False,
              help='Create a local directory tree with one directory per account.')
@click.option('--use-ou-structure', is_flag=True, default=False,
              help='Nest account directories under their OU hierarchy '
                   '(requires --create-directories).')
@click.option('--developer-role-name', default=None,
              help='When set, create a .envrc file in each account directory exporting '
                   'AWS_PROFILE to this role (requires --create-directories). '
                   'Omit to skip .envrc creation entirely.')
@click.option('--rebuild-cache', is_flag=True,
              help='Force a full refresh of the OU / account cache.')
@click.option('--sso-name',
              help='Override the SSO name that is normally extracted from the SSO start URL.')
@click.option('--create-repos-md', is_flag=True,
              help='Create a repos.md placeholder file in each account directory.')
@click.option('--skip-sso-name', is_flag=True,
              help='Do not create a top-level directory named after the SSO organisation.')
@click.option('--unified-root',
              help='Root directory under which the account tree is created '
                   '(default: current directory). '
                   'When the current directory is named "environment" '
                   'the SSO name directory is skipped automatically.')
@click.option('--validate', is_flag=True,
              help='Validate the current AWS SSO configuration instead of generating it.')
@click.option('--region', default='eu-west-1', show_default=True,
              help='AWS region.')
@click.option('--sso-session-name', default=None,
              help='Name of the [sso-session …] section to use in ~/.aws/config. '
                   'Auto-detected when exactly one such section exists, '
                   'otherwise defaults to "sso". '
                   'Useful when multiple SSO environments share the same config file.')
@click.option('--profile', default='sso-browser', show_default=True,
              help='AWS profile used to authenticate against SSO and AWS Organizations. '
                   'Must reference a valid sso_session in ~/.aws/config and have '
                   'permissions for sso:ListAccounts, sso:ListAccountRoles, and '
                   '(when --use-ou-structure is active) organizations:ListRoots, '
                   'organizations:ListOrganizationalUnitsForParent, '
                   'organizations:DescribeOrganizationalUnit, '
                   'organizations:ListParents.')
def cli(create_directories: bool, use_ou_structure: bool, developer_role_name: Optional[str],
        sso_name: Optional[str], create_repos_md: bool, skip_sso_name: bool,
        unified_root: Optional[str], rebuild_cache: bool, validate: bool,
        region: str, sso_session_name: Optional[str], profile: str):
    """Generate AWS CLI profiles and (optionally) a local directory tree from your SSO organisation.

    By default the tool only rewrites the SSO-managed block in ~/.aws/config, creating
    one profile per account/role combination.  Use --create-directories to also build a
    local directory tree, and add --developer-role-name to place a .envrc (for direnv)
    in every account directory.

    \b
    AUTHENTICATION
      The tool authenticates through the AWS profile given by --profile (default: sso-browser).
      That profile must be configured in ~/.aws/config with an sso_session reference, e.g.:

        [sso-session sso]
        sso_region              = eu-west-1
        sso_start_url           = https://my-company.awsapps.com/start
        sso_registration_scopes = sso:account:access

        [profile sso-browser]
        sso_session    = sso
        sso_account_id = 123456789012          # management / delegated-admin account
        sso_role_name  = OrganizationAccountAccessRole
        region         = eu-west-1

      Log in before running:
        aws sso login --profile sso-browser

    \b
    CONFIGURATION FILES
      Frequently used options can be stored in .sso-config-generator.ini so you don't
      have to repeat them on every invocation.  The tool reads (in order, later values
      override earlier ones):
        ~/.sso-config-generator.ini
        ./.sso-config-generator.ini   (current working directory)
      Command-line flags always take precedence over both files.

      Example .sso-config-generator.ini:
        [sso-config-generator]
        region              = eu-west-1
        profile             = sso-browser
        create_directories  = true
        use_ou_structure    = true
        developer_role_name = ReadOnlyAccess

    \b
    EXAMPLES
      # Update ~/.aws/config only (default)
      sso-config-generator

      # Also create a local directory tree
      sso-config-generator --create-directories

      # Directory tree with OU-based nesting
      sso-config-generator --create-directories --use-ou-structure

      # Directory tree + .envrc files for the ReadOnlyAccess role
      sso-config-generator --create-directories --developer-role-name ReadOnlyAccess

      # Force a cache refresh
      sso-config-generator --rebuild-cache

      # Use a non-default authentication profile
      sso-config-generator --profile my-admin-profile

      # Validate existing configuration
      sso-config-generator --validate
    """
    try:
        if validate:
            generator = SSOConfigGenerator(
                region=region,
                sso_session_name=sso_session_name,
                profile=profile,
            )
            if not generator.validate():
                sys.exit(1)
        else:
            generator = SSOConfigGenerator(
                create_directories=create_directories,
                use_ou_structure=use_ou_structure,
                developer_role_name=developer_role_name,
                sso_name=sso_name,
                create_repos_md=create_repos_md,
                skip_sso_name=skip_sso_name,
                unified_root=unified_root,
                region=region,
                sso_session_name=sso_session_name,
                profile=profile,
            )

            if rebuild_cache:
                removed_count = generator.clear_ou_cache_files()
                if removed_count:
                    print(f"Removed {removed_count} OU cache file(s)")
                else:
                    print("No OU cache files found to remove")

            if not generator.generate():
                sys.exit(1)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    cli()
