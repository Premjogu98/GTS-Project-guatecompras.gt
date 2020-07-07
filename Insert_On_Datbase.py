from datetime import datetime
import global_var
import time
import mysql.connector
import sys, os
import pymysql.cursors
import wx
app = wx.App()


def DB_connection():
    mydb_Local = ''
    a = 0
    while a == 0:
        try:
            mydb_Local = pymysql.connect(host='185.142.34.92',
                                         user='ams',
                                         password='TgdRKAGedt%h',
                                         db='tenders_db',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)

            a = 1
            return mydb_Local
        except pymysql.connect as e:
            # wx.MessageBox('Error On Local_connection Function', 'ageops.net', wx.OK | wx.ICON_ERROR)
            exc_type , exc_obj , exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname ,
                  "\n" , exc_tb.tb_lineno)
            a = 0
            time.sleep(10)


# def L2L_connection():
#     connection = ''
#     a3 = 0
#     while a3 == 0:
#         try:
#             File_Location = open("D:\\0 PYTHON EXE SQL CONNECTION & DRIVER PATH\\guatecompras.gt\\Location For Database & Driver.txt" , "r")
#             TXT_File_AllText = File_Location.read()

#             L2L_host = str(TXT_File_AllText).partition("L2L_host=")[2].partition(",")[0].strip()
#             L2L_user = str(TXT_File_AllText).partition("L2L_user=")[2].partition(",")[0].strip()
#             L2L_password = str(TXT_File_AllText).partition("L2L_password=")[2].partition(",")[0].strip()
#             L2L_db = str(TXT_File_AllText).partition("L2L_db=")[2].partition(",")[0].strip()
#             L2L_charset = str(TXT_File_AllText).partition("L2L_charset=")[2].partition("\")")[0].strip()

#             connection = pymysql.connect(host=str(L2L_host),
#                                          user=str(L2L_user),
#                                          password=str(L2L_password),
#                                          db=str(L2L_db),
#                                          charset=str(L2L_charset),
#                                          cursorclass=pymysql.cursors.DictCursor)
#             print('SQL Connected L2L_connection')
#             return connection
#         except pymysql.connect as e:
#             exc_type , exc_obj , exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname ,
#                   "\n" , exc_tb.tb_lineno)
#             time.sleep(10)
#             a3 = 0
#             connection.close()

def Error_fun(Error,Function_name,Source_name):
    mydb = DB_connection()
    mycursor = mydb.cursor()
    sql1 = "INSERT INTO errorlog_tbl(Error_Message,Function_Name,Exe_Name) VALUES('" + str(Error).replace("'","''") + "','" + str(Function_name).replace("'","''")+ "','"+str(Source_name)+"')"
    mycursor.execute(sql1)
    mydb.commit()
    mycursor.close()
    mydb.close()
    return sql1

def check_Duplication(get_htmlSource,SegFeild):
    global a1
    a1 = 0
    while a1 == 0:
        try:
            mydb = DB_connection()
            mycursor = mydb.cursor()
            if SegFeild[13] != '' and SegFeild[24] != '' and SegFeild[7] != '':
                commandText = "SELECT Posting_Id from americas_tenders_tbl where tender_notice_no = '" + str(SegFeild[13]) + "' and Country = '" + str(SegFeild[7]) + "' and doc_last= '" + str(SegFeild[24]) + "'"
            elif SegFeild[13] != "" and SegFeild[7] != "":
                commandText = "SELECT Posting_Id from americas_tenders_tbl where tender_notice_no = '" + str(SegFeild[13]) + "' and Country = '" + str(SegFeild[7]) + "'"
            elif SegFeild[19] != "" and SegFeild[24] != "" and SegFeild[7] != "":
                commandText = "SELECT Posting_Id from americas_tenders_tbl where short_desc = '" + str(SegFeild[19]) + "' and doc_last = '" + SegFeild[24] + "' and Country = '" + SegFeild[7] + "'"
            else:
                commandText = "SELECT Posting_Id from americas_tenders_tbl where short_desc = '" + str(SegFeild[19]) + "' and Country = '" + str(SegFeild[7]) + "'"
            mycursor.execute(commandText)
            results = mycursor.fetchall()
            mydb.close()
            mycursor.close()
            a1 = 1
            print("Code Reached On check_Duplication")
            return results
        except Exception as e:
            Function_name: str = sys._getframe().f_code.co_name
            Error: str = str(e)
            Source_name = str(SegFeild[31])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",exc_tb.tb_lineno)
            Error_fun(Error,Function_name,Source_name)
            time.sleep(10)
            a1 = 0


def insert_in_Local(get_htmlSource , SegFeild):

    results = check_Duplication(get_htmlSource , SegFeild)
    if len(results) > 0:
        print('Duplicate Tender')
        global_var.duplicate += 1
        return 1
    else:
        Fileid = create_filename(get_htmlSource , SegFeild)
    MyLoop = 0
    while MyLoop == 0:
        mydb = DB_connection()
        mycursor = mydb.cursor()
        sql = "INSERT INTO americas_tenders_tbl (Tender_ID,EMail,add1,Country,Maj_Org,tender_notice_no,notice_type,Tenders_details,short_desc,est_cost,currency,doc_cost,doc_last,earnest_money,Financier,tender_doc_file,source)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val= (str(Fileid) ,str(SegFeild[1]) , str(SegFeild[2]) , str(SegFeild[7]) , str(SegFeild[12]) , str(SegFeild[13]) , str(SegFeild[14]),
                str(SegFeild[18]) , str(SegFeild[19]) , str(SegFeild[20]) , str(SegFeild[21]) , str(SegFeild[22]), str(SegFeild[24]),str(SegFeild[26]) ,str(SegFeild[27]),
                str(SegFeild[28]) , str(SegFeild[31]))
        try:
            mycursor.execute(sql , val)
            mydb.commit()
            mydb.close()
            mycursor.close()
            global_var.inserted += 1
            print("Code Reached On insert_in_Local")
            MyLoop = 1
        except Exception as e:
            Function_name: str = sys._getframe().f_code.co_name
            Error: str = str(e)
            Source_name = str(SegFeild[31])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",exc_tb.tb_lineno)
            Error_fun(Error,Function_name,Source_name)
            MyLoop = 0
            time.sleep(10)

    insert_L2L(SegFeild, Fileid)


def create_filename(get_htmlSource , SegFeild):
    basename = "PY076"
    Current_dateTime = datetime.now().strftime("%Y%m%d%H%M%S%f")
    Fileid = "".join([basename , Current_dateTime])
    a = 0
    while a == 0:
        try:
            
            File_path = "Z:\\" + Fileid + ".html"
            file1 = open(File_path , "w", encoding='utf-8')
            # string_Translate_Table = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html xmlns=\"http://www.w3.org/1999/xhtml\">" +\
            #             "<BODY><table align=\"center\" border=\"1\" style=\"width:95%;border-spacing:0;border-collapse: collapse;border:1px solid #666666; margin-top:5px; margin-bottom:5px;\">" +\
            #             "<tr><td colspan=\"2\"; style=\"background-color:#004040; font-weight: bold; padding:7px;border-bottom:1px solid #666666; color:white;\">Tender Details</td></tr>" +\
            #             "<tr bgcolor=\"#e8eff1\" onmouseover=\"this.style.backgroundColor='#d6edf5'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Tender ID </td><td style=\"padding:7px;\">" + SegFeild[13] + "</td></tr>" + \
            #             "<tr bgcolor=\"#e8eff1\" onmouseover=\"this.style.backgroundColor='#d6edf5'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Title </td><td style=\"padding:7px;\">" + SegFeild[19] + "</td></tr>" + \
            #             "<tr bgcolor=\"#e8eff1\" onmouseover=\"this.style.backgroundColor='#d6edf5'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Purchaser </td><td style=\"padding:7px;\">" + SegFeild[12] + "</td></tr>" +\
            #             "<tr bgcolor=\"#e8eff1\" onmouseover=\"this.style.backgroundColor='#d6edf5'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Address </td><td style=\"padding:7px;\">" + SegFeild[2] + "</td></tr>" +\
            #             "<tr bgcolor=\"#e8eff1\" onmouseover=\"this.style.backgroundColor='#d6edf5'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">More Detail </td><td style=\"padding:7px;\">" + SegFeild[18] + "</td></tr>" +\
            #             "<tr bgcolor=\"#e8eff1\" onmouseover=\"this.style.backgroundColor='#d6edf5'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Closing Date </td><td style=\"padding:7px;\">" + SegFeild[24] + "</td></tr></table>"
            Final_Doc = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html xmlns=\"http://www.w3.org/1999/xhtml\"><head><meta content=\"text/html; charset=utf-8\" http-equiv=\"Content-Type\" /><title>Tender Document</title></head><style style=\"text/css\"> td{ padding:5px;}</style><BODY><Blockquote style='border:1px solid; padding:10px;'>" + get_htmlSource + "</Blockquote></BODY></html>"
            
            Final_Doc_list = []
            Final_HTML_Document1 = [Final_Doc[idx:idx + 1000] for idx , val in enumerate(Final_Doc)
                                    if idx % 1000 == 0]
            for Final_HTML_Document2 in Final_HTML_Document1:
                Final_Doc_list.append(Final_HTML_Document2)
            for Final_Doc_list1 in Final_Doc_list:
                file1.write(str(Final_Doc_list1))
            file1.close()
            print("Code Reached On create_filename")
            return Fileid
        except Exception as e:
            Function_name: str = sys._getframe().f_code.co_name
            Error: str = str(e)
            Source_name = str(SegFeild[31])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",exc_tb.tb_lineno)
            Error_fun(Error,Function_name,Source_name)
            a = 0
            time.sleep(10)


def insert_L2L(SegFeild , Fileid):
    ncb_icb = "icb"
    added_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    search_id = "1"
    cpv_userid = ""
    dms_entrynotice_tblquality_status = '1'
    quality_id = '1'
    quality_addeddate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Col1 = 'https://www.guatecompras.gt'
    if SegFeild[7] == "IN":
        Col2 = str(SegFeild[26]) + " * " + str(SegFeild[20])  # For India Only Other Wise Blank
    else:
        Col2 = ''
    Col3 = ''
    Col4 = ''
    Col5 = ''
    file_name = "D:\\Tide\\DocData\\" + Fileid + ".html"
    dms_downloadfiles_tbluser_id = 'DWN1011566'
    # Europe-DWN2554488,India-DWN00541021,Asia-DWN5046627,Africa-DWN302520,North America-DWN1011566,
    # South America-DWN1456891,Semi-Auto-DWN30531073,MFA-DWN0654200
    selector_id = ''
    select_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    is_english = '1'
    if SegFeild[36] == "":
        dms_entrynotice_tblstatus = "1"
        dms_downloadfiles_tblsave_status = '1'
        dms_downloadfiles_tblstatus = '1'
        dms_entrynotice_tbl_cqc_status = '1'
    else:
        dms_entrynotice_tblstatus = "2"
        dms_downloadfiles_tblsave_status = '2'
        dms_downloadfiles_tblstatus = '2'
        dms_entrynotice_tbl_cqc_status = '2'
    dms_downloadfiles_tbldatatype = "A"
    dms_entrynotice_tblnotice_type = '2'
    file_id = Fileid
    mydb = DB_connection()
    mycursor = mydb.cursor()
    if SegFeild[12] != "" and SegFeild[19] != "" and SegFeild[24] != "" and SegFeild[7] != "" and SegFeild[2] != "":
        dms_entrynotice_tblcompulsary_qc = "2"
    else:
        dms_entrynotice_tblcompulsary_qc = "1"
        global_var.QC_Tender += 1
        sql = "INSERT INTO qctenders_tbl(Source,tender_notice_no,short_desc,doc_last,Maj_Org,Address,doc_path,Country)VALUES(%s,%s,%s,%s,%s,%s,%s,%s) "
        val = (str(SegFeild[31]) , str(SegFeild[13]) , str(SegFeild[19]) , str(SegFeild[24]) , str(SegFeild[12]) ,str(SegFeild[2]) , "http://tottestupload3.s3.amazonaws.com/" + file_id + ".html" , str(SegFeild[7]))
        a4 = 0
        while a4 == 0:
            try:
                mydb = DB_connection()
                mycursor = mydb.cursor()
                mycursor.execute(sql , val)
                mydb.commit()
                mycursor.close()
                mydb.close()
                a4 = 1
                print("Code Reached On QCTenders")
            except Exception as e:
                Function_name: str = sys._getframe().f_code.co_name
                Error: str = str(e)
                Source_name = str(SegFeild[31])
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",exc_tb.tb_lineno)
                Error_fun(Error,Function_name,Source_name)
                a4 = 0
                time.sleep(10)

    sql = "INSERT INTO l2l_tenders_tbl(notice_no,file_id,purchaser_name,deadline,country,description,purchaser_address,purchaser_email,purchaser_url,purchaser_emd,purchaser_value,financier,deadline_two,tender_details,ncbicb,status,added_on,search_id,cpv_value,cpv_userid,quality_status,quality_id,quality_addeddate,source,tender_doc_file,Col1,Col2,Col3,Col4,Col5,file_name,user_id,status_download_id,save_status,selector_id,select_date,datatype,compulsary_qc,notice_type,cqc_status,DocCost,DocLastDate,is_english)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
    val = (str(SegFeild[13]) , file_id , str(SegFeild[12]) , str(SegFeild[24]) , str(SegFeild[7]) , str(SegFeild[19]) ,str(SegFeild[2]) ,str(SegFeild[1]) , str(SegFeild[8]) , str(SegFeild[26]) , str(SegFeild[20]) , str(SegFeild[27]) ,str(SegFeild[24]) , str(SegFeild[18]) , ncb_icb , dms_entrynotice_tblstatus , str(added_on) , search_id ,str(SegFeild[36]) ,cpv_userid , dms_entrynotice_tblquality_status , quality_id , str(quality_addeddate) , str(SegFeild[31]) ,str(SegFeild[28]) ,Col1 , Col2 , Col3 , Col4 , Col5 ,file_name , dms_downloadfiles_tbluser_id , dms_downloadfiles_tblstatus , dms_downloadfiles_tblsave_status ,selector_id , str(select_date) , dms_downloadfiles_tbldatatype ,dms_entrynotice_tblcompulsary_qc , dms_entrynotice_tblnotice_type , dms_entrynotice_tbl_cqc_status ,str(SegFeild[22]) , str(SegFeild[41]),is_english)
    a5 = 0
    while a5 == 0:
        try:
            mydb = DB_connection()
            mycursor = mydb.cursor()
            mycursor.execute(sql , val)
            mydb.commit()
            mydb.close()
            mycursor.close()
            print("Code Reached On insert_L2L")
            print('Live Tender')
            a5 = 1
        except Exception as e:
            Function_name: str = sys._getframe().f_code.co_name
            Error: str = str(e)
            Source_name = str(SegFeild[31])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",exc_tb.tb_lineno)
            Error_fun(Error,Function_name,Source_name)
            a5 = 0
            time.sleep(10)