packer {
  required_plugins {
    googlecompute = {
      source  = "github.com/hashicorp/googlecompute"
      version = ">= 1"
    }
  }
}

variable "project_id" {
  type    = string
  default = "dev-siddharth-dash-csye6225"
}

variable "source_image" {
  type    = string
  default = "centos-stream-8-v20240110"
}

variable "zone" {
  type    = string
  default = "us-central1-a"
}

variable "machine_type" {
  type    = string
  default = "n1-standard-1"
}

variable "ssh_username" {
  type    = string
  default = "packer"
}

source "googlecompute" "webapp" {
  project_id    = var.project_id
  source_image  = var.source_image
  zone          = var.zone
  instance_name = "csye6225-${formatdate("YYYYMMDDhhmmss", timestamp())}"
  disk_size     = "100"
  disk_type     = "pd-standard"
  ssh_username  = var.ssh_username
  machine_type  = var.machine_type
  tags          = ["csye6225"]
  network       = "default"
}

build {
  sources = ["sources.googlecompute.webapp"]

  provisioner "file" {
    source      = "packer/webservice.service"
    destination = "/tmp/webservice.service"
  }

  provisioner "file" {
    source      = "build/project-artifact.tar.gz"
    destination = "/tmp/webapp-1.0.0.tar.gz"
  }

  provisioner "shell" {
    inline = [
      "sudo groupadd -f csye6225",
      "sudo useradd -s /sbin/nologin -g csye6225 -d /opt/csye6225 -m csye6225",
      "sudo mv /tmp/webservice.service /etc/systemd/system/",
      "sudo cp /tmp/webapp-1.0.0.tar.gz /opt/csye6225/",
      "sudo tar -xzf /opt/csye6225/webapp-1.0.0.tar.gz -C /opt/csye6225/",
      "pwd",
      "sudo ls -ltr /opt/csye6225",
      "sudo cd /opt/csye6225",
      "sudo mv /opt/csye6225/webapp-1.0.0 /opt/csye6225/webapp",
      "sudo ls -ltr /opt/csye6225",
      "sudo chown -R csye6225:csye6225 /opt/csye6225",
      "sudo yum install -y python39",
      "sudo yum install -y python39-pip",
      "sudo yum install -y python3-devel",
      "sudo dnf install postgresql-server postgresql-contrib -y",
      "sudo yum install -y gcc make postgresql-devel --nobest",
      "sudo postgresql-setup initdb",
      "sudo systemctl start postgresql",
      "sudo systemctl enable postgresql",
      "sudo yum install -y postgresql-devel --nobest",
      "which pg_config",
      "pg_config --version",
      "export PG_CONFIG_PATH=$(find /usr -name pg_config | head -n 1)",
      "export PATH=$(dirname $PG_CONFIG_PATH):$PATH",
      "trap 'sudo journalctl -u postgresql.service > postgresql_logs.txt' EXIT",
      "sudo -u postgres psql -c \"ALTER USER postgres WITH PASSWORD 'password';\"",
      "echo 'PostgreSQL password changed'",
      "sudo -u postgres createdb csye6225",
      "sudo python3.9 -m venv /opt/csye6225/webapp/venv",
      "sudo /usr/bin/pip3.9 install psycopg2-binary==2.9.9",
      "sudo /usr/bin/pip3.9 install -r /opt/csye6225/webapp/requirements.txt",
      "echo 'FastAPI dependencies installed'",
      "sudo systemctl daemon-reload",
      "sudo systemctl enable webservice.service",
      "echo 'webservice.service enabled'",
      "sudo systemctl start webservice.service",
      "echo 'webservice.service started'"
    ]
  }
}



