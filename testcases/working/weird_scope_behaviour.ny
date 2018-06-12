coffee:
    sugar: if(diabetic 0 10)

candy:
    sweetener: if(diabetic "artificial" "sugar")

Joe:
    diabetic: 1>0
    snack: candy
    drick: cofee

-> Joe
  -> snack
    -> sweetener
