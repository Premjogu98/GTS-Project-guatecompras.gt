from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import global_var
import html
from Scraping_Things import Scrap_data
import sys, os
import ctypes
import wx
from googletrans import Translator
app = wx.App()


def ChromeDriver():
    # File_Location = open("D:\\0 PYTHON EXE SQL CONNECTION & DRIVER PATH\\guatecompras.gt\\Location For Database & Driver.txt", "r")
    # TXT_File_AllText = File_Location.read()
    # Chromedriver = str(TXT_File_AllText).partition("Driver=")[2].partition("\")")[0].strip()
    # chrome_options = Options()
    # chrome_options.add_extension('D:\\0 PYTHON EXE SQL CONNECTION & DRIVER PATH\\guatecompras.gt\\Browsec-VPN.crx')  # ADD EXTENSION Browsec-VPN
    # browser = webdriver.Chrome(executable_path=str(Chromedriver),
    #                            chrome_options=chrome_options)
    # browser = webdriver.Chrome(executable_path=str(Chromedriver))
    browser = webdriver.Chrome(executable_path=str(f"C:\\chromedriver.exe"))
    browser.get("""https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh%3Fhl%3Den&amp;ved=2ahUKEwivq8rjlcHmAhVtxzgGHZ-JBMgQFjAAegQIAhAB""")

    wx.MessageBox(' -_-  Add Extension and Select Proxy Between 25 SEC -_- ', 'Info', wx.OK | wx.ICON_WARNING)
    time.sleep(25)  # WAIT UNTIL CHANGE THE MANUAL VPN SETTING
    browser.get("https://www.guatecompras.gt/concursos/consultaConAvanz.aspx")
    browser.maximize_window()
    # browser.switch_to.window(browser.window_handles[1])
    # browser.close()
    # browser.switch_to.window(browser.window_handles[0])
    # time.sleep(2)
    time.sleep(1)
    # time.sleep(20)  # WAIT UNTIL CHANGE THE MANUAL VPN SETTING
    # browser.get("https://www.guatecompras.gt/concursos/consultaConAvanz.aspx")

    # browser.set_window_size(1024 , 600)
    # browser.maximize_window()
    # browser.switch_to.window(browser.window_handles[1])
    # browser.close()
    # browser.switch_to.window(browser.window_handles[0])
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
    # if From_date != "":
        # translator = Translator()
        # translator_text = translator.translate(str(From_date))
        # From_date = translator_text.text
        # From_date = From_date.replace(" de ", ".")
        # From_date = Translate(From_date).replace(" de ", ".")

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
    # if To_date != "":
        # translator = Translator()
        # translator_text = translator.translate(str(To_date))
        # To_date = translator_text.text
        # To_date = To_date.replace(" de ", ".")
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
            Nav_link(browser,List_href)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,"\n", exc_tb.tb_lineno)
            a = True


def Nav_link(browser,List_href):
    Main_href = []
    for href1 in List_href:
        if href1 not in Main_href:  # Remove Duplicate Links From Above List
            Main_href.append(href1)
    time.sleep(3)
    count = 0
    for link in Main_href:
        global a1
        a1 = True
        while a1 == True:
            try:
                browser.get(link)
                global_var.Total += 1
                Above_OuterHtml = ""
                for Contest_Detail in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_WUCDetalleConcurso_divDetalleConcurso"]'):
                    Contest_Detail = Contest_Detail.get_attribute("outerHTML")
                    Above_OuterHtml += Contest_Detail
                    break
                for Contest_Tab_Detail in browser.find_elements_by_xpath('//*[@id="MasterGC_ContentBlockHolder_divContenidoTab"]'):
                    Contest_Tab_Detail = Contest_Tab_Detail.get_attribute("outerHTML")
                    Above_OuterHtml += Contest_Tab_Detail
                    break
                Above_OuterHtml = Above_OuterHtml.replace('href="/concursos/','href="https://www.guatecompras.gt/concursos/').replace('href="/compradores/', 'href="https://www.guatecompras.gt/compradores/').replace('src="/imagenes/','src="https://www.guatecompras.gt/imagenes/').replace(
                    'position: fixed; left: 0px; top: 0px; z-index', '').replace('alt="Procesando"', '').replace(
                    'Por favor, espere un momento...', '').replace("indicator.gif", '')
                Entity_name_url = Above_OuterHtml.partition("Entidad:")[2].partition("</tr>")[0]
                Entity_name_url = Entity_name_url.partition('<a href="')[2].partition('\"')[0]
                Entity_name_Decoded_url = html.unescape(str(Entity_name_url))
                browser.get(Entity_name_Decoded_url)
                for Entity_name_URL_data in browser.find_elements_by_xpath('//*[@class="TablaForm3"]'):
                    Entity_name_URL_data = Entity_name_URL_data.get_attribute("outerHTML")
                    Above_OuterHtml += "<br><h2>Buyer Entity Detail</h2><br>" + Entity_name_URL_data
                    # browser.execute_script("window.history.go(-1)")
                    # time.sleep(2)
                    break
                Scrap_data(browser, Above_OuterHtml)
                count += 1
                print(f" Total: {str(global_var.Total)} Duplicate: {str(global_var.duplicate)} Expired: {str(global_var.expired)} Inserted: {str(global_var.inserted)} Skipped: {str(global_var.skipped)} Deadline Not given: {str(global_var.deadline_Not_given)} QC Tenders: {str(global_var.QC_Tender)}\n")
                time.sleep(5)
                if count == 20:
                    count = 0
                    browser.execute_script("location.reload(true);")
                    time.sleep(4)
                a1 = False
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                      "\n", exc_tb.tb_lineno)
                time.sleep(10)
                a1 = True
    ctypes.windll.user32.MessageBoxW(0, f"Total: {str(global_var.Total)}\nDuplicate: {str(global_var.duplicate)}\nExpired: {str(global_var.expired)}\nInserted: {str(global_var.inserted)}\nSkipped: {str(global_var.skipped)}\nDeadline Not given: {str(global_var.deadline_Not_given)} \nQC Tenders: {str(global_var.QC_Tender)}", "guatecompras.gt", 1)
    browser.close()
    sys.exit()


ChromeDriver()
