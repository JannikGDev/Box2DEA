from Environment import Environment
import time
from PIL import Image, ImageDraw, ImageFont


def show_solution(values):

    env = Environment(values, render=True)

    while env.running:
        env.step()
        time.sleep(0.015)

    return env.exit()


def print_solution(values, filename, stats=None):
    env = Environment(values, render=True)

    env.step()

    env.save_image(filename)

    if stats is not None:

        img = Image.open(filename)

        draw = ImageDraw.Draw(img)
        fnt = ImageFont.truetype('data/font.ttf', 30)
        draw.text((10, 10), "Gen: " + str(stats[0]), fill=(255, 255, 255), font=fnt)
        draw.text((10, 40), "Sigma: " + str(stats[1]), fill=(255, 255, 255), font=fnt)
        draw.text((10, 40), "Mutations: " + str(stats[2]), fill=(255, 255, 255), font=fnt)

        img.save(filename)

    return env.exit()


def load_solutions(filename):

    values = []

    with open(filename) as f:
        for line in f:
            part = line.split(",")

            numbers = []

            for s in part:
                numbers.append(float(s))

            values.append(numbers)

    return values


if __name__ == "__main__":

    solutions = load_solutions("data/best_solutions.txt")



    for i, s in enumerate(solutions):

        stats = [i,0.2,10]

        print_solution(s, "data/images/image_"+str(i)+".png",stats)
