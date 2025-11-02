import classes
import configparser


config = configparser.ConfigParser()
config.read('config.ini')


game = classes.Game()
for i in range(int(config['PLAYERS']['AMOUNT'])):
    game.add_player(classes.Player(i))

print(game.stack)