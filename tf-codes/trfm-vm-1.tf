provider "azurerm" {
  features {}
}
resource "azurerm_linux_virtual_machine" "example" {
  name                = "myfirstvm"
  resource_group_name = "resource_group_name-replaceme"
  location            = "location-replaceme"
  size                = "2cpu"
  admin_username      = "admin_Username-replaceme"
  network_interface_ids = [
    network_interface_ids-replaceme
  ]
  admin_ssh_key {
    username   = "username-replaceme"
    public_key = "public_key-replaceme"
    }

  os_disk {
    caching              = "caching-replaceme"
    storage_account_type = "storage_account_type-replaceme"
  }

  source_image_reference {
    publisher = "publisher-replaceme"
    offer     = "offer-replaceme"
    sku       = "sku-replaceme"
    version   = "version-relplaceme"
  }

  custom_data = custom_data-replaceme

  # Optional properties
  computer_name                 = "computer_name-replaceme"
  disable_password_authentication = disable_password_authentication-replaceme
  priority                      = "priority-replaceme"
  eviction_policy               = "eviction_policy-replaceme"
  ultra_ssd_enabled             = ultra_ssd_enabled-replaceme
  availability_set_id           = "availability_set_id-replaceme"
  zone                          = "zone-replaceme"

  identity {
    type = "type-replaceme"
  }

  boot_diagnostics {
    storage_account_uri = "storage_account_type-replaceme"
  }

  tags = {
    environment = "environment-replaceme"
    cost_center = "cost_center-replaceme"
  }

  plan {
    name      = "myfirstvm"
    publisher = "publisher-replaceme"
    product   = "product-replaceme"
  }

  extension {
    name                 = "extension-replaceme"
    publisher            = "publisher-replaceme"
    type                 = "type-replaceme"
    type_handler_version = "type_handler_version-replaceme"
    settings             = <<SETTINGS
      {
          "fileUris": ["fileUris-replaceme"],
          "commandToExecute": "commandToExecute-replaceme"
      }
    SETTINGS
  }
}
