import configparser
import os
import random


DEFAULT_HEIGHT = 40
DEFAULT_WIDTH = 40


class Game:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

    @staticmethod
    def from_config_file(config_path):
        configParser = configparser.RawConfigParser()
        configFilePath = config_path
        configParser.read(configFilePath)
        engineConfig = configParser.get('engine')
        width = engineConfig.getInt('width')
        height = engineConfig.getInt('height')
        return Game(height, width)

    @staticmethod
    def from_grid_config_file(config_path):
        config = open(config_path, 'r')
        row = 0
        lines = config.readlines()
        height = len(lines)
        width = len(lines[0])
        # padding to avoid index edge cases
        game = Game(height + 2, width + 2)
        for row in range(height):
            for col in range(width):
                # shift down and to the right by 1 to avoid index edge cases
                game.grid[row + 1][col +
                                   1] = 1 if lines[row][col] == '#' else 0
        return game

    @staticmethod
    def create_random():
        height = DEFAULT_HEIGHT
        width = DEFAULT_WIDTH
        game = Game(height + 2, width + 2)
        for row in range(height):
            for col in range(width):
                game.grid[row + 1][col + 1] = random.randint(0, 1)
        return game

    def get_neighbour_count(self, row: int, col: int):
        return sum([self.grid[i][j]
                    for i in range(row - 1, row + 2)
                    for j in range(col - 1, col + 2)]) \
            - self.grid[row][col]

    def __str__(self):
        s = ''
        for i in range(self.height):
            for j in range(self.width):
                s += '#' if self.grid[i][j] == 1 else '.'
                s += ' '
            s += os.linesep
        return s

    def update(self):
        """
            Any live cell with fewer than two live neighbours dies (referred to as underpopulation).
            Any live cell with more than three live neighbours dies (referred to as overpopulation).
            Any live cell with two or three live neighbours lives, unchanged, to the next generation.
            Any dead cell with exactly three live neighbours comes to life.
        """
        new_grid = []
        for row in range(0, self.height):
            new_grid.append(self.grid[row].copy())

        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                neighbours = self.get_neighbour_count(row, col)
                cell = self.grid[row][col]
                if cell == 1:
                    if neighbours < 2 or neighbours > 3:
                        new_grid[row][col] = 0
                elif cell == 0:
                    if neighbours == 3:
                        new_grid[row][col] = 1
        self.grid = new_grid


def main():
    game = Game.from_grid_config_file('grid.txt')
    print(game)
    print(game.get_neighbour_count(2, 2), game.get_neighbour_count(
        2, 3), game.get_neighbour_count(2, 4))
    print(game.get_neighbour_count(3, 2), game.get_neighbour_count(
        3, 3), game.get_neighbour_count(3, 4))


if __name__ == '__main__':
    main()
