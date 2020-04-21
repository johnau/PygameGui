# PygameGui
Simple GUI for pygame

Usage:

<b>from userinput import UserInputGroup, Button, TextBox, Label, ChoiceBox  </b> #Import classes

<b>self.screen = pg.display.set_mode([600, 600])</b>   #Pygame screen
<b>self.inputs = UserInputGroup()</b>   #Create Group

<b>label = Label(self.inputs, width = 200, text = "A Text Label", center = (200, 100))</b>  # create a basic Label
<b>button = Button(self.inputs, width = 200,  text = "A Button", center = (200, 150))</b>  # create a basic Button
<b>textbox = TextBox(self.inputs, width = 200, center = (200, 200))</b>  # create a basic TextBox
<b>choice = ChoiceBox(self.inputs, width = 200, center = (200, 250))</b>  # create a basic ChoiceBox

<b>self.inputs.update(delta_time)</b>   #update from update() function

<b>self.inputs.draw(self.screen)</b>   #draw from draw() function

