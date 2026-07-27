# DropperDragon Infrastructure Pack

Dropper WebServer Solution 

<p align="center">
  <img width="400" height="400" src="/Pictures/logo.svg"><br /><br />
  <img alt="GitHub License" src="https://img.shields.io/github/license/nickvourd/DropperDragon?style=social&logo=GitHub&logoColor=purple">
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/nickvourd/DropperDragon?logoColor=yellow"><br />
  <img alt="GitHub forks" src="https://img.shields.io/github/forks/nickvourd/DropperDragon?logoColor=red">
  <img alt="GitHub watchers" src="https://img.shields.io/github/watchers/nickvourd/DropperDragon?logoColor=blue">
  <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/nickvourd/DropperDragon?style=social&logo=GitHub&logoColor=green">
</p>

## Description

DropperDragon is a comprehensive infrastructure automation pack for deploying and configuring web servers on Azure. It leverages Terraform for infrastructure provisioning and Ansible for system configuration, providing a seamless automation workflow.

![Static Badge](https://img.shields.io/badge/Ansible-green?style=flat&logoSize=auto)
![Static Badge](https://img.shields.io/badge/Terraform-blue?style=flat&logoSize=auto)
![Static Badge](https://img.shields.io/badge/Python-purple?style=flat&logoSize=auto)
![Static Badge](https://img.shields.io/badge/Nginx-FF6900?style=flat&logoSize=auto)
![Static Badge](https://img.shields.io/badge/Azure-0078D4?style=flat&logoSize=auto)

The following list explains the meaning of each pack:

- **Scripts-Pack**: Python scripts that orchestrate infrastructure deployment and configuration workflows.
- **Terraform-Pack**: Infrastructure-as-Code that provisions Azure VMs and network resources.
- **Ansible-Pack**: Configuration management playbooks that harden systems, install web servers, and manage SSL certificates.

ℹ️ This project automates the complete deployment lifecycle from bare infrastructure to production-ready web servers with HTTPS.

> If you find any bugs, don't hesitate to [report them](https://github.com/nickvourd/DropperDragon/issues). Your feedback is valuable in improving the quality of this project!

## Disclaimer

The authors and contributors of this project are not liable for any misuse of the tool. It is intended for educational and authorized infrastructure deployment purposes only. Users are responsible for ensuring lawful and authorized usage.

## Table of Contents
- [DropperDragon Infrastructure Pack](#dropperdragon-infrastructure-pack)
  - [Description](#description)
  - [Disclaimer](#disclaimer)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Workflow](#workflow)
  - [Directory Structure](#directory-structure)
  - [Troubleshooting](#troubleshooting)

## Features

- **Automated Azure VM Provisioning**: One-command infrastructure deployment
- **System Hardening**: Automated security updates and package management
- **Web Server Configuration**: Automatic nginx installation and configuration
- **SSL Certificate Management**: Automated Let's Encrypt certificate provisioning
- **Idempotent Playbooks**: Safe to run multiple times without side effects
- **Production Ready**: Configured for secure HTTPS-only traffic

## Installation

Install the following dependencies on your local machine.

### For Linux (Ubuntu/Debian):

```bash
sudo apt install terraform npm ansible azure-cli python3 -y
```

### For Mac:

```bash
brew install terraform azure-cli node ansible python3
```

### Verify Installations:

```bash
terraform --version
ansible --version
az --version
python3 --version
ssh -V
```

## Usage

### Authentication

Before deploying infrastructure, authenticate with Azure:

```bash
az login
```

### Build Infra

#### 1. Clone The Project

```bash
git clone https://github.com/nickvourd/DropperDragon.git
cd DropperDragon
```

#### 2. Deploy Azure VM (Team Server)

```bash
python3 scripts-pack/setup.py \
  -l <azure_location> \
  -u <vm_username> \
  -n <resource_prefix> \
  -s <path_to_ssh_key> \
  -d <dns_prefix> \
  -v <vm_size>
```

**Example:**
```bash
python3 scripts-pack/setup.py \
  -l westus2 \
  -u azureuser \
  -n myapp \
  -s ~/.ssh/id_rsa \
  -d myapp-dns \
  -v standard_b2s
```

**Available Azure Locations:**
```
eastus, eastus2, westus, westus2, westus3, northeurope, 
westeurope, southeastasia, eastasia, australiaeast, 
australiasoutheast, japaneast, japanwest
```

**Available VM Sizes:**
```
standard_b1ms, standard_b2s, standard_b2ms
```

#### 3. Configure Azure VM with Ansible

After Terraform completes (2-3 minutes), configure the VM:

```bash
python3 scripts-pack/deploy.py --ssh-key <path_to_ssh_key>
```

**Example:**
```bash
python3 scripts-pack/deploy.py --ssh-key ~/.ssh/id_rsa
```

#### 4. Access Your Service

Once deployment completes, access your service via HTTPS:

```
https://<fqdn_from_setup_output>
```

The FQDN will be displayed in the `setup.py` output.

## Workflow

```
┌─────────────────────────────────────────────────────────┐
│  1. setup.py - Create Azure Infrastructure              │
│     ├─ Validates Azure CLI authentication               │
│     ├─ Creates terraform.tfvars with parameters         │
│     ├─ Provisions Azure VM and network resources        │
│     └─ Outputs: public_ip, fqdn, username               │
└─────────────────────────────────────────────────────────┘
                          ⬇
┌─────────────────────────────────────────────────────────┐
│  2. deploy.py - Configure VM with Ansible               │
│     ├─ Retrieves Terraform outputs                      │
│     ├─ Creates dynamic Ansible inventory                │
│     ├─ Tests SSH connectivity                           │
│     └─ Executes site.yml playbook                       │
└─────────────────────────────────────────────────────────┘
                          ⬇
┌─────────────────────────────────────────────────────────┐
│  3. site.yml - Ansible Playbook Tasks                   │
│     ├─ System updates (apt update, upgrade, etc)        │
│     ├─ Install nginx web server                         │
│     ├─ Install certbot for SSL management               │
│     ├─ Generate Let's Encrypt certificates              │
│     ├─ Deploy nginx configuration (HTTP→HTTPS)          │
│     ├─ Enable and restart services                      │
│     └─ Install additional utilities                     │
└─────────────────────────────────────────────────────────┘
                          ⬇
            ✅ Production-Ready Server
```

## Directory Structure

```
DropperDragon/
├── scripts-pack/
│   ├── setup.py              # Azure VM provisioning (Terraform)
│   ├── deploy.py             # Ansible orchestration
│   ├── README.md             # This file
│   └── __init__.py
│
├── Terraform-Pack/
│   ├── main.tf               # Main Terraform configuration
│   ├── outputs.tf            # Terraform outputs
│   ├── variables.tf          # Terraform variables
│   ├── terraform.tfvars      # Generated by setup.py
│   └── terraform.tfstate     # State file
│
├── Ansible-Pack/
│   ├── site.yml              # Main playbook with all tasks
│   ├── nginx_default.j2      # Nginx config template
│   └── inventory.ini         # Generated dynamically by deploy.py
│
└── docs/
    └── superpowers/
        └── plans/            # Implementation plans
```

## Playbook Tasks

The `site.yml` Ansible playbook performs the following tasks:

1. **System Updates**
   - Update apt package cache
   - Upgrade all installed packages (dist-upgrade)
   - Remove unnecessary packages (autoremove)

2. **Web Server Setup**
   - Install nginx
   - Enable nginx systemd service

3. **SSL Certificate Management**
   - Install snapd package manager
   - Install certbot via snap (classic mode)
   - Generate Let's Encrypt certificates for FQDN
   - Deploy nginx SSL configuration

4. **Utilities**
   - Install magic-wormhole for file transfer

5. **Service Management**
   - Restart nginx to apply configuration changes

## Troubleshooting

### SSH Connection Failed
- Verify the SSH key path is correct
- Ensure the private key has correct permissions: `chmod 600 ~/.ssh/id_rsa`
- Check that the VM is fully initialized (wait 2-3 minutes after Terraform completes)

### Ansible Playbook Fails
- Verify SSH connectivity manually: `ssh -i <key> <user>@<ip>`
- Check that Ansible is installed: `ansible --version`
- Review the inventory file in `Ansible-Pack/inventory.ini`

### Certbot Certificate Generation Fails
- Ensure FQDN is properly registered in DNS
- Check certbot logs: `sudo certbot certificates`
- Verify nginx is running: `sudo systemctl status nginx`

### Terraform Apply Fails
- Verify Azure CLI authentication: `az account show`
- Check Terraform files in `Terraform-Pack/`
- Ensure resource group name is unique in your subscription

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Created with ❤️ by the DropperDragon Contributors**
