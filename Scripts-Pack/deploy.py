#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TF_PACK = os.path.join(PROJECT_ROOT, "Terraform-Pack")
ANSIBLE_PACK = os.path.join(PROJECT_ROOT, "Ansible-Pack")
SCRIPTS_PACK = os.path.dirname(__file__)
PLAYBOOK_PATH = os.path.join(ANSIBLE_PACK, "site.yml")
INVENTORY_PATH = os.path.join(ANSIBLE_PACK, "inventory.ini")


def check_prerequisites():
    """Verify Terraform and Ansible are installed."""
    tools = ["terraform", "ansible-playbook", "ssh"]
    for tool in tools:
        if subprocess.run(["which", tool], capture_output=True).returncode != 0:
            print(f"[!] Error: {tool} is not installed")
            sys.exit(1)


def get_terraform_output(key):
    """Retrieve a single Terraform output value."""
    result = subprocess.run(
        ["terraform", "output", "-raw", key],
        cwd=TF_PACK,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"[!] Error retrieving Terraform output '{key}'")
        print(result.stderr)
        sys.exit(1)
    return result.stdout.strip()


def create_inventory(host, username, ssh_key, fqdn):
    """Create Ansible inventory file dynamically."""
    inventory_content = f"""[web_servers]
{host} ansible_user={username} ansible_ssh_private_key_file={ssh_key} ansible_host_key_checking=False

[web_servers:vars]
fqdn={fqdn}
"""
    with open(INVENTORY_PATH, "w") as f:
        f.write(inventory_content)
    print(f"[+] Created Ansible inventory at {INVENTORY_PATH}")


def run_playbook(ssh_key):
    """Execute the Ansible playbook."""
    print("\n[*] Executing Ansible playbook...\n")
    result = subprocess.run(
        ["ansible-playbook", "-i", INVENTORY_PATH, PLAYBOOK_PATH, "-v"],
        cwd=ANSIBLE_PACK
    )
    if result.returncode != 0:
        print("\n[!] Ansible playbook execution failed")
        sys.exit(1)
    print("\n[+] Ansible playbook completed successfully")


def main():
    parser = argparse.ArgumentParser(
        description="Deploy infrastructure to Azure VM using Ansible"
    )
    parser.add_argument(
        "-s", "--ssh-key",
        dest="ssh_key",
        required=True,
        help="Path to SSH private key for VM authentication"
    )

    args = parser.parse_args()

    if not os.path.isfile(args.ssh_key):
        print(f"[!] SSH key not found: {args.ssh_key}")
        sys.exit(1)

    if not os.path.isfile(PLAYBOOK_PATH):
        print(f"[!] Playbook not found: {PLAYBOOK_PATH}")
        sys.exit(1)

    if not os.path.isdir(ANSIBLE_PACK):
        print(f"[!] Ansible-Pack directory not found: {ANSIBLE_PACK}")
        sys.exit(1)

    check_prerequisites()

    print("[*] Retrieving Terraform outputs...\n")
    public_ip = get_terraform_output("public_ip")
    fqdn = get_terraform_output("fqdn")
    username = get_terraform_output("username")

    print(f"[+] Public IP: {public_ip}")
    print(f"[+] FQDN: {fqdn}")
    print(f"[+] Username: {username}\n")

    create_inventory(public_ip, username, args.ssh_key, fqdn)

    print("[*] Testing SSH connectivity...\n")
    ssh_test = subprocess.run(
        ["ssh", "-i", args.ssh_key, "-o", "ConnectTimeout=5",
         "-o", "StrictHostKeyChecking=accept-new",
         f"{username}@{public_ip}", "echo 'SSH connection successful'"],
        capture_output=True,
        text=True
    )
    if ssh_test.returncode != 0:
        print(f"[!] SSH connection failed:\n{ssh_test.stderr}")
        sys.exit(1)
    print("[+] SSH connection successful\n")

    run_playbook(args.ssh_key)

    print("\n[+] Infrastructure deployment complete!")
    print(f"[*] Access your service at: https://{fqdn}")


if __name__ == "__main__":
    main()
