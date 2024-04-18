# snake game with python that shows score too
class Game:
    def __init__(self):
        self.score = 0

    def start(self):
        # game loop
        while True:
            # get user input
            direction = input("Enter direction (w, a, s, d): ")

            # update game state
            if direction == "w":
                self.snake.move_up()
            elif direction == "a":
                self.snake.move_left()
            elif direction == "s":
                self.snake.move_down()
            elif direction == "d":
                self.snake.move_right()

            # check for collisions
            if self.snake.head.x == self.food.x and self.snake.head.y == self.food.y:
                self.score += 1
    
    
def main():
    game = Game()
    game.start()

if __name__ == "__main__":
    main()