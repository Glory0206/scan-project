from app.services.make_dataset.utils.random_rotate import random_rotate
from app.utils.find_text import find_texts
from app.services.make_dataset.utils.write import write_problem, write_sign
from app.services.make_dataset.utils.preprocessing import preprocess_image
from app.utils.coord import problem_box_check, small_box

def make_dataset(image, count: int, file_name: str):
    images = random_rotate(image, count)
    preprocess_images = [preprocess_image(img) for img in images]

    coord_top_left, coord_bottom_right, numbers, sign_box = find_texts(preprocess_images[0])
    num_of_problems = len(numbers)

    horizontal, vertical = problem_box_check(coord_top_left)
    small_horizontal, small_vertical = small_box(coord_top_left[0], coord_bottom_right[0])
    horizontal -= small_horizontal
    vertical -= small_vertical

    result_files = []

    for i in range(len(preprocess_images)):
        base_image = images[i]

        if sign_box:
            base_image = write_sign(base_image, sign_box)

        file_name_jpg, file_buffer = write_problem(
            base_image,
            file_name,
            coord_top_left,
            horizontal,
            vertical,
            num_of_problems,
            i
        )
        result_files.append((file_name_jpg, file_buffer))

    return result_files