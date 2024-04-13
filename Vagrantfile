# -*- mode: ruby -*-
# # vi: set ft=ruby :

IMAGE_NAME = "ubuntu/jammy64"
# IMAGE_NAME = "ubuntu/focal64"
# IMAGE_VERSION = "v20240305.0.0"
# IMAGE_NAME = "bento/ubuntu-22.04"
NODES = 1
ENV['VAGRANT_DEFAULT_PROVIDER'] = 'virtualbox'

Vagrant.configure("2") do |config|
    config.vm.provider "virtualbox" do |vbox, override|
      override.vm.box = IMAGE_NAME
      # override.vm.box_version = IMAGE_VERSION

      # Disable synced folders with virtualbox
      override.vm.synced_folder ".", "/vagrant", disabled: true
      vbox.memory = 2048
      vbox.cpus = 4

      # vbox.customize ['modifyvm', :id, '--accelerate3d', 'on']
      # This is commented out until resolution has been found for proper
      # usage. For now it will use the default graphics controller.
      vbox.customize ['modifyvm', :id, '--graphicscontroller', 'vmsvga']
      # vbox.customize ['modifyvm', :id, '--graphicscontroller', 'vboxvga']
      # vbox.customize ['modifyvm', :id, '--hwvirtex', 'on']
      # vbox.customize ['modifyvm', :id, '--ioapic', 'on']
      # vbox.customize ['modifyvm', :id, '--vram', '128']
      vbox.customize ['modifyvm', :id, '--audio', 'none']
    end

    config.vm.define "k8s-master" do |master|
      master.vm.hostname = "k8s-master"
      master.vm.network :private_network, ip: "192.168.56.10", netmask: "255.255.255.0"

      master.vm.provision "ansible" do |ansible|
          ansible.compatibility_mode = "2.0"
          ansible.playbook = "kubernetes-master.yml"
          ansible.groups = {
            "k8s-masters" => ["k8s-master"]
          }
          ansible.extra_vars = {
              allow_pods_on_master: true,
              network_cidr: "192.168.0.0/16",
              apiserver_advertise_address: "192.168.56.10",
              apiserver_cert_extra_sans: "192.168.56.10",
              node_ip: "192.168.56.10",
              hostname: "k8s-master",
          }
        end
    end

    (1..(NODES-1)).each do |i|
        config.vm.define "k8s-node-#{i}" do |node|
            node.vm.hostname = "k8s-node-#{i}"
            node.vm.network :private_network, ip: "192.168.56.#{i + 10}", netmask: "255.255.255.0"
            node.vm.provision "ansible" do |ansible|
              ansible.compatibility_mode = "2.0"
              ansible.playbook = "kubernetes-node.yml"
              ansible.groups = {
                "k8s-nodes" => ["k8s-node-#{i}"]
              }
              ansible.extra_vars = {
                  node_ip: "192.168.56.#{i + 10}",
                  hostname: "k8s-node-#{i}",
              }
            end
        end
    end
end
