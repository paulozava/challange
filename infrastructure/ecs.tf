module "ecs" {
  source  = "terraform-aws-modules/ecs/aws"
  version = "5.11.2"

  cluster_name = "${var.name}-cluster"

  cluster_configuration = {
    execute_command_configuration = {
      logging = "OVERRIDE"
      log_configuration = {
        cloud_watch_log_group_name = "/aws/ecs/${var.name}-ecs-cluster"
      }
    }
  }

  fargate_capacity_providers = {
    FARGATE = {
      default_capacity_provider_strategy = {
        weight = 100
      }
    }
    FARGATE_SPOT = {
      default_capacity_provider_strategy = {
        weight = 0
      }
    }
  }

  services = {
    (var.name) = {
      cpu    = 1024
      memory = 4096

      # Container definition(s)
      container_definitions = {

        (var.name) = {
          cpu       = 512
          memory    = 1024
          essential = true
          image     = "${aws_ecrpublic_repository.app.repository_uri}:${var.image_version}"

          port_mappings = [
            {
              name          = var.name
              containerPort = 8080
              protocol      = "tcp"
            }
          ]

          environment = [
            { name = "APP_DB_HOST", value = aws_rds_cluster.postgres.endpoint },
            { name = "APP_DB_USER", value = var.app_db.user },
            { name = "APP_DB_PASSWORD", value = var.app_db.password },
            { name = "APP_DB_NAME", value = var.app_db.name },
          ]

          readonly_root_filesystem  = false
          enable_cloudwatch_logging = true
          memory_reservation        = 100
        }
      }

      load_balancer = {
        service = {
          target_group_arn = aws_lb_target_group.tg-app.arn
          container_name   = var.name
          container_port   = 8080
        }
      }

      subnet_ids = [for s in aws_subnet.frontend-private : s.id]
      security_group_rules = {
        alb_ingress_8080 = {
          type                     = "ingress"
          from_port                = 8080
          to_port                  = 8080
          protocol                 = "tcp"
          description              = "Service port to ${var.name}"
          source_security_group_id = aws_security_group.app-lb.id
        }
        egress_all = {
          type        = "egress"
          from_port   = 0
          to_port     = 0
          protocol    = "-1"
          cidr_blocks = ["0.0.0.0/0"]
        }
      }
    }
  }
}
