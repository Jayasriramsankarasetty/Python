from tkinter import *
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from PIL import ImageTk
from PIL import Image, ImageDraw

# from PIL.ImageDraw import ImageDraw


class Paint:
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()
        self.root.title('Paint')
        self.root.geometry('700x500')
        self.root.maxsize(700, 500)
        self.root.minsize(700, 500)

        # Top row buttons (save, undo, redo, clear, zoom in, zoom out)
        self.top_row_frame = Frame(self.root, width=700, height=40, bg='#4c4c4c')
        self.top_row_frame.place(x=0, y=0)

        # Save button
        self.save_button = Button(self.top_row_frame, text="Save", command=self.save, bg='#4c4c4c', fg='white')
        self.save_button.grid(row=0, column=0, padx=5)

        # Undo button
        self.undo_button = Button(self.top_row_frame, text="Undo", command=self.undo, bg='#4c4c4c', fg='white')
        self.undo_button.grid(row=0, column=1, padx=5)


        # Clear button
        self.clear_button = Button(self.top_row_frame, text="Clear", command=self.clear_canvas, bg='#4c4c4c', fg='white')
        self.clear_button.grid(row=0, column=3, padx=5)


        # Pen size slider
        self.pen_size_slider = Scale(self.top_row_frame, from_=1, to=10, orient=HORIZONTAL)
        self.pen_size_slider.set(5)
        self.pen_size_slider.grid(row=0, column=6, padx=5)

        # Tools frame (left side tools section)
        self.paint_tools = Frame(self.root, width=100, height=500, relief=RIDGE, borderwidth=2, bg='#4c4c4c')
        self.paint_tools.place(x=0, y=40)

        # Pen tool button
        self.pen_logo = ImageTk.PhotoImage(Image.open('pen.png'))
        self.pen_button = Button(self.paint_tools, text="Pen", padx=6, image=self.pen_logo, borderwidth=2, command=self.use_pen, bg='#4c4c4c', fg='white')
        self.pen_button.place(x=10, y=10)

        # Brush tool button
        self.brush_logo = ImageTk.PhotoImage(Image.open('brush.png'))
        self.brush_button = Button(self.paint_tools, text="Brush", image=self.brush_logo, borderwidth=2, command=self.use_brush, bg='#4c4c4c', fg='white')
        self.brush_button.place(x=10, y=50)

        # Color chooser button
        self.color_logo = ImageTk.PhotoImage(Image.open('color.png'))
        self.color_button = Button(self.paint_tools, image=self.color_logo, borderwidth=2, command=self.choose_color, bg='#4c4c4c', fg='white')
        self.color_button.place(x=10, y=90)

        # Eraser tool button
        self.eraser_logo = ImageTk.PhotoImage(Image.open('eraser.png'))
        self.eraser_button = Button(self.paint_tools, text='Eraser', image=self.eraser_logo, borderwidth=2, command=self.use_eraser, bg='#4c4c4c', fg='white')
        self.eraser_button.place(x=10, y=130)

        self.shape_button_line = Label(self.paint_tools, text="Shapes", bg='#4c4c4c', fg='white',
                                 font=("Arial", 14, "bold"))
        self.shape_button_line.place(x=8, y=163)  # Center title between buttons

        # Shape tool buttons
        self.shape_button_line_logo = ImageTk.PhotoImage(Image.open('line.png'))
        self.shape_button_line = Button(self.paint_tools,image=self.shape_button_line_logo , text="Line", command=self.activate_line, bg='#4c4c4c', fg='white', relief=RAISED)
        self.shape_button_line.place(x=10, y=195)

        self.shape_button_rectangle_logo = ImageTk.PhotoImage(Image.open('Rectangle.png'))
        self.shape_button_rectangle = Button(self.paint_tools, image=self.shape_button_rectangle_logo, borderwidth=2, command=self.activate_rectangle, bg='#4c4c4c', fg='white', relief=RAISED)
        self.shape_button_rectangle.place(x=10, y=230)

        self.shape_button_circle_logo = ImageTk.PhotoImage(Image.open('Circle.png'))
        self.shape_button_circle = Button(self.paint_tools, image=self.shape_button_circle_logo, borderwidth=2, command=self.activate_circle, bg='#4c4c4c', fg='white', relief=RAISED)
        self.shape_button_circle.place(x=10, y=265)

        self.shape_button_square_logo = ImageTk.PhotoImage(Image.open('Square.png'))
        self.shape_button_square = Button(self.paint_tools, image=self.shape_button_square_logo, borderwidth=2, command=self.activate_square, bg='#4c4c4c', fg='white', relief=RAISED)
        self.shape_button_square.place(x=10, y=300)

        self.shape_button_triangle_logo = ImageTk.PhotoImage(Image.open('Triangle.png'))
        self.shape_button_triangle = Button(self.paint_tools, image=self.shape_button_triangle_logo, borderwidth=2, command=self.activate_triangle, bg='#4c4c4c', fg='white', relief=RAISED)
        self.shape_button_triangle.place(x=10, y=335)

        self.shape_button_diamond_logo = ImageTk.PhotoImage(Image.open('Diamond.png'))
        self.shape_button_diamond = Button(self.paint_tools, image=self.shape_button_diamond_logo, borderwidth=2, command=self.activate_diamond, bg='#4c4c4c', fg='white', relief=RAISED)
        self.shape_button_diamond.place(x=10, y=370)

        # Main drawing canvas
        self.c = Canvas(self.root, bg='white', width=600, height=500, relief=RIDGE, borderwidth=0)
        self.c.place(x=100, y=40)

        # Setup initial state
        self.setup()

        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.pen_size_slider.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.drawing_line = False
        self.drawing_rectangle = False
        self.drawing_circle = False
        self.drawing_square = False
        self.drawing_triangle = False
        self.drawing_diamond = False
        self.active_button = self.pen_button
        self.shape_preview = None  # Holds the preview shape ID for line/rectangle/circle
        self.actions = []  # Store all actions for undo
        self.redo_actions = []  # Store actions for redo

        self.c.bind('<ButtonPress-1>', self.on_press)
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)
        self.eraser_on = False
        self.drawing_line = False
        self.drawing_rectangle = False
        self.drawing_circle = False
        self.drawing_square = False
        self.drawing_triangle = False
        self.drawing_diamond = False

    def use_brush(self):
        self.activate_button(self.brush_button)
        self.eraser_on = False
        self.drawing_line = False
        self.drawing_rectangle = False
        self.drawing_circle = False
        self.drawing_square = False
        self.drawing_triangle = False
        self.drawing_diamond = False

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_line(self):
        self.drawing_line = True
        self.drawing_rectangle = False
        self.drawing_circle = False
        self.drawing_square = False
        self.drawing_triangle = False
        self.drawing_diamond = False

    def activate_rectangle(self):
        self.drawing_line = False
        self.drawing_rectangle = True
        self.drawing_circle = False
        self.drawing_square = False
        self.drawing_triangle = False
        self.drawing_diamond = False

    def activate_circle(self):
        self.drawing_line = False
        self.drawing_rectangle = False
        self.drawing_circle = True
        self.drawing_square = False
        self.drawing_triangle = False
        self.drawing_diamond = False

    def activate_square(self):
        self.drawing_line = False
        self.drawing_rectangle = False
        self.drawing_circle = False
        self.drawing_square = True
        self.drawing_triangle = False
        self.drawing_diamond = False

    def activate_triangle(self):
        self.drawing_line = False
        self.drawing_rectangle = False
        self.drawing_circle = False
        self.drawing_square = False
        self.drawing_triangle = True
        self.drawing_diamond = False

    def activate_diamond(self):
        self.drawing_line = False
        self.drawing_rectangle = False
        self.drawing_circle = False
        self.drawing_square = False
        self.drawing_triangle = False
        self.drawing_diamond = True

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def on_press(self, event):
        self.old_x = event.x
        self.old_y = event.y

    def paint(self, event):
        self.line_width = self.pen_size_slider.get()
        paint_color = 'white' if self.eraser_on else self.color

        if any([self.drawing_line, self.drawing_rectangle, self.drawing_circle,
                self.drawing_square, self.drawing_triangle, self.drawing_diamond]):
            # Handle shapes
            if self.shape_preview:
                self.c.delete(self.shape_preview)
            if self.drawing_line:
                self.shape_preview = self.c.create_line(
                    self.old_x, self.old_y, event.x, event.y, width=self.line_width, fill=paint_color)
            elif self.drawing_rectangle:
                self.shape_preview = self.c.create_rectangle(
                    self.old_x, self.old_y, event.x, event.y, outline=paint_color, width=self.line_width)
            elif self.drawing_circle:
                radius = max(abs(event.x - self.old_x), abs(event.y - self.old_y))
                self.shape_preview = self.c.create_oval(
                    self.old_x - radius, self.old_y - radius, self.old_x + radius, self.old_y + radius,
                    outline=paint_color, width=self.line_width)
            elif self.drawing_square:
                side = max(abs(event.x - self.old_x), abs(event.y - self.old_y))
                self.shape_preview = self.c.create_rectangle(
                    self.old_x, self.old_y, self.old_x + side, self.old_y + side, outline=paint_color,
                    width=self.line_width)
            elif self.drawing_triangle:
                base_mid_x = (self.old_x + event.x) // 2
                points = [
                    base_mid_x, self.old_y,  # Top vertex
                    self.old_x, event.y,  # Bottom-left vertex
                    event.x, event.y  # Bottom-right vertex
                ]
                self.shape_preview = self.c.create_polygon(points, outline=paint_color, fill="", width=self.line_width)
            elif self.drawing_diamond:
                mid_x = (self.old_x + event.x) // 2
                mid_y = (self.old_y + event.y) // 2
                points = [
                    mid_x, self.old_y,  # Top vertex
                    event.x, mid_y,  # Right vertex
                    mid_x, event.y,  # Bottom vertex
                    self.old_x, mid_y  # Left vertex
                ]
                self.shape_preview = self.c.create_polygon(points, outline=paint_color, fill="", width=self.line_width)
        else:
            # Handle free drawing for pen, brush, or eraser
            if self.old_x and self.old_y:
                self.actions.append(self.c.create_line(
                    self.old_x, self.old_y, event.x, event.y,
                    width=self.line_width, fill=paint_color, capstyle=ROUND, smooth=True))
            self.old_x = event.x
            self.old_y = event.y

    def reset(self, event):
        if self.shape_preview:
            self.actions.append(self.shape_preview)
            self.shape_preview = None
        self.old_x, self.old_y = None, None
        self.redo_actions.clear()  # Clear redo stack after new action

    def clear_canvas(self):
        self.c.delete("all")
        self.actions.clear()
        self.redo_actions.clear()

    def undo(self):
        if self.actions:
            last_action = self.actions.pop()
            self.c.delete(last_action)
            self.redo_actions.append(last_action)

    def save(self):
        # Ask the user for a file name and location to save the file
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg"),
                                                            ("All files", "*.*")])
        if file_path:
            # Create a Pillow image with the size of the canvas
            canvas_width = self.c.winfo_width()
            canvas_height = self.c.winfo_height()
            image = Image.new("RGB", (canvas_width, canvas_height), "white")
            draw = ImageDraw.Draw(image)

            # Draw the canvas content onto the Pillow image
            items = self.c.find_all()
            for item in items:
                coords = self.c.coords(item)
                item_type = self.c.type(item)
                color = self.c.itemcget(item, "fill") or "black"

                # Safely convert width to an integer
                width_str = self.c.itemcget(item, "width")
                try:
                    width = int(float(width_str))  # Convert '5.0' -> 5
                except ValueError:
                    width = 1  # Default to 1 if width is invalid

                if item_type == "line":
                    draw.line(coords, fill=color, width=width)
                elif item_type == "rectangle":
                    draw.rectangle(coords, outline=color, width=width)
                elif item_type == "oval":
                    draw.ellipse(coords, outline=color, width=width)
                elif item_type == "polygon":
                    draw.polygon(coords, outline=color, width=width)

            # Save the image
            image.save(file_path)


if __name__ == '__main__':
    Paint()

