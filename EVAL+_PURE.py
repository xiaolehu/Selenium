from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import pyautogui
import time
import keyboard
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
browser = webdriver.Chrome(options=options)
# 获取所有打开的窗口句柄
window_handles = browser.window_handles

# 假设你想切换到第二个窗口（根据你的需要调整）
target_window_handle = window_handles[1]  # 0 是第一个窗口，1 是第二个窗口

# 切换到目标窗口
browser.switch_to.window(target_window_handle)
previous_p_element2 = ''
paused = True
was_paused = True  # 用于检测暂停状态的变化

def toggle_pause():
    global paused
    paused = not paused
    if paused:
        print("Script paused.")
    else:
        print("Script resumed.")

# 监听 Tab 键
keyboard.add_hotkey('tab', toggle_pause)

while True:
    if paused:
        was_paused = True  # 标记脚本处于暂停状态
        continue
    else:
        # 检测到从暂停状态恢复
        if was_paused:
            previous_p_element2 = ''  # 恢复时重置 previous_p_element2
            was_paused = False  # 重置暂停状态标记

        try:
            current_p_element2 = browser.find_element(By.XPATH,"/html/body/app-root/main/app-player/div[2]/div[3]/div[4]/div/app-test-info/div[1]/div[1]/span[2]").text

            if current_p_element2 != previous_p_element2:
                time.sleep(1)
                try:
                    # 找到指定的p标签并打印其文本内容
                    p_element = browser.find_element(By.XPATH,"/html/body/app-root/main/app-player/div[2]/div[3]/div[4]/div/app-test-info/div[1]/div[2]/app-sequence-informations-display/div/div[2]/div[3]/p").text.replace(' ','')

                except:
                    p_element = browser.find_element(By.XPATH,"/html/body/app-root/main/app-player/div[2]/div[3]/div[4]/div/app-test-info/div[1]/div[2]/app-sequence-informations-display/div/div[2]/div[4]/p").text.replace(' ','')

                # print(p_element)
                # print(p_element2)
                previous_p_element2 = current_p_element2

                # 初始化变量
                transaction_amount = "1000"
                arc_value = "3030"
                transaction_type = "00"
                amount_match = re.search(r'Pleaseentertransactionamountas(\d+(\.\d{2})?)', p_element)
                if amount_match:
                    # 获取匹配到的金额值
                    transaction_amount = amount_match.group(1)
                    # 如果没有小数点，则在末尾加上两个零
                    if "." not in transaction_amount:
                        transaction_amount += "00"
                        # 去除小数点
                        transaction_amount = transaction_amount.replace(".", "")
                    else:
                        transaction_amount = transaction_amount.replace(".", "")
                # 确保transaction_amount长度为12，不足前面补零
                transaction_amount = transaction_amount.zfill(12)

                # 匹配文本中的ARC值
                arc_match = None
                if "PleaseconfigurehosttosendARC" in p_element or "PleaseconfigurehostsuchthatARC" in p_element:
                    arc_match = re.search(r'PleaseconfigurehosttosendARC=3030|PleaseconfigurehostsuchthatARC=3030', p_element)
                    if arc_match:
                        arc_value = "3030"
                    else:
                        arc_value = "3035"  # 如果不是=3030，则使用3035作为默认值

                # 匹配文本中的Transaction type
                transaction_type_match = re.search(r'Transactiontypeas(\d{2})', p_element)
                if transaction_type_match:
                    transaction_type = transaction_type_match.group(1)

                # 如果输出文本为 "None"，则使用默认值
                if p_element.strip() == "None":
                    transaction_amount = "000000001000"
                    arc_value = "3030"
                    transaction_type = "00"


                # print(transaction_amount)
                # print(transaction_type)
                # print(arc_value)

                pyautogui.moveTo(-137,750)
                pyautogui.doubleClick()
                time.sleep(0.1)
                pyautogui.typewrite(transaction_amount)

                # pyautogui.moveTo(435,225)
                # pyautogui.doubleClick()
                # pyautogui.typewrite(arc_value)

                pyautogui.moveTo(-168,723)
                pyautogui.doubleClick()
                time.sleep(0.1)
                pyautogui.typewrite(transaction_type)
                time.sleep(0.5)
                pyautogui.click(-265,964)
                pyautogui.click(-673,623)
            time.sleep(2)

        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(2)  # 等待2秒后重试