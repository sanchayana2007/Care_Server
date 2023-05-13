variable "region" {
    type= string
  default     = "us-west-2"
  description = "AWS region"
}


variable "ami" {
    type= string
  default     = "ami-830c94e3"
  description = "AWS ami"
}


variable "instance_type" {
    type= string
  default     = "t2.micro"
  description = "AWS instance_type "
}


variable "access_key" {
    type= string
  default     = "AKIAUGOYHAG2ZVNGTYMP"
  description = "AWS access_key"
}


variable "welcome_message" {
    type= string
  default     = "Hi Sanchez"
  description = "AWS welcome_message"
}




variable "public_key" {
type= string
 default  = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDF/OaGscb4cof6id2fKN+cJ8cC6ar/6jzGC5Y0B2umhw/7gjg9ypYXv3HuPosJn4D85FEmngJrk9Cb9lL8qIb76IZWXohiZIPJ8qVlVBzG8CrUa1YqeXLE2YMYEvZ3cCGZcM6IlQ8lKhWD4APOoie2ms3tO/qdZqBTK5Q7/euD7KbBdovpxIqRs1MdddhSrrPUEL84P2u8o9VYS86FqKYfS6++V5ySvX6u0J5KWQPAtLPpeftIXRHzye+YaEu1ih5sOEWScT6SglDN/wF18W2eIQbVCEXxTJib0Wi5wj5Lu4ZA7LT9Sc+9FKFuISwfXUyu2UQ4kcnTx3Tcw0JJtqgLypczIT8+EVVGy7HElbt1MQVy425lJjHrM7iCBLpgHvu+x1IyicrABlX2cIBauiLcGZReLjf/BbFH129UdsZmQa7QSxtPH3aKoz/jOYA1e4Xy02oAr5uCGnNhVZVhLEaI211HqkQa3KFX6ML+IbZh3VvJAox6br8UJQh3ZAmIll0= sanch@sanch-HP-Laptop-14-ck2xxx"

}


variable "secret_key" {
    type= string
  default     = "SUqsWrF0npkT03p2G3/5TmtHSXKPmFKNNmagxh8I"
  description = "AWS secret_key"
}
