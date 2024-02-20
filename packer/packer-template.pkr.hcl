source "googlecompute" "custom_image" {
  account_file        = "${secrets.GCP_CREDENTIALS}"
  project_id          = "dev-siddharth-dash-csye6225"
  source_image_family = "centos-stream-8"
  zone                = "us-central1-a"
  ssh_username        = "packer"
  network             = "default"
}

build {
  sources = [
    "source.googlecompute.custom_image"
  ]

  provisioner "shell" {
    script = "scripts/install_dependencies.sh"
  }
}
