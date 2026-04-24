#!/usr/bin/env python3
"""
NetworkBuster Vercel Domain Setup Automation
Complete domain configuration for Vercel deployment
"""

import subprocess
import sys
import json
import time
from pathlib import Path

PROJECT_PATH = Path(__file__).parent.resolve()

class VercelDomainSetup:
    """Automate Vercel domain configuration."""
    
    def __init__(self, domain="networkbuster.net"):
        self.domain = domain
        self.www_domain = f"www.{domain}"
        self.api_domain = f"api.{domain}"
        self.vercel_installed = self._check_vercel_cli()
    
    def _check_vercel_cli(self):
        """Check if Vercel CLI is installed."""
        try:
            result = subprocess.run(
                ["vercel", "--version"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                print(f"✅ Vercel CLI installed: {result.stdout.strip()}")
                return True
            else:
                print("⚠️  Vercel CLI not found")
                return False
        except FileNotFoundError:
            print("⚠️  Vercel CLI not found")
            return False
    
    def install_vercel_cli(self):
        """Install Vercel CLI if not present."""
        if self.vercel_installed:
            print("✅ Vercel CLI already installed")
            return True
        
        print("\n📦 Installing Vercel CLI...")
        try:
            subprocess.run(
                ["npm", "install", "-g", "vercel"],
                check=True,
                capture_output=True
            )
            print("✅ Vercel CLI installed successfully")
            self.vercel_installed = True
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Vercel CLI: {e}")
            return False
        except FileNotFoundError:
            print("❌ npm not found. Please install Node.js first.")
            return False
    
    def login_vercel(self):
        """Authenticate with Vercel."""
        if not self.vercel_installed:
            print("❌ Vercel CLI not installed")
            return False
        
        print("\n🔐 Checking Vercel authentication...")
        result = subprocess.run(
            ["vercel", "whoami"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Logged in as: {result.stdout.strip()}")
            return True
        else:
            print("⚠️  Not logged in to Vercel")
            print("🔑 Running Vercel login...")
            
            # Interactive login
            result = subprocess.run(["vercel", "login"])
            return result.returncode == 0
    
    def get_project_info(self):
        """Get current Vercel project information."""
        if not self.vercel_installed:
            return None
        
        print("\n📊 Fetching project information...")
        try:
            result = subprocess.run(
                ["vercel", "inspect"],
                capture_output=True,
                text=True,
                cwd=PROJECT_PATH
            )
            if result.returncode == 0:
                print("✅ Project linked to Vercel")
                print(result.stdout)
                return result.stdout
            else:
                print("⚠️  Project not linked to Vercel")
                return None
        except Exception as e:
            print(f"⚠️  Could not fetch project info: {e}")
            return None
    
    def link_project(self):
        """Link local project to Vercel."""
        print("\n🔗 Linking project to Vercel...")
        
        result = subprocess.run(
            ["vercel", "link"],
            cwd=PROJECT_PATH
        )
        
        if result.returncode == 0:
            print("✅ Project linked successfully")
            return True
        else:
            print("❌ Failed to link project")
            return False
    
    def add_domain(self, domain):
        """Add domain to Vercel project."""
        if not self.vercel_installed:
            return False
        
        print(f"\n➕ Adding domain: {domain}")
        
        result = subprocess.run(
            ["vercel", "domains", "add", domain],
            cwd=PROJECT_PATH,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Domain {domain} added successfully")
            print(result.stdout)
            return True
        else:
            if "already exists" in result.stderr.lower():
                print(f"ℹ️  Domain {domain} already added")
                return True
            else:
                print(f"❌ Failed to add domain: {result.stderr}")
                return False
    
    def show_dns_config(self):
        """Display required DNS configuration."""
        print("\n" + "="*70)
        print("  📋 DNS CONFIGURATION REQUIRED")
        print("="*70)
        
        print(f"\n🌐 Root Domain: {self.domain}")
        print("   Type: A Record")
        print("   Name: @")
        print("   Value: 76.76.21.21")
        print("   TTL: 3600")
        print("   --- OR ---")
        print("   Type: CNAME")
        print("   Name: @")
        print("   Value: cname.vercel-dns.com")
        
        print(f"\n🌐 WWW Subdomain: {self.www_domain}")
        print("   Type: CNAME")
        print("   Name: www")
        print("   Value: cname.vercel-dns.com")
        print("   TTL: 3600")
        
        print(f"\n🔧 API Subdomain: {self.api_domain}")
        print("   Type: CNAME")
        print("   Name: api")
        print("   Value: <your-azure-container-app>.azurecontainerapps.io")
        print("   TTL: 3600")
        
        print("\n" + "="*70)
        print("  🔒 SSL/TLS Configuration")
        print("="*70)
        print("  ✅ Vercel automatically provisions SSL certificates")
        print("  ✅ HTTPS enforced by default")
        print("  ✅ Certificate auto-renewal enabled")
        
        print("\n" + "="*70)
        print("  ⏱️  Propagation Time")
        print("="*70)
        print("  • DNS changes take 5 minutes to 48 hours to propagate")
        print("  • SSL certificate issued after DNS verification")
        print("  • Check status: vercel domains ls")
        print("\n")
    
    def check_domain_status(self):
        """Check status of added domains."""
        if not self.vercel_installed:
            return
        
        print("\n🔍 Checking domain status...")
        
        result = subprocess.run(
            ["vercel", "domains", "ls"],
            capture_output=True,
            text=True,
            cwd=PROJECT_PATH
        )
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("⚠️  Could not fetch domain status")
    
    def verify_dns(self):
        """Verify DNS configuration using nslookup."""
        print("\n🔍 Verifying DNS configuration...")
        
        for domain in [self.domain, self.www_domain]:
            print(f"\nChecking {domain}...")
            result = subprocess.run(
                ["nslookup", domain],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                if "76.76.21.21" in result.stdout or "vercel" in result.stdout.lower():
                    print(f"  ✅ {domain} configured correctly")
                else:
                    print(f"  ⚠️  {domain} not pointing to Vercel yet")
                print(f"  Output: {result.stdout[:200]}")
            else:
                print(f"  ❌ DNS lookup failed for {domain}")
    
    def deploy_to_production(self):
        """Deploy project to production on Vercel."""
        if not self.vercel_installed:
            return False
        
        print("\n🚀 Deploying to Vercel production...")
        
        result = subprocess.run(
            ["vercel", "--prod"],
            cwd=PROJECT_PATH
        )
        
        if result.returncode == 0:
            print("✅ Deployment successful!")
            return True
        else:
            print("❌ Deployment failed")
            return False
    
    def setup_environment_vars(self):
        """Setup environment variables in Vercel."""
        print("\n⚙️  Environment Variables Setup")
        print("="*70)
        
        env_vars = {
            "DOMAIN_NAME": self.domain,
            "API_URL": f"https://{self.api_domain}",
            "NODE_ENV": "production"
        }
        
        print("Recommended environment variables:")
        for key, value in env_vars.items():
            print(f"  • {key}={value}")
        
        print("\nTo add environment variables:")
        print("  1. Visit: https://vercel.com/dashboard/settings")
        print("  2. Select your project")
        print("  3. Go to Settings > Environment Variables")
        print("  4. Add the variables above")
        print("\nOr use CLI:")
        for key, value in env_vars.items():
            print(f"  vercel env add {key} production")
    
    def run_full_setup(self):
        """Run complete domain setup process."""
        print("\n" + "="*70)
        print("  🚀 NETWORKBUSTER VERCEL DOMAIN SETUP")
        print("="*70)
        print(f"  Domain: {self.domain}")
        print("="*70 + "\n")
        
        # Step 1: Check/Install Vercel CLI
        if not self.vercel_installed:
            if not self.install_vercel_cli():
                print("\n❌ Setup aborted: Could not install Vercel CLI")
                return False
        
        # Step 2: Login to Vercel
        if not self.login_vercel():
            print("\n❌ Setup aborted: Authentication required")
            return False
        
        # Step 3: Link project (if not already linked)
        project_info = self.get_project_info()
        if not project_info:
            if not self.link_project():
                print("\n❌ Setup aborted: Could not link project")
                return False
        
        # Step 4: Add domains
        domains_to_add = [self.domain, self.www_domain]
        for domain in domains_to_add:
            self.add_domain(domain)
        
        # Step 5: Show DNS configuration
        self.show_dns_config()
        
        # Step 6: Check current domain status
        self.check_domain_status()
        
        # Step 7: Environment variables
        self.setup_environment_vars()
        
        # Step 8: Verify DNS (optional)
        print("\n" + "="*70)
        verify = input("Do you want to verify DNS configuration now? (y/n): ").strip().lower()
        if verify == 'y':
            self.verify_dns()
        
        # Step 9: Deploy to production
        print("\n" + "="*70)
        deploy = input("Deploy to production now? (y/n): ").strip().lower()
        if deploy == 'y':
            self.deploy_to_production()
        
        print("\n" + "="*70)
        print("  ✅ VERCEL DOMAIN SETUP COMPLETE")
        print("="*70)
        print("\n📝 Next Steps:")
        print("  1. Configure DNS records at your domain registrar")
        print("  2. Wait for DNS propagation (5 min - 48 hours)")
        print("  3. Monitor domain status: vercel domains ls")
        print("  4. Verify SSL certificate: https://{self.domain}")
        print("\n")
        
        return True

def main():
    """Main setup function."""
    
    # Check if custom domain provided
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = input("Enter your domain (default: networkbuster.net): ").strip()
        if not domain:
            domain = "networkbuster.net"
    
    setup = VercelDomainSetup(domain)
    setup.run_full_setup()

if __name__ == "__main__":
    main()
