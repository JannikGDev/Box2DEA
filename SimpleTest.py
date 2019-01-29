from Environment import Environment
import time


def show_solution(solution):

    env = Environment(solution, render=True)
    step = 0
    while env.running:
        env.step()
        #time.sleep(0.015)
        env.save_image("data/images/step_"+str(step)+".png")
        step += 1

    return env.exit()


if __name__ == "__main__":

    solution = (0.02, 0.8,   0.0, 1.0,    0.98, 0.8)

    show_solution(solution)
