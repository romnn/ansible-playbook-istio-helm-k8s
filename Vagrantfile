# -*- mode: ruby -*-
# # vi: set ft=ruby :

IMAGE_NAME = "ubuntu/jammy64"
NODES = 1
ENV['VAGRANT_DEFAULT_PROVIDER'] = 'virtualbox'

Vagrant.configure("2") do |config|
    # config.ssh.username = "vagrant"
    # config.ssh.password = "vagrant"
    config.ssh.insert_key = false
    # config.ssh.private_key_path = "~/.ssh/id_rsa"
    # config.ssh.forward_agent = true

    config.vm.provider "virtualbox" do |v, override|
      override.vm.box = IMAGE_NAME
      # Disable synced folders with virtualbox
      override.vm.synced_folder ".", "/vagrant", disabled: true
      v.memory = 2048
      v.cpus = 2
    end

    config.vm.define "k8s-master" do |master|
      # master.vm.network "private_network", ip: "192.168.56.10"
      # master.vm.network "private_network", ip: "10.0.2.15"
      # master.vm.network :private_network, ip: "192.168.56.10", netmask: "255.255.255.0"
      master.vm.network :private_network, ip: "192.168.56.10", netmask: "255.255.255.0"
      master.vm.network :forwarded_port, guest: 80, host: 8080

      master.vm.hostname = "k8s-master"
      master.vm.provision "ansible" do |ansible|
          ansible.compatibility_mode = "2.0"
          ansible.playbook = "kubernetes-master.yml"
          ansible.groups = {
            "k8s-masters" => ["k8s-master"]
          }
          # apiserver_advertise_address: "192.168.56.10",
          # apiserver_advertise_address: "0.0.0.0",

          ansible.extra_vars = {
              allow_pods_on_master: true,
              network_cidr: "192.168.0.0/16",
              apiserver_advertise_address: "192.168.56.10",
              apiserver_cert_extra_sans: "192.168.56.10",
              node_ip: "192.168.56.10",
          }
        end
    end

    (1..(NODES-1)).each do |i|
        config.vm.define "k8s-node-#{i}" do |node|
            node.vm.network :private_network, ip: "192.168.56.#{i + 10}", netmask: "255.255.255.0"
            # node.vm.network "private_network", ip: "192.168.56.#{i + 10}"
            node.vm.hostname = "k8s-node-#{i}"
            node.vm.provision "ansible" do |ansible|
              ansible.compatibility_mode = "2.0"
                ansible.playbook = "kubernetes-node.yml"
                ansible.groups = {
                  "k8s-nodes" => ["k8s-node-#{i}"]
                }
                ansible.extra_vars = {
                    node_ip: "192.168.56.#{i + 10}",
                }
            end
        end
    end
end
