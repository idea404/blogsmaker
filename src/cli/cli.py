from generator.generator import BlogGenerator


class CommandLineInterface: 
    def __init__(self):
       self.generator = BlogGenerator()
       print("CLI initialized")

    def start(self):
      val = input("Pass subjects separated by comma: \n")
      subjects = [x.strip() for x in val.split(",")]
      self.generator.generate(subjects)
  