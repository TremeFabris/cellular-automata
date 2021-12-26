import numpy as np
import matplotlib.pyplot as plt

# SITUAÇÃO: Estou tentando mudar a forma com que organizo meu array rule_arr para tornar
#           mais fácil a generalização. Preciso testar se a codificação das regras ainda condizem
#           com a codificação do Wolfram.

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

    nbhd = 2*r + 1                  # nbhd: neighborhood
    pstt = nbhd * (k - 1) + 1       # pstt: possible states

    rule_arr = np.zeros(pstt, dtype=int)
    rule_str = np.base_repr(rule_num, base=k, padding=pstt)[-pstt:]

    for i in range(pstt):
        rule_arr[i] = int(rule_str[ -(i + 1) ])     # Garantir que isso dá certo

    return rule_arr

# Realiza o cálculo de gerações
def gen_calc(matrix: np.ndarray, num_gen: int, rule_arr: np.ndarray, r: int):

    ''' Documentation '''

    size_gen = len(matrix[0])

    for i in range(num_gen - 1):
        next_index = np.zeros(size_gen, dtype=int)      # Se pá que isso é desnecessário...

        gen = matrix[i]                                 # ...já que eu posso botar gen diretamente lá
        for j in range(1, r + 1):
            next_index += np.roll(gen, j) + np.roll(gen, -j)
        next_index += gen

        matrix[i+1] = np.take(rule_arr, next_index)

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

    size_gen = 2 * num_gen + 1
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
