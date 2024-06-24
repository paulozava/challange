variable "name" {
  type    = string
  default = "revolut"
}

variable "region" {
  type    = string
  default = "eu-west-1"
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "3.2.2"
    }
  }
  required_version = "~> 1.8.0"
}

provider "aws" {
  region = var.region
}

locals {
  docker_sha = sha1(timestamp())
}

module "infrastructure" {
  source        = "./infrastructure"
  name          = var.name
  region        = var.region
  image_version = local.docker_sha
}

resource "null_resource" "docker_build" {
  depends_on = [module.infrastructure]

  triggers = {
    infrastructure_image_sha = local.docker_sha
  }
  provisioner "local-exec" {
    command = <<-EOT
        docker login -u AWS -p $(aws ecr get-login-password --region ${var.region}) ${module.infrastructure.image_reg}
        docker build -t ${module.infrastructure.image_reg}:${local.docker_sha} .
        docker push ${module.infrastructure.image_reg}:${local.docker_sha}
    EOT
  }
}

output "app" {
  value = <<-EOT
How to access your site:

*Important: it could take few minutes to be available on the first deploy.

To add an user:
curl -X PUT -v -k https://${module.infrastructure.access_your_site}/hello/<username> -H "Content-Type: application/json" -d '{"dateOfBirth": "1990-01-01"}'

To get the user:
curl -v -k https://${module.infrastructure.access_your_site}/hello/<username>

To get all usernames at database:
curl -v -k https://${module.infrastructure.access_your_site}/-/all
EOT
}
