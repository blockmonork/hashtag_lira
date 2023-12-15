import pyautogui
import time

# script pra capturar a posicao x-y do mouse apenas...faça em 7 segundos!


class GetPosition:

    monitor_origem = (1366, 768)  # 1366,768

    common_task = [
        {
            'start_menu': {'x': 10, 'y': 6}
        },
        {
            'terminal': {'x': 100, 'y': 4}
        },
    ]

    def __init__(self):
        pass

    def int_calc(self, valor_origem, valor_novo, constante):
        return int(round((int(valor_novo) / int(valor_origem)) * int(constante), 0))

    def convert_screen(self, monitor_destino=(0, 0), x_origem=0, y_origem=0):
        # return new (x, y)
        x = int(x_origem)
        y = int(y_origem)
        return (
            x if x <= 10 else self.int_calc(
                self.monitor_origem[0], monitor_destino[0], x),
            y if y <= 10 else self.int_calc(
                self.monitor_origem[1], monitor_destino[1], y)
        )

    def print_common_task(self):
        print('======= common task =======')
        print(
            f'(para monitor {self.monitor_origem[0]} x {self.monitor_origem[1]})')
        for x in self.common_task:
            for y in x:
                print(f'{y}: x=({x[y]["x"]}) , y=({x[y]["y"]})')

    def get_common_task(self, task):
        for x in self.common_task:
            for y in x:
                if y == task:
                    return (x[y]['x'], x[y]['y'])
        return False

    def get_position_run(self):
        # print(p.KEYBOARD_KEYS)
        print(pyautogui.position())
        print("=======")
        # print( p.press('printscreen') )

    def temporizador(self, t):
        print(t)
        t -= 1
        time.sleep(1)
        if t > 0:
            self.temporizador(t)
        else:
            self.get_position_run()

    def start_mouse_capture(self):
        print("=======| pyautogui get_position |=======")
        tempo = int(
            input("qual o tempo de contagem regressiva antes de pegar as posições?  "))
        autoloop = input(
            "ao terminar a contagem, voltar para esta tela (S|N)?  ")
        autoloop = autoloop.upper()

        if tempo <= 0:
            print("tempo deve ser maior que zero")
            self.start_mouse_capture()

        if autoloop != "S" and autoloop != "N":
            print("autoloop deve ser S para sim ou N para não")
            self.start_mouse_capture()

        self.temporizador(tempo)

        if autoloop == "S":
            self.start_mouse_capture()
# end class


class MyAutoGui:

    dir_img = '~/Imagens'
    dir_home = '~/home'
    dir_docs = '~/home/Documentos'
    gp = None
    monitor = ()
    emails_account = {
        'blockmonork': '0',
        'fafmmoreira': '1'
    }

    def __init__(self, pause_between_actions=.5, resolution=(1366, 768)) -> None:
        pyautogui.PAUSE = pause_between_actions
        self.gp = GetPosition()
        self.monitor = resolution

    def set_emails_account(self, dict_emails_account):
        self.emails_account = dict_emails_account

    def get_xy(self, _x, _y):
        return self.gp.convert_screen(self.monitor, _x, _y)

    def wait(self, delay):
        if delay > 0:
            pyautogui.sleep(delay)

    def tabs(self, times):
        for i in range(0, times+1):
            pyautogui.press('tab')
            self.wait(.5)

    def click(self, x, y, repeat=2):
        # bug click not working on browser
        for i in range(1, repeat):
            pyautogui.click(x+i, y+i)
            self.wait(.3)

    def move_mouse(self, to_x, to_y):
        pyautogui.move(to_x, to_y)

    def open_terminal(self):
        t = self.gp.get_common_task('terminal')
        terminal = self.get_xy(t[0], t[1])
        pyautogui.click(terminal[0], terminal[1])
        pyautogui.sleep(.5)

    def start_menu(self):
        m = self.gp.get_common_task('start_menu')
        st = self.get_xy(m[0], m[1])
        pyautogui.click(st[0], st[1])
        pyautogui.sleep(.5)

    def start_application(self, app_name, delay=0.0):
        self.wait(delay)
        self.start_menu()
        pyautogui.write(app_name)
        pyautogui.press('enter')

    def go_to_url(self, url, browser, delay=0.0):
        self.wait(delay)
        self.start_application(browser)
        self.wait(5)
        if browser == 'firefox':
            self.tabs(16)  # to go to navbar url
        # TODO: add else se chrome e tela 'selecione o perfil' estiver ativa. incluir os clicks nesta tela/perfil
        pyautogui.write(url)
        pyautogui.press('enter')

    def write_email(self, account, to, subject, message, delay=0.0):
        # user = 0 if account == 'blockmonork' else 1
        user = self.emails_account[account]
        self.go_to_url(
            f'https://mail.google.com/mail/?tab=rm&authuser={user}&ogbl',
            'chrome',
            delay
        )

        self.wait(5)
        self.move_mouse(41, 240)
        self.click(x=41, y=240)  # click new email
        self.wait(3)
        pyautogui.write(to)
        self.tabs(1)
        pyautogui.write(subject)
        # casos em que tab conta +1!
        self.tabs(0)
        # self.click(x=947, y=473)
        self.wait(.5)
        pyautogui.write(message)
        self.tabs(0)
        pyautogui.press('enter')

    def screenshot(self, delay=0.0):
        self.wait(delay)
        self.open_terminal()
        pyautogui.write(
            f"scrot '%Y-%m-%d_%H-%M-%S_scrot.png' -e 'mv $f {self.dir_img}'")
        pyautogui.press('enter')
        self.wait(.5)
        pyautogui.write('exit')
        pyautogui.press('enter')

    def turn_off_pc(self, delay=0.0):
        self.wait(delay)
        self.open_terminal()
        pyautogui.write('shutdown')
        pyautogui.press('enter')

# end class

# mag = MyAutoGui(1)

# mag.gp.start_mouse_capture()

# mag.open_terminal()
# mag.screenshot(3)
# mag.wait(2)
# mag.turn_off_pc()
# mag.open_browser('firefox')
# mag.open_browser('chrome')
# mag.go_to_url('http://cptlnrmtl.app.br/normatel', 'firefox')
# mag.go_to_url('http://cptlnrmtl.app.br/normatel', 'chrome')
# mag.write_email('blockmonork', 'fafmmoreira@gmail.com', 'testando MyAutoGui', 'apenas um teste')
# mag.write_email('fafmmoreira', 'blockmonork@gmail.com', 'testando MyAutoGui', 'apenas um teste')


classes_my_pyautogui_comments = '''
gp = GetPosition()

#gp.start_mouse_capture()
#gp.print_common_task()

# teste - convertendo common_task start_menu pra monitor 1024x768
pos_x = gp.common_task[0]['start_menu']['x']
pos_y = gp.common_task[0]['start_menu']['y']

new_pos = gp.convert_screen( (2732,1536), pos_x, pos_y )
print(f'antes: x={pos_x}, y={pos_y}, depois={new_pos}')

new_pos = gp.convert_screen( (683,384), pos_x, pos_y )
print(f'antes: x={pos_x}, y={pos_y}, depois={new_pos}')

new_pos = gp.convert_screen( (2732,1536), 1346, 762 )
print(f'antes: x={pos_x}, y={pos_y}, depois={new_pos}')

start_menu = gp.get_common_task('start_menu')
if start_menu:
    print(start_menu)

'''
