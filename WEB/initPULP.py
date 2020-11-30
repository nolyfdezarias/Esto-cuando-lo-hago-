

import pulp


def makeMatriz(matriz):

    newM = []

    for j in range(len(matriz[0])):
        newM.append([])
    
    for j in range(len(matriz[0])):
        for i in range(len(matriz)):
            newM[j].append(matriz[i][j])

    return newM


def runPulp(matriz) :
    prop = pulp.LpProblem("Asignacion",pulp.LpMinimize)

    acts = []
    d_acts = {}
    for j in range(len(matriz[0])):
        acts.append(f'A{j}')
        d_acts[f'A{j}'] = 1
    
    turns = []
    d_turns = {}
    for i in range(len(matriz)):
        turns.append(f'T{i}')
        d_turns[f'T{i}'] = 1

    
    newM = makeMatriz(matriz)

    costos = pulp.makeDict([acts,turns],newM,0)

    asigns = [(c,b) for c in acts for b in turns]

    x = pulp.LpVariable.dicts("asigns", (acts,turns),lowBound = 0, cat = pulp.LpInteger)

    prop += sum(x[c][b] * costos [c][b] for (c,b) in asigns) #, \ "Suma_de_costos_de asigns"

    for c in acts:
        prop += sum([x[c][b] for b in turns]) == d_acts[c] #, \ "Suma_de_productos_que_salen_de_%s"%c

    for b in turns:
        prop += sum([x[c][b] for c in acts]) <= d_turns[b] #, \ "Suma_de_productos_que_entran_a_%s"%b

    
    prop.solve()
    solve = []
    
    for v in prop.variables():
       
        if v.varValue == 1.0 :
            s = v.name.split('_')
            s = s[1:]
            i = int(s[1][1:])
            j = int(s[0][1:])
            solve.append((i,j))

    
    return solve



