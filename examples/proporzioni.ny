"Compiti di Amerigo Guagagno."

"Per avviare:"
"[veggero@yara nylo]$ py src/main.py examples/proporzioni.ny"

proporzione:
    int ext_sx: int_dx*int_sx/ext_dx
    int ext_dx: int_dx*int_sx/ext_sx
    int int_sx: ext_dx*ext_sx/int_dx
    int int_dx: ext_dx*ext_sx/int_sx
    
    esempio:
        proporzione
            ext_sx: ((7/12 + 2/5) / (59/6)) + (1/2) * (3/5)
            int_dx: ((9 + 1/2) * (1/2)) + 1/4
            ext_dx: 1/2 + (1/2) * (1 - 1/3)
            -> int_sx  
    
misure:
    chilometri: metri / 1000
    metri: chilometri * 1000

    esempio:
        misure
            metri: 6
            -> chilometri
            
-> proporzione
    -> esempio
