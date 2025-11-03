Opis dla config [GAME]
    - MIN_DOUBLE_DOWN_SUM - minimalna suma kart, dla których można zrobić double down (zakres od 0, oznacza że można robić do bez dolnego limitu)
    - MAX_DOUBLE_DOWN_SUM - maksymalna suma kart, dla których można zrobić double down (zakres do 21, oznacza ze aż do blackjack można podwajać)
    - DOUBLE_AFTER_SPLIT - czy można podwajać po split
    - MAX_SPLIT_AMOUNT - ile razy wolno dzielić pary.
    - RESPLIT_ACES - jeżeli po podzieleniu pary asów jedna z par znowu będzie parą A-A, to czy można ponownie rozdzielić aż do limitu max_split_amount. (standard = 0)
    - PLAY_SPLIT_ACES - czy można grać po rozdzieleniu asów (jeżeli False, gracz otrzymuje jedną kartę (czyli ma 2 na parę) i gra się kończy (standard = 0))
    - BLACKJACK_AFTER_SPLIT_COUNTS_AS_21 - po rozdzieleniu jeżeli dostaje się A-10, NIE liczy się to jako blackjack (standard = 1)
    - ALLOW_SPLIT_TENS - czy można rozdzielać pary o wartośći 10 (np. 10-10, K-K) (standard = 1)
    - INSURANCE_ALLOWED - czy ubezpieczenie jest dozwolone

Opcje dla config [GAME][SURRENDER_TYPE]
    - none - poddanie niemożliwe
    - early - wczesne poddanie, zanim dealer sprawdzi czy ma bj
    - late - można się poddać, o ile dealer nie ma blackjacka (standard)

Opcje dla config [DEALER][HOLE_CARD]
    - american_peek - dealer otrzymuje na start hole_card (zakrytą) i sprawdza czy nie ma blackjacka przed ruchami graczy
    - american_peek_ace_only - jak wyżej tylko peek jest gdy odkrytą kartą jest as
    - european_no_hole_card - dealer otrzymuje na start tylko jedną odkrytą kartę, drugą otrzymuje po ruchach wszystkich graczy (gracz traci tylko zakład pierwotny w przypadku blackjacka dealera) (!!! wartość surrender musi być ustawiona na none/early, bo late wymaga hole card do działania !!!)

Opcje dla config[PLAYERS][BETTING_STRATEGIES]
    - minimal_bet - za każdym razem stały bet równy minimalnemu MIN_BET

Opcje dla config[PLAYERS][PLAYING_STRATEGIES]
    - basic_strategy - gra tylko według basic strategy
    - mimic_the_dealer - gry z uzyciem strategii dealera
