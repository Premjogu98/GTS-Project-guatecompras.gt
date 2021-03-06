import re
import time
import urllib.request
import urllib.parse
import sys , os
import string
from datetime import datetime,timedelta
import global_var
import requests
import html
from Insert_On_Datbase import create_filename,insert_in_Local
import wx
import html
app = wx.App()


# def Translate_close(text_without_translate):
#     String2 = ""
#     try:
#         String2 = str(text_without_translate)
#         url = "https://translate.google.com/m?hl=en&sl=auto&tl=en&ie=UTF-8&prev=_m&q=" + str(String2) + ""
#         response1 = requests.get(str(url))
#         response2 = response1.url
#         user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
#         headers = {'User-Agent': user_agent , }
#         request = urllib.request.Request(response2, None , headers)  # The assembled request
#         time.sleep(1.2)
#         response = urllib.request.urlopen(request)
#         htmldata: str = response.read().decode('utf-8')
#         trans_data = re.search(r'(?<=dir="ltr" class="t0">).*?(?=</div>)', htmldata).group(0)
#         trans_data = html.unescape(str(trans_data))
#         return trans_data
#     except:
#         return String2


def Scrap_data(browser, get_htmlSource):

    SegFeild = []
    for data in range(45):
        SegFeild.append('')
    Decoded_get_htmlSource: str = html.unescape(str(get_htmlSource))
    Decoded_get_htmlSource: str = re.sub(' +', ' ', str(Decoded_get_htmlSource)).replace("\n","").replace("<br>","")
    a = True
    while a == True:
        try:
            # ==================================================================================================================
            # Email_ID

            Email_ID = Decoded_get_htmlSource.partition("Direcciones de Correo:</td>")[2].partition("</tr>")[0]
            Email_ID = Email_ID.partition("<a href=")[2].partition("</td>")[0]
            Email_ID = Email_ID.partition(">")[2].partition("</a>")[0].strip()
            SegFeild[1] = Email_ID

            # ==================================================================================================================
            # Address

            Municipality = Decoded_get_htmlSource.partition("Municipio:")[2].partition("</span>")[0]
            cleanr = re.compile('<.*?>')
            Municipality = re.sub(cleanr, '', Municipality).strip()
            # if Municipality != "":
            #     Municipality = Translate(Municipality).lower()
            # else:pass

            Direction = Decoded_get_htmlSource.partition("Dirección:")[2].partition("</span>")[0]
            cleanr = re.compile('<.*?>')
            Direction = re.sub(cleanr, '', Direction)
            # if Direction != "":
            #     Direction = Translate(Direction).strip()
            # else:pass

            Phones = Decoded_get_htmlSource.partition("Teléfonos:")[2].partition("</span>")[0]
            cleanr = re.compile('<.*?>')
            Phones = re.sub(cleanr, '', Phones).strip()

            Fax_Numbers = Decoded_get_htmlSource.partition("Números de Fax:")[2].partition("</span>")[0]
            cleanr = re.compile('<.*?>')
            Fax_Numbers = re.sub(cleanr, '', Fax_Numbers).strip()

            Postal_mail = Decoded_get_htmlSource.partition("Apartado Postal:")[2].partition("</span>")[0]
            cleanr = re.compile('<.*?>')
            Postal_mail = re.sub(cleanr, '', Postal_mail).strip()

            if Postal_mail != "[--No Especificado--]":
                Collected_Address = Municipality + "," + Direction + "<br>\n" + "Teléfonos: " + Phones + "<br>\n" + "Números de Fax: " + Fax_Numbers + "<br>\n" + "Apartado Postal: " + Postal_mail
                SegFeild[2] = Collected_Address
            else:
                Collected_Address = str(Municipality) + "," + str(Direction) + "<br>\n" + "Teléfonos: " + str(Phones)
                Collected_Address = string.capwords(str(Collected_Address.strip()))
                SegFeild[2] = Collected_Address

            # ==================================================================================================================
            # Country

            SegFeild[7] = "GT"

            # ==================================================================================================================
            # Purchaser WebSite URL

            Websites = Decoded_get_htmlSource.partition("Páginas Web:")[2].partition("</tr>")[0]
            Websites = Websites.partition("<a href=\"")[2].partition("\" target")[0].strip()
            if Websites != "[--No Especificado--]":
                SegFeild[8] = Websites.strip()
            else:
                SegFeild[8] = ""

            # ==================================================================================================================
            # Purchaser Name

            Entity = Decoded_get_htmlSource.partition("MasterGC_ContentBlockHolder_lblEntidad")[2].partition("</span>")[0]
            Entity = Entity.partition('">')[2].strip()
            if Entity != "":
                # Entity = Translate(Entity)
                SegFeild[12] = Entity.strip().upper()
            else:
                SegFeild[12] = ""

            # ==================================================================================================================
            # Tender no

            Tender_no = Decoded_get_htmlSource.partition("NOG:")[2].partition("</b>")[0]
            cleanr = re.compile('<.*?>')
            Tender_no = re.sub(cleanr, '', Tender_no)
            SegFeild[13] = Tender_no.strip()

            # ==================================================================================================================
            # notice type
            SegFeild[14] = "2"

            # ==================================================================================================================
            # Tender Details

            Title = Decoded_get_htmlSource.partition("Descripción:  </div>")[2].partition("</div>")[0]
            cleanr = re.compile('<.*?>')
            Title = re.sub(cleanr, '', Title)
            Title = string.capwords(str(Title.strip()))
            if Title != "":
                # Title = Translate(Title)
                SegFeild[19] = Title
            else: pass

            Modality = Decoded_get_htmlSource.partition("Modalidad:  </div>")[2].partition("</div>")[0]
            cleanr = re.compile('<.*?>')
            Modality = re.sub(cleanr, '', Modality)
            Modality = string.capwords(str(Modality.strip()))
            # if Modality != "":
            #     Modality = Translate(Modality)
            # else:
            #     pass

            Type_of_contest = Decoded_get_htmlSource.partition("Tipo de concurso:  </div>")[2].partition("</div>")[0]
            cleanr = re.compile('<.*?>')
            Type_of_contest = re.sub(cleanr, '', Type_of_contest)
            Type_of_contest = string.capwords(str(Type_of_contest.strip()))
            # if Type_of_contest != "":
            #     Type_of_contest = Translate(Type_of_contest)
            # else:pass

            Receiving_Offers = Decoded_get_htmlSource.partition("Tipo de recepción de ofertas: </div>")[2].partition("</div>")[0]
            cleanr = re.compile('<.*?>')
            Receiving_Offers = re.sub(cleanr, '', Receiving_Offers).strip()
            Receiving_Offers = string.capwords(str(Receiving_Offers.strip()))
            # if Receiving_Offers != "":
            #     Receiving_Offers = Translate(Receiving_Offers)
            # else:pass

            Process_Type = Decoded_get_htmlSource.partition("Tipo Proceso:  </div>")[2].partition("</div>")[0]
            cleanr = re.compile('<.*?>')
            Process_Type = re.sub(cleanr, '', Process_Type)
            Process_Type = string.capwords(str(Process_Type.strip()))
            # if Process_Type != "":
            #     Process_Type = Translate(Process_Type)
            # else:pass

            Compliance_Bond_percentage = Decoded_get_htmlSource.partition("Porcentaje de Fianza de cumplimiento:  </div>")[2].partition("</div>")[0]
            cleanr = re.compile('<.*?>')
            Compliance_Bond_percentage = re.sub(cleanr, '', Compliance_Bond_percentage)
            # if Compliance_Bond_percentage != "":
            #     Compliance_Bond_percentage = Translate(Compliance_Bond_percentage).strip()
            # else:
            #     pass
            Percentage_of_support_bond = Decoded_get_htmlSource.partition("Porcentaje de Fianza de sostenimiento:  </div>")[2].partition("</div>")[0]
            cleanr = re.compile('<.*?>')
            Percentage_of_support_bond = re.sub(cleanr, '', Percentage_of_support_bond).strip()

            Status = Decoded_get_htmlSource.partition("> Estatus:  </div>")[2].partition("</div>")[0]
            cleanr = re.compile('<.*?>')
            Status = re.sub(cleanr, '', Status).strip()
            Status = string.capwords(str(Status.strip()))
            # if Status != "":
            #     Status = Translate(Status)
            # else:
            #     pass

            Collected_Tender_Details = str(Title) + "<br>\n" + "Modalidad: " + str(Modality) + "<br>\n" + "Tipo de concurso: " + str(Type_of_contest) + "<br>\n" + "Tipo de recepción de ofertas: " + str(Receiving_Offers)\
                                        + "<br>\n" + "Tipo Proceso: " + str(Process_Type) + "<br>\n" + "Porcentaje de Fianza de cumplimiento: " + str(Compliance_Bond_percentage) + "<br>\n" + "Porcentaje de Fianza de sostenimiento: " + str(Percentage_of_support_bond) \
                                        + "<br>\n" + "Estatus: " + str(Status)
            Collected_Tender_Details = string.capwords(str(Collected_Tender_Details.strip()))
            SegFeild[18] = Collected_Tender_Details

            # ==================================================================================================================
            # Tender Submission Date

            Bid_submission_date = Decoded_get_htmlSource.partition("Fecha de presentación de ofertas:  </div>")[2].partition("</div>")[0]
            cleanr = re.compile('<.*?>')
            Bid_submission_date = re.sub(cleanr, '', Bid_submission_date)
            Bid_submission_date = Bid_submission_date.partition("Hora:")[0].strip().replace(' ', '')
            Month = Bid_submission_date.partition(".")[2].partition(".")[0].strip().lower()

            if Month == "enero":
                Bid_submission_date = Bid_submission_date.replace('.enero.', '.January.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFeild[24] = mydate

            elif Month == "febrero":
                Bid_submission_date = Bid_submission_date.replace('.febrero.', '.February.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFeild[24] = mydate

            elif Month == "marzo":
                Bid_submission_date = Bid_submission_date.replace('.marzo.', '.March.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFeild[24] = mydate

            elif Month == "abril":
                Bid_submission_date = Bid_submission_date.replace('.abril.', '.April.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFeild[24] = mydate

            elif Month == "mayo":
                Bid_submission_date = Bid_submission_date.replace('.mayo.', '.May.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFeild[24] = mydate

            elif Month == "junio":
                Bid_submission_date = Bid_submission_date.replace('.junio.', '.June.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFeild[24] = mydate

            elif Month == "julio" :
                Bid_submission_date = Bid_submission_date.replace('.julio.', '.July.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFeild[24] = mydate

            elif Month == "agosto":
                Bid_submission_date = Bid_submission_date.replace('.agosto.', '.August.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFeild[24] = mydate

            elif Month == "septiembre" :
                Bid_submission_date = Bid_submission_date.replace('.septiembre.', '.September.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFeild[24] = mydate

            elif Month == "octubre":
                Bid_submission_date = Bid_submission_date.replace('.octubre.', '.October.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFeild[24] = mydate

            elif Month == "noviembre":
                Bid_submission_date = Bid_submission_date.replace('.noviembre.', '.November.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFeild[24] = mydate

            elif Month == "diciembre":
                Bid_submission_date = Bid_submission_date.replace('.diciembre.', '.December.')
                datetime_object = datetime.strptime(Bid_submission_date, '%d.%B.%Y')
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegFeild[24] = mydate

            SegFeild[22] = "0"

            SegFeild[26] = "0.0"

            SegFeild[27] = "0" # Financier

            SegFeild[28] = "https://www.guatecompras.gt/concursos/consultaConcurso.aspx?nog="+str(SegFeild[13]).strip()

            # Source Name
            SegFeild[31] = 'guatecompras.gt'

            SegFeild[20] = ''
            SegFeild[21] = ''
            SegFeild[42] = SegFeild[7]
            SegFeild[43] = ''
            for SegIndex in range(len(SegFeild)):
                print(SegIndex, end=' ')
                print(SegFeild[SegIndex])
                SegFeild[SegIndex] = html.unescape(str(SegFeild[SegIndex]))
                SegFeild[SegIndex] = str(SegFeild[SegIndex]).replace("'", "''")
            if len(SegFeild[19]) >= 200:
                SegFeild[19] = str(SegFeild[19])[:200]+'...'

            if len(SegFeild[18]) >= 1500:
                SegFeild[18] = str(SegFeild[18])[:1500]+'...'
                
            check_date(get_htmlSource, SegFeild)
            a = False

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                  exc_tb.tb_lineno)
            a = True


def check_date(get_htmlSource, SegFeild):
    deadline = str(SegFeild[24])
    curdate = datetime.now()
    curdate_str = curdate.strftime("%Y-%m-%d")
    try:
        if deadline != '':
            datetime_object_deadline = datetime.strptime(deadline, '%Y-%m-%d')
            datetime_object_curdate = datetime.strptime(curdate_str, '%Y-%m-%d')
            timedelta_obj = datetime_object_deadline - datetime_object_curdate
            day = timedelta_obj.days
            if day > 0:
                insert_in_Local(get_htmlSource, SegFeild)
            else:
                print("Expired Tender")
                global_var.expired += 1
        else:
            print("Deadline Not Given")
            global_var.deadline_Not_given += 1
    except Exception as e:
        exc_type , exc_obj , exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname , "\n" ,exc_tb.tb_lineno)