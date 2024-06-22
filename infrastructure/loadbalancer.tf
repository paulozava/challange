######################################################
# ELB                                                #
######################################################

## Security Group for Load Balancer
resource "aws_security_group" "app-lb" {
  vpc_id      = aws_vpc.main.id
  name        = "${var.name}-lb-sg"
  description = "lb sg that allows http/https from anywhere and egress all traffic"

  ingress {
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  ingress {
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

## Create a self-signed certificate
resource "tls_private_key" "app" {
  algorithm = "RSA"
}

resource "tls_self_signed_cert" "app" {
  private_key_pem = tls_private_key.app.private_key_pem

  subject {
    common_name  = aws_lb.app.dns_name
    organization = "YOUR WEB APP SERVER, Inc"
  }

  validity_period_hours = 48

  allowed_uses = [
    "key_encipherment",
    "digital_signature",
    "server_auth",
  ]
}

resource "aws_acm_certificate" "cert" {
  private_key      = tls_private_key.app.private_key_pem
  certificate_body = tls_self_signed_cert.app.cert_pem
}

## Load Balancer
resource "aws_lb" "app" {
  name                       = "${var.name}-app-lb"
  internal                   = false
  load_balancer_type         = "application"
  security_groups            = [aws_security_group.app-lb.id]
  subnets                    = [for subnet in aws_subnet.dmz-public : subnet.id]
  enable_deletion_protection = false
  tags = {
    Name = "${var.name}-app-lb"
  }
}

### Listener
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.app.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.app.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = aws_acm_certificate.cert.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app-tg.arn
  }
}

### Target Group
resource "aws_lb_target_group" "app-tg" {
  name        = "${var.name}-app-tg"
  port        = 8080
  protocol    = "HTTP"
  target_type = "instance"
  vpc_id      = aws_vpc.main.id

  health_check {
    path                = "/-/health"
    protocol            = "HTTP"
    port                = "8080"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    interval            = 30
    matcher             = "200-299"
  }
}

## Output
output "access_your_site" {
  value = aws_lb.app.dns_name
}

