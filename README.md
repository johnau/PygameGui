# PygameGui
Simple GUI for pygame

<b>TODO: Function & Callback (for button)</b>

Usage:

Import classes

`from userinput import UserInputGroup, Button, TextBox, Label, ChoiceBox`

Pygame screen (to pass to draw function below)

`self.screen = pygame.display.set_mode([600, 600])` 

Create Input Group

`self.inputs = UserInputGroup()`

Create Inputs (names must be unique within the group)

    label = Label(self.inputs, name = "label1", width = 200, text = "A Text Label", center = (200, 100))
    
    textbox = TextBox(self.inputs, name = "text1", width = 200, center = (200, 200))
    
    choice = ChoiceBox(self.inputs, name = "choice1", width = 200, center = (200, 250), items = ["one", "two", "three"])
    
    click_func = lambda: print(f"Textbox text: {textbox.text}")
    button = Button(self.inputs, name = "button1", width = 200,  text = "A Button", center = (200, 150), on_click = click_func)
    
Update (probably from update(delta_time) function)

`self.inputs.update(delta_time)`

Draw (probably from draw(surface) function)

`self.inputs.draw(self.screen)`

Access value (called when needed)

`self.inputs.get_input("text1").text`

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


<b>Minimal working example:</b>

    import pygame
    from userinput import UserInputGroup, Button, TextBox, Label, ChoiceBox

    class App:
        def __init__(self):
            self.screen = pygame.display.set_mode([600, 600])
            self.inputs = UserInputGroup()
            label = Label(self.inputs, name = "label1", width = 200, text = "A Text Label", center = (200, 100))
            textbox = TextBox(self.inputs, name = "text1", width = 200, center = (200, 150))
            choice = ChoiceBox(self.inputs, name = "choice1", width = 200, center = (200, 250), items = ["one", "two", "three"])
            click_func = lambda: print(f"Textbox text: {textbox.text}, Choicebox choice: {choice.text}")
            button = Button(self.inputs, name = "button1", width = 200,  text = "A Button", center = (200, 350), on_click = click_func)

        def handle_events(self, events):
            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.inputs.mouse_down(pygame.mouse.get_pos())
                if e.type == pygame.MOUSEBUTTONUP:
                    self.inputs.mouse_up(pygame.mouse.get_pos())
                if e.type == pygame.KEYDOWN:
                    self.inputs.key_down(e)
                if e.type == pygame.KEYUP:
                    self.inputs.key_up(e)

        def update(self, delta_time):
            self.inputs.update(delta_time)

        def draw(self):
            self.screen.fill(pygame.Color('white'))
            self.inputs.draw(self.screen)
            pygame.display.update()

    pygame.init()
    app = App()

    pygame.display.set_caption('User Input Example')
    clock = pygame.time.Clock()

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        dt = clock.tick(60)
        app.handle_events(events)
        app.update(dt)
        app.draw()

    pygame.quit()
