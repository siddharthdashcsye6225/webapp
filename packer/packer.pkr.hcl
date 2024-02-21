source "googlecompute" "custom_image" {
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
    script = "packer/scripts/install_dependencies.sh"
  }
}

