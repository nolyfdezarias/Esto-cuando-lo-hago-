

def CoverZeros(matriz, len_matriz,assingLines,finalyAssing):
    
    markedLines = []
    markedCol = []
    
    for i in range(0,len_matriz):
        if not(i in assingLines):
            markedLines.append(i)

    change = True

    while change:
        change = False
        for index in markedLines:
            for j in range(0,len_matriz):
                if matriz[index][j] == 0 and not(j in markedCol) :
                    markedCol.append(j)
                    change = True

        for x in finalyAssing:
            i,k = x
            for j in markedCol:
                if k == j and not(i in markedLines):
                    markedLines.append(i)
                    change = True

    no_mark_lines = []

    for i in range(0,len_matriz):
        if not(i in markedLines):
            no_mark_lines.append(i)
    
    return markedCol,no_mark_lines


matriz1 = [[2500,4000,3500],
          [4000,6000,3500],
          [2000,4000,2500]]

matriz0 = [
    [58,58,60,54],
    [66,70,70,78],
    [106,104,100,95],
    [52,54,64,54]
]

matriz2 = [[1500,4000,4500],
          [2000,6000,3500],
          [2000,4000,2500]]

matriz = [[14,1,2,3,4,5,6,7,8,9,10,11,12,13],
           [1,23,2,3,4,5,6,7,8,9,10,11,12,13],
           [1,2,0,3,4,5,6,7,8,9,10,11,12,13],
           [1,2,0,0,4,5,6,7,8,9,10,11,12,13],
           [1,2,3,4,0,5,6,7,8,9,0,11,12,13],
           [1,2,3,4,5,0,6,7,8,9,10,11,12,13],
           [1,2,3,4,0,6,0,7,8,9,10,11,12,13],
           [1,2,3,4,5,6,7,5,8,9,10,11,12,13],
           [1,2,3,4,5,6,7,8,40,9,10,11,12,13],
           [1,2,3,4,5,6,7,8,9,3,10,11,12,13],
           [1,2,3,4,5,6,7,8,9,10,1,11,12,13],
           [1,2,3,4,5,6,7,8,9,10,11,32,12,13],
           [1,2,3,4,5,6,7,8,9,10,11,12,2,13],
           [1,2,3,4,5,6,7,8,9,10,11,12,13,37]]

def hungarina_Alg(matriz):
    len_matriz = len(matriz)

    for i in range(0,len_matriz):
        min_row = min(matriz[i])
        if min_row > 0 :
            for j in range(0,len_matriz):
                matriz[i][j] -= min_row

    #print(matriz)

    for j in range(0,len_matriz):
        min_col = 10000000
        for i in range(0,len_matriz):
            min_col = min(min_col,matriz[i][j])
        if min_col > 0 :
            for i in range(0,len_matriz):
                matriz[i][j] -= min_col

    #print(matriz)

    while True:
        Finally_assing = []
        assingLines = []
        invalidCol = []
        zeros = []
        zerosRow = [0] * (len_matriz)
        zerosCol = [0] * (len_matriz)
        

        for i in range(0,len_matriz):
            for j in range(0,len_matriz):
                if matriz[i][j] == 0:
                    zerosRow[i] += 1
                    zerosCol[j] += 1
                    zeros.append((i,j))

        while len(zeros) > 0:
            zerosToRemove = []
            min_Zeros = min(zerosRow)
            index_min_Zeros = zerosRow.index(min_Zeros)
            posible_zeros = []
            for x in zeros:
                i,j = x 
                if i == index_min_Zeros:
                    #Finally_assing.append((i,j))
                    #assingLines.append(i)
                    #invalidCol.append(j)
                    posible_zeros.append(x)
                    #break
            zero_asignado = 0
            min_col = len_matriz

            for x in range(len(posible_zeros)):
                i,j = posible_zeros[x]
                if zerosCol[j] < min_col:
                    min_col = zerosCol[j]
                    zero_asignado = x
            
            i,j = posible_zeros[zero_asignado]
            Finally_assing.append((i,j))
            assingLines.append(i)
            invalidCol.append(j)


            for x in zeros:
                i,j = x 
                if (i in assingLines) or (j in invalidCol):
                    zerosRow[i] -= 1
                    if zerosRow[i] == 0 :
                        zerosRow[i] = len_matriz
                    zerosToRemove.append(x)
            
            for x in zerosToRemove:
                zeros.remove(x)


        if len(assingLines) == len_matriz:
            #print(Finally_assing)
            return Finally_assing
            #break
        else:

            markedColumns,marked_lines = CoverZeros(matriz,len_matriz,assingLines,Finally_assing)
            no_marked_min = 10000000

            for i in range(0,len_matriz):
                for j in range(0,len_matriz):
                    if not(i in marked_lines) and not(j in markedColumns) : 
                        no_marked_min = min(matriz[i][j],no_marked_min)

            for i in range(0,len_matriz):
                for j in range(0,len_matriz):
                    if not(i in marked_lines):
                        matriz[i][j] -= no_marked_min
                    if (j in markedColumns):
                        matriz[i][j] += no_marked_min
        #print(matriz)
        #print()


#print(hungarina_Alg(matriz0))
            
       

