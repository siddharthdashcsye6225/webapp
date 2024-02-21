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
    source      = "webservice.service"
    destination = "/tmp/webservice.service"
  }

  provisioner "file" {
    source      = "../build/production-package.tar.gz"
    destination = "/tmp/webapp-1.0.0.tar.gz"
  }

  provisioner "shell" {
    inline = [
      "sudo groupadd -f csye6225",
      "echo 'csye6225 group created'",
      "sudo useradd -s /sbin/nologin -g csye6225 -d /opt/csye6225 -m csye6225",
      "echo 'csye6225 user created'",
      "sudo mv /tmp/webservice.service /etc/systemd/system/",
      "echo 'webservice.service moved'",
      "sudo cp /tmp/webapp-1.0.0.tar.gz /opt/csye6225/",
      "sudo tar -xzf /opt/csye6225/webapp-1.0.0.tar.gz -C /opt/csye6225/",
      "sudo ls -ltr /opt/csye6225",
      "echo 'webapp-1.0.0.tar.gz extracted'",
      "sudo chown -R csye6225:csye6225 /opt/csye6225",
      "echo 'permissions updated'",
      #"sudo yum update -y",
      #"echo 'yum updated'",
      "pwd",
      "sudo yum install -y python39",
      "sudo yum install -y python39-pip",
      #"sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm",
      "sudo yum install -y postgresql-contrib",
      "sudo yum install -y postgresql-server",
      "which psql",
      #"systemctl status postgresql",
      "sudo dnf install postgresql-server postgresql-contrib -y",
      "sudo postgresql-setup initdb",
      "echo 'enabling postgres below'",
      "sudo systemctl start postgresql",
      "sudo systemctl enable postgresql",
      "echo 'Python  and PostgreSQL installed'",
      "whoami",
      "pwd",
      #"sudo systemctl enable postgresql",
      "df -h",
      "pwd",
      "sudo yum install -y postgresql-devel --nobest",
      "which pg_config",
      "sudo yum install -y gcc make postgresql-devel --nobest",
      "sudo yum install -y python3-devel",
      "pg_config --version",
      "sudo /usr/bin/pip3.9 install psycopg2-binary==2.9.9",
      "export PG_CONFIG_PATH=$(find /usr -name pg_config | head -n 1)",
      "export PATH=$(dirname $PG_CONFIG_PATH):$PATH",
      #"sudo systemctl enable postgresql",
      #"echo 'PostgreSQL enabled'",
      # "if sudo systemctl start postgresql; then",
      #"echo 'PostgreSQL started successfully'",
      #"else",
      # "echo 'PostgreSQL failed to start'",
      #"fi",
      #"sleep 10", // Wait for a few seconds for logs to become available
      "trap 'sudo journalctl -u postgresql.service > postgresql_logs.txt' EXIT",
      "sudo -u postgres psql -c \"ALTER USER postgres WITH PASSWORD 'password';\"",
      "echo 'PostgreSQL password changed'",
      "sudo -u postgres createdb csye6225",
      "sudo mkdir -p /opt/fastapi_app",
      "sudo chown -R csye6225:csye6225 /opt/fastapi_app",
      "echo 'FastAPI directory created'",
      "sudo tar -xzf /tmp/webapp-1.0.0.tar.gz -C /opt/fastapi_app",
      "echo 'FastAPI artifact extracted'",
      "sudo python3.9 -m venv /opt/fastapi_app/venv",
      "sudo ls -ltr /opt/fastapi_app/webapp/",
      "sudo /usr/bin/pip3.9 install -r /opt/fastapi_app/webapp/requirements.txt",
      "echo 'FastAPI dependencies installed'",
      "sudo ls -ltr /opt/fastapi_app",
      "pwd",
      "sudo ls -ltr /opt/fastapi_app/webapp",
      "pwd",
      "sudo ls -ltr /opt/fastapi_app/webapp/csye6225project",
      "sudo ls -ltr /opt/fastapi_app/webapp/csye6225project/csye6225",
      "pwd",
      "echo 'Switched to FastAPI project directory'",
      # Additional steps for finding and running uvicorn
      "uvicorn_path=$(sudo find / -type f -name uvicorn | grep '/bin/uvicorn' | head -n 1)",
      "echo 'uvicorn binary found at: $uvicorn_path'",
      "echo $uvicorn_path",
      "ls -ltr $uvicorn_path",
      "sudo -u csye6225 $uvicorn_path /opt/fastapi_app/webapp/csye6225project/csye6225/main:app --host 0.0.0.0 --port 8000 &",
      #"sudo /opt/csye6225/env/bin/uvicorn main:app --host 0.0.0.0 --port 8000 &",
      "echo 'FastAPI application started'",
      "sudo systemctl enable webservice.service",
      "echo 'webservice.service enabled'",
      "sudo systemctl start webservice.service",
      "echo 'webservice.service started'"
    ]
  }
}



