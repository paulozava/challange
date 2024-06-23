variable "name" {
  type = string
}

variable "region" {
  type = string
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
