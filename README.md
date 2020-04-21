# PygameGui
Simple GUI for pygame

<b>Usage:</b>

<b>from userinput import UserInputGroup, Button, TextBox, Label, ChoiceBox  #Import classes

self.screen = pg.display.set_mode([600, 600])  #Pygame screen
self.inputs = UserInputGroup()  #Create Group

label = Label(self.inputs, width = 200, text = "A Text Label", center = (200, 100)) # create a basic Label
button = Button(self.inputs, width = 200,  text = "A Button", center = (200, 150)) # create a basic Button
textbox = TextBox(self.inputs, width = 200, center = (200, 200)) # create a basic TextBox
choice = ChoiceBox(self.inputs, width = 200, center = (200, 250)) # create a basic ChoiceBox

self.inputs.update(delta_time)  #update from update() function

self.inputs.draw(self.screen)  #draw from draw() function

</b>
