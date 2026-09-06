import pyfiglet

text = input("Enter text: ")

ascii_art = pyfiglet.figlet_format(text)

print(ascii_art)