def sorting(numbers, blanks, fixed_keyword='감독관 확인'):
    # 첫 번째 값이 고정 조건에 맞는지 확인
    if numbers[0] == fixed_keyword:
        fixed_numbers = numbers[:1]  # 첫 번째 값만 고정
        fixed_blanks = blanks[:1]
        print("고정: ", fixed_numbers)
        
        # 나머지 값들 분리
        remaining_numbers = numbers[1:]
        remaining_blanks = blanks[1:]
    else:
        # 고정값이 없을 경우 모두 정렬
        fixed_numbers = []
        fixed_blanks = []
        remaining_numbers = numbers
        remaining_blanks = blanks

    # 나머지 값들을 숫자로 변환하여 정렬
    paired_dict = dict(zip(map(int, remaining_numbers), remaining_blanks))
    sorted_dict = dict(sorted(paired_dict.items()))

    # 정렬된 값들을 리스트로 변환
    sorted_numbers = list(map(str, sorted_dict.keys()))  # 정렬 후 문자열로 변환
    sorted_blanks = list(sorted_dict.values())

    # 고정된 값과 정렬된 값을 합침
    final_numbers = fixed_numbers + sorted_numbers
    final_blanks = fixed_blanks + sorted_blanks

    return final_numbers, final_blanks
