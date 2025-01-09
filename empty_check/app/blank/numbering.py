def sorting(numbers, blanks, images, fixed_keyword='감독관 확인'):
    # 첫 번째 값이 고정 조건에 맞는지 확인
    if numbers[0] == fixed_keyword:
        fixed_numbers = numbers[:1]  # 첫 번째 값만 고정
        fixed_blanks = blanks[:1]
        fixed_images = images[:1]
        
        # 나머지 값들 분리
        remaining_numbers = numbers[1:]
        remaining_blanks = blanks[1:]
        remaining_images = images[1:]
    else:
        # 고정값이 없을 경우 모두 정렬
        fixed_numbers = []
        fixed_blanks = []
        fixed_images = []
        remaining_numbers = numbers
        remaining_blanks = blanks
        remaining_images = images

    # 나머지 값들을 숫자로 변환하여 정렬
    paired_list = list(zip(map(int, remaining_numbers), remaining_blanks, remaining_images))
    sorted_list = sorted(paired_list, key=lambda x: x[0])  # 숫자 기준으로 정렬

    # 정렬된 값들을 리스트로 변환
    sorted_numbers = list(map(lambda x: str(x[0]) + '번', sorted_list))  # 정렬 후 문자열로 변환
    sorted_blanks = list(map(lambda x: x[1], sorted_list))
    sorted_images = list(map(lambda x: x[2], sorted_list))

    # 고정된 값과 정렬된 값을 합침
    final_numbers = fixed_numbers + sorted_numbers
    final_blanks = fixed_blanks + sorted_blanks
    final_images = fixed_images + sorted_images

    return final_numbers, final_blanks, final_images
