def sorting(numbers, blanks):
    paired_dict = dict(zip(numbers, blanks))
    sorted_dict = dict(sorted(paired_dict.items()))
    
    # dict_keys와 dict_values를 일반 리스트로 변환
    numbers_list = list(sorted_dict.keys())
    blanks_list = list(sorted_dict.values())

    return numbers_list, blanks_list
