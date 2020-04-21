# PygameGui
Simple GUI for pygame

Usage:

Import classes

`from userinput import UserInputGroup, Button, TextBox, Label, ChoiceBox`

Pygame screen

`self.screen = pg.display.set_mode([600, 600])` 

Create Input Group

`self.inputs = UserInputGroup()`

Create Inputs

    label = Label(self.inputs, width = 200, text = "A Text Label", center = (200, 100))
    button = Button(self.inputs, width = 200,  text = "A Button", center = (200, 150))
    textbox = TextBox(self.inputs, width = 200, center = (200, 200))
    choice = ChoiceBox(self.inputs, width = 200, center = (200, 250))

Update (probably from update(delta_time) function)

`self.inputs.update(delta_time)`

Draw (probably from draw(surface) function)

`self.inputs.draw(self.screen)`

List of keyword args that can be passed into the constructor of each input, with default value

        ("width", 50)
        ("height", 20)
        ("bg_color", (0,0,0))
        ("center", (0,0))
        ("text", '')
        ("fg_color", (255,255,255))
        ("font", pg.font.SysFont('Arial', False, False, 16))
        ("text_align", 1) # 1: left, 2: center, 3: right
        ("hl_color", (0,50,200))
        ("padding", 20)
        ("border_thick", 2)

