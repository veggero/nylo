moto:
    int velocita_iniziale

test:

    moto asse_x
    moto asse_y
    
    gittata: asse_x(->velocita_iniziale) * asse_y(->velocita_iniziale)
    
    asse_x
        velocita_iniziale: gittata / asse_y(->velocita_iniziale)
    asse_y
        velocita_iniziale: gittata / asse_x(->velocita_iniziale)
    
-> test
    asse_x: moto
        velocita_iniziale: 10
    asse_y: moto
    gittata: 50
    -> asse_y(->velocita_iniziale)
    
