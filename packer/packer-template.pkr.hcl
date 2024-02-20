source "googlecompute" "custom_image" {
  account_file        = "dev-siddharth-dash-csye6225-a3631f1ff719.json"
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
