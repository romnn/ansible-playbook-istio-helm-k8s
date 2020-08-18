IMAGE_NAME = "ubuntu/bionic64"
NODES = 2
ENV['VAGRANT_DEFAULT_PROVIDER'] = 'virtualbox'

Vagrant.configure("2") do |config|
    config.ssh.insert_key = false

    config.vm.provider "virtualbox" do |v, override|
      override.vm.box = IMAGE_NAME
      # Disable synced folders with virtualbox
      override.vm.synced_folder ".", "/vagrant", disabled: true
      v.memory = 2048
      v.cpus = 2
    end

    config.vm.define "k8s-master" do |master|
      master.vm.network "private_network", ip: "192.168.50.10"
      master.vm.hostname = "k8s-master"
      master.vm.network :forwarded_port, guest: 80, host: 8080
      master.vm.provision "ansible" do |ansible|
          ansible.compatibility_mode = "2.0"
          ansible.playbook = "kubernetes-master.yml"
          ansible.extra_vars = {
              allow_pods_on_master: true,
              network_cidr: "192.168.0.0/16",
              apiserver_advertise_address: "192.168.50.10",
              node_ip: "192.168.50.10",
          }
        end
    end

    (1..(NODES-1)).each do |i|
        config.vm.define "k8s-node-#{i}" do |node|
            node.vm.network "private_network", ip: "192.168.50.#{i + 10}"
            node.vm.hostname = "k8s-node-#{i}"
            node.vm.provision "ansible" do |ansible|
              ansible.compatibility_mode = "2.0"
                ansible.playbook = "kubernetes-node.yml"
                ansible.extra_vars = {
                    node_ip: "192.168.50.#{i + 10}",
                }
            end
        end
    end
end
