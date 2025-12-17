import turtle as myName
import math
import colorsys

# global constants for window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

NAME = "Nader Abdelshahid"
FONT_NAME = "Arial"
FONT_SIZE = 64
FONT_STYLE = "bold"
DEPTH_LAYERS = 10  # number of layers used to fake extrusion (back -> front)
ANIMATION_DELAY_MS = 40  # delay between frames in milliseconds


def init():
    """
    Initialize the drawing coordinate system and screen.
    """
    screen = myName.Screen()
    screen.title("Nader Abdelshahid - 3D Animated")
    screen.setup(WINDOW_WIDTH, WINDOW_HEIGHT)
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


def prepare_letters(name):
    """Return list of (char, x, y) positions centered on screen.

    We estimate character width from FONT_SIZE. This is an approximation but
    works well for monospaced spacing of letters drawn with turtle.write.
    """
    # approximate width per character
    char_w = FONT_SIZE * 0.6
    letters = list(name)
    total_w = char_w * len(letters)
    start_x = -total_w / 2 + char_w / 2
    positions = []
    y = 0
    for i, ch in enumerate(letters):
        x = start_x + i * char_w
        positions.append((ch, x, y))
    return positions


def draw_frame(t, positions, frame):
    """Draw a single animation frame. Clears previous frame before drawing."""
    t.clear()
    angle = math.radians(frame)

    # loop letters and draw depth layers back-to-front
    for i, (ch, base_x, base_y) in enumerate(positions):
        # compute a time-varying hue per letter so each cycles colors smoothly
        # hue_base spreads letters across the spectrum; hue_shift animates over time
        hue_base = (i / max(1, len(positions))) % 1.0
        hue_shift = (frame % 360) / 360.0  # 0..1 over one full rotation
        hue = (hue_base + hue_shift) % 1.0
        base_rgb = hsv_to_rgb255(hue, 0.85, 0.95)

        # small per-letter phase so extrusion motion is slightly offset
        phase = i * 0.18

        # Draw from back to front so front layers overwrite
        for layer in range(DEPTH_LAYERS, -1, -1):
            # depth offset simulates rotation around a virtual vertical axis
            depth = layer
            depth_scale = 0.8
            offset_x = depth * math.cos(angle + phase) * depth_scale
            offset_y = depth * math.sin(angle + phase) * depth_scale * 0.45

            # shade the color so deeper layers are darker
            shade = 1.0 - (depth / (DEPTH_LAYERS + 3)) * 0.7
            r = max(0, min(255, int(base_rgb[0] * shade)))
            g = max(0, min(255, int(base_rgb[1] * shade)))
            b = max(0, min(255, int(base_rgb[2] * shade)))

            t.color((r, g, b))
            t.penup()
            # write centered on the computed position
            t.goto(base_x + offset_x, base_y + offset_y - FONT_SIZE * 0.35)
            t.pendown()
            # For space just advance without writing
            if ch != ' ':
                t.write(ch, align="center", font=(FONT_NAME, FONT_SIZE, FONT_STYLE))

    # small highlight pass: write a thinner white highlight at the very front
    highlight_phase = 0.15
    for i, (ch, base_x, base_y) in enumerate(positions):
        if ch == ' ':
            continue
        offset_x = math.cos(angle + i * highlight_phase) * 0.3
        offset_y = math.sin(angle + i * highlight_phase) * 0.15
        t.color((255, 255, 255))
        t.penup()
        t.goto(base_x + offset_x, base_y + offset_y - FONT_SIZE * 0.35)
        t.pendown()
        t.write(ch, align="center", font=(FONT_NAME, int(FONT_SIZE * 0.18), "normal"))


def animate(screen, t, positions, frame=0):
    """Animation callback using ontimer so the window remains responsive."""
    draw_frame(t, positions, frame)
    screen.update()
    # schedule next frame
    screen.ontimer(lambda: animate(screen, t, positions, (frame + 4) % 360), ANIMATION_DELAY_MS)


def main():
    screen = init()
    t = myName.Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()

    positions = prepare_letters(NAME)

    # start animation
    animate(screen, t, positions, frame=0)

    # allow user to click to exit
    screen.listen()
    screen.onkey(screen.bye, "q")
    screen.onclick(lambda x, y: screen.bye())
    screen.mainloop()


if __name__ == "__main__":
    main()
