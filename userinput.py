import pygame as pg

class UserInputGroup:
    def __init__(self):
        self._members = pg.sprite.Group()

    def update(self, delta_time):
        for m in self._members:
            m.update(delta_time)

    def draw(self, surface):
        for m in self._members:
            surface.blit(m.image, (m.rect.x, m.rect.y))

    def mouse_down(self, mouse_pos):
        any_hit = 0
        for m in self._members:
            hit = m.rect.collidepoint(mouse_pos)
            if hit:
                m.on_mousedown()
                if m.has_focus: self.remove_focus_except(m)
                any_hit = 1
                break

        if not any_hit:
            for m in self._members:
                m.reset()
                self.remove_focus_except(None)

    def mouse_up(self, mouse_pos):
        any_hit = 0
        for m in self._members:
            hit = m.rect.collidepoint(mouse_pos)
            if hit:
                m.on_mouseup()
                if m.has_focus: self.remove_focus_except(m)
                any_hit = 1
                break

        if not any_hit:
            for m in self._members:
                m.reset()

    def key_down(self, key_event):
        for m in self._members:
            if m.has_focus:
                m.on_keydown(key_event)
                break

    def key_up(self, key_event):
        pass

    def remove_focus_except(self, ip):
        for m in self._members:
            if not m is ip:
                m.has_focus = False

    def clear(self):
        self._members = []

    def __bool__(self):
        return bool(self._members)

    def __len__(self):
        return len(self._members)

    def __iadd__(self, ip):
        assert ip is not None
        #if isinstance(ip, (tuple, list)):
        #    self._members += ip
        #    return self
        self._members.add(ip)
        return self

    def __isub__(self, ip):
        for i, m in enumerate(self._members):
            if m is ip:
                del self._members[i]
                return self
        return self

    def append(self, ip):
        assert ip is not None
        self._members.add(ip)
        return self

    def __iter__(self):
        return iter(self._members)

class UserInput(pg.sprite.Sprite):
    def __init__(self, parent_group, **kwargs):
        super().__init__()
        parent_group += self
        self.parent_group = parent_group
        self._down = False
        self._has_focus = False

        self._width = kwargs.pop("width", 50)
        self._height = kwargs.pop("height", 20)
        self._bg_color = kwargs.pop("bg_color", (0,0,0))
        self._center = kwargs.pop("center", (0,0))
        self._text = kwargs.pop("text", '')
        self._fg_color = kwargs.pop("fg_color", (255,255,255))
        self._font = kwargs.pop("font", pg.font.SysFont('Arial', False, False, 16))
        self._text_align = kwargs.pop("text_align", 1) # 1: left, 2: center, 3: right
        self._hl_color = kwargs.pop("hl_color", (0,50,200))
        self._padding = kwargs.pop("padding", 20)
        self._border_thick = kwargs.pop("border_thick", 2)

        surf = pg.Surface((self._width, self._height))
        self.image = surf.convert()
        self.rect = self.image.get_rect(center = self._center)

        self._render_chain = [
                lambda surf, width, height, foreground, background, highlight, padding, font, text, border_thick: self._render_bg(surf, width, height, foreground, background, highlight, padding, font, text, border_thick),
                lambda surf, width, height, foreground, background, highlight, padding, font, text, border_thick: self._render_text(surf, width, height, foreground, background, highlight, padding, font, text, border_thick),
                lambda surf, width, height, foreground, background, highlight, padding, font, text, border_thick: self._render_border(surf, width, height, foreground, background, highlight, padding, font, text, border_thick),
            ]

        self._dirty = True

        self._dt = 0

    def _render_internal(self):
        if not self._dirty: return

        foreground = pg.Color(self._fg_color[0], self._fg_color[1], self._fg_color[2])
        background = pg.Color(self._bg_color[0], self._bg_color[1], self._bg_color[2])
        highlight = pg.Color(self._hl_color[0], self._hl_color[1], self._hl_color[2])

        surf = pg.Surface([self.rect.width, self.rect.height])
        for r in self._render_chain:
            r(surf, self._width, self._height, foreground, background, highlight, self._padding, self._font, self._text, self._border_thick)

        self.image = surf.convert()
        self.dirty = False

    def _render_bg(self, surf, width, height, foreground, background, highlight, padding, font, text, border_thick):
        surf.fill(background)

    def _render_text(self, surf, width, height, foreground, background, highlight, padding, font, text, border_thick):
        tcol = highlight if self._has_focus else foreground
        tsurf = self._font.render(self._text, True, tcol)
        tsize = self._font.size(self._text)
        tpos = [0,0]
        tadj = [0,0] if tsize[0] <= self._width-self._padding*2 else [self._width-self._padding*2-tsize[0], 0]

        if self._text_align == 1:
            tpos = [self._padding+tadj[0], self._height//2 - tsize[1]//2]
        elif self._text_align == 2:
            tpos = [self._width//2-tsize[0]//2+tadj[0], self._height//2 - tsize[1]//2]
        elif self._text_align == 3:
            tpos = [self._width-tsize[0]-self._padding+tadj[0], self._height//2 - tsize[1]//2]
        surf.blit(tsurf, tpos)

    def _render_border(self, surf, width, height, foreground, background, highlight, padding, font, text, border_thick):
        if self._has_focus:
            pg.draw.rect(surf, highlight, pg.Rect(0,0,self._width-1, self._height-1), 4)
        elif self._border_thick > 0:
            pg.draw.rect(surf, foreground, pg.Rect(0,0,self._width-self._border_thick//2, self._height-self._border_thick//2), self._border_thick)

    def update(self, delta_time):
        self._dt += delta_time
        self._render_internal()

    def reset(self):
        self._down = False

    @property
    def has_focus(self):
        return self._has_focus

    @has_focus.setter
    def has_focus(self, b):
        self._has_focus = b

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, wid):
        self._width = wid
        ow = self.rect.width
        self.rect.width = wid
        self.rect.x += ow-wid

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, hgt):
        self._height = hgt
        oh = self.rect.height
        self.rect.height = hgt
        self.rect.y += oh-hgt

    def on_mousedown(self):
        if not self._down:
            self._down = True
            self.dirty = True

    def on_mouseup(self, hit = False):
        if self._down:
            self._down = False
            self.dirty = True

    def on_keydown(self, key_event):
        pass

    def on_keyup(self, key_event):
        pass

class Button(UserInput):
    def __init__(self, parent_group, **kwargs):
        super().__init__(parent_group, text_align = 2, fg_color = (255,255,255), bg_color = (0,0,0), border_thick = 0, **kwargs)
    
    def on_mouseup(self):
        super().on_mouseup()
        print("Activate button")
        self.has_focus = True
        self.dirty = True

class TextBox(UserInput):
    def __init__(self, parent_group, **kwargs):
        super().__init__(parent_group, text_align = 1, fg_color = (0,0,0), bg_color = (255,255,255), **kwargs)

    def on_keydown(self, key_event):
        if key_event.key == pg.K_BACKSPACE:
            if self._text: self._text = self._text[:-1]
            self.dirty = True
        else:
            chr = key_event.unicode
            if chr:
                self._text += chr
                self.dirty = True

    def on_mousedown(self):
        super().on_mousedown()
        if not self.has_focus:
            self.has_focus = True
            self.dirty = True

    def on_mouseup(self, hit = False):
        super().on_mouseup(hit)

class Label(UserInput):
    def __init__(self, parent_group, **kwargs):
        super().__init__(parent_group, text_align = 1, fg_color = (0,0,0), bg_color = (255,255,255), border_thick = 0, **kwargs)

class ChoiceBox(UserInput):
    def __init__(self, parent_group, items, **kwargs):
        super().__init__(parent_group, text_align = 1, fg_color = (0,0,0), bg_color = (255,255,255), **kwargs)

        self._items = []
        if isinstance(items, list): self._items = items
        else: raise ValueError("Items variable must be a list")

        self._item_idx = 0

        self._render_chain.insert(len(self._render_chain)-2, lambda surf, width, height, foreground, background, highlight, padding, font, text, border_thick: self._render_arrows(surf, width, height, foreground, background, highlight, padding, font, text, border_thick))

    def _render_arrows(self, surf, width, height, foreground, background, highlight, padding, font, text, border_thick):
        aw = 14
        
        pg.draw.rect(surf, background, pg.Rect(width-border_thick*4-aw, border_thick, aw+border_thick*4, height-border_thick*2), 0)

        down_points = [[-aw//2, -aw//2], [aw//2, -aw//2], [0, aw//2]]
        up_points = [[-aw//2, aw//2], [aw//2, aw//2], [0, -aw//2]]
        for p in down_points:
            p[0] += width-border_thick*4-aw//2
            p[1] += height*3//4-border_thick*2-aw//4
        for p in up_points:
            p[0] += width-border_thick*4-aw//2
            p[1] += height//4+border_thick*2+aw//4

        clr = highlight if self._has_focus else foreground
        pg.draw.polygon(surf, clr, down_points, 0)
        pg.draw.polygon(surf, clr, up_points, 0)

    def update(self, delta_time):
        if self._items:
            self._text = self._items[self._item_idx]
        else:
            self._text = "No Items"
        super().update(delta_time)

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        if isinstance(items, list):
            self._items = items
            self.dirty = True
        elif isinstance(items, str):
            self._items.append(str)
            self.dirty = True
        else:
            print("Unsupported item added to choicebox")

    def on_keydown(self, key_event):
        if key_event.key == pg.K_UP:
            self._item_idx -= 1
            if self._item_idx < 0: self._item_idx = len(self._items)-1
            self.dirty = True
        elif key_event.key == pg.K_DOWN:
            self._item_idx += 1
            if self._item_idx > len(self._items)-1: self._item_idx = 0
            self.dirty = True

    def on_mousedown(self):
        super().on_mousedown()
        if not self.has_focus:
            self.has_focus = True
            self.dirty = True

    def on_mouseup(self, hit = False):
        super().on_mouseup(hit)