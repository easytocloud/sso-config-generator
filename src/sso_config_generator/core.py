import os
import sys
import json
import boto3
import yaml
import datetime
import configparser
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class SSOConfigGenerator:
    """Main class for generating AWS SSO configuration and directory structures."""
    
    def __init__(self, create_directories: bool = True,
                 use_ou_structure: bool = True,
                 developer_role_name: str = "AdministratorAccess",
                 sso_name: Optional[str] = None,
                 create_repos_md: bool = False,
                 skip_sso_name: bool = False,
                 unified_root: Optional[str] = None):
        """Initialize the SSO Config Generator.
        
        Args:
            create_directories: Whether to create directory structure
            use_ou_structure: Whether to use OU structure in directories
            developer_role_name: Role name to use for .envrc files
            sso_name: SSO name to use instead of SSO start URL
            create_repos_md: Whether to create repos.md files
            skip_sso_name: Whether to skip SSO name in paths
            unified_root: Custom root directory for unified environment
        """
        self.create_directories = create_directories
        self.use_ou_structure = use_ou_structure
        self.developer_role_name = developer_role_name
        self.sso_name = sso_name
        self.create_repos_md = create_repos_md
        self.skip_sso_name = skip_sso_name
        self.unified_root = unified_root or os.path.expanduser("~/unified-environment")
        
        # AWS clients
        self.sso_client = boto3.client('sso')
        self.org_client = boto3.client('organizations') if use_ou_structure else None
        
        # Config paths
        self.aws_config_path = os.path.expanduser("~/.aws/config")
        self.ou_cache_path = os.path.expanduser("~/.aws/.ou")
        self.config = configparser.ConfigParser()
        
    def generate(self) -> bool:
        """Generate AWS SSO configuration and directory structure.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print("\n=== Generating SSO Configuration ===\n")
            
            # Get SSO information
            sso_info = self._get_sso_info()
            if not sso_info:
                return False
                
            # Get account and role information
            accounts = self._get_accounts()
            if not accounts:
                return False
                
            # Generate AWS CLI config
            if not self._generate_aws_config(sso_info, accounts):
                return False
                
            # Create directory structure if requested
            if self.create_directories:
                if not self._create_directory_structure(accounts):
                    return False
                    
            print("\nSSO configuration generated successfully!")
            return True
            
        except Exception as e:
            print(f"Error generating SSO configuration: {str(e)}", file=sys.stderr)
            return False
            
    def validate(self) -> bool:
        """Validate current AWS SSO configuration.
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            print("\n=== Validating SSO Configuration ===\n")
            
            # Check AWS config file exists
            if not os.path.exists(self.aws_config_path):
                print("Error: AWS config file not found", file=sys.stderr)
                return False
                
            # Validate SSO access
            if not self._validate_sso_access():
                return False
                
            # Test role assumptions
            if not self._test_role_assumptions():
                return False
                
            print("\nSSO configuration is valid!")
            return True
            
        except Exception as e:
            print(f"Error validating SSO configuration: {str(e)}", file=sys.stderr)
            return False
            
    def _get_sso_info(self) -> Optional[Dict]:
        """Get SSO configuration information.
        
        Returns:
            Optional[Dict]: SSO information if successful, None otherwise
        """
        try:
            # Get SSO start URL and region from AWS config if exists
            self.config.read(self.aws_config_path)
            if "default" in self.config:
                return {
                    "start_url": self.config["default"].get("sso_start_url"),
                    "region": self.config["default"].get("sso_region"),
                    "name": self.sso_name or self._extract_sso_name()
                }
            
            # Otherwise prompt for information
            start_url = input("Enter SSO start URL: ").strip()
            region = input("Enter SSO region [us-east-1]: ").strip() or "us-east-1"
            
            return {
                "start_url": start_url,
                "region": region,
                "name": self.sso_name or self._extract_sso_name(start_url)
            }
            
        except Exception as e:
            print(f"Error getting SSO information: {str(e)}", file=sys.stderr)
            return None
            
    def _get_accounts(self) -> Optional[List[Dict]]:
        """Get AWS account information with OU structure.
        
        Returns:
            Optional[List[Dict]]: List of account information if successful, None otherwise
        """
        try:
            # Check if cache exists and should be used
            if os.path.exists(self.ou_cache_path):
                print("\nFound OU cache, using cached data.")
                print("Use --rebuild-cache to refresh the OU structure.\n")
                return self._get_accounts_from_cache()
            
            return self._build_accounts_cache()
            
        except Exception as e:
            print(f"Error getting account information: {str(e)}", file=sys.stderr)
            return None
            
    def _get_accounts_from_cache(self) -> Optional[List[Dict]]:
        """Get account information from cache.
        
        Returns:
            Optional[List[Dict]]: List of account information if successful, None otherwise
        """
        try:
            with open(self.ou_cache_path, 'r') as f:
                cache_data = json.load(f)
                
            accounts = []
            for account in cache_data['accounts']:
                roles = self._get_account_roles(account['id'])
                if roles:
                    account['roles'] = roles
                    accounts.append(account)
                    
            if not accounts:
                print("No accessible accounts found in cache", file=sys.stderr)
                return None
                
            return accounts
            
        except Exception as e:
            print(f"Error reading cache: {str(e)}", file=sys.stderr)
            return None
            
    def _build_accounts_cache(self) -> Optional[List[Dict]]:
        """Build account and OU structure cache.
        
        Returns:
            Optional[List[Dict]]: List of account information if successful, None otherwise
        """
        try:
            print("Building OU structure cache...")
            
            # Get root OU
            roots = self.org_client.list_roots()['Roots']
            if not roots:
                raise Exception("No organization root found")
                
            root_id = roots[0]['Id']
            
            # Build OU tree
            ou_tree = self._build_ou_tree(root_id)
            
            # Get all accounts
            accounts = []
            paginator = self.sso_client.get_paginator('list_accounts')
            
            for page in paginator.paginate():
                for account in page['accountList']:
                    # Get account OU path
                    ou_path = self._get_account_ou_path(account['accountId'])
                    roles = self._get_account_roles(account['accountId'])
                    
                    if roles:
                        account_info = {
                            'id': account['accountId'],
                            'name': account['accountName'],
                            'ou_path': ou_path,
                            'roles': roles
                        }
                        accounts.append(account_info)
            
            if not accounts:
                print("No accessible accounts found", file=sys.stderr)
                return None
                
            # Save to cache
            cache_data = {
                'ou_tree': ou_tree,
                'accounts': accounts,
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            os.makedirs(os.path.dirname(self.ou_cache_path), exist_ok=True)
            with open(self.ou_cache_path, 'w') as f:
                json.dump(cache_data, f, indent=2)
                
            return accounts
            
        except Exception as e:
            print(f"Error building cache: {str(e)}", file=sys.stderr)
            return None
            
    def _build_ou_tree(self, parent_id: str, path: str = "/") -> Dict:
        """Recursively build OU tree structure.
        
        Args:
            parent_id: Parent OU ID
            path: Current path in OU tree
            
        Returns:
            Dict: OU tree structure
        """
        tree = {'id': parent_id, 'path': path, 'children': []}
        
        paginator = self.org_client.get_paginator('list_organizational_units_for_parent')
        for page in paginator.paginate(ParentId=parent_id):
            for ou in page['OrganizationalUnits']:
                ou_path = f"{path}{ou['Name']}/"
                child_tree = self._build_ou_tree(ou['Id'], ou_path)
                tree['children'].append(child_tree)
                
        return tree
        
    def _get_account_ou_path(self, account_id: str) -> str:
        """Get OU path for an account.
        
        Args:
            account_id: AWS account ID
            
        Returns:
            str: OU path for the account
        """
        try:
            parents = self.org_client.list_parents(ChildId=account_id)['Parents']
            if not parents:
                return "/"
                
            parent_id = parents[0]['Id']
            path_parts = []
            
            while True:
                ou = self.org_client.describe_organizational_unit(
                    OrganizationalUnitId=parent_id
                )['OrganizationalUnit']
                path_parts.insert(0, ou['Name'])
                
                parents = self.org_client.list_parents(ChildId=parent_id)['Parents']
                if not parents or parents[0]['Type'] == 'ROOT':
                    break
                    
                parent_id = parents[0]['Id']
                
            return "/" + "/".join(path_parts) + "/"
            
        except Exception:
            return "/"
            
    def _get_account_roles(self, account_id: str) -> List[str]:
        """Get available roles for an account.
        
        Args:
            account_id: AWS account ID
            
        Returns:
            List[str]: List of role names
        """
        try:
            roles = []
            paginator = self.sso_client.get_paginator('list_account_roles')
            
            for page in paginator.paginate(accountId=account_id):
                roles.extend([role['roleName'] for role in page['roleList']])
                
            return roles
            
        except Exception:
            return []
            
    def _generate_aws_config(self, sso_info: Dict, accounts: List[Dict]) -> bool:
        """Generate AWS CLI config file.
        
        Args:
            sso_info: SSO configuration information
            accounts: List of account information
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            config = configparser.ConfigParser()
            
            # Add default section
            config['default'] = {
                'sso_start_url': sso_info['start_url'],
                'sso_region': sso_info['region'],
                'sso_account_id': accounts[0]['id'],  # Use first account as default
                'sso_role_name': accounts[0]['roles'][0],  # Use first role as default
                'region': sso_info['region']
            }
            
            # Add profile for each account/role combination
            for account in accounts:
                for role in account['roles']:
                    profile_name = f"{role}@{account['name']}"
                    config[f"profile {profile_name}"] = {
                        'sso_start_url': sso_info['start_url'],
                        'sso_region': sso_info['region'],
                        'sso_account_id': account['id'],
                        'sso_role_name': role,
                        'region': sso_info['region']
                    }
            
            # Write config file
            os.makedirs(os.path.dirname(self.aws_config_path), exist_ok=True)
            with open(self.aws_config_path, 'w') as f:
                config.write(f)
                
            return True
            
        except Exception as e:
            print(f"Error generating AWS config: {str(e)}", file=sys.stderr)
            return False
            
    def _create_directory_structure(self, accounts: List[Dict]) -> bool:
        """Create directory structure for accounts.
        
        Args:
            accounts: List of account information
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            base_path = Path(self.unified_root)
            if not self.skip_sso_name:
                base_path = base_path / self._sanitize_path(self.sso_name)
                
            # Create base directory
            base_path.mkdir(parents=True, exist_ok=True)
            
            # Store generator config
            self._store_generator_config(base_path)
            
            # Create account directories
            for account in accounts:
                account_path = base_path / self._sanitize_path(account['name'])
                account_path.mkdir(exist_ok=True)
                
                # Create .envrc file
                role_name = self.developer_role_name or account['roles'][0]
                if role_name in account['roles']:
                    self._create_envrc_file(account_path, f"{role_name}@{account['name']}")
                    
                # Create repos.md if requested
                if self.create_repos_md:
                    self._create_repos_md(account_path, account)
                    
            return True
            
        except Exception as e:
            print(f"Error creating directory structure: {str(e)}", file=sys.stderr)
            return False
            
    def _store_generator_config(self, base_path: Path) -> None:
        """Store generator configuration for future updates.
        
        Args:
            base_path: Base directory path
        """
        config = {
            'create_directories': self.create_directories,
            'use_ou_structure': self.use_ou_structure,
            'developer_role_name': self.developer_role_name,
            'sso_name': self.sso_name,
            'create_repos_md': self.create_repos_md,
            'skip_sso_name': self.skip_sso_name,
            'unified_root': str(self.unified_root)
        }
        
        with open(base_path / '.generate-sso-config', 'w') as f:
            yaml.dump(config, f)
            
    def _create_envrc_file(self, directory: Path, profile: str) -> None:
        """Create .envrc file in directory.
        
        Args:
            directory: Directory to create file in
            profile: AWS profile name
        """
        with open(directory / '.envrc', 'w') as f:
            f.write(f'export AWS_PROFILE="{profile}"\n')
            
    def _create_repos_md(self, directory: Path, account: Dict) -> None:
        """Create repos.md file in directory.
        
        Args:
            directory: Directory to create file in
            account: Account information
        """
        with open(directory / 'repos.md', 'w') as f:
            f.write(f"# Repositories in {account['name']}\n\n")
            f.write("Run `cclist --create-repos-md` to populate this file.\n")
            
    def _extract_sso_name(self, url: Optional[str] = None) -> str:
        """Extract SSO name from start URL.
        
        Args:
            url: SSO start URL (optional)
            
        Returns:
            str: Extracted SSO name
        """
        if not url and "default" in self.config:
            url = self.config["default"].get("sso_start_url")
            
        if url:
            # Extract domain from URL (e.g., 'company' from 'company.awsapps.com')
            return url.split('//')[1].split('.')[0]
            
        return "default-sso"
            
    def _sanitize_path(self, name: str) -> str:
        """Sanitize name for use in paths.
        
        Args:
            name: Name to sanitize
            
        Returns:
            str: Sanitized name
        """
        return name.lower().replace(' ', '-')
            
    def _validate_sso_access(self) -> bool:
        """Validate SSO access.
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            self.sso_client.list_accounts()
            return True
        except Exception as e:
            print(f"Error validating SSO access: {str(e)}", file=sys.stderr)
            return False
            
    def _test_role_assumptions(self) -> bool:
        """Test role assumptions.
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Test first profile in config
            self.config.read(self.aws_config_path)
            for section in self.config.sections():
                if section.startswith('profile '):
                    profile = section[8:]  # Remove 'profile ' prefix
                    print(f"Testing profile: {profile}")
                    session = boto3.Session(profile_name=profile)
                    sts = session.client('sts')
                    sts.get_caller_identity()
                    return True
                    
            print("No profiles found to test", file=sys.stderr)
            return False
            
        except Exception as e:
            print(f"Error testing role assumption: {str(e)}", file=sys.stderr)
            return False
