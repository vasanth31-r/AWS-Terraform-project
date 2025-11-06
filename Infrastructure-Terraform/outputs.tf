output "alb_dns" {
  value = aws_lb.alb.dns_name
}

output "app_private_ip" {
  value = aws_instance.app.private_ip
}

output "rds_endpoint" {
  value = aws_db_instance.postgres.address
}

output "vpc_id" {
  value = aws_vpc.main.id
}
output "public_subnet_a_id" {
  value = aws_subnet.public_a.id
}

output "public_subnet_b_id" {
  value = aws_subnet.public_b.id
}
