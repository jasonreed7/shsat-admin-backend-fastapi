terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.67"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

data "local_file" "pgp_key" {
  filename = "public-key-binary.gpg"
}

# S3 bucket
resource "aws_s3_bucket" "shsat_images" {
  bucket = "shsat-images"

  tags = {
    Name = "SHSAT Images"
  }
}

# IAM user
resource "aws_iam_user" "shsat_admin" {
  name = "shsat-admin"
}

# IAM group
resource "aws_iam_group" "shsat_admin_group" {
  name = "shsat-admin-group"
}

# IAM group membership
resource "aws_iam_group_membership" "group_membership" {
  name = "shsat-admin-group-membership"

  users = [
    aws_iam_user.shsat_admin.name,
  ]

  group = aws_iam_group.shsat_admin_group.name
}

# IAM policy for group to be able to upload to the S3 bucket
resource "aws_iam_policy" "shsat_admin_policy" {
  name        = "shsat-admin-policy"
  description = "SHSAT admin policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:PutObject",
        ]
        Effect = "Allow"
        Resource = [
          "${aws_s3_bucket.shsat_images.arn}/*",
        ]
      },
    ]
  })
}

# Attaching the policy to the group
resource "aws_iam_policy_attachment" "attach" {
  name       = "shsat_admin_attachment"
  groups     = [aws_iam_group.shsat_admin_group.name]
  policy_arn = aws_iam_policy.shsat_admin_policy.arn
}

# IAM Access key
resource "aws_iam_access_key" "shsat_admin_access_key" {
  user    = aws_iam_user.shsat_admin.name
  pgp_key = data.local_file.pgp_key.content_base64
}

output "access_key_id" {
  value = aws_iam_access_key.shsat_admin_access_key.id
}

output "secret_access_key" {
  value = aws_iam_access_key.shsat_admin_access_key.encrypted_secret
}
