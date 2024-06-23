resource "aws_ecrpublic_repository" "app" {
  provider        = aws.us_east_1
  repository_name = var.name
}

