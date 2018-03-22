argument_from_command_line = False
file_name = ""
correctly_identified = 0
incorrectly_identified = 0
correctly_identified_names = []
incorrectly_identified_names = []
number_of_correctly_identified_fields = 0
number_of_incorrectly_identified_fields = 0

mistake_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

img_names = ["p1.png",
             "p2.jpg",
             "p3.jpg",
             "p4.jpg",
             "p5.jpg",
             "p6.png",
             "p7.jpg",
             "p8.jpg",
             "p9.jpg",
             "p10.jpg",
             "p11.jpg",
             "p12.jpg",
             "p13.jpg",
             "p14.jpg",
             "p15.jpg",
             "p16.png",
             "p17.png",
             "p18.jpg",
             "p19.jpg",
             "p20.jpg",
             "p21.jpg",
             "p22.jpg",
             "p23.jpg",
             "p24.jpg",
             "p25.jpg",
             "p26.jpg",
             "p27.jpg",
             "p28.jpg",
             # "p29.jpg", //nie pełnia założeń
             "p30.jpg",
             # "p31.jpg", //nie pełnia założeń
             "p32.jpg",
             # "p33.jpg", //nie pełnia założeń
             "p34.jpg",
             "p35.jpg",
             "p36.jpg",
             "p37.jpg",
             "p38.jpg",
             "p39.jpg",
             # "p40.jpg", //nie pełnia założeń
             # "p41.jpg", //nie pełnia założeń
             "p42.jpg",
             # "p43.jpg", //nie pełnia założeń
             # "p44.jpg", //nie pełnia założeń
             # "p45.jpg", //nie pełnia założeń
             "p46.jpg",
             "p47.jpg",
             "p48.jpg",
             "p49.jpg",
             # "p50.jpg", //nie pełnia założeń
             # "p51.jpg", //nie pełnia założeń
             "p52.jpg",
             "p53.jpg",
             "p54.jpg",
             "p55.jpg",
             # "p56.jpg", //nie pełnia założeń
             # "p57.jpg", //nie pełnia założeń
             # "p58.jpg", //nie pełnia założeń
             # "p59.jpg", //nie pełnia założeń
             # "p60.jpg", //nie pełnia założeń
             # "p61.jpg", //nie pełnia założeń
             "p62.jpg",
             "p63.jpg",
             "p64.jpg",
             "p65.jpg",
             "p66.jpg"]


def check_correctness(game_array, img_name):
    number_of_mistakes = 0
    is_correct = True
    correct_result = correct_results.get(img_name)
    if correct_result is None:
        print("Nie mozna sprawdzic poprawnosci wyniku programowo (wynik niezdefiniowany odgornie)",
              img_name)
        return False
    for i in range(3):
        sub_array_to_check = game_array[i]
        for j in range(3):
            char_to_check = sub_array_to_check[j]
            if char_to_check != correct_result[i * 3 + j]:
                is_correct = False
                number_of_mistakes += 1
    return is_correct, number_of_mistakes


correct_results = {
    "p1.png": "-o---xx--",
    "p2.jpg": "o---oxx--",
    "p3.jpg": "o---oxx--",
    "p4.jpg": "--x-x-o-o",
    "p5.jpg": "--x-x-o-o",
    "p6.png": "---------",
    "p7.jpg": "x---o-x-o",
    "p8.jpg": "x---o---x",
    "p9.jpg": "x---o---x",
    "p10.jpg": "oxo-x----",
    "p11.jpg": "-o--xxo--",
    "p12.jpg": "-o-----o-",
    "p13.jpg": "oxooxxxox",
    "p14.jpg": "-o-----o-",
    "p15.jpg": "o-o-x----",
    "p16.png": "o-xxxoo--",
    "p17.png": "-o--o---x",
    "p18.jpg": "-o-x-----",
    "p19.jpg": "-o-x-----",
    "p20.jpg": "-o-xxo---",
    "p21.jpg": "-oxo----x",
    "p22.jpg": "-xxoo-o--",
    "p23.jpg": "xoxoxooox",
    "p24.jpg": "o-o-x-x--",
    "p25.jpg": "xoxxo-x-o",
    "p26.jpg": "xooxoxxox",
    "p27.jpg": "x---o----",
    "p28.jpg": "-xo-oxo--",
    "p29.jpg": "----x--o-",
    "p30.jpg": "---o-x-x-",
    "p31.jpg": "----x---o",
    "p32.jpg": "--o------",
    "p33.jpg": "---o-o-x-",
    "p34.jpg": "-x--o--x-",
    "p35.jpg": "xo--x----",
    "p36.jpg": "xoo-x--x-",
    "p37.jpg": "x-x-o---o",
    "p38.jpg": "-ox-x-oox",
    "p39.jpg": "o---x----",
    "p40.jpg": "----o----",
    "p41.jpg": "-----o-x-",
    "p42.jpg": "--oxo----",
    "p43.jpg": "-ox-ox---",
    "p44.jpg": "------x-o",
    "p45.jpg": "-o--x--o-",
    "p46.jpg": "-o--x--o-",
    "p47.jpg": "--x-o---x",
    "p48.jpg": "-ox-o---x",
    "p49.jpg": "----ox--x",
    "p50.jpg": "-x-------",
    "p51.jpg": "-x-xo----",
    "p52.jpg": "--oox----",
    "p53.jpg": "xxoooxxxo",
    "p54.jpg": "xxoooxxxo",
    "p55.jpg": "xxoooxxxo",
    "p56.jpg": "----x-o--",
    "p57.jpg": "----x-o--",
    "p58.jpg": "--xx--ooo",
    "p59.jpg": "--xx--ooo",
    "p60.jpg": "o---x----",
    "p61.jpg": "--x-o-x--",
    "p62.jpg": "-o--x--o-",
    "p63.jpg": "--oxo----",
    "p64.jpg": "--x-o---x",
    "p65.jpg": "-ox-ox---",
    "p66.jpg": "-x-------"

}
