"""Text Animator Studio using the turtle module.

This module provides an interactive text animation application built with
the standard library `turtle` graphics. It is intended as a small GUI demo
and is exercised by the project's tests.
"""

# Allow this module to keep its original name and acknowledge that some
# turtle attributes are detected dynamically by the runtime; disable those
# pylint checks here. Also relax complexity and whitespace checks for this
# single-file demo application.
# pylint: disable=invalid-name,no-member,c0303,r0915,r0914,w0613,w0603
import turtle as myName
import math
import colorsys

# global constants for window dimensions
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600

NAME = ""  # Will be set by user input
FONT_NAME = "Arial"
FONT_SIZE = 64
FONT_STYLE = "bold"
DEPTH_LAYERS = 10  # number of layers used to fake extrusion (back -> front)
ANIMATION_DELAY_MS = 40  # delay between frames in milliseconds

# Animation type selection
ANIMATION_TYPE = "3d_rotation"

# Menu state
SHOW_MENU = True
IS_ANIMATING = False
MENU_TURTLE = None  # Separate turtle for persistent menu


def init():
    """
    Initialize the drawing coordinate system and screen.
    """
    screen = myName.Screen()
    screen.title("Text Animator Studio")
    screen.setup(WINDOW_WIDTH, WINDOW_HEIGHT)
    screen.bgcolor("black")  # Set background to black
    # choose coordinates so (0,0) is near the center
    myName.setworldcoordinates(-WINDOW_WIDTH/2, -WINDOW_HEIGHT/2,
                              WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    # Use 255-based RGB tuples
    screen.colormode(255)
    # Turn off automatic animation updates for speed
    screen.tracer(0, 0)
    return screen


def hsv_to_rgb255(h, s, v):
    """Convert HSV (0..1) to 0..255 RGB tuple."""
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


def show_text_input_screen(t, screen, current_text="", show_cursor=True):
    """Show a text input prompt on the turtle screen."""
    t.clear()
    t.color(0, 255, 255)  # Cyan
    t.penup()
    
    # Title
    t.goto(0, 150)
    t.write("TEXT ANIMATOR STUDIO", align="center",
            font=("Arial", 36, "bold"))
    
    # Prompt
    t.color(255, 255, 255)  # White
    t.goto(0, 80)
    t.write("Enter your text to animate:", align="center",
            font=("Arial", 20, "normal"))
    
    # Show current input
    t.goto(0, 20)
    t.color(0, 255, 0)  # Green
    if current_text:
        t.write(current_text, align="center",
                font=("Arial", 24, "bold"))
    
    # Show blinking cursor after text
    if show_cursor:
        if current_text:
            # Position cursor after the last character
            # Approximate character width for Arial 24pt bold
            char_width = 15
            text_width = len(current_text) * char_width
            cursor_x = (text_width / 2) + 5
        else:
            cursor_x = 0
        t.goto(cursor_x, 18)  # Slightly lower for proper alignment
        t.write("_", align="left", font=("Arial", 24, "bold"))
    
    # Instructions
    t.goto(0, -40)
    t.color(255, 200, 0)  # Yellow
    t.write("Press ENTER when done", align="center",
            font=("Arial", 16, "italic"))
    
    t.goto(0, -80)
    t.color(150, 150, 150)  # Gray
    t.write("Backspace to delete | ESC for default",
            align="center", font=("Arial", 12, "normal"))
    
    screen.update()


def get_text_input(screen, t):
    """Get text input from user using keyboard on the turtle screen."""
    input_text = ""
    input_complete = [False]
    cursor_visible = [True]
    
    def add_char(char):
        nonlocal input_text
        if len(input_text) < 50:  # Limit length
            input_text += char
            show_text_input_screen(t, screen, input_text, cursor_visible[0])
    
    def backspace():
        nonlocal input_text
        if input_text:
            input_text = input_text[:-1]
            show_text_input_screen(t, screen, input_text, cursor_visible[0])
    
    def finish():
        input_complete[0] = True
    
    def use_default():
        nonlocal input_text
        input_text = "Your Name Here"
        input_complete[0] = True
    
    def blink_cursor():
        """Toggle cursor visibility for blinking effect."""
        if not input_complete[0]:
            cursor_visible[0] = not cursor_visible[0]
            show_text_input_screen(t, screen, input_text, cursor_visible[0])
            screen.ontimer(blink_cursor, 500)  # Blink every 500ms
    
    # Show initial screen
    show_text_input_screen(t, screen, input_text, True)
    
    # Start cursor blinking
    screen.ontimer(blink_cursor, 500)
    
    # Setup key bindings for all printable characters
    screen.listen()
    
    # Letters
    for char in "abcdefghijklmnopqrstuvwxyz":
        screen.onkey(lambda c=char: add_char(c), char)
        screen.onkey(lambda c=char.upper(): add_char(c), char.upper())
    
    # Numbers
    for num in "0123456789":
        screen.onkey(lambda n=num: add_char(n), num)
    
    # Space and common punctuation
    screen.onkey(lambda: add_char(" "), "space")
    screen.onkey(lambda: add_char("!"), "exclam")
    screen.onkey(lambda: add_char("."), "period")
    screen.onkey(lambda: add_char(","), "comma")
    screen.onkey(lambda: add_char("?"), "question")
    screen.onkey(lambda: add_char("-"), "minus")
    screen.onkey(lambda: add_char("'"), "apostrophe")
    
    # Control keys
    screen.onkey(backspace, "BackSpace")
    screen.onkey(finish, "Return")
    screen.onkey(use_default, "Escape")
    
    # Wait for input to complete
    while not input_complete[0]:
        screen.update()
    
    # Clear all key bindings used for input
    for char in "abcdefghijklmnopqrstuvwxyz":
        screen.onkey(None, char)
        screen.onkey(None, char.upper())
    for num in "0123456789":
        screen.onkey(None, num)
    screen.onkey(None, "space")
    screen.onkey(None, "exclam")
    screen.onkey(None, "period")
    screen.onkey(None, "comma")
    screen.onkey(None, "question")
    screen.onkey(None, "minus")
    screen.onkey(None, "apostrophe")
    screen.onkey(None, "BackSpace")
    screen.onkey(None, "Return")
    screen.onkey(None, "Escape")
    
    # Clear the input screen
    t.clear()
    screen.update()
    
    return input_text if input_text else "Your Name Here"


def draw_menu(menu_t, screen, show_confirmation=False,
              confirm_msg="", anim_t=None):
    """Draw the interactive menu on screen (persistent on sides)."""
    menu_t.clear()
    
    # LEFT SIDE MENU
    left_x = -520
    
    # Title - Left
    menu_t.color(0, 255, 255)  # Cyan
    menu_t.penup()
    menu_t.goto(left_x, 250)
    menu_t.write("TEXT", align="left", font=("Arial", 24, "bold"))
    menu_t.goto(left_x, 220)
    menu_t.write("ANIMATOR", align="left", font=("Arial", 24, "bold"))
    
    # Current name display
    menu_t.color(255, 200, 100)  # Orange
    menu_t.goto(left_x, 180)
    display_name = NAME if NAME else "[No name]"
    if len(display_name) > 15:
        display_name = display_name[:15] + "..."
    menu_t.write(f'Text: "{display_name}"', align="left",
                 font=("Arial", 12, "italic"))
    
    # Font Size Options - Left
    menu_t.color(255, 255, 255)  # White
    menu_t.goto(left_x, 140)
    menu_t.write("LETTER SIZE", align="left", font=("Arial", 16, "bold"))
    menu_t.goto(left_x, 120)
    menu_t.write("(Press 1-5)", align="left", font=("Arial", 12, "normal"))
    
    # Size options
    menu_t.color(100, 200, 255)
    size_options = [
        "1 = Small (32px)",
        "2 = Medium (48px)",
        "3 = Large (64px)",
        "4 = X-Large (80px)",
        "5 = Huge (96px)"
    ]
    
    y_pos = 90
    for option in size_options:
        menu_t.goto(left_x, y_pos)
        menu_t.write(option, align="left", font=("Arial", 11, "normal"))
        y_pos -= 22
    
    # Current settings
    menu_t.goto(left_x, -50)
    menu_t.color(0, 255, 0)  # Bright green
    if show_confirmation and confirm_msg:
        menu_t.write(confirm_msg, align="left", font=("Arial", 12, "bold"))
    else:
        menu_t.write(f"Size: {FONT_SIZE}px", align="left",
                     font=("Arial", 12, "normal"))
        menu_t.goto(left_x, -70)
        menu_t.write(f"Type: {ANIMATION_TYPE}", align="left",
                     font=("Arial", 12, "normal"))
    
    # RIGHT SIDE MENU
    right_x = 320
    
    # Animation Type Options - Right
    menu_t.color(255, 255, 255)  # White
    menu_t.goto(right_x, 140)
    menu_t.write("ANIMATION TYPE", align="left", font=("Arial", 16, "bold"))
    menu_t.goto(right_x, 120)
    menu_t.write("(Press A-E)", align="left", font=("Arial", 12, "normal"))
    
    # Animation options
    menu_t.color(100, 255, 150)
    anim_options = [
        "A = 3D Rotation",
        "B = Wave",
        "C = Spiral",
        "D = Bounce",
        "E = Rainbow Pulse"
    ]
    
    y_pos = 90
    for option in anim_options:
        menu_t.goto(right_x, y_pos)
        menu_t.write(option, align="left", font=("Arial", 11, "normal"))
        y_pos -= 22
    
    # Instructions - Right
    menu_t.goto(right_x, -50)
    menu_t.color(255, 200, 0)  # Bright orange-yellow
    status = "ANIMATING..." if IS_ANIMATING else "Press SPACE"
    menu_t.write(status, align="left", font=("Arial", 14, "bold"))
    
    menu_t.goto(right_x, -80)
    menu_t.color(255, 100, 100)  # Light red/pink
    menu_t.write("SPACE = Start", align="left", font=("Arial", 11, "normal"))
    menu_t.goto(right_x, -100)
    menu_t.write("M = Pause/Resume", align="left",
                 font=("Arial", 11, "normal"))
    menu_t.goto(right_x, -120)
    menu_t.write("N = New Name", align="left", font=("Arial", 11, "normal"))
    menu_t.goto(right_x, -140)
    menu_t.write("Q = Quit", align="left", font=("Arial", 11, "normal"))
    
    # Draw separator lines
    menu_t.color(100, 100, 100)  # Gray
    menu_t.goto(-300, 300)
    menu_t.setheading(270)
    menu_t.pendown()
    menu_t.goto(-300, -300)
    menu_t.penup()
    
    menu_t.goto(300, 300)
    menu_t.setheading(270)
    menu_t.pendown()
    menu_t.goto(300, -300)
    menu_t.penup()
    
    screen.update()


def prepare_letters(name):
    """Return list of (char, x, y) positions centered on screen.

    We estimate character width from FONT_SIZE. This is an approximation but
    works well for monospaced spacing of letters drawn with turtle.write.
    Automatically wraps text into multiple lines if too wide.
    """
    # Center area boundaries (between the menu panels)
    max_width = 550  # Maximum width for text (between x=-275 and x=275)
    
    # Calculate text width with current font size
    char_w = FONT_SIZE * 0.6
    line_height = FONT_SIZE * 1.2  # Spacing between lines
    
    # Split text into words
    words = name.split()
    if not words:
        return []
    
    # Build lines that fit within max_width
    lines = []
    current_line = []
    current_width = 0
    
    for word in words:
        word_width = len(word) * char_w
        space_width = char_w  # Width of a space
        
        # Check if adding this word exceeds max width
        test_width = current_width + word_width
        if current_line:  # Add space if not first word
            test_width += space_width
        
        if test_width <= max_width or not current_line:
            # Add word to current line
            if current_line:
                current_line.append(' ')
                current_width += space_width
            current_line.append(word)
            current_width += word_width
        else:
            # Start new line
            lines.append(''.join(current_line))
            current_line = [word]
            current_width = word_width
    
    # Add the last line
    if current_line:
        lines.append(''.join(current_line))
    
    # Calculate vertical centering
    total_height = len(lines) * line_height
    start_y = total_height / 2 - line_height / 2
    
    # Create positions for all characters
    positions = []
    for line_idx, line in enumerate(lines):
        y = start_y - (line_idx * line_height)
        line_width = len(line) * char_w
        start_x = -line_width / 2 + char_w / 2
        
        for char_idx, ch in enumerate(line):
            x = start_x + char_idx * char_w
            positions.append((ch, x, y))
    
    return positions


def draw_frame_3d_rotation(t, positions, frame):
    """3D rotation animation (original style)."""
    angle = math.radians(frame)

    # loop letters and draw depth layers back-to-front
    for i, (ch, base_x, base_y) in enumerate(positions):
        hue_base = (i / max(1, len(positions))) % 1.0
        hue_shift = (frame % 360) / 360.0
        hue = (hue_base + hue_shift) % 1.0
        base_rgb = hsv_to_rgb255(hue, 0.85, 0.95)
        phase = i * 0.18

        for layer in range(DEPTH_LAYERS, -1, -1):
            depth = layer
            depth_scale = 0.8
            offset_x = depth * math.cos(angle + phase) * depth_scale
            offset_y = depth * math.sin(angle + phase) * depth_scale * 0.45

            shade = 1.0 - (depth / (DEPTH_LAYERS + 3)) * 0.7
            r = max(0, min(255, int(base_rgb[0] * shade)))
            g = max(0, min(255, int(base_rgb[1] * shade)))
            b = max(0, min(255, int(base_rgb[2] * shade)))

            t.color((r, g, b))
            t.penup()
            t.goto(base_x + offset_x, base_y + offset_y - FONT_SIZE * 0.35)
            t.pendown()
            if ch != ' ':
                t.write(ch, align="center",
                        font=(FONT_NAME, FONT_SIZE, FONT_STYLE))


def draw_frame_wave(t, positions, frame):
    """Wave animation - letters move up and down in a wave pattern."""
    for i, (ch, base_x, base_y) in enumerate(positions):
        if ch == ' ':
            continue
        
        hue = ((frame + i * 15) % 360) / 360.0
        rgb = hsv_to_rgb255(hue, 0.85, 0.95)
        
        wave_offset_y = math.sin(math.radians(frame * 3 + i * 30)) * 30
        
        t.color(rgb)
        t.penup()
        t.goto(base_x, base_y + wave_offset_y - FONT_SIZE * 0.35)
        t.pendown()
        t.write(ch, align="center",
                font=(FONT_NAME, FONT_SIZE, FONT_STYLE))


def draw_frame_spiral(t, positions, frame):
    """Spiral animation - letters spiral around center."""
    for i, (ch, base_x, base_y) in enumerate(positions):
        if ch == ' ':
            continue
        
        hue = ((frame + i * 20) % 360) / 360.0
        rgb = hsv_to_rgb255(hue, 0.85, 0.95)
        
        angle = math.radians(frame * 2 + i * 25)
        radius = 20 + math.sin(math.radians(frame + i * 30)) * 15
        spiral_x = math.cos(angle) * radius
        spiral_y = math.sin(angle) * radius
        
        t.color(rgb)
        t.penup()
        t.goto(base_x + spiral_x, base_y + spiral_y - FONT_SIZE * 0.35)
        t.pendown()
        t.write(ch, align="center",
                font=(FONT_NAME, FONT_SIZE, FONT_STYLE))


def draw_frame_bounce(t, positions, frame):
    """Bounce animation - letters bounce up and down."""
    for i, (ch, base_x, base_y) in enumerate(positions):
        if ch == ' ':
            continue
        
        hue = (i / max(1, len(positions))) % 1.0
        rgb = hsv_to_rgb255(hue, 0.85, 0.95)
        
        bounce_phase = (frame * 4 + i * 20) % 360
        bounce_y = abs(math.sin(math.radians(bounce_phase))) * 50
        
        t.color(rgb)
        t.penup()
        t.goto(base_x, base_y + bounce_y - FONT_SIZE * 0.35)
        t.pendown()
        t.write(ch, align="center",
                font=(FONT_NAME, FONT_SIZE, FONT_STYLE))


def draw_frame_rainbow_pulse(t, positions, frame):
    """Rainbow pulse - letters pulse in size with rainbow colors."""
    for i, (ch, base_x, base_y) in enumerate(positions):
        if ch == ' ':
            continue
        
        hue = ((frame * 2 + i * 15) % 360) / 360.0
        rgb = hsv_to_rgb255(hue, 0.85, 0.95)
        
        pulse = 1.0 + math.sin(math.radians(frame * 3 + i * 25)) * 0.3
        pulse_size = int(FONT_SIZE * pulse)
        
        t.color(rgb)
        t.penup()
        t.goto(base_x, base_y - pulse_size * 0.35)
        t.pendown()
        t.write(ch, align="center",
                font=(FONT_NAME, pulse_size, FONT_STYLE))


def draw_frame(t, positions, frame):
    """Draw a single animation frame. Clears previous frame before drawing."""
    t.clear()
    
    # Select animation based on ANIMATION_TYPE
    if ANIMATION_TYPE == "wave":
        draw_frame_wave(t, positions, frame)
    elif ANIMATION_TYPE == "spiral":
        draw_frame_spiral(t, positions, frame)
    elif ANIMATION_TYPE == "bounce":
        draw_frame_bounce(t, positions, frame)
    elif ANIMATION_TYPE == "rainbow_pulse":
        draw_frame_rainbow_pulse(t, positions, frame)
    else:  # default to 3d_rotation
        draw_frame_3d_rotation(t, positions, frame)


def animate(screen, anim_t, menu_t, positions, frame=0):
    """Animation callback using ontimer so the window remains responsive."""
    # Always check if we should continue
    if not IS_ANIMATING:
        # Keep menu visible when paused (text stays frozen)
        draw_menu(menu_t, screen)
        screen.update()
        return
    
    draw_frame(anim_t, positions, frame)
    # Redraw menu to keep it visible
    draw_menu(menu_t, screen)
    screen.update()
    # schedule next frame only if still animating
    if IS_ANIMATING:
        next_frame = (frame + 4) % 360
        screen.ontimer(lambda: animate(screen, anim_t, menu_t,
                                        positions, next_frame),
                       ANIMATION_DELAY_MS)


def handle_size_key(key, screen, menu_t, anim_t, positions):
    """Handle font size selection."""
    global FONT_SIZE
    
    size_map = {"1": 32, "2": 48, "3": 64, "4": 80, "5": 96}
    if key in size_map:
        FONT_SIZE = size_map[key]
        # Update positions with new size (will wrap to multiple lines if needed)
        positions.clear()
        positions.extend(prepare_letters(NAME))
        draw_menu(menu_t, screen)


def handle_animation_key(key, screen, menu_t, anim_t):
    """Handle animation type selection."""
    global ANIMATION_TYPE
    
    anim_map = {
        "a": "3d_rotation",
        "b": "wave",
        "c": "spiral",
        "d": "bounce",
        "e": "rainbow_pulse"
    }
    if key in anim_map:
        ANIMATION_TYPE = anim_map[key]
        draw_menu(menu_t, screen)


def start_animation(screen, anim_t, menu_t, positions):
    """Start the animation after menu selection."""
    global IS_ANIMATING
    
    if not IS_ANIMATING:
        IS_ANIMATING = True
        animate(screen, anim_t, menu_t, positions, frame=0)
    draw_menu(menu_t, screen)


def toggle_animation(screen, anim_t, menu_t, positions):
    """Toggle animation on/off."""
    global IS_ANIMATING
    
    if IS_ANIMATING:
        # Pause the animation (keep text visible by not clearing)
        IS_ANIMATING = False
        draw_menu(menu_t, screen)
        screen.update()
    else:
        # Resume/start the animation
        IS_ANIMATING = True
        animate(screen, anim_t, menu_t, positions, frame=0)


def setup_main_keys(screen, menu_t, anim_t, positions):
    """Setup keyboard handlers for main menu."""
    screen.listen()
    
    # Size keys
    for key in "12345":
        screen.onkey(lambda k=key: handle_size_key(
            k, screen, menu_t, anim_t, positions), key)
    
    # Animation keys
    for key in "abcdeABCDE":
        screen.onkey(lambda k=key.lower(): handle_animation_key(
            k.lower(), screen, menu_t, anim_t), key)
    
    # Space to start/toggle
    screen.onkey(lambda: start_animation(
        screen, anim_t, menu_t, positions), "space")
    
    # M to pause/resume
    screen.onkey(lambda: toggle_animation(
        screen, anim_t, menu_t, positions), "m")
    
    # N to change name
    screen.onkey(lambda: change_name(
        screen, menu_t, anim_t, positions), "n")
    
    # Q to quit
    screen.onkey(screen.bye, "q")


def change_name(screen, menu_t, anim_t, positions):
    """Prompt user to enter a new name."""
    global NAME, IS_ANIMATING
    
    # Pause animation
    IS_ANIMATING = False
    # Immediately clear previous animated text so it doesn't linger
    anim_t.clear()
    # Refresh menu while entering input
    draw_menu(menu_t, screen)
    screen.update()
    
    # Get user input using on-screen keyboard
    new_name = get_text_input(screen, menu_t)
    
    if new_name and new_name.strip():
        NAME = new_name.strip()
        # Update positions with new name
        positions.clear()
        positions.extend(prepare_letters(NAME))
    
    # Rebind main menu keys
    setup_main_keys(screen, menu_t, anim_t, positions)
    
    # After changing name with N key, wait for SPACE to start
    IS_ANIMATING = False
    draw_menu(menu_t, screen)


def main():
    """Create screen/turtles, collect name and run animation loop."""
    global MENU_TURTLE, NAME
    
    screen = init()
    
    # Create turtle for input screen
    input_t = myName.Turtle()
    input_t.hideturtle()
    input_t.speed(0)
    input_t.penup()
    
    # Get user's name using on-screen input
    NAME = get_text_input(screen, input_t)
    
    # Create separate turtles for menu and animation
    menu_t = myName.Turtle()
    menu_t.hideturtle()
    menu_t.speed(0)
    menu_t.penup()
    MENU_TURTLE = menu_t
    
    anim_t = myName.Turtle()
    anim_t.hideturtle()
    anim_t.speed(0)
    anim_t.penup()

    positions = list(prepare_letters(NAME))

    # Setup keyboard handlers
    setup_main_keys(screen, menu_t, anim_t, positions)
    
    # Auto-start animation after initial text entry
    global IS_ANIMATING
    IS_ANIMATING = True
    animate(screen, anim_t, menu_t, positions, frame=0)
    
    screen.mainloop()


if __name__ == "__main__":
    main()
