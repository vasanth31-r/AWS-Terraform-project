variable "aws_region" {
  default = "ap-south-1"
}

variable "ami_id" {
  default = "ami-02b8269d5e85954ef" 
}

variable "project" {
  default = "Project-tf"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  default = "10.0.1.0/24"
}

variable "private_subnet_cidr" {
  default = "10.0.2.0/24"
}

variable "key_name" {
  default = "project-key"
}

variable "db_username" {
  default = "dbadmin"
}

variable "db_password" {
  default   = "Password@123"
  sensitive = true
}
