#Code in place libraries used only!

from graphics import Canvas
import random
import time

#constants for different difficulty levels
DIFFICULTY_SETTINGS = {
    'Easy': (400, 16, 0.8, 10),
    'Medium': (400, 16, 0.6, 12),
    'Hard': (560, 16, 0.3, 12),
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
                    'grey'
                )

#Player_moves
def move_player(canvas, player, maze, endpoint, blue_path, cell_size):
    key = canvas.get_last_key_press()
    if not key:
        return False

    player_coords = canvas.coords(player)
    player_x, player_y = player_coords[0], player_coords[1]
    next_x, next_y = player_x, player_y

    if key == 'a' and player_x > cell_size:  #Left
        next_x -= cell_size
    elif key == 'd' and player_x < len(maze[0]) * cell_size - cell_size * 2:  # Right
        next_x += cell_size
    elif key == 'w' and player_y > cell_size:  #up
        next_y -= cell_size
    elif key == 's' and player_y < len(maze) * cell_size - cell_size * 2:  #down
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

    #xreating new canvas for every game
    canvas = Canvas(canvas_size, canvas_size)
    grid_size = canvas_size // cell_size

    #generating and drawing new maze
    maze = generate_maze(grid_size, grid_size)
    draw_maze(canvas, maze, cell_size)

    #our player
    blue_player = canvas.create_rectangle(
        cell_size, cell_size, cell_size * 2, cell_size * 2, 'blue'
    )

    #red player atthe same position as our player
    red_player = canvas.create_rectangle(
        cell_size, cell_size, cell_size * 2, cell_size * 2, 'red'
    )

    #Making a list to store blue's path
    blue_path = [(cell_size, cell_size)]

    #Displaying the game start message for 3 seconds
    message_text = f"Starting the game at {difficulty} level.\nYou have {chase_time} seconds to run."
    message_id = canvas.create_text(canvas_size // 2, canvas_size // 2, text=message_text, color="black", font='Arial', font_size=14)
    canvas.sleep(3)
    canvas.delete(message_id)

    print(f"Starting the game at {difficulty} level...")
    print(f"You have {chase_time} seconds to run.")

    #mainloop
    chase_start_time = time.time() + chase_time
    red_move_time = chase_start_time + red_chasing_speed
    red_index = 0

    while True:
        #handling our player moment
        if move_player(canvas, blue_player, maze, (grid_size - 2, grid_size - 2), blue_path, cell_size):
            return True

        #handling red movement and collision detection
        if time.time() >= chase_start_time:
            if time.time() >= red_move_time:
                red_index = follow_blue_path(canvas, red_player, blue_path, red_index, cell_size)
                red_move_time = time.time() + red_chasing_speed

            #checking collision only if chase_start_time has passed
            red_coords = canvas.coords(red_player)
            blue_coords = canvas.coords(blue_player)

            #checks if red player overlaps with blue player (within a small margin)
            if (abs(red_coords[0] - blue_coords[0]) < cell_size / 2 and
                abs(red_coords[1] - blue_coords[1]) < cell_size / 2):
                canvas.create_text(canvas_size // 8, canvas_size // 2, text="Game Over! Try Again!", color="red", font='Roboto', font_size=30)
                time.sleep(3)
                return False

        canvas.sleep(0.01)  #trying my best to optimize the game :|

#function to display the initial messages
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
    welcome_canvas.create_text(2, 300, text="-> To move blue player to the Bottom Right Corner through the maze before Red catches you!", color="black", font='Arial', font_size=12)
    welcome_canvas.create_text(2, 330, text="-> Use WSAD keys to move. Your player is beneath red so move and it will come out!", color="black", font='Arial', font_size=12)
    welcome_canvas.create_text(65, 360, text="Feel free to suggest improvements and optimizations for this game if you like it!", color="grey", font='Garamond', font_size=14)
    welcome_canvas.create_text(240, 380, text ="https://github.com/rahulsharmaYS/MazeGame", color='grey',font='Roboto',font_size=12)
    
    welcome_canvas.sleep(3)
    #welcome_canvas.clear()
    while True:
        click = welcome_canvas.get_last_click()
        if click is not None:
            break
    welcome_canvas.clear()
#function to select difficulty level
def select_difficulty():
    difficulty_canvas = Canvas(500, 400)
    difficulty_canvas.create_text(120, 50, text="Select Difficulty Level", color="Brown", font='Papyrus', font_size=30)
    y_position = 100
    difficulty_options = list(DIFFICULTY_SETTINGS.keys())
    
    #adjusting the starting y-position and the increment between difficulty options
    for difficulty in difficulty_options:
        difficulty_canvas.create_text(120, y_position, text=difficulty, color="black", font='Papyrus', font_size=20)
        y_position += 50
    
    selected_difficulty = None
    while not selected_difficulty:
        click = difficulty_canvas.get_last_click()
        if click:
            click_x, click_y = click
            #determining the selected difficulty based on the y-position of the click
            for i, difficulty in enumerate(difficulty_options):
                if 100 + i * 50 <= click_y <= 150 + i * 50:
                    selected_difficulty = difficulty
                    break
    
    difficulty_canvas.clear()
    return selected_difficulty

#Function to display congrats message and next level prompt
def display_congrats_message(next_difficulty=None):
    congrats_canvas = Canvas(500, 400)
    if next_difficulty:
        congrats_canvas.create_text(100, 200, text=f"🎉Congratulations! Now try {next_difficulty} level!🎉", color="Green", font='Arial', font_size=20)
    else:
        congrats_canvas.create_text(30, 100, text="🎉Congratulations! You have cleared all difficulty levels! 🎉", color="Green", font='Arial', font_size=16)
        congrats_canvas.create_text(30, 150, text="My developer could only do up to Very Hard, so that's as tough as it gets!", color="black", font='Arial', font_size=14)
        congrats_canvas.create_text(30, 200, text="Feel free to replay or suggest improvements to the game.", color="black", font='Arial', font_size=14)
        congrats_canvas.create_text(30, 250, text="Github: https://github.com/rahulsharmaYS/MazeGame", color="black", font='Arial', font_size=14)
    time.sleep(10)
    congrats_canvas.clear()


#Main flow execution of how game interpretes
show_initial_message()

while True:
    difficulty = select_difficulty()
    if not difficulty or difficulty not in DIFFICULTY_SETTINGS:
        print("Invalid choice. Setting difficulty to Easy.")
        difficulty = 'Easy'
    
    while True:
        if start_game(difficulty):
            current_difficulty_index = list(DIFFICULTY_SETTINGS.keys()).index(difficulty)
            next_difficulty_index = (current_difficulty_index + 1) % len(DIFFICULTY_SETTINGS)
            if next_difficulty_index == 0:
                display_congrats_message()
                break
            else:
                difficulty = list(DIFFICULTY_SETTINGS.keys())[next_difficulty_index]
                display_congrats_message(difficulty)
        else:
            break
