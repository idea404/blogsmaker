class BlogGenerator:
    def __init__(self) -> None:
        print("BlogGenerator initialized")

    def generate(self, subjects):
        print("Generating blog posts for subjects: ", ", ".join(subjects))