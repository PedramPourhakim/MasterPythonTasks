from pynput import keyboard
import webbrowser
import os

def open_google():
    webbrowser.open('https://google.com')

def say_hello():
    print("Hello There !!!")

def exit_program():
    print("Goodbye")
    listener.stop()

def read_file():
    try:
        with open('test.txt', 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print("File test.txt not found")

def get_folder_contents():
    folder_path = os.getcwd()
    for item in os.listdir(folder_path):
        print(item)

with keyboard.GlobalHotKeys({
    '<ctrl>+<alt>+g':open_google,
    '<ctrl>+<alt>+h':say_hello,
    '<ctrl>+<alt>+q':exit_program,
    '<ctrl>+<alt>+d':read_file,
    '<ctrl>+<alt>+f':get_folder_contents,
}) as listener:
    listener.join()

