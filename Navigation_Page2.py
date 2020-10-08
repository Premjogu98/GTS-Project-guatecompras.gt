from selenium import webdriver
import time
from datetime import datetime
import global_var
import wx
from Scraping_Things import Scrap_data
import sys, os
import html
import ctypes
app = wx.App()
browser = webdriver.Chrome(executable_path=str(f"C:\\chromedriver.exe"))
browser.get("""https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh%3Fhl%3Den&amp;ved=2ahUKEwivq8rjlcHmAhVtxzgGHZ-JBMgQFjAAegQIAhAB""")
browser.maximize_window()
wx.MessageBox(' -_-  Add Extension and Select Proxy Between 25 SEC -_- ', 'Info', wx.OK | wx.ICON_WARNING)
time.sleep(25)

def Nav_link():
    f = open("C:\\guatecompras_links\\guatecompras_links.txt", "r")
    links = f.read()
    All_Links = links.splitlines()
    print(All_Links)
    count = 0
    for link in All_Links:
        a1 = True
        while a1 == True:
            try:
                browser.get(str(link).strip())
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
                global_var.Total += 1
                count += 1
                print(f" Total: {str(global_var.Total)} Duplicate: {str(global_var.duplicate)} Expired: {str(global_var.expired)} Inserted: {str(global_var.inserted)} Skipped: {str(global_var.skipped)} Deadline Not given: {str(global_var.deadline_Not_given)} QC Tenders: {str(global_var.QC_Tender)}\n")
                
                del All_Links[0]
                file1 = open("C:\\guatecompras_links\\guatecompras_links.txt","w")
                for link in All_Links:
                    file1.write(f"{str(link)} \n") 
                file1.close() #to change file access modes 
                a1 = False
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                      "\n", exc_tb.tb_lineno)
                browser.execute_script("location.reload(true);")
                time.sleep(10)
                a1 = True
    ctypes.windll.user32.MessageBoxW(0, f"Total: {str(global_var.Total)}\nDuplicate: {str(global_var.duplicate)}\nExpired: {str(global_var.expired)}\nInserted: {str(global_var.inserted)}\nSkipped: {str(global_var.skipped)}\nDeadline Not given: {str(global_var.deadline_Not_given)} \nQC Tenders: {str(global_var.QC_Tender)}", "guatecompras.gt", 1)
    browser.close()
    sys.exit()

Nav_link()