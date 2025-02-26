#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
module: azure_stateful_node
version_added: 1.1.0
short_description: Create, update or delete Spot Azure Stateful Nodes
author: Spot by NetApp (@anuragsharma-123)
description: >
    Create, update, delete or perform actions (pause, resume, recyce) on Spot Azure Stateful Nodes.
    You will have to have a credentials file in this location - <home>/.spotinst/credentials
    The credentials file must contain a row that looks like this
    token = <YOUR TOKEN>
    Full documentation available at [our docs site](https://docs.spot.io/)
extends_documentation_fragment:
  - spot.cloud_modules.requirements
options:
    token:
        type: str
        description:
            - "Optional parameter that allows to set an token inside the module configuration. By default this is retrieved from the credentials path"
    credentials_path:
        type: str
        default: "/root/.spotinst/credentials"
        description: "Optional parameter that allows to set a non-default credentials path."
    state:
        type: str
        choices:
            - present
            - absent
        default: present
        description: "create update or delete"
    account_id:
        type: str
        description:
            - "Optional parameter that allows to set an account-id inside the module configuration. By default this is retrieved from the credentials path"
    id:
        type: str
        description:
            - "The Stateful Node ID if it already exists and you want to update or delete it."
            - "This will have no effect unless the `uniqueness_by` field is set to ID."
            - "When this is set, and the `uniqueness_by` field is set, the node will either be updated or deleted, but not created."
    uniqueness_by:
        type: str
        choices:
            - id
            - name
        description:
            - "If your Stateful Node names are not unique, you may use this feature to update or delete a specific node."
            - "Whenever this property is set, you must set a an `id` in order to update or delete a node, otherwise a node will be created."
    do_not_update:
        type: list
        elements: str
        description:
            - "A list of dotted paths to attributes that you don't wish to update during an update operation."
            - "Example: Specifying `compute.product` will make sure that this attribute is never updated."
    action:
        type: str
        choices:
            - pause
            - resume
            - recycle
        description:
            - Perform the desired action on the azure stateful node. This has no effect on delete operations.
    stateful_node_config:
        type: dict
        description: "Various configurations related to the stateful node"
        suboptions:
            deletion_config:
                type: dict
                description: "Configurations related to the deletion of the stateful node"
                suboptions:
                    deallocation_config:
                        type: dict
                        description: "Deletion configuration for each stateful node's resources"
                        suboptions:
                            disk_deallocation_config:
                                type: dict
                                description: "Disk Deallocation Configuration."
                                suboptions:
                                    should_deallocate:
                                        type: bool
                                        description: "Indicates whether to delete the stateful node's disk resources."
                                    ttl_in_hours:
                                        type: int
                                        description: "Hours to keep the resource alive before deletion. Default: 96"
                            network_deallocation_config:
                                type: dict
                                description: "Network Deallocation Configuration."
                                suboptions:
                                    should_deallocate:
                                        type: bool
                                        description: "Indicates whether to delete the stateful node's network resources."
                                    ttl_in_hours:
                                        type: int
                                        description: "Hours to keep the resource alive before deletion. Default: 96"
                            public_ip_deallocation_config:
                                type: dict
                                description: "Public IP Deallocation Configuration."
                                suboptions:
                                    should_deallocate:
                                        type: bool
                                        description: "Indicates whether to delete the stateful node's public ip resources."
                                    ttl_in_hours:
                                        type: int
                                        description: "Hours to keep the resource alive before deletion. Default: 96"
                            snapshot_deallocation_config:
                                type: dict
                                description:
                                    - Snapshot Deallocation Configuration.
                                suboptions:
                                    should_deallocate:
                                        type: bool
                                        description: "Indicates whether to delete the stateful node's snapshot resources."
                                    ttl_in_hours:
                                        type: int
                                        description: "Hours to keep the resource alive before deletion. Default: 96"
                            should_terminate_vm:
                                type: bool
                                description: "Indicates whether to delete the stateful node's VM."
    stateful_node:
        type: dict
        description: "Describe the desired properties of the stateful node under this object."
        suboptions:
            name:
                type: str
                description: "The stateful node's name."
                required: true
            region:
                type: str
                description: "The Azure region in which the Stateful Node will be launched."
                required: true
            resource_group_name:
                type: str
                description: "The Azure resource group in which the VM and all of the subsequent subresources will be launched."
                required: true
            description:
                type: str
                description: "optional description for the stateful node."
            persistence:
                type: dict
                description: Defines the persistence of the Stateful Node.
                suboptions:
                    data_disks_persistence_mode:
                        type: str
                        description: "Defines the persistency handling for data disks. valid values: `reattach`, `onLaunch`"
                    os_disk_persistence_mode:
                        type: str
                        description: "Defines the persistency handling for os disk. valid values: `reattach`, `onLaunch`"
                    should_persist_data_disks:
                        type: bool
                        description: "Enables the data disks persistency."
                    should_persist_network:
                        type: bool
                        description: "Enables the network persistency."
                    should_persist_os_disk:
                        type: bool
                        description: "Enables the OS disk persistency."
            health:
                type: dict
                description: "Set health check and auto-healing of unhealthy VMs."
                suboptions:
                    health_check_types:
                        type: list
                        elements: str
                        description: "Health check types to use in order to validate VM health."
                    auto_healing:
                        type: bool
                        description: "Auto healing replaces the instance automatically in case the health check fails"
                    grace_period:
                        type: int
                        description: "The amount of time (in seconds) after a new VM has launched before terminating the old VM."
                    unhealthy_duration:
                        type: int
                        description: "Amount of time (in seconds) for the VM to remain unhealthy before a replacement is triggered."
            scheduling:
                type: dict
                description: "Scheduling settings for stateful node"
                suboptions:
                    tasks:
                        type: list
                        elements: dict
                        description: "Scheduled tasks to excute for the stateful node"
                        suboptions:
                            type:
                                type: str
                                description: "The type of scheduled task. valid values: `pause`, `resume`, `recycle`"
                            cron_expression:
                                type: str
                                description: "A valid cron expression that describes the scheduled task (UTC)."
                            is_enabled:
                                type: bool
                                description: "Describes whether the task is enabled. When true the task should run when false it should not run."
            strategy:
                type: dict
                description: "The strategy to launch the underlying VM and Spot behavior for the Stateful Node."
                suboptions:
                    draining_timeout:
                        type: int
                        description: "The time in seconds to allow the node be drained from incoming TCP connections and detached from LB before
                          terminating it. Default: 120."
                    fallback_to_od:
                        type: bool
                        description: "In case of no spots available, stateful node will launch an On-demand instance instead"
                    od_windows:
                        type: list
                        elements: str
                        description: "Define the time windows in which the underlying VM will be set as an on-demand lifecycle type."
                    optimization_windows:
                        type: list
                        elements: str
                        description: "When performAt is `timeWindow`: must specify a list of `timeWindows` with at least one time window Each string
                          is in theformat of - `ddd:hh:mm-ddd:hh:mm ddd` = day of week = Sun | Mon | Tue | Wed | Thu | Fri | Sat hh = hour 24 = 0 - 23
                            mm = minute = 0 - 59"
                    preferred_lifecycle:
                        type: str
                        description: "The preferred lifecycle to launch VM, valid values: `spot`, `od`. Default: `spot`"
                    revert_to_spot:
                        type: dict
                        description: "Hold settings for strategy correction - replacing On-Demand for Spot VMs."
                        suboptions:
                            perform_at:
                                type: str
                                description: "Valid values: `always`, `never`, `timeWindow`. Default: `always`"
                    signals:
                        type: list
                        elements: dict
                        description: Signals that VMs are expected to send to the platform.
                        suboptions:
                            timeout:
                                type: int
                                description: "The timeout in seconds to hold the vm until a signal is sent. Default: 1800"
                            type:
                                type: str
                                description: "The defined type of signal. Valid values: `vmReady`, `vmReadyToShutdown`"
            compute:
                type: dict
                description: "Defines the computational parameters to use when launch the VM for the Stateful Node."
                suboptions:
                    os:
                        type: str
                        description: "Defines the type of the operating system. Valid Values: `Linux`, `Windows`"
                    zones:
                        type: list
                        elements: str
                        description: "List of Azure Availability Zones in the defined region. Valid Values: `1`, `2`, `3`"
                    preferred_zone:
                        type: str
                        description: "The AZ to prioritize when launching VMs. Valid Values: `1`, `2`, `3`"
                    vm_sizes:
                        type: dict
                        description: "Defines the VM sizes to use when launching VMs."
                        suboptions:
                            od_sizes:
                                type: list
                                elements: str
                                description: "Defines the on-demand sizes to use when launching VMs."
                            spot_sizes:
                                type: list
                                elements: str
                                description: "Defines the spot-VM sizes to use when launching VMs."
                            preferred_spot_sizes:
                                type: list
                                elements: str
                                description: "Prioritize Spot VM sizes when launching Spot VMs."
                    launch_specification:
                        type: dict
                        description: "Defines the launch specification of the VM."
                        suboptions:
                            boot_diagnostics:
                                type: dict
                                description: "Will enable boot diagnostics in Azure when a new VM is launched"
                                suboptions:
                                    is_enabled:
                                        type: bool
                                        description: "Allows you to enable and disable the configuration of boot diagnostics at launch"
                                    storage_uri:
                                        type: str
                                        description: "The storage URI that is used if a type is unmanaged."
                                    type:
                                        type: str
                                        description: "Defines the storage type on VM launch in Azure. Valid Values: `managed`, `unmanaged`"
                            custom_data:
                                type: str
                                description: "Defines the custom data (YAML encoded at Base64) that will be executed upon VM launch."
                            data_disks:
                                type: list
                                elements: dict
                                description: "The definitions of data disks that will be created and attached to the stateful node's VM."
                                suboptions:
                                    lun:
                                        type: int
                                        description: "The LUN of the data disk."
                                    size_g_b:
                                        type: int
                                        description: "The size of the data disk in GB, required if dataDisks is specified."
                                    type:
                                        type: str
                                        description: "Type of data disk. Valid Values: `Standard_LRS`, `Premium_LRS`, `StandardSSD_LRS`, `UltraSSD_LRS`"
                            extensions:
                                type: list
                                elements: dict
                                description: "A list of objects for Azure extensions."
                                suboptions:
                                    api_version:
                                        type: str
                                        description: "The API version of the extension. Required if extension specified."
                                    minor_version_auto_upgrade:
                                        type: bool
                                        description: "Required on compute.launchSpecification.extensions object"
                                    name:
                                        type: str
                                        description: "Required on compute.launchSpecification.extensions object"
                                    publisher:
                                        type: str
                                        description: "Required on compute.launchSpecification.extensions object"
                                    type:
                                        type: str
                                        description: "Required on compute.launchSpecification.extensions object"
                            image:
                                type: dict
                                description: "Defines the image with which the VM will be launched."
                                suboptions:
                                    custom:
                                        type: dict
                                        description: "Custom image definitions."
                                        suboptions:
                                            name:
                                                type: str
                                                description: "The name of the custom image."
                                            resource_group_name:
                                                type: str
                                                description: "The resource group name for custom image."
                                    gallery:
                                        type: dict
                                        description: "Gallery image definitions."
                                        suboptions:
                                            gallery_name:
                                                type: str
                                                description: "Name of the gallery."
                                            image_name:
                                                type: str
                                                description: "Name of the gallery image."
                                            resource_group_name:
                                                type: str
                                                description: "The resource group name for gallery image."
                                            spot_account_id:
                                                type: str
                                                description: "The Spot account ID that connected to the Azure subscription to which the gallery belongs."
                                            version_name:
                                                type: str
                                                description: "Image's version. Can be in the format x.x.x or 'latest'."
                                    marketplace:
                                        type: dict
                                        description: "Select an image from Azure's Marketplace image catalogue."
                                        suboptions:
                                            offer:
                                                type: str
                                                description: "Image offer."
                                            publisher:
                                                type: str
                                                description: "Image publisher."
                                            sku:
                                                type: str
                                                description: "Image Stock Keeping Unit, which is the specific version of the image."
                                            version:
                                                type: str
                                                description: "Image Version. Default: `latest`"
                            license_type:
                                type: str
                                description:
                                    - "Specify an existing Azure license type to use when launching new VMs."
                                    - "Valid values for Windows OS: `Windows_Server`, `Windows_Client`"
                                    - "Valid values for Linux OS: `RHEL_BYOS`, `SLES_BYOS`"
                            load_balancers_config:
                                type: dict
                                description: "Configure a Load Balancer."
                                suboptions:
                                    load_balancers:
                                        type: list
                                        elements: dict
                                        description: "Add a load balancer. For Azure Gateway, each Backend Pool is a separate load balancer."
                                        suboptions:
                                            backend_pool_names:
                                                type: list
                                                elements: str
                                                description: "Name of the Backend Pool to register the Stateful Node VMs to."
                                            load_balancer_sku:
                                                type: str
                                                description:
                                                    - "if type is LoadBalancer then Valid Values are: `Standard`, `Basic`"
                                                    - "if ApplicationGateway then Valid Values are: `Standard_Large`, `Standard_Medium`, `Standard_Small`,
                                                      `Standard_v2`, `WAF_v2`, `WAF_Large`, `WAF_Medium`"
                                            name:
                                                type: str
                                                description: "Name of the Application Gateway/Load Balancer"
                                            resource_group_name:
                                                type: str
                                                description: "The Resource Group name of the Load Balancer."
                                            type:
                                                type: str
                                                description: "The type of load balancer. Valid Values: `loadBalancer`, `applicationGateway`"
                            login:
                                type: dict
                                description: "Specify the authentication details to be used for launching VMs."
                                suboptions:
                                    password:
                                        type: str
                                        description: "Defines the password for admin access to Windows VMs."
                                    ssh_public_key:
                                        type: str
                                        description: "Defines the SSH public key for admin access to Linux VMs."
                                    user_name:
                                        type: str
                                        description: "Defines the admin user name for launching VMs."
                            managed_service_identities:
                                type: list
                                elements: dict
                                description: "Defines a user-assigned managed identity to the launched VMs."
                                suboptions:
                                    resource_group_name:
                                        type: str
                                        description: "Defines the resource group of the managed service identities."
                                    name:
                                        type: str
                                        description: "Defines the name of the managed service identities."
                            network:
                                type: dict
                                description: "Defines the network profile with which the VM will be launched."
                                suboptions:
                                    resource_group_name:
                                        type: str
                                        description: "Defines the resource group name of the virtual network with which the VM will be launched."
                                    virtual_network_name:
                                        type: str
                                        description: "Defines the name of the virtual network with which the VM will be launched."
                                    network_interfaces:
                                        type: list
                                        elements: dict
                                        description: "Defines the network interfaces with which the VM will be launched."
                                        suboptions:
                                            additional_ip_configurations:
                                                type: list
                                                elements: dict
                                                description: "Defines a list of extra IPs to be dynamically allocated."
                                                suboptions:
                                                    private_ip_address_version:
                                                        type: str
                                                        description: "Defines the version of the private IP address. Valid Values: `IPv4`, `IPv6`"
                                                    name:
                                                        type: str
                                                        description: "The name of the additional Ip Configuration."
                                            application_security_groups:
                                                type: list
                                                elements: dict
                                                description:
                                                    - Defines the Application Security Groups that will be associated to the primary IP configration
                                                      of the network interface.
                                                suboptions:
                                                    resource_group_name:
                                                        type: str
                                                        description: "Specify the resource group of the Application Security Group."
                                                    name:
                                                        type: str
                                                        description: "Specify the name of the Application Security Group."
                                            assign_public_ip:
                                                type: bool
                                                description: "Defines if a Public IP should be assigned in this network interface."
                                            enable_ip_forwarding:
                                                type: bool
                                                description: "Enables IP forwarding on the network interface."
                                            is_primary:
                                                type: bool
                                                description: "Defines whether the network interface is primary or not."
                                            network_security_group:
                                                type: dict
                                                description: "Defines the network security group to which the network interface will be assigned."
                                                suboptions:
                                                    resource_group_name:
                                                        type: str
                                                        description: "Specify the resource group of the network security group."
                                                    name:
                                                        type: str
                                                        description: "Specify the name of the network security group to use in this network interface."
                                            private_ip_addresses:
                                                type: list
                                                elements: str
                                                description: "Specify the private IP pool in which the VMs will be launched."
                                            public_ips:
                                                type: list
                                                elements: dict
                                                description: "Specify the public IP pool in which the VMs will be launched."
                                                suboptions:
                                                    resource_group_name:
                                                        type: str
                                                        description: "Specify the resource group of the public IP."
                                                    name:
                                                        type: str
                                                        description: "Specify the name of the public IP to which the VMs will be assigned."
                                            public_ip_sku:
                                                type: str
                                                description: "Defines the type of public IP to assign the VM. Valid Values: `Standard`, `Basic`"
                                            subnet_name:
                                                type: str
                                                description: "Defines the subnet to which the network interface will be connected."
                            os_disk:
                                type: dict
                                description: "Specify OS disk specification other than default."
                                suboptions:
                                    size_g_b:
                                        type: int
                                        description: "The size of the OS disk in GB."
                                    type:
                                        type: str
                                        description: "Type of OS disk. Valid Values: `Standard_LRS`, `Premium_LRS`, `StandardSSD_LRS`"
                            secrets:
                                type: list
                                elements: dict
                                description: "Set of certificates that should be installed on the VM"
                                suboptions:
                                    source_vault:
                                        type: dict
                                        description: "The key vault reference, contains the required certificates"
                                        suboptions:
                                            name:
                                                type: str
                                                description: "The name of the key vault"
                                            resource_group_name:
                                                type: str
                                                description: "The resource group name of the key vault"
                                    vault_certificates:
                                        type: list
                                        elements: dict
                                        description: "The required certificate references"
                                        suboptions:
                                            certificate_store:
                                                type: str
                                                description: "The certificate store directory the VM."
                                            certificate_url:
                                                type: str
                                                description: "The URL of the certificate under the key vault"
                            shutdown_script:
                                type: str
                                description: "Defines the shutdown script (encoded at Base64) to execute once the VM is detached."
                            tags:
                                description: "Defines the tags (unique key-value pairs) to tag your resources."
                                type: list
                                elements: dict
                                suboptions:
                                    tag_key:
                                        type: str
                                        description: "Tag key for all resources."
                                    tag_value:
                                        type: str
                                        description: "Tag value for all resources."
                            vm_name:
                                type: str
                                description: "Set a VM name that will be persisted throughout the entire node lifecycle."
                            vm_name_prefix:
                                type: str
                                description: "Set a VM name prefix to be used for all launched VMs and the VM resources."
"""

EXAMPLES = """
# Basic Example
- hosts: localhost
  tasks:
    - name: stateful_node
      spot.cloud_modules.azure_stateful_node:
        state: present
        uniqueness_by: "id"
        do_not_update:
          - region
          - resource_group_name
        stateful_node:
          name: "ansible-stateful-node-example"
          description: "a sample Stateful Node created via Ansible"
          region: "eastus"
          resource_group_name: "AutomationResourceGroup"
          persistence:
            data_disks_persistence_mode: "reattach"
            os_disk_persistence_mode: "reattach"
            should_persist_data_disks: true
            should_persist_network: true
            should_persist_os_disk: true
          health:
            health_check_types: ["vmState"]
            auto_healing: true
            grace_period: 300
            unhealthy_duration: 120
          strategy:
            draining_timeout: 300
            fallback_to_od: true
            preferred_lifecycle: "spot"
            revert_to_spot:
              perform_at: "always"
          compute:
            os: "Linux"
            zones: ["1", "2"]
            preferred_zone: "2"
            vm_sizes:
              od_sizes: ["standard_a1_v2", "standard_a2_v2"]
              spot_sizes: ["standard_a1_v2", "standard_a2_v2"]
              preferred_spot_sizes: ["standard_a1_v2"]
            launch_specification:
              data_disks:
                - lun: 0
                  size_g_b: 30
                  type: "Standard_LRS"
              image:
                marketplace:
                  publisher: "Canonical"
                  version: "latest"
                  sku: "18.04-LTS"
                  offer: "UbuntuServer"
              login:
                user_name: "ubuntu"
                ssh_public_key: <add-your-ssh-key-here>
              network:
                resource_group_name: "AutomationResourceGroup"
                virtual_network_name: "Automation-VirtualNetwork"
                network_interfaces:
                  - is_primary: true
                    assign_public_ip: true
                    public_ip_sku: "Standard"
                    subnet_name: "Automation-PrivateSubnet"
                    enable_ip_forwarding: true
              os_disk:
                size_g_b: 30
                type: "Standard_LRS"
              tags:
                - tag_key: "Creator"
                  tag_value: "Ansible Test"
                - tag_key: "Name"
                  tag_value: "Ansible Basic Example"
      register: result
    - debug: var=result
"""

RETURN = """
---
stateful_node_id:
    description: The ID of the stateful node that was just created/update/deleted.
    returned: success
    type: str
    sample: ssn-792f7f87
"""

HAS_SPOTINST_SDK = False


from ansible.module_utils.basic import env_fallback
from ansible_collections.spot.cloud_modules.plugins.module_utils.spot_ansible_module import SpotAnsibleModule
import copy

try:
    import spotinst_sdk2 as spotinst
    from spotinst_sdk2.client import SpotinstClientException

    HAS_SPOTINST_SDK = True

except ImportError as e:
    pass


CLS_NAME_BY_ATTR_NAME = {
    "stateful_node.compute.launch_specification.load_balancers_config": "LoadBalancerConfig",
    "stateful_node.compute.launch_specification.managed_service_identities": "ManagedServiceIdentity",
    "stateful_node.compute.launch_specification.extension": "Extension",
    "stateful_node.compute.launch_specification.network.network_interfaces": "NetworkInterface",
    "stateful_node.compute.launch_specification.data_disks": "DataDisk",
    "stateful_node.compute.launch_specification.extensions": "Extension",
    "stateful_node.compute.launch_specification.secrets": "Secret",
    "stateful_node.compute.launch_specification.tags": "Tag",
    "stateful_node.strategy.signals": "Signal",
    "stateful_node.scheduling.tasks": "SchedulingTask"
}

LIST_MEMBER_CLS_NAME_BY_ATTR_NAME = {
    "stateful_node.compute.launch_specification.load_balancers_config.load_balancers": "LoadBalancer",
    "stateful_node.compute.launch_specification.network.network_interfaces.application_security_groups": "ApplicationSecurityGroup",
    "stateful_node.compute.launch_specification.network.network_interfaces.additional_ip_configurations": "AdditionalIpConfiguration",
    "stateful_node.compute.launch_specification.secrets.vault_certificates": "VaultCertificate"
}


def to_snake_case(camel_str):
    import re
    ret_val = re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()

    return ret_val


def to_pascal_case(snake_str):
    return "".join(word.title() for word in snake_str.split("_"))


def is_primitive(some_obj):
    return any(isinstance(some_obj, x) for x in [bool, float, int, str])


def find_in_overrides(curr_path):
    return CLS_NAME_BY_ATTR_NAME.get(curr_path, None) or LIST_MEMBER_CLS_NAME_BY_ATTR_NAME.get(curr_path, None)


def get_client(module):
    creds_file_loaded_vars = dict()

    credentials_path = module.custom_params.get("credentials_path")

    if credentials_path is not None:
        try:
            with open(credentials_path, "r") as creds:
                for line in creds:
                    eq_index = line.find(":")
                    var_name = line[:eq_index].strip()
                    string_value = line[eq_index + 1:].strip()
                    creds_file_loaded_vars[var_name] = string_value
        except IOError:
            pass
    # End of creds file retrieval

    token = module.custom_params.get("token")
    if not token:
        token = creds_file_loaded_vars.get("token")

    account = module.custom_params.get("account_id")

    if not account:
        account = creds_file_loaded_vars.get("account")

    if account is not None:
        session = spotinst.SpotinstSession(auth_token=token, account_id=account)
    else:
        session = spotinst.SpotinstSession(auth_token=token)

    client = session.client("stateful_node_azure")

    return client


def turn_to_model(content, field_name: str, curr_path=None):
    if content is None:
        return None
    elif is_primitive(content):
        return content
    elif isinstance(content, list):
        new_l = []

        for item in content:
            value = turn_to_model(item, field_name, curr_path)
            new_l.append(value)

        return new_l

    elif isinstance(content, dict):
        if curr_path is not None:
            curr_path += "." + field_name
        else:
            curr_path = field_name

        override = find_in_overrides(curr_path)
        key_to_use = override if override else to_pascal_case(field_name)

        class_ = getattr(spotinst.models.stateful_node, key_to_use)
        instance = class_()

        for key, value in content.items():
            new_value = turn_to_model(value, key, curr_path)
            setattr(instance, key, new_value)

        return instance


def find_ssn_with_same_name(stateful_nodes, name):
    ret_val = []
    for node in stateful_nodes:
        if node["name"] == name:
            ret_val.append(node)

    return ret_val


def clean_do_not_update_fields(
        stateful_node_module_copy: dict, do_not_update_list: list
):
    ret_val = stateful_node_module_copy

    # avoid deleting parent dicts before children
    do_not_update_list = sorted(do_not_update_list, key=len, reverse=True)

    for dotted_path in do_not_update_list:
        curr_dict = stateful_node_module_copy
        path_as_list = dotted_path.split(".")
        last_part_of_path = path_as_list[-1]

        for path_part in path_as_list[:-1]:
            new_dict = curr_dict.get(path_part)
            curr_dict = new_dict

        if curr_dict.get(last_part_of_path) is not None:
            del curr_dict[last_part_of_path]

    return ret_val


def get_id_and_operation(client, state: str, module):
    operation, id = None, None
    uniqueness_by = module.custom_params.get("uniqueness_by")
    manually_provided_ssn_id = module.custom_params.get("id")
    stateful_node = module.custom_params.get("stateful_node")

    if state == "present":

        if uniqueness_by == "id":
            if manually_provided_ssn_id is None:
                operation = "create"
            else:
                id = manually_provided_ssn_id
                operation = "update"
        else:
            all_stateful_nodes = client.get_all_stateful_nodes()
            name = stateful_node["name"]
            nodes_with_name = find_ssn_with_same_name(all_stateful_nodes, name)

            if len(nodes_with_name) == 0:
                operation = "create"
            elif len(nodes_with_name) == 1:
                id = nodes_with_name[0]["id"]
                operation = "update"
            else:
                msg = f"Failed updating stateful node - 'uniqueness_by' is set to 'name' but there's more than one stateful node with the name '{name}'"
                module.fail_json(changed=False, msg=msg)

    elif state == "absent":
        operation = "delete"

        if uniqueness_by == "id":
            if manually_provided_ssn_id is not None:
                id = module.custom_params.get("id")
            else:
                msg = "Failed deleting stateful node - 'uniqueness_by' is set to `id` but parameter 'id' was not provided"
                module.fail_json(changed=False, msg=msg)
        else:
            all_stateful_nodes = client.get_all_stateful_nodes()
            name = stateful_node["name"]
            nodes_with_name = find_ssn_with_same_name(all_stateful_nodes, name)

            if len(nodes_with_name) == 1:
                id = nodes_with_name[0]["id"]
            elif len(nodes_with_name) > 1:
                msg = f"Failed deleting stateful node - 'uniqueness_by' is set to 'name' but there's more than one stateful node with the name '{name}'"
                module.fail_json(changed=False, msg=msg)
            elif len(nodes_with_name) == 0:
                msg = f"Failed deleting stateful node - 'uniqueness_by' is set to 'name' but there is no stateful node with the name '{name}'"
                module.fail_json(changed=False, msg=msg)

    else:
        msg = f"Spot Ansible Module error: got unknown state {state}"
        module.fail_json(changed=False, msg=msg)
    return operation, id


def handle_stateful_node(client, module):
    ssn_models = spotinst.models.stateful_node
    stateful_node_module_copy = copy.deepcopy(module.custom_params.get("stateful_node"))
    state = module.custom_params.get("state")

    operation, ssn_id = get_id_and_operation(client, state, module)

    if operation == "create":
        has_changed, stateful_node_id, message = handle_create_stateful_node(client, stateful_node_module_copy)
    elif operation == "update":
        has_changed, stateful_node_id, message = handle_update_stateful_node(client, stateful_node_module_copy, ssn_id, module)
    elif operation == "delete":
        has_changed, stateful_node_id, message = handle_delete_stateful_node(client, ssn_id, ssn_models, module)
    else:
        module.fail_json(changed=False, msg=f"Unknown operation {operation} - "
                                            f"this is probably a bug in the module's code: please report")
        return None, None, None  # for IDE - fail_json stops execution

    return stateful_node_id, message, has_changed


def handle_delete_stateful_node(client, ssn_id, ssn_models, module):
    stateful_node_id = ssn_id
    delete_args = dict(node_id=stateful_node_id)

    handle_deletion_config(delete_args, ssn_models, module)

    try:
        client.delete_stateful_node(**delete_args)
        message = f"Stateful node {stateful_node_id} deleted successfully"
        has_changed = True
    except SpotinstClientException as exc:
        if "STATEFUL_NODE_DOES_NOT_EXIST" in exc.message:
            message = f"Failed deleting stateful node - Stateful Node with ID {stateful_node_id} doesn't exist"
            module.fail_json(changed=False, msg=message)
        else:
            message = f"Failed deleting stateful node (ID: {stateful_node_id}), error: {exc.message}"
            module.fail_json(msg=message)
        has_changed = False

    return has_changed, stateful_node_id, message


def handle_update_stateful_node(client, stateful_node_module_copy, ssn_id, module):
    stateful_node_module_copy = clean_do_not_update_fields(
        stateful_node_module_copy,
        module.custom_params.get("do_not_update")
    )
    ami_sdk_object = turn_to_model(stateful_node_module_copy, "stateful_node")

    try:
        res: dict = client.update_stateful_node(node_id=ssn_id, node_update=ami_sdk_object)
        stateful_node_id = res["id"]
        message = "Stateful node updated successfully"
        has_changed = True

        action_type = module.custom_params.get("action", None)
        should_perform_action = action_type is not None

        if should_perform_action:
            message = attempt_stateful_action(
                action_type, client, stateful_node_id, message
            )

    except SpotinstClientException as exc:
        if "STATEFUL_NODE_DOES_NOT_EXIST" in exc.message:
            message = f"Failed updating stateful node - stateful node with ID {stateful_node_id} doesn't exist"
            module.fail_json(changed=False, msg=message)
        else:
            message = f"Failed updating stateful node (ID {stateful_node_id}), error: {exc.message}"
            module.fail_json(msg=message)
        has_changed = False

    return has_changed, stateful_node_id, message


def handle_create_stateful_node(client, stateful_node_module_copy):
    ami_sdk_object = turn_to_model(
        stateful_node_module_copy, "stateful_node"
    )

    res: dict = client.create_stateful_node(node=ami_sdk_object)
    stateful_node_id = res["id"]
    message = "Stateful node created successfully"
    has_changed = True
    return has_changed, stateful_node_id, message


def handle_deletion_config(delete_args, ssn_models, module):
    ssn_config = module.custom_params.get("stateful_node_config")

    if ssn_config is not None:
        deletion_config = ssn_config.get("deletion_config")

        if deletion_config is not None:
            deallocation_config = deletion_config.get("deallocation_config")

            if deallocation_config is not None:
                disk_deallocation_config = deallocation_config.get("disk_deallocation_config")
                network_deallocation_config = deallocation_config.get("network_deallocation_config")
                public_ip_deallocation_config = deallocation_config.get("public_ip_deallocation_config")
                snapshot_deallocation_config = deallocation_config.get("snapshot_deallocation_config")
                should_terminate_vm = deallocation_config.get("should_terminate_vm")

                configs = {}
                if disk_deallocation_config is not None:
                    dealloc_sdk_object = turn_to_model(disk_deallocation_config, "deallocate")
                    configs["disk_deallocation_config"] = dealloc_sdk_object

                if network_deallocation_config is not None:
                    dealloc_sdk_object = turn_to_model(network_deallocation_config, "deallocate")
                    configs["network_deallocation_config"] = dealloc_sdk_object

                if public_ip_deallocation_config is not None:
                    dealloc_sdk_object = turn_to_model(public_ip_deallocation_config, "deallocate")
                    configs["public_ip_deallocation_config"] = dealloc_sdk_object

                if snapshot_deallocation_config is not None:
                    dealloc_sdk_object = turn_to_model(snapshot_deallocation_config, "deallocate")
                    configs["snapshot_deallocation_config"] = dealloc_sdk_object

                if should_terminate_vm is not None:
                    configs["should_terminate_vm"] = should_terminate_vm

                delete_args["deallocation_config"] = configs


def attempt_stateful_action(action_type, client, stateful_node_id, message):
    try:
        if action_type == "pause":
            client.update_stateful_node_state(node_id=stateful_node_id, state="pause")
        if action_type == "resume":
            client.update_stateful_node_state(node_id=stateful_node_id, state="resume")
        if action_type == "recycle":
            client.update_stateful_node_state(node_id=stateful_node_id, state="recycle")

        message = message + f" and action '{action_type}' started"
    except SpotinstClientException as exc:
        message = message + f" but action '{action_type}' failed, error: {exc.message}"
    return message


def main():
    persistence_fields = dict(
        data_disks_persistence_mode=dict(type="str"),
        os_disk_persistence_mode=dict(type="str"),
        should_persist_data_disks=dict(type="bool"),
        should_persist_network=dict(type="bool"),
        should_persist_os_disk=dict(type="bool"),
    )

    health_fields = dict(
        health_check_types=dict(type="list", elements="str"),
        auto_healing=dict(type="bool"),
        grace_period=dict(type="int"),
        unhealthy_duration=dict(type="int"),
    )

    task_fields = dict(
        type=dict(type="str"),
        cron_expression=dict(type="str"),
        is_enabled=dict(type="bool"),
    )

    scheduling_fields = dict(
        tasks=dict(type="list", elements="dict", options=task_fields)
    )

    revert_to_spot_fields = dict(perform_at=dict(type="str"))

    signal_fields = dict(
        type=dict(type="str"),
        timeout=dict(type="int"),
    )

    strategy_fields = dict(
        draining_timeout=dict(type="int"),
        fallback_to_od=dict(type="bool"),
        od_windows=dict(type="list", elements="str"),
        optimization_windows=dict(type="list", elements="str"),
        preferred_lifecycle=dict(type="str"),
        revert_to_spot=dict(type="dict", options=revert_to_spot_fields),
        signals=dict(type="list", elements="dict", options=signal_fields),

    )

    boot_diagnostics_fields = dict(
        is_enabled=dict(type="bool"),
        storage_uri=dict(type="str"),
        type=dict(type="str"),
    )

    data_disk_fields = dict(
        lun=dict(type="int"),
        size_g_b=dict(type="int"),
        type=dict(type="str"),
    )

    extension_fields = dict(
        api_version=dict(type="str"),
        minor_version_auto_upgrade=dict(type="bool"),
        name=dict(type="str"),
        publisher=dict(type="str"),
        type=dict(type="str"),
    )

    marketplace_image_fields = dict(
        publisher=dict(type="str"),
        offer=dict(type="str"),
        sku=dict(type="str"),
        version=dict(type="str"),
    )

    gallery_image_fields = dict(
        gallery_name=dict(type="str"),
        image_name=dict(type="str"),
        resource_group_name=dict(type="str"),
        spot_account_id=dict(type="str"),
        version_name=dict(type="str"),
    )

    custom_image_fields = dict(
        resource_group_name=dict(type="str"),
        name=dict(type="str"),
    )

    image_fields = dict(
        marketplace=dict(type="dict", options=marketplace_image_fields),
        custom=dict(type="dict", options=custom_image_fields),
        gallery=dict(type="dict", options=gallery_image_fields),
    )

    load_balancers_fields = dict(
        backend_pool_names=dict(type="list", elements="str"),
        load_balancer_sku=dict(type="str"),
        name=dict(type="str"),
        resource_group_name=dict(type="str"),
        type=dict(type="str"),
    )

    load_balancers_config_fields = dict(
        load_balancers=dict(type="list", elements="dict", options=load_balancers_fields)
    )

    login_fields = dict(
        ssh_public_key=dict(type="str"),
        user_name=dict(type="str"),
        password=dict(type="str"),
    )

    managed_service_identity_fields = dict(
        resource_group_name=dict(type="str"),
        name=dict(type="str"),
    )

    additional_ip_configuration_fields = dict(
        name=dict(type="str"),
        private_ip_address_version=dict(type="str"),
    )

    security_group_fields = dict(
        name=dict(type="str"),
        resource_group_name=dict(type="str"),
    )

    public_ip_fields = dict(
        name=dict(type="str"),
        resource_group_name=dict(type="str"),
    )

    network_interface_fields = dict(
        additional_ip_configurations=dict(type="list", elements="dict", options=additional_ip_configuration_fields),
        application_security_groups=dict(type="list", elements="dict", options=security_group_fields),
        assign_public_ip=dict(type="bool"),
        enable_ip_forwarding=dict(type="bool"),
        is_primary=dict(type="bool"),
        network_security_group=dict(type="dict", options=security_group_fields),
        private_ip_addresses=dict(type="list", elements="str"),
        public_ips=dict(type="list", elements="dict", options=public_ip_fields),
        public_ip_sku=dict(type="str"),
        subnet_name=dict(type="str"),
    )

    network_fields = dict(
        network_interfaces=dict(type="list", elements="dict", options=network_interface_fields),
        virtual_network_name=dict(type="str"),
        resource_group_name=dict(type="str"),
    )

    os_disk_fields = dict(
        size_g_b=dict(type="int"),
        type=dict(type="str"),
    )

    source_vault_fields = dict(
        name=dict(type="str"),
        resource_group_name=dict(type="str"),
    )

    vault_certificate_fields = dict(
        certificate_store=dict(type="str"),
        certificate_url=dict(type="str"),
    )

    secret_fields = dict(
        source_vault=dict(type="dict", options=source_vault_fields),
        vault_certificates=dict(type="list", elements="dict", options=vault_certificate_fields),
    )

    tags_fields = dict(tag_key=dict(type="str"), tag_value=dict(type="str"))

    launch_spec_fields = dict(
        boot_diagnostics=dict(type="dict", options=boot_diagnostics_fields),
        custom_data=dict(type="str"),
        data_disks=dict(type="list", elements="dict", options=data_disk_fields),
        extensions=dict(type="list", elements="dict", options=extension_fields),
        image=dict(type="dict", options=image_fields),
        license_type=dict(type="str"),
        load_balancers_config=dict(type="dict", options=load_balancers_config_fields),
        login=dict(type="dict", options=login_fields),
        managed_service_identities=dict(type="list", elements="dict", options=managed_service_identity_fields),
        network=dict(type="dict", options=network_fields),
        os_disk=dict(type="dict", options=os_disk_fields),
        secrets=dict(type="list", elements="dict", options=secret_fields),
        shutdown_script=dict(type="str"),
        tags=dict(type="list", elements="dict", options=tags_fields),
        vm_name=dict(type="str"),
        vm_name_prefix=dict(type="str"),
    )

    vm_sizes_fields = dict(
        od_sizes=dict(type="list", elements="str"),
        preferred_spot_sizes=dict(type="list", elements="str"),
        spot_sizes=dict(type="list", elements="str"),
    )

    compute_fields = dict(
        launch_specification=dict(type="dict", options=launch_spec_fields),
        os=dict(type="str"),
        preferred_zone=dict(type="str"),
        vm_sizes=dict(type="dict", options=vm_sizes_fields),
        zones=dict(type="list", elements="str"),
    )

    actual_fields = dict(
        name=dict(type="str", required=True),
        region=dict(type="str", required=True),
        resource_group_name=dict(type="str", required=True),
        description=dict(type="str"),
        persistence=dict(type="dict", options=persistence_fields),
        health=dict(type="dict", options=health_fields),
        scheduling=dict(type="dict", options=scheduling_fields),
        strategy=dict(type="dict", options=strategy_fields),
        compute=dict(type="dict", options=compute_fields)
    )

    deallocate_config = dict(
        should_deallocate=dict(type="bool"),
        ttl_in_hours=dict(type="int"),
    )

    deallocation_config_fields = dict(
        disk_deallocation_config=dict(type="dict", options=deallocate_config),
        network_deallocation_config=dict(type="dict", options=deallocate_config),
        public_ip_deallocation_config=dict(type="dict", options=deallocate_config),
        snapshot_deallocation_config=dict(type="dict", options=deallocate_config),
        should_terminate_vm=dict(type="bool"),
    )

    deletion_config_fields = dict(
        deallocation_config=dict(type="dict", options=deallocation_config_fields)
    )

    stateful_node_config_fields = dict(
        deletion_config=dict(type="dict", options=deletion_config_fields)
    )

    fields = dict(
        # region config fields
        token=dict(
            type="str", fallback=(env_fallback, ["SPOTINST_TOKEN"]), no_log=True
        ),
        credentials_path=dict(type="path", default="~/.spotinst/credentials"),
        state=dict(type="str", default="present", choices=["present", "absent"]),
        account_id=dict(
            type="str", fallback=(env_fallback, ["SPOTINST_ACCOUNT_ID", "ACCOUNT"])
        ),
        id=dict(type="str"),
        uniqueness_by=dict(type="str", choices=["id", "name"], default="name"),
        do_not_update=dict(type="list", elements="str"),
        # endregion

        # region stateful node specific config fields
        action=dict(type="str", choices=["pause", "resume", "recycle"]),
        stateful_node_config=dict(type="dict", options=stateful_node_config_fields),
        # endregion

        # region stateful_node
        stateful_node=dict(type="dict", required=True, options=actual_fields)
        # endregion
    )

    module = SpotAnsibleModule(argument_spec=fields)

    if not HAS_SPOTINST_SDK:
        module.fail_json(
            msg="the Spotinst SDK library is required. (pip install spotinst-sdk2)"
        )

    client = get_client(module=module)

    stateful_node_id, message, has_changed = handle_stateful_node(
        client=client, module=module
    )

    module.exit_json(
        changed=has_changed, stateful_node_id=stateful_node_id, message=message
    )


if __name__ == "__main__":
    main()
