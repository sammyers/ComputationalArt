""" TODO: Put your header comment here """

import random
from PIL import Image
from math import cos, sin, pi


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function, with a random depth between the minimum and maximum. 
                 This can be evaluated directly with input values.
    """
    prod = lambda a, b, t: a * b
    avg = lambda a, b, t: 0.5 * (a + b)
    cos_pi = lambda a, t: cos(pi * a * (1 - t))
    sin_pi = lambda a, t: sin(pi * a * (1 - t))
    x = lambda a, b, t: a * (1 - t)
    y = lambda a, b, t: b * (1 - t)
    square = lambda a, t: a**2
    absdiff = lambda a, b, t: (abs(a) - abs(b))

    if min_depth == 1 and max_depth == 1:
        return random.choice([x, y])
    elif min_depth == 1:
        if random.choice([True, False]):
            return random.choice([x, y])
        else: 
            max_depth -= 1
    else:
        min_depth -= 1
        max_depth -= 1

    funcs = [prod, avg, cos_pi, sin_pi, x, y, square, absdiff]
    func = random.choice(funcs)
    
    if func in [prod, avg, x, y, absdiff]:
        func1 = build_random_function(min_depth, max_depth)
        func2 = build_random_function(min_depth, max_depth)
        new_func = lambda a, b, t: func(func1(a, b, t), func2(a, b, t), t)
    elif func == cos_pi or func == sin_pi or func == square:
        inner_func = build_random_function(min_depth, max_depth)
        new_func = lambda a, b, t: func(inner_func(a, b, t), t)
    return new_func


# def evaluate_random_function(f, x, y):
#     """ Evaluate the random function f with inputs x,y
#         Representation of the function f is defined in the assignment writeup

#         f: the function to evaluate
#         x: the value of x to be used to evaluate the function
#         y: the value of y to be used to evaluate the function
#         returns: the function value

#         >>> evaluate_random_function(["x"],-0.5, 0.75)
#         -0.5
#         >>> evaluate_random_function(["y"],0.1,0.02)
#         0.02
#     """
#     def prod(x, y): return x * y
#     def avg(x, y): return 0.5 * (x + y)
#     def cos_pi(x): return cos(pi * x)
#     def sin_pi(x): return sin(pi * x)
#     def x(x, y): return x
#     def y(x, y): return y
#     funcs = [prod, avg, cos_pi, sin_pi, x, y]

#     if f == ["x"]:
#         return x
#     if f == ["y"]:
#         return y

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    old_range = float(input_interval_end - input_interval_start)
    new_range = float(output_interval_end - output_interval_start)
    new_val = (val - input_interval_start) * (new_range / old_range) + output_interval_start
    return new_val


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename=None, frames=1, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    for time in range(frames):
        if frames > 1:
            filename = 'frame{}.png'.format(('00' + str(time))[-3:])
            t = remap_interval(time, 0, frames, -1, 1)
        # Create image and loop over all pixels
        im = Image.new("RGB", (x_size, y_size))
        pixels = im.load()
        for i in range(x_size):
            for j in range(y_size):
                x = remap_interval(i, 0, x_size, -1, 1)
                y = remap_interval(j, 0, y_size, -1, 1)
                pixels[i, j] = (
                        color_map(red_function(x, y, t)),
                        color_map(green_function(x, y, t)),
                        color_map(blue_function(x, y, t))
                        )

        if filename: 
            im.save(filename)
        else:
            im.save('test.png')

def lots_o_art(number):
    suffixes = range(number)
    names = ['art' + str(suffix) + '.png' for suffix in suffixes]
    for name in names:
        generate_art(name)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # lots_o_art(10)
    # generate_art("art.png")
    generate_art(frames=150)
