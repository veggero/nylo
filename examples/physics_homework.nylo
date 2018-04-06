"Gli esempi mostrano l'utilizzo della funzione."
"Sono presi direttamente dal mio libro di fisica."

"Per avviare:"
"[veggero@yara nylo]$ py src/runfile.py examples/physics_homework.nylo"

g: 9.81

conversioni_velocita:
        
    metri_al_secondo: chilometri_orari / 3.6
    chilometri_orari: metri_al_secondo * 3.6

    esempio: 
        conversioni_velocita
            metri_al_secondo: 5
            -> chilometri_orari
    
moto_rettilineo_uniforme:
    tempo_iniziale: 0
    tempo: delta_spazio / velocita
    delta_tempo: tempo - tempo_iniziale
    
    spazio_iniziale: 0
    spazio: velocita * delta_tempo
    delta_spazio: spazio - spazio_iniziale
    
    velocita: delta_spazio / delta_tempo
    
    esempio:
        moto_rettilineo_uniforme
            velocita: 5.5
            tempo: 120
            -> spazio
    
moto_rettilineo_uniformemente_accelerato:
    tempo_iniziale: 0
    tempo: tempo_iniziale + (delta_velocita / accelerazione)
    delta_tempo: tempo - tempo_iniziale
    
    spazio_iniziale: 0
    spazio: 
        (spazio_iniziale) + (velocita_iniziale * delta_tempo) + (accelerazione * delta_tempo * delta_tempo / 2)
    delta_spazio: spazio - delta_spazio
    
    velocita_iniziale: 0
    velocita: 
        velocita_iniziale + (accelerazione * delta_tempo)
    delta_velocita: velocita - velocita_iniziale
    
    accelerazione: delta_velocita / delta_tempo
    
    esempio:
        moto_rettilineo_uniformemente_accelerato
            velocita_iniziale: 2.5
            tempo: 25
            accelerazione: 0.04
            -> velocita
            
corpo:
    massa
    forza_peso: massa * g
    forza_normale: 0 - massa * g
    
    mu_s
    mu_d
    forza_attrito_statico: forza_peso * mu_s
    forza_attrito_dinamico: forza_peso * mu_d
    
    esempio:
        moto_rettilineo_uniformemente_accelerato
            velocita_iniziale: 4
            velocita: 0
            accelerazione: 0 - corpo
                "La massa viene semplificata e non e' esplicitata."
                "Ogni massa qui va bene."
                massa: 5
                mu_d: 0.05
                -> forza_attrito_dinamico / massa
            -> spazio
                
                
esempio: corpo(->esempio)
                
-> esempio
