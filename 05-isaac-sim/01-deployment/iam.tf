###############################################################################
# The teammate. Can start/stop/connect to the ONE instance; explicitly cannot
# create, resize, re-image, or destroy it. See 00-plan.md §5.
###############################################################################

resource "aws_iam_user" "teammate" {
  name = var.iam_user_name
}

# Console login. Password is stored in TF state (sensitive output); the
# teammate must change it on first sign-in.
resource "aws_iam_user_login_profile" "teammate" {
  user                    = aws_iam_user.teammate.name
  password_reset_required = true
}

# Programmatic access for the AWS CLI (start/stop/connect from a terminal).
resource "aws_iam_access_key" "teammate" {
  user = aws_iam_user.teammate.name
}

resource "aws_iam_policy" "operator" {
  name        = "isaac-sim-operator"
  description = "Start/stop/connect to the Isaac Sim instance; deny anything that changes its shape or fleet."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "ReadInstanceState"
        Effect = "Allow"
        Action = [
          "ec2:DescribeInstances",
          "ec2:DescribeInstanceStatus",
          "ec2:DescribeInstanceTypes",
          "ec2:DescribeTags"
        ]
        # Describe* does not support resource-level scoping.
        Resource = "*"
      },
      {
        Sid      = "StartStopThisInstanceOnly"
        Effect   = "Allow"
        Action   = ["ec2:StartInstances", "ec2:StopInstances"]
        Resource = local.instance_arn
      },
      {
        Sid      = "ConnectViaInstanceConnect"
        Effect   = "Allow"
        Action   = ["ec2-instance-connect:SendSSHPublicKey"]
        Resource = local.instance_arn
        Condition = {
          StringEquals = { "ec2:osuser" = "ubuntu" }
        }
      },
      {
        # Explicit Deny always wins — even if a broader policy is ever
        # attached, the teammate can never resize / rebuild / destroy.
        Sid    = "DenyShapeAndFleetChanges"
        Effect = "Deny"
        Action = [
          "ec2:RunInstances",
          "ec2:TerminateInstances",
          "ec2:ModifyInstanceAttribute",
          "ec2:ModifyInstanceCreditSpecification",
          "ec2:CreateImage",
          "ec2:ModifyVolume",
          "ec2:AttachVolume",
          "ec2:DetachVolume",
          "ec2:CreateTags",
          "ec2:DeleteTags"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_user_policy_attachment" "teammate" {
  user       = aws_iam_user.teammate.name
  policy_arn = aws_iam_policy.operator.arn
}
