food:
    diabetic: 1<0
    coffee: 
        sugar: if(diabetic 0 10)
    candy: 
        sweetener: if(diabetic "artificial" "sugar")

Joe:
    diabetic: 1>0
    snack: food
        -> candy
    drink: food
        -> coffee
        
Test:
    k: a + 1
    a: 5

-> Joe
    -> snack
        -> sweetener
