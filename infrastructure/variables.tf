variable "name" {
  type    = string
  default = "study"
}

variable "region" {
  type    = string
  default = "eu-west-1"
}

variable "image_version" {
  type    = string
  default = "latest"
}

variable "app_db" {
  type = map(string)
  default = {
    user     = "foofoofoo"
    password = "barbarbar"
    name     = "hello"
  }
}
