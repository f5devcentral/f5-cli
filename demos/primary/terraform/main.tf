resource "azurerm_resource_group" "deployment" {
  name     = "${var.env_prefix}"
  location = "${var.location}"
}

resource "azurerm_virtual_network" "deployment" {
  name                = "${var.env_prefix}-network"
  address_space       = ["10.0.0.0/16"]
  location            = "${azurerm_resource_group.deployment.location}"
  resource_group_name = "${azurerm_resource_group.deployment.name}"
}

resource "azurerm_subnet" "deployment" {
  name                 = "default"
  resource_group_name  = "${azurerm_resource_group.deployment.name}"
  virtual_network_name = "${azurerm_virtual_network.deployment.name}"
  address_prefix       = "10.0.0.0/24"
}

resource "azurerm_public_ip" "deployment" {
  name                = "${var.env_prefix}-pip"
  location            = "${azurerm_resource_group.deployment.location}"
  resource_group_name = "${azurerm_resource_group.deployment.name}"
  allocation_method   = "Static"
}

resource "azurerm_network_security_group" "deployment" {
  name                = "${var.env_prefix}-sg"
  location            = "${azurerm_resource_group.deployment.location}"
  resource_group_name = "${azurerm_resource_group.deployment.name}"
  security_rule {
    name                       = "ssh"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
  security_rule {
    name                       = "https"
    priority                   = 120
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "8443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_network_interface" "deployment" {
  name                = "${var.env_prefix}-nic"
  location            = "${azurerm_resource_group.deployment.location}"
  resource_group_name = "${azurerm_resource_group.deployment.name}"
  network_security_group_id     = "${azurerm_network_security_group.deployment.id}"

  ip_configuration {
    name                          = "${var.env_prefix}-nic1"
    subnet_id                     = "${azurerm_subnet.deployment.id}"
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = "${azurerm_public_ip.deployment.id}"
  }
}

resource "azurerm_virtual_machine" "deployment" {
  name                  = "${var.env_prefix}-vm"
  location              = "${azurerm_resource_group.deployment.location}"
  resource_group_name   = "${azurerm_resource_group.deployment.name}"
  network_interface_ids = ["${azurerm_network_interface.deployment.id}"]
  vm_size               = "Standard_DS3_v2"

  # This means the OS Disk will be deleted when Terraform destroys the Virtual Machine
  # NOTE: This may not be optimal in all cases.
  delete_os_disk_on_termination = true

  # This means the Data Disk Disk will be deleted when Terraform destroys the Virtual Machine
  # NOTE: This may not be optimal in all cases.
  delete_data_disks_on_termination = true

  storage_image_reference {
    publisher = "${var.publisher}"
    offer     = "${var.offer}"
    sku       = "${var.sku}"
    version   = "latest"
  }

  plan {
    publisher = "${var.publisher}"
    product   = "${var.offer}"
    name      = "${var.sku}"
  }
  
  storage_os_disk {
    name              = "osdisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  os_profile {
    computer_name  = "hostname"
    admin_username = "${var.admin_username}"
    admin_password = "${var.admin_password}"
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }
}
# add a delay for now, should explore CLI ready check perhaps?
resource "null_resource" "delay_three_minutes" {
  provisioner "local-exec" {
    command = "sleep 180"
  }
  depends_on = ["azurerm_virtual_machine.deployment"]
}

resource "null_resource" "configure_auth" {
  provisioner "local-exec" {
    command = "f5 bigip configure-auth --host ${azurerm_public_ip.deployment.ip_address} --user ${var.admin_username} --password ${var.admin_password}"
  }
  triggers = {
    # prefer fileexists + file here, when available (TF v0.12): https://www.terraform.io/docs/configuration/functions/fileexists.html
    always_run = "${timestamp()}"
  }
  depends_on = ["null_resource.delay_three_minutes"]
}

resource "null_resource" "onboarding" {
  provisioner "local-exec" {
    command = "f5 bigip toolchain service create --install-component --component do --declaration ${path.module}/../declarations/do_decl.json"
  }
  triggers = {
    declaration_hash = "${sha1(file("${path.module}/../declarations/do_decl.json"))}"
  }
  depends_on = ["null_resource.configure_auth"]
}

resource "null_resource" "as3" {
  provisioner "local-exec" {
    command = "f5 bigip toolchain service create --install-component --component as3 --declaration ${path.module}/../declarations/as3_decl.json"
  }
  triggers = {
    declaration_hash = "${sha1(file("${path.module}/../declarations/as3_decl.json"))}"
  }
  depends_on = ["null_resource.configure_auth", "null_resource.onboarding"]
}

output "public_ip_address" {
  value = "${azurerm_public_ip.deployment.ip_address}"
}
