# Usage

## Prerequisites

```bash
pip3 install ansible
pip3 install ansible[azure]
pip3 install f5-cloud-cli
```

## Run

```bash
export AZURE_SUBSCRIPTION_ID=''; export AZURE_CLIENT_ID=''; AZURE_SECRET=''; AZURE_TENANT=''.
export ADMIN_PWD='<insert password>'
ansible-playbook demos/primary/main.yml -e "admin_password=${ADMIN_PWD}" -e "env_prefix=f5cloudclidemo" -v
```

### Advanced Options

Using python virtual env:

```bash
virtualenv ansible-env
source ansible-env/bin/activate
# install prereqs 
export ANSIBLE_PYTHON_INTERPRETER="$(realpath ansible-env)/bin/python"
# add to playbook call: -e "ansible_python_interpreter=${ANSIBLE_PYTHON_INTERPRETER}"
```
