import PySimpleGUI as sg
ch: int


def draw_gui():
    global ch
    sg.theme('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text('Table plotter v0.32')],
              [sg.Text('Enter channel number'), sg.InputText()],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):  # if user closes window or clicks cancel
            break
        elif event in 'Ok':
            ch = int(values[0])
            break

    window.close()
    return ch
