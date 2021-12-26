import numpy as np
import matplotlib.pyplot as plt

# SITUAÇÃO: Fazer o rule_array com duas camadas me impossibilitou de usar np.take para calcular
#           gen_calc. Pode ser que, por isso, o código tenha um custo de memória muito grande.
#           Contudo, pensando nisso, já deixo aqui uma solução: basta, ao invés de criarmos uma
#           matriz para rule_arr, criar um vetor simples particionado apenas logicamente para separar
#           os casos de regra, onde os indíces 0, 1, 2 representam o primeiro estado da célula central,
#           os índices 3, 4, 5 o segundo estado da célula central, etc. Assim, teremos um único vetor e
#           (EU SUPONHO) poderemos usar np.take em gen_calc.

# SITUAÇÃO: size_gen continua sendo 2*num_gen + 1. Será que eu deveria trocar isso pra permitir
#           uma escolha mais queer de linhas e colunas?

# SITUAÇÃO: Codifiquei a regra do meu jeito, talvez deva mudar? Falar com Odemir.

# Inicializa matriz-malha
def init_matrix(rows: int, cols: int):
    
    ''' Initializes matrix with all zeros
    
        Input:
            rows (int): number of rows the matrix must have
            cols (int): number of columns the matrix must have
        Output:
            mat (array): initialized matrix '''

    return np.zeros((rows, cols), dtype=int)

# Configura impulso inicial
def config_impulse(impulse_type: str, size: int, k: int):
    
    ''' Documentation '''

    first_impulse = np.zeros(size, dtype=int)
    impulse_str = impulse_type.lower()

    if impulse_str == "custom":
        
        print("\nCustom seed must be the decimal codification of the array of alive cells.")
        aux_seed = int(input("SEED: "))

        str_seed = np.base_repr(aux_seed, base=k)
        for i in range(1, len(str_seed) + 1):
            first_impulse[-i] = int(str_seed[-i])
    
    elif impulse_str == "random":
        first_impulse = np.random.choice(range(k), size=size)

    else:
        start = int(input("Value of initial cell (0 <= val < {}): ".format(k)))

        if impulse_str == "left":
            index = 1
        elif impulse_str == "right":
            index = size - 2
        else: #impulse_str == "center":
            index = size // 2

        first_impulse[index] = start
    
    return first_impulse

# Calcula o array da regra
def rule_array(rule_num: int, r: int, k: int):

    ''' Documentation '''

    pstt = 2 * r * (k - 1) + 1      # pstt:     possible states
    max_bits = pstt * k             # max_bits: maximum amnt of bits possible for rules

    rule_arr = np.zeros((k, pstt), dtype=int)
    rule_str = np.base_repr(rule_num, base=k, padding=max_bits)[-max_bits:]

    #print("DEBUG:: rule_str == {}".format(rule_str))

    offset = 0
    for i in range(k):
        for j in range(pstt):
            rule_arr[i][j] = rule_str[-(j + offset + 1)]    # Certeza que eu posso fazer isso por módulo...
        offset += j + 1

    #print("DEBUG:: rule_arr == {}".format(rule_arr))
    return rule_arr

# Realiza o cálculo de gerações
def gen_calc(matrix: np.ndarray, num_gen: int, rule_arr: np.ndarray, r: int):

    ''' Documentation '''
    
    size_gen = len(matrix[0])

    # FAZER GENERALIZAÇÃO PARA r (FEITO?) E k (SINTO QUE JÁ TAVA FEITO)

    for i in range(num_gen - 1):

        next_index = np.zeros(size_gen, dtype=int)
        gen = matrix[i]
        for j in range(1, r + 1):
            next_index += np.roll(gen, j) + np.roll(gen, -j)

        rule_set = rule_arr[gen]

        #print("DEBUG:: rule_set ({}) == {}".format(i, rule_set))
        #print("DEBUG:: next_index ({}) == {}".format(i, next_index))

        for j in range(size_gen):
            matrix[i+1][j] = rule_set[j][next_index[j]]  # Isso PARECE estar certo...
            #print("DEBUG:: krl dos indice ({}) == {}".format(i, rule_set[j][next_index[j]]))
        

    return matrix

# Plotta o gráfico de evolução da matriz de autômatos
def plot_automata(matrix: np.ndarray):
    
    ''' Plots the automata matrix
        
        Input:
            matrix (array): matrix to plot
        Output:
            None (matrix is plotted without return value) '''
    
    plt.rcParams["image.cmap"] = "binary"

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.matshow(matrix)
    ax.axis(False)
    plt.show()

# Envelope para rodar as funções
def run_automata(rule: int, num_gen: int, impulse: str, r: int, k: int):

    ''' Documentation '''

    rule_index = rule_array(rule, r, k)

    size_gen = 2 * num_gen + 1                  # Talvez mudar essa lógica de size_gen?
    matrix_ca = init_matrix(num_gen, size_gen)
    matrix_ca[0] = config_impulse(impulse, size_gen, k)

    return gen_calc(matrix_ca, num_gen, rule_index, r)

if __name__ == "__main__":

    r = int(input("NEIGHBORHOOD SIZE (r): "))
    k = int(input("NUMBER OF CELL STATES (0..k): "))

    RULE = int(input("\nRULE: "))
    GEN  = int(input("NUMBER OF GENERATIONS: "))
    IMPL = input("IMPULSE [\"left\", \"center\", \"right\", \"custom\" or \"random\"]: ")

    MATRIX = run_automata(RULE, GEN, IMPL, r, k)
    plot_automata(MATRIX)
