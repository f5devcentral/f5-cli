# Usage

This demo provisions a standalone BIG-IP in Azure and performs system configuration (NTP, DNS, etc.) using Declarative Onboarding.  Once that is done it configures L4-7 application services using AS3.

Note: Includes both ansible and terraform variations.

## Ansible

### Prerequisites

```bash
pip3 install -r demos/ansible/requirements.txt
```

### Run

```bash
export AZURE_SUBSCRIPTION_ID=''; export AZURE_CLIENT_ID=''; AZURE_SECRET=''; AZURE_TENANT=''.
export ADMIN_PWD='<insert password>'
ansible-playbook demos/primary/main.yml -e "admin_password=${ADMIN_PWD}" -e "env_prefix=f5clidemo" -v
```

### Teardown

```bash
ansible-playbook demos/primary/teardown.yml -e "env_prefix=f5clidemo" -v
```

### Notes

Using python virtual env:

```bash
virtualenv ansible-env
source ansible-env/bin/activate
# install prereqs 
export ANSIBLE_PYTHON_INTERPRETER="$(realpath ansible-env)/bin/python"
# add to playbook call: -e "ansible_python_interpreter=${ANSIBLE_PYTHON_INTERPRETER}"
```

## Terraform

### Prerequisites

- Install terraform
- `terraform init`

### Run

```bash
export ADMIN_PWD='<insert password>'
# run terraform plan first - optional
terraform plan -var="env_prefix=f5clidemotf" -var="admin_password=${ADMIN_PWD}"
# apply
terraform apply -var="env_prefix=f5clidemotf" -var="admin_password=${ADMIN_PWD}" -auto-approve
```

### Teardown

```bash
terraform destroy -var="env_prefix=f5clidemotf" -var="admin_password=${ADMIN_PWD}" -auto-approve
```

## Advanced Options

Ignore HTTP(s) warnings (not recommended):

```bash
export PYTHONWARNINGS="ignore:Unverified HTTPS request"
```
