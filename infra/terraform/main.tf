terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type    = string
  default = "production"
}

resource "aws_vpc" "nexus_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "agentops-nexus-vpc"
    Environment = var.environment
  }
}

resource "aws_internet_gateway" "nexus_igw" {
  vpc_id = aws_vpc.nexus_vpc.id

  tags = {
    Name = "agentops-nexus-igw"
  }
}

resource "aws_subnet" "public_subnet_1" {
  vpc_id            = aws_vpc.nexus_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "agentops-nexus-public-1"
  }
}

resource "aws_subnet" "public_subnet_2" {
  vpc_id            = aws_vpc.nexus_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "agentops-nexus-public-2"
  }
}

resource "aws_db_instance" "postgres" {
  allocated_storage      = 20
  db_name                = "agentops_nexus"
  engine                 = "postgres"
  engine_version         = "16.1"
  instance_class         = "db.t4g.micro"
  username               = "agentops"
  password               = "securepassword123!"
  parameter_group_name   = "default.postgres16"
  skip_final_snapshot    = true
  publicly_accessible    = false
  vpc_security_group_ids = [aws_security_group.db_sg.id]

  tags = {
    Environment = var.environment
  }
}

resource "aws_security_group" "db_sg" {
  name        = "agentops-db-sg"
  description = "Allow inbound database traffic"
  vpc_id      = aws_vpc.nexus_vpc.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
