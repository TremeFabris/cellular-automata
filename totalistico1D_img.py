import numpy as np
import matplotlib.pyplot as plt
import totalistico1D as ca

# TODO: Documentar
# TODO: Adicionar escolha aleatória de n regras para rodar imagem

def input_saveimg():

    ''' Documentation '''

    temp = input("\nSave image? [\"yes\", \"no\"]: ")

    if temp.lower() == "yes":
        return True
    else:
        return False

# TODO: Adicionar info sobre r e k no nome da imagem
def plot_automata_saveimg(matrix: np.ndarray, save_img: bool, rule_num: int, impl: str):
    
    ''' Documentation '''

    plt.rcParams['image.cmap'] = 'binary'

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.matshow(matrix)
    ax.axis(False)
    if save_img:
        plt.savefig("img/T_{}_plot{}.png".format(impl, rule_num), dpi=300, bbox_inches='tight')
    else:
        plt.show()
    plt.close()

if __name__ == "__main__":

    r = int(input("NEIGHBORHOOD SIZE (r): "))
    k = int(input("NUMBER OF CELL STATES (0..k): "))

    GEN  = int(input("\nNUMBER OF GENERATIONS: "))
    IMPL = input("IMPULSE [\"left\", \"center\", \"right\", \"custom\" or \"random\"]: ").lower()
    AMNT_RULES = int(input("HOW MANY RULES TO RUN: "))

    max_rules = k ** ((2*r + 1) * (k-1) + 1)

    if AMNT_RULES >= max_rules:
        print("\nThis might take a while...")
        for i in range(max_rules):
            matrix = ca.run_automata(i, GEN, IMPL, r, k)
            plot_automata_saveimg(matrix, True, i, IMPL)
        print("\nImages saved!")
    
    elif AMNT_RULES > 1:
        INPUT_ARRAY = input("\nRULES: ")
        RULES_ARRAY = [ int(r) for r in INPUT_ARRAY.split() ]

        print("\nThis might take a while...")
        for r in RULES_ARRAY:
            matrix = ca.run_automata(r, GEN, IMPL, r, k)
            plot_automata_saveimg(matrix, True, r, IMPL)
        print("\nImages saved!")

    elif AMNT_RULES == 1:
        RULE = int(input("\nRULE: "))

        SAVE_IMG = input_saveimg()
        matrix = ca.run_automata(RULE, GEN, IMPL, r, k)
        plot_automata_saveimg(matrix, SAVE_IMG, RULE, IMPL)

    else:
        print("\nExiting...")