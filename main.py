import classes
import configparser


config = configparser.ConfigParser()
config.read('config.ini')


game = classes.Game()
players = []
for i in range(int(config['PLAYERS']['AMOUNT'])):
    players.append(classes.Player(i))

