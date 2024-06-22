resource "awscc_ecr_repository" "app" {
  repository_name      = var.name
  image_tag_mutability = "MUTABLE"

  lifecycle_policy = {
    lifecycle_policy_text = <<EOF
        {
            "rules": [
                {
                    "rulePriority": 1,
                    "description": "Keep last 30 images",
                    "selection": {
                        "tagStatus": "untagged",
                        "countType": "imageCountMoreThan",
                        "countNumber": 30
                    },
                    "action": {
                        "type": "expire"
                    }
                }
            ]
        }
        EOF
  }

  lifecycle {
    ignore_changes = all
  }
}

