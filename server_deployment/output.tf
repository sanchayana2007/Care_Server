output "instance_ip" {
  description = "The public ip for ssh access"
  value       = aws_instance.app_server.public_ip
}
