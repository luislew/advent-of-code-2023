from day_15 import get_steps, LightBoxes


if __name__ == "__main__":
    boxes = LightBoxes()
    for step in get_steps():
        boxes.process_step(step)
    print(boxes.get_focusing_power())
