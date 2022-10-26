"""

  ___________________
((                   ))
 )) CODED BY BREADY ((
((                   ))
  -------------------


File Renamer V2.0:
Improvements:
    - GUI
    - Folder Settings
"""


# from classes import *
import classes as cl
import PySimpleGUI as sg

# step 1: select design
sg.theme('Default1')
# step 2: Define the windows layout
# Step 2.1: Define Input List
input_list = [[sg.Text('Source')],
              [sg.Input(enable_events=True, key='-SOURCE-'), sg.FolderBrowse()],
              [sg.Listbox(values=[], size=(80, 20), key='-LIST-')]]
# Step 2.2: Define Output List
output_list = [[sg.Text('Destination')],
               [sg.Input(enable_events=True, key='-DESTINATION-'), sg.FolderBrowse()],
               [sg.Listbox(values=[], size=(80, 20), key='-LIST2-')]]
# Step 2.3: Define Console Window
console_window = [[sg.Multiline(autoscroll=True, size=(165, 10), key='-CONSOLE-',
                                reroute_cprint=True, disabled=True)]]
# Step 2.4: Define Layout:
layout = [
    [sg.Col(input_list),
     sg.VSep(),
     sg.Col(output_list)],
    [sg.Col(console_window, justification='center')],
    [sg.Button('CONVERT'), sg.Button('SETTINGS')],
    [sg.Button('CLOSE')]
]
# step 3: create window
window = sg.Window('File Renamer', layout)


# step 4: create while loop


def main():
    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WINDOW_CLOSED or event == 'CLOSE':
            break
        if event == 'CONVERT':
            cl.convertPDF()
        if event == 'SETTINGS':
            cl.notImplemented()
    # step 5: close window
    window.close()
    exit()


if __name__ == '__main__':
    main()
