# Blackjack monte carlo simulator

## OVERVIEW
### Before working with the application, make sure to read LICENSE file.
This is fully functional script, which is using monte carlo method for simulating output of blackjack game, with possibility of adjusting different game rules.<br>
The output of simulations is being exported to csv file after each simulation, allowing for further statistical analysis.<br>

## REQUIREMENTS
- Python3

## GETTING STARTED
1. Create new virtual environment in root directory: 
```python3 -m venv .venv```

2. Activate the virtual environment: 
```. .venv/bin/activate```

3. Install venv dependencies: 
```pip install -r requirements.txt```

4. Use proper configuration before simulation
```config.ini```

5. Run the simulation and wait for results
```python3 main.py```


## CONFIGURATION
The simulator so far consists of one, non-sensitive configuration file. Below there is description of most of the configration variables (some of them are not listed below, they are only in config.ini and are self-explanatory)<br>
<b>All bool values are supposed to be either 0 or 1</b><br>

### GAME
| Name | Type | Description |
| ---- | ---- | ----------- |
| MIN_DOUBLE_DOWN_SUM | INT | min sum of cards, for which is allowed to double down (when set 0 there is no bottom limit) |
| MAX_DOUBLE_DOWN_SUM | INT | max sum of cards, for which is allowed to double down (when set to 21 there is no upper limit) |
| DOUBLE_AFTER_SPLIT | BOOL | is it allowed to double down after splitting cards |
| MAX_SPLIT_AMOUNT | INT | how many times it is allowed to split |
| RESPLIT_ACES | BOOL | is it allowed to split aces more than once per round (if 0 player can only split first pair A-A; if 1 player can split further possible A-A pairs up to the MAX_SPLIT_LIMIT) |
| PLAY_SPLIT_ACES | BOOL | is it allowed to further play after splitting aces (if 0, after splitting A-A player will receive only one additional card per hand without ability to make any move) |
| BLACKJACK_AFTER_SPLIT_COUNTS_AS_21 | BOOL | does blackjack after splitting (A + 10pt. card) pays as blackjack (if 1 A+10pt. after splitting pays normal; if 0 A+10pt. after splitting pays as blackjack) | 
| ALLOW_SPLIT_TENS | BOOL | is it allowed to split pairs with 10 value (ex, 10-10, K-K) |
| INSURANCE_ALLOWED | BOOL | is insurance allowed

### GAME-SURRENDER_TYPE
| Value | Description | Important |
| ----- | ----------- | --------- |
| none | surrendering is impossible | |
| early | early surrendering is possible | |
| late | late surrendering is possible | can't be set if [DEALER][HOLE_CARD] = european_no_hole_card |

### DEALER-HOLE_CARD
| Value | Description | Important |
| ----- | ----------- | --------- |
| american_peek | dealer receives 2 cards during initial play (1x hole card) and checks if doesn't have blackjack before any player movements | |
| american_peek_ace_only | same as american_peek, but checking for blackjack only applies to face card being an ace | |
| european_no_hole_card | dealer receives 1 card during initial play (0x hole card), second card is being dealt after all players finish plays | can't be set if [GAME][SURRENDER_TYPE] = early |

### [PLAYERS][BETTING_STRATEGIES]
| Value | Description | Important |
| ----- | ----------- | --------- |
| minimal_bet | every time player sets a bet equal to [GAME][MIN_BET] | | 

## [PLAYERS][PLAYING_STRATEGIES]
| Value | Description | Important |
| ----- | ----------- | --------- |
| basic_strategy | player plays only using basic strategy table | table is located in strategies module, verify the moves because they might differ for different rules |
| mimic_the_dealer | player plays the same way as dealer | | 
