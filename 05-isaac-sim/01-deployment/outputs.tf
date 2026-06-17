output "instance_id" {
  description = "EC2 instance id — use this for start/stop/connect by id."
  value       = aws_instance.isaac.id
}

output "instance_public_ip" {
  description = "Auto-assigned public IP (changes on each stop/start)."
  value       = aws_instance.isaac.public_ip
}

output "instance_type" {
  description = "Confirm the GPU shape that was deployed."
  value       = aws_instance.isaac.instance_type
}

output "iam_user_name" {
  description = "Teammate's IAM user."
  value       = aws_iam_user.teammate.name
}

output "iam_user_initial_password" {
  description = "One-time console password (reset required on first login)."
  value       = aws_iam_user_login_profile.teammate.password
  sensitive   = true
}

output "iam_access_key_id" {
  description = "Teammate's AWS CLI access key id."
  value       = aws_iam_access_key.teammate.id
  sensitive   = true
}

output "iam_secret_access_key" {
  description = "Teammate's AWS CLI secret. View with: terraform output -raw iam_secret_access_key"
  value       = aws_iam_access_key.teammate.secret
  sensitive   = true
}
