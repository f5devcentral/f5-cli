# Usage

## Prerequisites

```bash
pip3 install -r demos/requirements.txt
```

## Run

```bash
export AZURE_SUBSCRIPTION_ID=''; export AZURE_CLIENT_ID=''; AZURE_SECRET=''; AZURE_TENANT=''.
export ADMIN_PWD='<insert password>'
ansible-playbook demos/primary/main.yml -e "admin_password=${ADMIN_PWD}" -e "env_prefix=f5cloudclidemo" -v
```

## Teardown

```bash
ansible-playbook demos/primary/teardown.yml -e "env_prefix=f5cloudclidemo" -v
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

Ignore HTTP(s) warnings (not recommended):

```bash
export PYTHONWARNINGS="ignore:Unverified HTTPS request"
```
