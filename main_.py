import pyautogui
import time
import cv2

button_image = 'button.png'

def click_button():
    try:
        button_location = pyautogui.locateCenterOnScreen(button_image, confidence=0.8) #caso tivesse outros botões muito parecidos, seria bom aumentar esse confidence
        if button_location:
            pyautogui.click(button_location)
            print('Botão clicado!')
        else:
            print('Botão não encontrado.')
    except Exception as e:
        print(f'Erro ao tentar clicar no botão: {e}')


while True:
    click_button()
    time.sleep(10)
