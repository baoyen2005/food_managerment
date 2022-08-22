from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
# import MySQLdb
from PyQt5.uic import loadUiType
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import os
import pandas as pd
from datetime import datetime

ui, _ = loadUiType('food_manager.ui')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # self.Handel_UI_Changes()  # xu ly thay doi giao dien
        self.Handel_Buttons()  # them xu ly button

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("food_manager.db")

        # Show NguyenLieu
        self.Show_All_NguyenLieu()

    def Handel_UI_Changes(self):
        self.tabWidget.tabBar().setVisible(False)
        # self.showMaximized() # hien thi ung dung ban dau full man hinh

    def Handel_Buttons(self):
        # Nguyen Lieu
        self.pushButton.clicked.connect(self.NguyenLieu)  # ket noi button vs chuyen tab
        # self.tab.clicked.connect(self.NguyenLieu)  # ket noi button vs chuyen tab
        self.pushButton_7.clicked.connect(self.Add_NguyenLieu)
        self.pushButton_8.clicked.connect(self.Save_All_Change_NguyenLieu)
        self.pushButton_10.clicked.connect(self.Save_Excel_NguyenLieu)

        # Mon An
        self.pushButton_2.clicked.connect(self.MonAn)
        # self.tab_2.clicked.connect(self.MonAn)
        self.pushButton_2.clicked.connect(self.Show_All_MonAn)

        self.pushButton_11.clicked.connect(self.Add_MonAn)
        self.pushButton_9.clicked.connect(self.Save_All_Change_MonAn)
        self.pushButton_12.clicked.connect(self.Save_Excel_MonAn)

        # ThucDOn
        self.pushButton_3.clicked.connect(self.ThucDon)
        # self.tab_3.clicked.connect(self.ThucDon)
        self.pushButton_3.clicked.connect(self.Show_All_ThucDon)
        self.pushButtonThemThucDon.clicked.connect(self.Add_ThucDon)
        self.pushButtonLuuThucDon.clicked.connect(self.Save_All_Change_ThucDon)
        self.pushButtonXuatThucDon.clicked.connect(self.Save_Excel_Thuc_Don)

    # -----------------------------------NGUYEN LIEU-----------------------------------------
    def NguyenLieu(self):
        self.tabWidget.setCurrentIndex(0)

    def MonAn(self):
        self.tabWidget.setCurrentIndex(1)

    def ThucDon(self):
        self.tabWidget.setCurrentIndex(2)

    def Add_NguyenLieu(self):
        self.db.open()

        # new_id = get_last_id("NguyenLieu")+1

        short_name = self.lineEdit.text()
        full_name = self.lineEdit_2.text()
        supllier = self.lineEdit_3.text()
        unit = self.lineEdit_4.text()
        unit_price = self.lineEdit_5.text()

        # self.db.open()
        query = QSqlQuery()
        query.exec(
            f"""
            INSERT INTO NguyenLieu (
                short_name, full_name, supllier, unit, unit_price
            )
            VALUES ('{short_name}', '{full_name}', '{supllier}', '{unit}', '{unit_price}')
            """
        )
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')

        print("--- Da add Nguyen Lieu")
        self.db.commit()

        log = get_now_time()[1:] + "Thêm NguyenLieu:\t" + "short_name = " + str(short_name) + ", full_name = " + str(
            full_name) + ", supllier = " + str(supllier) + ", unit = " + str(unit) + ", unit_price = " + str(
            unit_price) + "\n"
        ghi_log(log)

        self.Show_All_NguyenLieu()
        self.db.close()

    def Show_All_NguyenLieu(self):
        print("----------Show ALl Nguyen Lieu")
        # self.tableWidget.setColumnWidth(0, 80)
        self.db.open()
        query = QSqlQuery(
            """SELECT short_name, full_name, supllier, unit, unit_price FROM NguyenLieu""")  # tra ve true neu truy van thanh cong
        # làm mới kết quả hiển thị trên table
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)

        self.tableWidget.setRowCount(0)  # set vi tri hang bat dau
        column = self.tableWidget.columnCount()
        while query.next():  # tung hang gia tri
            rows = self.tableWidget.rowCount()  # lay vi tri hang hien tai

            self.tableWidget.setRowCount(rows + 1)  # set vi tri dung hien tai tren view
            for col in range(column):
                self.tableWidget.setItem(rows, col, QTableWidgetItem(
                    str(query.value(col))))  # set các mục dữ liệu , chú ý id là số nguyên nên cần chuyển sang string
        # self.tableWidget.resizeColumnsToContents()
        self.db.close()

    def Save_All_Change_NguyenLieu(self):
        self.db.open()

        short_name = []
        full_name = []
        supllier = []
        unit = []
        unit_price = []
        row = self.tableWidget.rowCount()  # so hang du lieu

        for r in range(row):
            short_name.append(self.tableWidget.item(r, 0).text())
            full_name.append(self.tableWidget.item(r, 1).text())
            supllier.append(self.tableWidget.item(r, 2).text())
            unit.append(self.tableWidget.item(r, 3).text())
            unit_price.append(self.tableWidget.item(r, 4).text())

        self.db.open()
        query = QSqlQuery()

        query.exec("DELETE from NguyenLieu")
        for i in range(len(short_name)):
            query.exec(
                f"""
                INSERT INTO NguyenLieu (
                     short_name, full_name, supllier, unit, unit_price
                )
                VALUES ('{short_name[i]}', '{full_name[i]}', '{supllier[i]}', '{unit[i]}', '{unit_price[i]}')
                """
            )
        print("---Da luu Nguyen Lieu")
        self.db.commit()

        log = get_now_time()[1:] + """Thay Doi NguyenLieu:\t""" + "short_name = " + str(
            short_name) + ", full_name = " + str(full_name) + ", supllier = " + str(supllier) + ", unit = " + str(
            unit) + ", unit_price = " + str(unit_price) + "\n"
        ghi_log(log)
        self.db.close()
        self.Show_All_NguyenLieu()

    def Save_Excel_NguyenLieu(self):
        self.db.open()

        row = self.tableWidget.rowCount()  # so hang du lieu
        table = []
        for r in range(row):
            short_name = self.tableWidget.item(r, 0).text()
            full_name = self.tableWidget.item(r, 1).text()
            supllier = self.tableWidget.item(r, 2).text()
            unit = self.tableWidget.item(r, 3).text()
            unit_price = self.tableWidget.item(r, 4).text()
            table.append([short_name, full_name, supllier, unit, unit_price])

        df = pd.DataFrame(table,
                          columns=['Tên tắt Nguyên liệu', 'Tên Nguyên liệu', 'Nhà cung cấp', 'Đơn vị', 'Đơn giá'])

        time_str = get_now_time()
        df.to_excel('save_excel/NguyenLieu' + time_str + '.xlsx', index=False, encoding='utf8')
        print("--- Da luu file Nguyen Lieu")

        log = get_now_time()[1:] + "Da luu file Nguyen Lieu\n"
        ghi_log(log)

    # ----------------------------------MON AN ------------------------------------
    def Show_All_MonAn(self):

        global tenNL
        print("----------Show ALl Mon An")
        # self.tableWidget_2.setColumnWidth(0, 80)
        self.db.open()
        NguyenLieu = []
        query1 = QSqlQuery("""SELECT short_name, unit  FROM NguyenLieu""")
        while query1.next():  # tung hang gia tri
            short_name = query1.value(0)
            unit = query1.value(1)
            NguyenLieu.append([short_name, unit])
        # print(NguyenLieu) #[['tcb', 'KG'], ['gs', 'KG'], ['tn', 'KG'], ['mocm', 'KG']]
        print("NguyenLieu:xxxxxxxxxxx ", NguyenLieu)
        # print("--------------")
        DinhLuongMonAn = []  # sau dc add them NL_unit
        tenNL = ""
        query1 = QSqlQuery("""SELECT *  FROM DinhLuongMonAn""")
        while query1.next():  # tung hang gia tri
            id = query1.value(0)
            dinhMucNguyenLieu = query1.value(1)
            donVi = query1.value(2)
            laMonChinh = query1.value(3)
            idNguyenLieu = query1.value(4)
            idMonAn = query1.value(5)
            for nl in NguyenLieu:
                if nl[0] == idNguyenLieu:
                    tenNL += nl[1]
                    break
            DinhLuongMonAn.append([id, dinhMucNguyenLieu, donVi, laMonChinh, idNguyenLieu, idMonAn])

        print("NguyenLieuItem: ",
              DinhLuongMonAn)  # [[0, 0.77, 'tn', 'KG', 'tqlmm'], [1, 0.003, 'mocm', 'KG', 'tqlmm'], [2, 0.5, 'tn', 'KG', 1]]

        # print("--------------")
        MonAn = []
        query2 = QSqlQuery("""SELECT *  FROM MonAn""")
        while query2.next():  # tung hang gia tri
            MonAn_short_name = query2.value(0)
            MonAn_full_name = query2.value(1)
            for nli in DinhLuongMonAn:
                if MonAn_short_name == nli[5]:
                    NL_dinhMuc = nli[1]
                    NL_donVi = nli[2]
                    NL_laMonChinh = nli[3]
                    tenVietTat = nli[4]
                    MonAn.append([MonAn_short_name, MonAn_full_name, tenVietTat, NL_dinhMuc, NL_donVi, NL_laMonChinh])

        print("MonAn", MonAn)

        # làm mới kết quả hiển thị trên table
        self.tableWidget_2.insertRow(0)

        self.tableWidget_2.setRowCount(0)  # set vi tri hang bat dau
        rows = len(MonAn)
        column = self.tableWidget_2.columnCount()

        for row in range(rows):
            view_row = self.tableWidget_2.rowCount()
            self.tableWidget_2.setRowCount(view_row + 1)  # set vi tri dung hien tai tren view
            for col in range(column):
                self.tableWidget_2.setItem(row, col, QTableWidgetItem(
                    str(MonAn[row][col])))  # set các mục dữ liệu , chú ý id là số nguyên nên cần chuyển sang string
        # self.tableWidget.resizeColumnsToContents()

        # set choices in combobox khi them
        print("NguyenLieu: koooooooooooo ", NguyenLieu)
        NL_short_name_list = []  # list of NL_short_name
        for i in range(len(NguyenLieu)):
            NL_short_name_list.append(NguyenLieu[i][0])
        self.comboBox_idNL.addItems(NL_short_name_list)

    def Add_MonAn(self):
        self.db.open()
        MonAn_short_name = self.lineEdit_ma_monAN.text()
        MonAn_full_name = self.lineEdit_tenMoAn.text()
        NguyenLieu_short_name = self.comboBox_idNL.currentText()
        donVi = self.lineEdit_donViMA.text()
        laMonChinh = self.lineEdit_laMonChinh.text()
        dinhMuc = self.lineEdit_dinhMuc.text()

        # get list MonAn_short_name da co
        MonAn_short_name_list = []
        query1 = QSqlQuery("""SELECT short_name  FROM MonAn""")
        while query1.next():  # tung hang gia tri
            short_name = query1.value(0)
            MonAn_short_name_list.append(short_name)

        # neu chua ton tai MonAn_short_name
        if MonAn_short_name not in MonAn_short_name_list:
            # them vao bang MonAn
            print("Them bang MonAn")
            query = QSqlQuery()
            query.exec(
                f"""
                INSERT INTO MonAn (
                    short_name, full_name
                )
                VALUES ('{MonAn_short_name}', '{MonAn_full_name}')
                """
            )
        # them vao bang DinhLuongMonAn trong ca 2 TH
        query = QSqlQuery()
        query.exec(
            f"""
            INSERT INTO DinhLuongMonAn (
                 dinhMucNguyenLieu , donVi , laMonChinh, idNguyenLieu, idMonAn
            )
            VALUES ('{dinhMuc}', '{donVi}', '{laMonChinh}','{NguyenLieu_short_name}', '{MonAn_short_name}')
            """
        )

        print("--- Da add Mon An")
        self.lineEdit_ma_monAN.setText('')
        self.lineEdit_tenMoAn.setText('')
        self.lineEdit_donViMA.setText('')
        self.lineEdit_laMonChinh.setText('')
        self.lineEdit_dinhMuc.setText('')
        self.comboBox_idNL.setCurrentIndex(0)
        self.db.commit()

        log = get_now_time()[1:] + "Thêm Mon An:\n"
        ghi_log(log)
        self.Show_All_MonAn()

        self.db.close()

    def Save_All_Change_MonAn(self):
        # main()
        self.db.open()

        short_name_MonAn = []
        full_name_MonAn = []
        short_name_NguyenLieu = []
        dinhMuc = []
        donVi = []
        laMonChinh = []
        idDinhLuong = []

        new_MonAn = {}

        row = self.tableWidget_2.rowCount()  # so hang du lieu

        for r in range(row):
            short_name_MonAn.append(self.tableWidget_2.item(r, 0).text())
            full_name_MonAn.append(self.tableWidget_2.item(r, 1).text())
            short_name_NguyenLieu.append(self.tableWidget_2.item(r, 2).text())
            dinhMuc.append(self.tableWidget_2.item(r, 3).text())
            donVi.append(self.tableWidget_2.item(r, 4).text())
            laMonChinh.append(self.tableWidget_2.item(r, 5).text())
            new_MonAn[self.tableWidget_2.item(r, 0).text()] = self.tableWidget_2.item(r, 1).text()

        # Xử lý bảng MonAn
        # print(new_MonAn)

        query = QSqlQuery()
        for short_name, full_name in new_MonAn.items():
            query.exec("""
                   UPDATE MonAn
                   SET full_name=%s
                   WHERE short_name=%s
                """, (full_name, short_name))

        # Xu ly bang DinhLuongMonAn
        new_id_NLI = 1

        for i in range(len(short_name_NguyenLieu)):
            query = QSqlQuery()
            query.exec("""
                              UPDATE DinhLuongMonAn
                              SET dinhMucNguyenLieu=%s,
                              donVi = %s,
                              laMonChinh = %s
                              idNguyenLieu = %s
                              WHERE idMonAn=%s
                           """, (dinhMuc[i], donVi[i], laMonChinh[i], short_name_NguyenLieu[i]))

        print("---Da luu Mon An")
        self.db.commit()
        #
        log = get_now_time()[1:] + "Da luu thay doi Mon An \n"
        ghi_log(log)
        self.db.close()
        self.Show_All_NguyenLieu()

    def Save_Excel_MonAn(self):
        self.db.open()

        row = self.tableWidget_2.rowCount()  # so hang du lieu
        table = []
        for r in range(row):
            short_name_MonAn = self.tableWidget_2.item(r, 0).text()
            full_name_MonAn = self.tableWidget_2.item(r, 1).text()
            short_name_NguyenLieu = self.tableWidget_2.item(r, 2).text()
            donVi = self.tableWidget_2.item(r, 3).text()
            laMonChinh = self.tableWidget_2.item(r, 4).text()
            table.append([short_name_MonAn, full_name_MonAn, short_name_NguyenLieu, donVi, laMonChinh])

        df = pd.DataFrame(table,
                          columns=['Tên tắt Món ăn', 'Tên Món ăn', 'Tên tắt Nguyên liệu', 'Định luợng', 'Đơn vị',
                                   'Là món chính hay không'])

        time_str = get_now_time()
        df.to_excel('save_excel/MonAn' + time_str + '.xlsx', index=False, encoding='utf8')
        print("--- Da luu file Mon An")

        log = get_now_time()[1:] + "Da luu file Mon An \n"
        ghi_log(log)

    # ----------------Thuc don----------------------
    def Show_All_ThucDon(self):
        print("----------Show ALl Thuc Don")
        # self.tableWidget_2.setColumnWidth(0, 80)
        self.db.open()

        # print("--------------")
        DinhLuongMonAn = []
        tenNL = ""
        query1 = QSqlQuery("""SELECT *  FROM DinhLuongMonAn""")
        while query1.next():  # tung hang gia tri
            id = query1.value(0)
            dinhMucNguyenLieu = query1.value(1)
            donVi = query1.value(2)
            laMonChinh = query1.value(3)
            idNguyenLieu = query1.value(4)
            idMonAn = query1.value(5)
            DinhLuongMonAn.append([id, dinhMucNguyenLieu, donVi, laMonChinh, idNguyenLieu, idMonAn])

        print("DinhLuongMonAn thuc don: ",
              DinhLuongMonAn)  # [[0, 0.77, 'tn', 'KG', 'tqlmm'], [1, 0.003, 'mocm', 'KG', 'tqlmm'], [2, 0.5, 'tn', 'KG', 1]]

        # print("--------------")
        MonAn = []
        query2 = QSqlQuery("""SELECT *  FROM MonAn""")
        MonAn_short_name = ""
        while query2.next():  # tung hang gia tri
            MonAn_short_name += query2.value(0)
            MonAn_full_name = query2.value(1)
            for nli in DinhLuongMonAn:
                if MonAn_short_name == nli[5]:
                    NL_dinhMuc = nli[1]
                    NL_donVi = nli[2]
                    NL_laMonChinh = nli[3]
                    tenVietTat = nli[4]
                    MonAn.append([MonAn_short_name, MonAn_full_name, tenVietTat, NL_dinhMuc, NL_donVi, NL_laMonChinh])

        print("MonAn", MonAn)
        # print("--------------")
        Thu = []
        query2 = QSqlQuery("""SELECT *  FROM Thu""")
        while query2.next():  # tung hang gia tri
            id = query2.value(0)
            thuString = query2.value(1)
            Thu.append([id, thuString])

        print("Thu", Thu)
        # print("--------------")
        Thu_MonAn = []
        query2 = QSqlQuery("""SELECT *  FROM Thu_MonAn""")
        while query2.next():  # tung hang gia tri
            id = query2.value(0)
            id_mon_an = query2.value(1)
            id_thu = query2.value(2)
            Thu_MonAn.append([id, id_mon_an, id_thu])

        print("Thu_MonAn", Thu_MonAn)

        # print("--------------")
        ThucDon = []
        query2 = QSqlQuery("""SELECT *  FROM ThucDon""")
        while query2.next():  # tung hang gia tri
            id = query2.value(0)
            NgayBatDau = query2.value(1)
            tongChiPhiNgay = query2.value(2)
            ngayKetThuc = query2.value(3)
            idThu_MonAn = query2.value(4)
            for nli in Thu_MonAn:
                if idThu_MonAn == nli[0]:
                    idThu = nli[2]
            for nli  in Thu:
                if idThu == nli[0]:
                    _thu = nli[1]
                    ThucDon.append([id, NgayBatDau, tongChiPhiNgay,ngayKetThuc, _thu])

        print("ThucDon", ThucDon)

        # làm mới kết quả hiển thị trên table
        self.tableWidget_3.insertRow(0)

        self.tableWidget_3.setRowCount(0)  # set vi tri hang bat dau
        rows = len(ThucDon)
        column = self.tableWidget_3.columnCount()

        for row in range(rows):
            view_row = self.tableWidget_3.rowCount()
            self.tableWidget_3.setRowCount(view_row + 1)  # set vi tri dung hien tai tren view
            for col in range(column):
                self.tableWidget_3.setItem(row, col, QTableWidgetItem(
                    str(ThucDon[row][col])))  # set các mục dữ liệu , chú ý id là số nguyên nên cần chuyển sang string
        # self.tableWidget.resizeColumnsToContents()

        # set choices in combobox khi them
        print("Monan: ", MonAn)
        Mon_An_short_name_list = []  # list of NL_short_name
        for i in range(len(MonAn)):
            Mon_An_short_name_list.append(MonAn[i][0])
        self.comboBox_thu_2.addItems(Mon_An_short_name_list)
        self.comboBox_thu_3.addItems(Mon_An_short_name_list)
        self.comboBox_thu_4.addItems(Mon_An_short_name_list)
        self.comboBox_thu_5.addItems(Mon_An_short_name_list)
        self.comboBox_thu_6.addItems(Mon_An_short_name_list)
        self.comboBox_thu_7.addItems(Mon_An_short_name_list)


    def Add_ThucDon(self):
        self.db.open()
        # ca =
        thu = self.lineEdit_8.text()
        ngayBatDau = self.lineEdit_7.text()
        ngayKetThuc = self.lineEdit_8.text()
        ngayKetThuc = self.lineEdit_8.text()
        NguyenLieu_short_name = self.comboBox.currentText()
        ratio = self.lineEdit_6.text()

        # get list MonAn_short_name da co
        MonAn_short_name_list = []
        short_name = ""
        MonAn_full_name = ""
        query1 = QSqlQuery("""SELECT short_name  FROM MonAn""")
        while query1.next():  # tung hang gia tri
            short_name += query1.value(0)
            MonAn_full_name += query1.value(1)
            MonAn_short_name_list.append(short_name)

        # neu chua ton tai MonAn_short_name
        if short_name not in MonAn_short_name_list:
            # them vao bang MonAn
            print("Them bang MonAn")
            query = QSqlQuery()
            query.exec(
                f"""
                       INSERT INTO MonAn (
                           short_name, full_name
                       )
                       VALUES ('{short_name}', '{MonAn_full_name}')
                       """
            )
        # them vao bang NguyenLieuItem trong ca 2 TH
        new_id_NLI = get_last_id("NguyenLieuItem") + 1
        query = QSqlQuery()
        query.exec(
            f"""
                   INSERT INTO NguyenLieuItem (
                       id, ratio, NguyenLieu_short_name, MonAn_short_name
                   )
                   VALUES ('{new_id_NLI}', '{ratio}', '{NguyenLieu_short_name}', '{short_name}')
                   """
        )

        print("--- Da add Mon An")
        self.lineEdit_6.setText('')
        self.lineEdit_7.setText('')
        self.lineEdit_8.setText('')
        self.comboBox.setCurrentIndex(0)
        self.db.commit()

        log = get_now_time()[1:] + "Thêm Mon An:\n"
        ghi_log(log)
        self.Show_All_MonAn()

        self.db.close()


    def Show_All_THuc_don(self):
        print("----------Show ALl Nguyen Lieu")
        # self.tableWidget.setColumnWidth(0, 80)
        self.db.open()
        query = QSqlQuery(
            """SELECT short_name, full_name, supllier, unit, unit_price FROM NguyenLieu""")  # tra ve true neu truy van thanh cong
        # làm mới kết quả hiển thị trên table
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)

        self.tableWidget.setRowCount(0)  # set vi tri hang bat dau
        column = self.tableWidget.columnCount()
        while query.next():  # tung hang gia tri
            rows = self.tableWidget.rowCount()  # lay vi tri hang hien tai

            self.tableWidget.setRowCount(rows + 1)  # set vi tri dung hien tai tren view
            for col in range(column):
                self.tableWidget.setItem(rows, col, QTableWidgetItem(
                    str(query.value(col))))  # set các mục dữ liệu , chú ý id là số nguyên nên cần chuyển sang string
        # self.tableWidget.resizeColumnsToContents()
        self.db.close()


    def Save_All_Change_ThucDon(self):
        self.db.open()

        short_name = []
        full_name = []
        supllier = []
        unit = []
        unit_price = []
        row = self.tableWidget.rowCount()  # so hang du lieu

        for r in range(row):
            short_name.append(self.tableWidget.item(r, 0).text())
            full_name.append(self.tableWidget.item(r, 1).text())
            supllier.append(self.tableWidget.item(r, 2).text())
            unit.append(self.tableWidget.item(r, 3).text())
            unit_price.append(self.tableWidget.item(r, 4).text())

        self.db.open()
        query = QSqlQuery()

        query.exec("DELETE from NguyenLieu")
        for i in range(len(short_name)):
            query.exec(
                f"""
                    INSERT INTO NguyenLieu (
                         short_name, full_name, supllier, unit, unit_price
                    )
                    VALUES ('{short_name[i]}', '{full_name[i]}', '{supllier[i]}', '{unit[i]}', '{unit_price[i]}')
                    """
            )
        print("---Da luu Nguyen Lieu")
        self.db.commit()

        log = get_now_time()[1:] + """Thay Doi NguyenLieu:\t""" + "short_name = " + str(
            short_name) + ", full_name = " + str(full_name) + ", supllier = " + str(supllier) + ", unit = " + str(
            unit) + ", unit_price = " + str(unit_price) + "\n"
        ghi_log(log)
        self.db.close()
        self.Show_All_NguyenLieu()


    def Save_Excel_Thuc_Don(self):
        self.db.open()

        row = self.tableWidget_3.rowCount()  # so hang du lieu
        table = []
        for r in range(row):
            ca = self.tableWidget_3.item(r, 0).text()
            coCau = self.tableWidget_3.item(r, 1).text()
            thu2 = self.tableWidget_3.item(r, 2).text()
            thu3 = self.tableWidget_3.item(r, 3).text()
            thu4 = self.tableWidget_3.item(r, 4).text()
            thu5 = self.tableWidget_3.item(r, 5).text()
            thu6 = self.tableWidget_3.item(r, 6).text()
            thu7 = self.tableWidget_3.item(r, 7).text()
            table.append([ca, coCau, thu2, thu3, thu4, thu5, thu6, thu7])

        df = pd.DataFrame(table,
                          columns=['Ca', 'Cơ cấu', 'Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7'])

        time_str = get_now_time()
        df.to_excel('save_excel/ThucDon' + time_str + '.xlsx', index=False, encoding='utf8')
        print("--- Da luu file Thuc don")

        log = get_now_time()[1:] + "Da luu file Thuc don \n"
        ghi_log(log)


# -----------------------------------Hàm ngoài class
def get_last_id(table_name):
    query = QSqlQuery()
    query.exec(f"""
        SELECT id 
        FROM {table_name}
        WHERE id = (
            SELECT MAX(id) 
            FROM {table_name})
    """)
    query.first()

    return query.value(0)


def create_save_folder(csv_folder_path):
    if not os.path.exists(csv_folder_path):
        os.makedirs(csv_folder_path)


def get_now_time():
    date = datetime.now().strftime("%Y-%m-%d")  # date object
    now = datetime.now().time().strftime("%H:%M:%S")  # time object

    date = str(date).split('-')
    now = str(now).split(':')
    time_str = "_"
    for d in date:
        time_str += d + "_"
    time_str += now[0] + "h_"
    time_str += now[1] + "ph_"
    return time_str


def ghi_log(log):
    f = open("log.txt", 'a', encoding="utf8")
    f.write(log)
    f.close()


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()

    app.exec_()


if __name__ == '__main__':
    csv_folder_path = 'save_excel'
    create_save_folder(csv_folder_path)
    main()
