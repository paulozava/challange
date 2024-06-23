variable "name" {
  type    = string
  default = "study"
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
}

provider "aws" {
  region = var.region
}


module "infrastructure" {
  source = "./infrastructure"
  name   = var.name
  region = var.region
}

resource "null_resource" "docker_build" {
  provisioner "local-exec" {
    command = <<-EOT
        docker login -u AWS -p $(aws ecr get-login-password --region ${var.region}) ${module.infrastructure.image_reg}
        docker build -t ${module.infrastructure.image_reg} .
        docker push ${module.infrastructure.image_reg}
    EOT
  }
}

output "app" {
  value = module.infrastructure.access_your_site
}
