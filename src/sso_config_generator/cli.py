import os
import sys
import click
from . import __version__
from .core import SSOConfigGenerator

@click.group()
@click.version_option(version=__version__)
def cli():
    """SSO Config Generator - Generate AWS SSO configuration and directory structures."""
    pass

@cli.command()
@click.option('--create-directories/--no-create-directories', default=True, help='Create a directory for each account')
@click.option('--use-ou-structure/--no-use-ou-structure', default=True, help='Use the OU structure in the unified environment')
@click.option('--developer-role-name', default="AdministratorAccess", help='Create .envrc files for the specified role')
@click.option('--rebuild-cache', is_flag=True, help='Force rebuild of OU structure cache')
@click.option('--sso-name', help='Use specified SSO name instead of SSO start URL')
@click.option('--create-repos-md', is_flag=True, help='Run cclist --create-repos-md for each directory')
@click.option('--skip-sso-name', is_flag=True, help='Do not use the SSO name in the path')
@click.option('--unified-root', help='Use different root for unified environment')
def generate(create_directories: bool, use_ou_structure: bool, developer_role_name: str,
            sso_name: str, create_repos_md: bool, skip_sso_name: bool, unified_root: str,
            rebuild_cache: bool):
    """Generate AWS SSO configuration and directory structure.
    
    This command will:
    1. Generate AWS CLI config file with SSO profiles
    2. Create directory structure (optional)
    3. Set up environment files for direnv
    
    Example usage:
        sso-config-generator generate --create-directories
        sso-config-generator generate --create-directories --use-ou-structure
        sso-config-generator generate --developer-role-name DevRole
    """
    try:
        # Remove cache if rebuild requested
        if rebuild_cache:
            cache_path = os.path.expanduser("~/.aws/.ou")
            if os.path.exists(cache_path):
                os.remove(cache_path)
                print("Removed existing OU cache.")
        
        generator = SSOConfigGenerator(
            create_directories=create_directories,
            use_ou_structure=use_ou_structure,
            developer_role_name=developer_role_name,
            sso_name=sso_name,
            create_repos_md=create_repos_md,
            skip_sso_name=skip_sso_name,
            unified_root=unified_root
        )
        
        if not generator.generate():
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

@cli.command()
def validate():
    """Validate current AWS SSO configuration.
    
    This command will:
    1. Check AWS CLI config file
    2. Verify SSO access
    3. Test role assumptions
    
    Example usage:
        sso-config-generator validate
    """
    try:
        generator = SSOConfigGenerator()
        
        if not generator.validate():
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    cli()
