# resource "aws_ecrpublic_repository" "app" {
#   provider        = aws.us_east_1
#   repository_name = var.name
# }
#
resource "aws_ecr_repository" "app" {
  name                 = var.name
  image_tag_mutability = "MUTABLE"
}

output "image_reg" {
  value = aws_ecr_repository.app.repository_url
}
