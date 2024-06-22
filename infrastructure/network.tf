##############################################
# Network                                    #
##############################################

data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  vpc_cidr_block = "10.0.0.0/22"
  azs_ranges = {
    "dmz-public" : "10.0.0.0/24",
    "frontend-private" : "10.0.1.0/24",
    "backend-private" : "10.0.2.0/24",
  }
  azs = data.aws_availability_zones.available.names
}

## VPC
resource "aws_vpc" "main" {
  cidr_block           = local.vpc_cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "${var.name}-vpc"
  }
}

## Subnets
resource "aws_subnet" "dmz-public" {
  for_each = {
    for az in local.azs : az => cidrsubnet(local.azs_ranges["dmz-public"], length(local.azs), index(local.azs, az))
  }
  vpc_id                  = aws_vpc.main.id
  availability_zone       = each.key
  cidr_block              = each.value
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.name}-dmz-public"
  }
}

resource "aws_subnet" "frontend-private" {
  for_each = {
    for az in local.azs : az => cidrsubnet(local.azs_ranges["frontend-private"], length(local.azs), index(local.azs, az))
  }
  vpc_id            = aws_vpc.main.id
  availability_zone = each.key
  cidr_block        = each.value

  tags = {
    Name = "${var.name}-frontend-private"
  }
}

resource "aws_subnet" "backend-private" {
  for_each = {
    for az in local.azs : az => cidrsubnet(local.azs_ranges["backend-private"], length(local.azs), index(local.azs, az))
  }
  vpc_id            = aws_vpc.main.id
  availability_zone = each.key
  cidr_block        = each.value

  tags = {
    Name = "${var.name}-backend-private"
  }
}

## Internet Gateway
resource "aws_internet_gateway" "dmz-public" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.name}-igw"
  }
}

## NAT Gateway
resource "aws_eip" "nat" {
  for_each = aws_subnet.dmz-public
  domain   = "vpc"
}

resource "aws_nat_gateway" "nat" {
  for_each      = aws_subnet.dmz-public
  allocation_id = aws_eip.nat[each.key].id
  subnet_id     = each.value.id

  tags = {
    Name = "${var.name}-nat-${each.key}"
  }
}

## Route tables
resource "aws_route_table" "dmz-public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.dmz-public.id
  }

  tags = {
    Name = "${var.name}-dmz-public"
  }
}

resource "aws_route_table_association" "dmz-public" {
  for_each       = aws_subnet.dmz-public
  subnet_id      = each.value.id
  route_table_id = aws_route_table.dmz-public.id
}

resource "aws_route_table" "frontend-private" {
  for_each = aws_subnet.frontend-private
  vpc_id   = aws_vpc.main.id
}

resource "aws_route_table" "backend-private" {
  for_each = aws_subnet.backend-private
  vpc_id   = aws_vpc.main.id
}

resource "aws_route_table_association" "frontend-private" {
  for_each       = aws_subnet.frontend-private
  subnet_id      = each.value.id
  route_table_id = aws_route_table.frontend-private[each.key].id
}

resource "aws_route_table_association" "backend-private" {
  for_each       = aws_subnet.backend-private
  subnet_id      = each.value.id
  route_table_id = aws_route_table.backend-private[each.key].id
}

resource "aws_route" "frontend-nat" {
  for_each               = aws_nat_gateway.nat
  route_table_id         = aws_route_table.frontend-private[each.key].id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = each.value.id

  depends_on = [
    aws_route_table.frontend-private
  ]
}

resource "aws_route" "backend-nat" {
  for_each               = aws_nat_gateway.nat
  route_table_id         = aws_route_table.backend-private[each.key].id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = each.value.id

  depends_on = [
    aws_route_table.backend-private
  ]
}
