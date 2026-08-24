def CalcularPromedio(Lista):
    s=0
    for x in Lista:
     s=s+x
    return s/len(Lista)
 
l=[1,2,3,4,5]
print(CalcularPromedio(l))