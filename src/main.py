import nylo

r = nylo.Reader('ciao(k, a: 15, 15: k, a -> 42) ')
k = nylo.Symbol(r)
print(k.value)
