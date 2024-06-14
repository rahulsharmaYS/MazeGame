#Code in place libraries used only!

from graphics import Canvas
import random
import time

#constants for different difficulty levels
DIFFICULTY_SETTINGS = {
    'Easy': (400, 16, 0.8, 10),
    'Medium': (400, 16, 0.6, 10),
    'Hard': (560, 16, 0.4, 15),
    'Very Hard': (560, 16, 0.2, 15),
    'Impossible': (560, 16, 0.1, 20)
}

#generating a random maze
def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]
    stack = [(1, 1)]
    maze[1][1] = 0

    while stack:
        current = stack[-1]
        neighbors = []

        for direction in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
            nx, ny = current[0] + direction[0], current[1] + direction[1]
            if 0 < nx < height and 0 < ny < width and maze[nx][ny] == 1:
                neighbors.append((nx, ny))

        if neighbors:
            next_cell = random.choice(neighbors)
            maze[next_cell[0]][next_cell[1]] = 0
            maze[(next_cell[0] + current[0]) // 2][(next_cell[1] + current[1]) // 2] = 0
            stack.append(next_cell)
        else:
            stack.pop()

    return maze

#rendering the maze
def draw_maze(canvas, maze, cell_size):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 1:
                canvas.create_rectangle(
                    x * cell_size, y * cell_size,
                    (x + 1) * cell_size, (y + 1) * cell_size,
                    'black'
                )

#Player moves
def move_player(canvas, player, maze, endpoint, blue_path, cell_size):
    key = canvas.get_last_key_press()
    if not key:
        return False

    player_coords = canvas.coords(player)
    player_x, player_y = player_coords[0], player_coords[1]
    next_x, next_y = player_x, player_y

    if key == 'a' and player_x > cell_size:  # Left
        next_x -= cell_size
    elif key == 'd' and player_x < len(maze[0]) * cell_size - cell_size * 2:  # Right
        next_x += cell_size
    elif key == 'w' and player_y > cell_size:  # Up
        next_y -= cell_size
    elif key == 's' and player_y < len(maze) * cell_size - cell_size * 2:  # Down
        next_y += cell_size
    else:
        return False

    next_cell_x = next_x // cell_size
    next_cell_y = next_y // cell_size
    if maze[next_cell_y][next_cell_x] == 0:
        canvas.move(player, next_x - player_x, next_y - player_y)
        if (next_x, next_y) not in blue_path:
            blue_path.append((next_x, next_y))

    if next_cell_x == endpoint[0] and next_cell_y == endpoint[1]:
        canvas.create_text(len(maze[0]) * cell_size // 4, len(maze) * cell_size // 2, text="Congratulations!", color="blue", font='Arial', font_size=30)
        return True

    return False

#follow blue path with delayed movement
def follow_blue_path(canvas, red_player, blue_path, red_index, cell_size):
    if red_index < len(blue_path):
        next_x, next_y = blue_path[red_index]
        red_coords = canvas.coords(red_player)
        canvas.move(red_player, next_x - red_coords[0], next_y - red_coords[1])
        return red_index + 1
    return red_index

#starting of the game
def start_game(difficulty):
    canvas_size, cell_size, red_chasing_speed, chase_time = DIFFICULTY_SETTINGS[difficulty]

    #creating new canvas for every game
    canvas = Canvas(canvas_size, canvas_size)
    grid_size = canvas_size // cell_size

    #generating and drawing new maze
    maze = generate_maze(grid_size, grid_size)
    draw_maze(canvas, maze, cell_size)

    #Our player
    blue_player = canvas.create_rectangle(
        cell_size, cell_size, cell_size * 2, cell_size * 2, 'blue'
    )

    #red player at the same position as our player
    red_player = canvas.create_rectangle(
        cell_size, cell_size, cell_size * 2, cell_size * 2, 'red'
    )

    #making a list to store blue's path
    blue_path = [(cell_size, cell_size)]

    print(f"Starting the game at {difficulty} level...")
    print(f"You have {chase_time} seconds to run. Click on the canvas screen to start moving your player!")

    #main_loop
    chase_start_time = time.time() + chase_time  # Start chasing after chase_time seconds
    player_move_time = time.time() + 0.1
    red_move_time = chase_start_time + red_chasing_speed  # Red player moves every red_chasing_speed seconds
    red_index = 0

    while True:
        #handling our player movement
        if move_player(canvas, blue_player, maze, (grid_size - 2, grid_size - 2), blue_path, cell_size):
            return True

        #handling red movement and collision detection
        if time.time() >= chase_start_time:
            if time.time() >= red_move_time:
                red_index = follow_blue_path(canvas, red_player, blue_path, red_index, cell_size)
                red_move_time = time.time() + red_chasing_speed

            # checking collision only if chase_start_time has passed
            red_coords = canvas.coords(red_player)
            blue_coords = canvas.coords(blue_player)

            #checks if red player overlaps with blue player(within a small margin)
            if (abs(red_coords[0] - blue_coords[0]) < cell_size / 2 and
                abs(red_coords[1] - blue_coords[1]) < cell_size / 2):
                canvas.create_text(canvas_size // 2, canvas_size // 2, text="Game Over!", color="red", font='Arial', font_size=30)
                return False

        canvas.sleep(0.01)  #trying my best to optimize the game :|

def show_initial_message():
    welcome_canvas = Canvas(500, 400)
    welcome_canvas.create_text(100, 50, text="Welcome to Maze Game", color="Brown", font='Papyrus', font_size=30)
    welcome_canvas.create_text(170, 90, text="Small Disclaimer: ", color="Gray", font='Lucida Console', font_size=20)
    welcome_canvas.create_text(80, 120, text="You might experience some lag while playing.", color="black", font='Lucida Handwriting', font_size=14)
    welcome_canvas.create_text(60, 150, text="Because of using basic coding and CIP libraries only,", color="black", font='Lucida Handwriting', font_size=14)
    welcome_canvas.create_text(80, 180, text="it became a little difficult for me to optimize :/", color="black", font='Lucida Handwriting', font_size=14)
    welcome_canvas.create_text(110, 210, text="Set difficulty to Easy if you feel the lag!", color="black", font='Lucida Handwriting', font_size=14)
    welcome_canvas.create_text(190, 240, text="Anyway Let's enjoy!", color="black", font='Lucida Handwriting', font_size=14)
    welcome_canvas.create_text(10, 270, text="Goal: ", color="Green", font='Lucida Console', font_size=20)
    welcome_canvas.create_text(10, 300, text="To move blue player to the Bottom Right Corner through the maze before Red catches you!", color="black", font='Arial', font_size=12)
    welcome_canvas.create_text(10, 330, text="Use WSAD keys to move", color="black", font='Arial', font_size=12)
    welcome_canvas.create_text(65, 360, text="Feel free to suggest improvements and optimizations for this game if you like it!", color="black", font='Garamond', font_size=14)
    welcome_canvas.create_text(200, 380, text ="https://github.com/rahulsharmaYS/MazeGame", color='black',font='Roboto',font_size=14) 
    welcome_canvas.sleep(10)
    welcome_canvas.clear()

show_initial_message()
#difficulty selection loop
difficulty = input("Enter your choice (Easy, Medium, Hard, Very Hard, Impossible): ")
if difficulty not in DIFFICULTY_SETTINGS:
    print("Invalid choice. Setting difficulty to Easy.")
    difficulty = 'Easy'

while True:
    if start_game(difficulty):
        current_difficulty_index = list(DIFFICULTY_SETTINGS.keys()).index(difficulty)
        next_difficulty_index = (current_difficulty_index + 1) % len(DIFFICULTY_SETTINGS)
        if next_difficulty_index == 0:
            print("Congratulations! You have cleared all difficulty levels! 🎉")
            print("My developer could only do up to Very Hard, so that's as tough as it gets!")
            print("Feel free to replay or suggest improvements to the game.")
            print("Github: https://github.com/rahulsharmaYS/MazeGame")
            break
        else:
            difficulty = list(DIFFICULTY_SETTINGS.keys())[next_difficulty_index]
            print(f"Next difficulty level: {difficulty}")
    else:
        break
