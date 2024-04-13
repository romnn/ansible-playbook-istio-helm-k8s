This is an ansible playbook to provision bare metal servers
to create a `kubernetes` cluster.

#### This playbook includes

- [docker](https://www.docker.com/)
- [kubernetes](https://kubernetes.io) (kubeadm, kubelet, kubectl)
- [helm](https://helm.sh/) (with Tiller for Helm 2)
- [istio](https://istio.io/) (disabled by default)

The playbook also takes care of setting up a kubernetes _master_ and
makes the _worker_ machines join the cluster.

#### Try it out

ansible-galaxy collection install ansible.posix
ansible-galaxy collection install community.general
ansible-galaxy collection install kubernetes.core

To try out the playbook, install the following packages (assumes you are running on ubuntu):

- [virtualbox](https://www.virtualbox.org/) by downloading the `.deb` from [the download page](https://www.virtualbox.org/wiki/Linux_Downloads) and installing it with
  ```bash
  sudo apt install ./Downloads/virtualbox-6.1_6.1.12-139181_Ubuntu_eoan_amd64.deb
  ```
- [ansible](https://www.ansible.com/) with
  ```bash
  pip install ansible
  # Or using apt...
  sudo apt update
  sudo apt install software-properties-common
  sudo apt-add-repository --yes --update ppa:ansible/ansible
  sudo apt install ansible
  ```
- [vagrant](https://www.vagrantup.com/) by downloading the binary from [the download page](https://www.vagrantup.com/downloads) and adding it to the `$PATH`, e.g.
  ```bash
  sudo mv ./Downloads/vagrant /usr/local/bin/
  ```

Vagrant is used to setup a virtualized kubernetes cluster with a master node and any number of workers.

Now start a cluster with

```
cd ansible-playbook-istio-helm-k8s
vagrant up
```

This creates a kubernetes cluster with two nodes (master and worker).
To change the number of workers simply change the `NODES` variable in the `Vagrantfile`.

To `ssh` into one of the nodes run either of

```
vagrant ssh k8s-master
vagrant ssh k8s-node-<node-number>
```

where `<node-number>` is one of 1..<`NODES`.

#### Notice

This playbook is not considered production ready.

## TODO

- remove checksums from downloads in defaults

```bash
$ tree /etc/containerd/certs.d
/etc/containerd/certs.d
└── docker.io
    └── hosts.toml

$ cat /etc/containerd/certs.d/docker.io/hosts.toml
server = "https://docker.io"

[host."https://registry-1.docker.io"]
  capabilities = ["pull", "resolve"]
```
