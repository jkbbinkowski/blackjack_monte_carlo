1. Initialize the game by creating game object. It initalizes the game with config from config[GAME] as well as creates dealer object withing game. Creating new game automatically shuffles the cards.
2. Create the players for a game by simply running for loop to create amount of players specified in config[PLAYERS]. The capital list in config[PLAYERS] shall be the length of the amount of the players.
3. Add players to the game. This step can be done at any time. Use game.add_player method.
