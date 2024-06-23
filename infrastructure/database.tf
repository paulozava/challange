resource "aws_security_group" "postgres" {
  vpc_id      = aws_vpc.main.id
  name        = "${var.name}-postgres-sg"
  description = "postgres sg"

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [for subnet in aws_subnet.frontend-private : subnet.cidr_block]
  }
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

resource "aws_db_subnet_group" "postgres" {
  name       = "${var.name}-postgres-subnet-group"
  subnet_ids = [for subnet in aws_subnet.backend-private : subnet.id]

  tags = {
    Name = "${var.name}-postgres-subnet-group"
  }
}

resource "aws_rds_cluster" "postgres" {
  cluster_identifier        = "${var.name}-postgres"
  vpc_security_group_ids    = [aws_security_group.postgres.id]
  db_subnet_group_name      = aws_db_subnet_group.postgres.name
  engine                    = "postgres"
  engine_version            = "16.1"
  database_name             = var.app_db.name
  master_username           = var.app_db.user
  master_password           = var.app_db.password
  deletion_protection       = false
  skip_final_snapshot       = true
  final_snapshot_identifier = "${var.name}-postgres-final-snapshot"
  allocated_storage         = 100
  db_cluster_instance_class = "db.m5d.large"
  iops                      = 1000
  storage_type              = "io1"
}

output "postgres_endpoint" {
  value = aws_rds_cluster.postgres.endpoint
}

