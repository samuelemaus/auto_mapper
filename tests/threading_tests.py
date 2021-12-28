import tile_image_processor
from timeit import default_timer as timer


def time(func, image, tile_indices, rows_count: int, columns_count: int):
    print('starting timer on: ' + str(func))
    start = timer()
    tile_images = func(image, tile_indices, rows_count, columns_count)
    end = timer()
    print('ending timer on: ' + str(func))
    return end - start


def run_thread_test(image_name: str, tile_width, tile_height):
    image = tile_image_processor.load_image(image_name)
    image_height = image.shape[0]
    image_width = image.shape[1]

    rows_count = image_height // tile_height
    columns_count = image_width // tile_width
    tile_indices = tile_image_processor.get_tile_indices_inferred(image_width, image_height, tile_width, tile_height, rows_count,
                                                                    columns_count)

    times = {}

    # inferred_time = time(tile_image_processor.get_tile_images_inferred, image, tile_indices, rows_count,
                           # columns_count)
    threaded_time_inner = time(tile_image_processor.get_tile_images_threaded_portrait, image, tile_indices,
                               rows_count, columns_count)
    threaded_time_outer = time(tile_image_processor.get_tile_images_threaded_landscape, image, tile_indices, rows_count,
                               columns_count)

    # times['inferred'] = inferred_time
    times['threaded_inner'] = threaded_time_inner
    times['threaded_reoriented'] = threaded_time_outer

    return times


def test_threading(runs: int, image_name: str, tile_width: int, tile_height: int):
    inferred = "inferred"
    threaded_inner = "threaded_inner"
    threaded_reoriented = "threaded_reoriented"

    image = tile_image_processor.load_image(image_name)
    image_height = image.shape[0]
    image_width = image.shape[1]

    rows_count = image_height // tile_height
    columns_count = image_width // tile_width
    tile_indices = tile_image_processor.get_tile_indices_unthreaded(image_width, image_height, tile_width, tile_height, rows_count,
                                                                    columns_count)

    times_averages = {}
    times_totals = []

    for i in range(runs):
        print('run #: ' + str(i + 1))

        times = {}

        inferred_time = time(tile_image_processor.get_tile_images_threaded, image, tile_indices, rows_count,
                             columns_count)
        threaded_time_inner = time(tile_image_processor.get_tile_images_threaded_portrait, image, tile_indices,
                                   rows_count, columns_count)
        threaded_time_outer = time(tile_image_processor.get_tile_images_threaded_landscape, image, tile_indices,
                                   rows_count, columns_count)

        times[inferred] = inferred_time
        times[threaded_inner] = threaded_time_inner
        times[threaded_reoriented] = threaded_time_outer

        times_totals.append(times)

    for total in times_totals:
        times_averages[inferred] = total[inferred]
        times_averages[threaded_inner] = total[threaded_inner]
        times_averages[threaded_reoriented] = total[threaded_reoriented]

    times_averages[inferred] /= runs
    times_averages[threaded_inner] /= runs
    times_averages[threaded_reoriented] /= runs

    return {"averages": times_averages,
            "totals": times_totals}
