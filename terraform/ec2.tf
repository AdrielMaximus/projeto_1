resource "aws_instance" "app" {
  ami           = "ami-0f85876b1aff99dde"
  instance_type = "t3.micro"

  key_name = "projeto"

  security_groups = [aws_security_group.app_sg.name]

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install docker -y
    systemctl start docker
    systemctl enable docker

    curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
      -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
  EOF

  tags = {
    Name = "demo-app"
  }
}
