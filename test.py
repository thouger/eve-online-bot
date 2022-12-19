import cv2
import numpy as np

from pywinauto.application import Application

# create a pywinauto application object
app = Application().connect(title="MyApplication")

# get the main window of the application
window = app.MyApplication

# enumerate all the child windows of the main window
children = window.children()

# print the title of each child window
for i, child in enumerate(children):
    print(f"Window {i+1}: {child.title}")