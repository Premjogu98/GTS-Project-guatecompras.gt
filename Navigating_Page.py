from selenium import webdriver
import time
from datetime import datetime
import global_var
import html
import ctypes
import wx
import sys, os
from googletrans import Translator
app = wx.App()


def ChromeDriver():
    browser = webdriver.Chrome(executable_path=str(f"C:\\chromedriver.exe"))
    browser.get("""https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh%3Fhl%3Den&amp;ved=2ahUKEwivq8rjlcHmAhVtxzgGHZ-JBMgQFjAAegQIAhAB""")

    wx.MessageBox(' -_-  Add Extension and Select Proxy Between 25 SEC -_- ', 'Info', wx.OK | wx.ICON_WARNING)
    time.sleep(25)  # WAIT UNTIL CHANGE THE MANUAL VPN SETtING
    browser.get("https://www.guatecompras.gt/concursos/consultaConAvanz.aspx")
    browser.maximize_window()
    time.sleep(1)
    for Click_Estatus in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_ddlEstatus"]/option[1]'):
        Click_Estatus.click()
        time.sleep(3)
        break
    for Fecha in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_ddlTipoFecha"]/option[1]'):
        Fecha.click()
        time.sleep(8)
        break

    From_date = global_var.From_Date.partition("Date (FROM)")[2].partition("00:")[0].strip()
    From_date = datetime.strptime(From_date , '%Y-%m-%d')
    From_date = From_date.strftime("%d.%B.%Y").lower()
    From_date = From_date.replace('january', 'enero').replace('february', 'febrero').replace('march', 'marzo') \
        .replace('april', 'abril').replace('may', 'Mayo').replace('june', 'junio').replace('july', 'julio') \
        .replace('august', 'agosto').replace('september', 'septiembre').replace('october', 'octubre') \
        .replace('november', 'noviembre').replace('december', 'diciembre')

    for SetFrom_date in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_txtFechaIni"]'):
        browser.execute_script("arguments[0].value = arguments[1]" , SetFrom_date , str(From_date))
        break
    time.sleep(3)

    To_date = global_var.To_Date.partition("Date (TO)")[2].partition("00:")[0].strip()
    To_date = datetime.strptime(To_date , '%Y-%m-%d')
    To_date = To_date.strftime("%d.%B.%Y").lower()
    To_date = To_date.replace('january', 'enero').replace('february', 'febrero').replace('march', 'marzo')\
        .replace('april', 'abril').replace('may', 'Mayo').replace('june', 'junio').replace('july', 'julio') \
        .replace('august', 'agosto').replace('september', 'septiembre').replace('october', 'octubre') \
        .replace('november', 'noviembre').replace('december', 'diciembre')
    for SetTo_date in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_txtFechaFin"]'):
        browser.execute_script("arguments[0].value = arguments[1]" , SetTo_date , str(To_date))
        break
    time.sleep(3)
    for Search in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_btnBuscar"]'):
        Search.click()
        break
    time.sleep(13)
    for NO_data_Found in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_lblMensaje"]'):
        NO_data_Found = NO_data_Found.get_attribute('innerHTML').strip()
        if NO_data_Found == 'No existen concursos, de acuerdo a los parámetros elegidos.':
            wx.MessageBox(' -_-  No Data Found ', 'guatecompras.gt', wx.OK | wx.ICON_INFORMATION)
        break

    Collect_link(browser)


def Collect_link(browser):
    List_href = []
    a = True
    while a == True:
        try:
            for next_page in range(1, 11, 1):
                a1 = False
                while a1 == False:
                    try:
                        for table_href in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_dgResultado"]/tbody/tr/td[2]/div/div/a'):
                            List_href.append(table_href.get_attribute('href'))
                        for next_page_btn in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_dgResultado"]/tbody/tr[52]/td/a['+str(next_page)+']'):
                            next_page_btn.click()
                            break
                        a1 = True
                    except:
                        a1 = False

            for next_page in range(5, 15, 1):
                a2 = False
                while a2 == False:
                    try:
                        for table_href in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_dgResultado"]/tbody/tr/td[2]/div/div/a'):
                            List_href.append(table_href.get_attribute('href'))
                        for next_page_btn in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_dgResultado"]/tbody/tr[52]/td/a['+str(next_page)+']'):
                            next_page_btn.click()
                            break
                        a2 = True
                    except:
                        a2 = False

            for next_page in range(2, 12, 1):
                a3 = False
                while a3 == False:
                    try:
                        for table_href in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_dgResultado"]/tbody/tr/td[2]/div/div/a'):
                            List_href.append(table_href.get_attribute('href'))
                        for next_page_btn in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_dgResultado"]/tbody/tr[52]/td/a[' + str(next_page) + ']'):
                            next_page_btn.click()
                            break
                        a3 = True
                    except:
                        a3 = False
            for next_page in range(2, 12, 1):
                a4 = False
                while a4 == False:
                    try:
                        for table_href in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_dgResultado"]/tbody/tr/td[2]/div/div/a'):
                            List_href.append(table_href.get_attribute('href'))
                        for next_page_btn in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_dgResultado"]/tbody/tr[52]/td/a[' + str(next_page) + ']'):
                            next_page_btn.click()
                            break
                        a4 = True
                    except:
                        a4 = False
            a = False
            Main_href = []
            for href1 in List_href:
                if href1 not in Main_href:  # Remove Duplicate Links From Above List
                    Main_href.append(href1)
            file1 = open("C:\\guatecompras_links\\guatecompras_links.txt","w")
            for link in Main_href:
                file1.write(f"{str(link)} \n") 
            file1.close() #to change file access modes 
            wx.MessageBox(f' Total Link Collected: {len(Main_href)}', 'Info', wx.OK | wx.ICON_INFORMATION)
            browser.close()
            sys.exit()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,"\n", exc_tb.tb_lineno)
            a = True

ChromeDriver()
