###############################################################################
# Manual start, automatic stop. The teammate powers the box ON on demand; one
# EventBridge Scheduler entry guarantees it goes OFF at 16:00 to cap cost. No
# auto-start, no Lambda. Timezone America/New_York => automatic DST. §6.
###############################################################################

# Role the scheduler assumes; can only STOP this one instance.
resource "aws_iam_role" "scheduler" {
  name = "isaac-sim-scheduler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "scheduler.amazonaws.com" }
      Action    = "sts:AssumeRole"
      Condition = {
        StringEquals = { "aws:SourceAccount" = data.aws_caller_identity.current.account_id }
      }
    }]
  })
}

resource "aws_iam_role_policy" "scheduler" {
  name = "isaac-sim-scheduler-stop"
  role = aws_iam_role.scheduler.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["ec2:StopInstances"]
      Resource = local.instance_arn
    }]
  })
}

resource "aws_scheduler_schedule" "stop" {
  name        = "isaac-sim-stop"
  description = "Power the Isaac Sim box OFF at the end of the working window"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression          = var.schedule_stop_cron
  schedule_expression_timezone = var.schedule_timezone

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:ec2:stopInstances"
    role_arn = aws_iam_role.scheduler.arn
    input    = jsonencode({ InstanceIds = [aws_instance.isaac.id] })
  }
}
