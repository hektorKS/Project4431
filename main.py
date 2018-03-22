from board_finding import *
from x_and_o_detection import *
import sys
import globals


def main():
    if len(sys.argv) > 1:
        names = [sys.argv[1]]
        globals.argument_from_command_line = True
        globals.file_name = sys.argv[1]
    else:
        names = globals.img_names

    boards_finding(names)

    games_arrays = x_and_o_detection(names)

    if globals.argument_from_command_line:
        print("Tablica wynikowa algorytmu")
        print(games_arrays[0][0])
        print(games_arrays[0][1])
        print(games_arrays[0][2])
    else:
        print("Nazwy poprawnie wykrytych zdjęć:")
        print(globals.correctly_identified_names)
        print("Nazwy niepoprawnie wykrytych zdjęć:")
        print(globals.incorrectly_identified_names)
        correct = globals.correctly_identified
        incorrect = globals.incorrectly_identified
        miss_arr = globals.mistake_array
        print("Ilości pomyłek: ")
        for i in range(len(miss_arr)):
            print(miss_arr[i], "pomyłek o ", i, "pól/pola")
        corr_fields = globals.number_of_correctly_identified_fields
        incorr_fields = globals.number_of_incorrectly_identified_fields
        print("Ilosc obrazkow testowych: ", correct + incorrect)
        print("Poprawnie wykryto pol (pojedynczych): ", corr_fields)
        print("Niepoprawnie wykryto pol (pojedynczych): ", incorr_fields)
        print("Skutecznosc w wykrywaniu pojedynczych pol: ",
              (corr_fields / (corr_fields + incorr_fields)) * 100, "%")
        print("Poprawnie wykryto plansz (calych): ", correct)
        print("Niepoprawnie wykryto (calych): ", incorrect)
        print("Procent skuteczności w wykrywaniu calych plansz: ", (correct / (correct + incorrect)) * 100, "%")


if __name__ == '__main__':
    main()
