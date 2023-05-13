terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

#create a key to conenct to the instance
resource "aws_key_pair" "ssh-key" {
  key_name   = "ssh-key"
  public_key = var.public_key
}


data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

owners = ["099720109477"]

}


#Create the zip file from the main
resource "null_resource" "dump_db_file1" {
  provisioner "local-exec" {
    command = "mongodump --db BigBase --out=./dbdumps/ --gzip "
  }

}

resource "null_resource" "dump_db_file2" {
  provisioner "local-exec" {
    command = "mongodump --db DocBookingService --out=./dbdumps/ --gzip "
  }

}




#Create the zip file from the main
resource "null_resource" "tar_db_files" {
  provisioner "local-exec" {
    command = "tar -zcvf dump.tar.gz dbdumps/"
  }
   depends_on = [null_resource.dump_db_file2, null_resource.dump_db_file1, ]
}


#Create the zip file from the main
resource "null_resource" "tar_server_files" {
  provisioner "local-exec" {
    command = "tar -zcvf server.tar.gz  ../server_v2/"
  }

}


resource "aws_instance" "app_server" {
  #ami           = var.ami
  instance_type = var.instance_type
  ami           = data.aws_ami.ubuntu.id

  #key_name = var.public_key
  tags = {
    Name = "DocAppServerInstance"
  }

  key_name         = "ssh-key"
  vpc_security_group_ids = [aws_security_group.allow_traffic.id]
   depends_on = [null_resource.tar_server_files, null_resource.tar_db_files ]

  provisioner "file" {
    source = "server.tar.gz "
    destination = "/home/ubuntu/server.tar.gz "
    connection {
      host = "${self.public_ip}"
      type = "ssh"
      user = "ubuntu"
      private_key = "${file("~/.ssh/id_rsa")}"
    }

  }

    provisioner "file" {
      source = "dump.tar.gz"
      destination = "/home/ubuntu/dump.tar.gz"
      connection {
        host = "${self.public_ip}"
        type = "ssh"
        user = "ubuntu"
        private_key = "${file("~/.ssh/id_rsa")}"
      }

    }



  provisioner "remote-exec" {
   inline = [
     "wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -",
     "sudo apt-get install gnupg",
     "wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -",
     "echo \"deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.4 multiverse\" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list",
     "sudo apt-get update",
     "sudo apt-get install -y mongodb-org",
     "sudo service mongod start",
     "sudo service mongod status",
     "yes  | sudo  apt-get -y install python3-pip",
     "yes  |  sudo apt install nginx",
     "pip3 install boson",
     "pip3 install ",
     "tar -zxvf dump.tar.gz",
     "mongorestore  --gzip dbdumps/",
     ]

     connection {
      host = "${self.public_ip}"
      type = "ssh"
      user = "ubuntu"
      private_key = "${file("~/.ssh/id_rsa")}"
    }
 }


  }
