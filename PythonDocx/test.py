set_ex_type_list_transfer = ['545_10nm', 'minus545_10nm', '545_100nm', 'minus545_100nm', '1000_10nm', 'minus1000_10nm',
                             '1000-100nm',
                             'minus1000-100nm',
                             '1500-100nm', 'minus1500-100nm', '1900_100nm', 'minus1900_100nm']

for ex_type in set_ex_type_list_transfer:
    new_str = ex_type.replace("minus", "-")
    print(new_str)
