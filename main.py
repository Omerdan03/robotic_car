import argparse

import PySimpleGUI as sg
from car_class import Car

TOTAL_FIELD_LENGTH = 100
START_POS = 0
FIELD_X = 600
EFFECTIVE_FIELD_X = FIELD_X - 150
FIELD_Y = 120

CAR_IMG = 'car.png'
AXIS_IMG = 'axis.png'


def str2bool(input_value):
    if input_value.lower() == 'true':
        return True
    elif input_value.lower() == 'false':
        return False
    else:
        raise argparse.ArgumentTypeError('Debug arg must be True or False.')


def assert_mode(input_value):
    if input_value.lower() in ['simple', 'advance']:
        return input_value.lower()
    else:
        raise argparse.ArgumentTypeError('Mode arg must be either simple or advance.')


def get_args():
    parser = argparse.ArgumentParser(
        prog='car_gui',
        formatter_class=argparse.RawTextHelpFormatter,
        description="Runs robotic car GUI.")

    parser.add_argument('-debug', metavar='debug', default=False, type=str2bool,
                        help='option for running the GUI in debug mode. (default=False)')
    parser.add_argument('-mode', metavar='mode', default='simple', type=assert_mode,
                        help='option for selecting run mode (can be "simple" or "advance". (default=simple)')
    args = parser.parse_args()
    return args


def convert_pos_to_pixel(pos: float) -> float:
    """
    This function gets a position in physics units and return the position in pixels
    """
    pixel_pos = EFFECTIVE_FIELD_X/2 + pos * (EFFECTIVE_FIELD_X/TOTAL_FIELD_LENGTH)
    return pixel_pos


def main():
    args = get_args()

    car = Car(start_pos=START_POS, mode=args.mode)
    car_id = -1

    # Initiate the GUI element where the car will move
    field = sg.Graph(
        canvas_size=(FIELD_X, FIELD_Y),
        graph_bottom_left=(0, 0),
        graph_top_right=(FIELD_X, FIELD_Y),
        background_color='white')

    # Initiate the GUI window
    window = sg.Window(title='CAR', layout=[[field],
                                            [sg.Image(AXIS_IMG, size=(FIELD_X, FIELD_Y/2))],
                                            [sg.Text('Current position: '), sg.Text(car.pos, key='car_pos')],
                                            [sg.Text('Target position: '), sg.Input(0, key='target_pos')],
                                            [sg.Text('Velocity : '), sg.Input(0, key='car_speed'), sg.Text('Units/sec')],
                                            [sg.Button('MOVE', key='activation_button'), sg.Button('Quit')]],
                       margins=(400, 300))
    while True:
        event, values = window.read(timeout=50)

        # Draw car figure on the board (if there is old figure delete it)
        if car_id != -1:
            field.delete_figure(car_id)
        car_id = field.draw_image(filename=CAR_IMG, location=(convert_pos_to_pixel(car.pos), FIELD_Y))

        # Get target position from target_pos input
        try:
            car.target_pos = float(values['target_pos'])
        except ValueError:
            pass  # todo add pop-up when inserted invalid number

        if args.mode == 'simple':
            # Get car position from target_pos input
            try:
                car.speed = float(values['car_speed'])
            except ValueError:
                pass  # todo add pop-up when inserted invalid number

        # Change car activation according to the activation button
        if event == 'activation_button':
            if car.is_active:
                window['activation_button'].update('MOVE')
                window['target_pos'].update(disabled=False)
                if args.mode == 'simple':
                    window['car_speed'].update(disabled=False)
            else:
                window['activation_button'].update('STOP')
                window['target_pos'].update(disabled=True)
                if args.mode == 'simple':
                    window['car_speed'].update(disabled=True)

            car.is_active = not car.is_active

        # Update car position and speed texts
        window['car_pos'].update(car.pos)
        window['car_speed'].update(car.speed)

        # Print car stats for debugging
        print(car) if args.debug else None

        # Move car according to physics
        car.run()

        # In case window is closed or Quit button is clicked closed the window
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        window.refresh()

    window.close()

if __name__ == '__main__':
    main()
