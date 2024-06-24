resource "aws_ecr_repository" "app" {
  name                 = var.name
  image_tag_mutability = "MUTABLE"
}

output "image_reg" {
  value = aws_ecr_repository.app.repository_url
}
