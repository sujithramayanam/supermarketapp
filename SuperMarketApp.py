import sys
import mysql.connector
from datetime import date
from PyQt5.QtWidgets import QMainWindow,QApplication
from SuperMarketUI import *

class SPM(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui =Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.submit.clicked.connect(self.submit)
        self.ui.reset.clicked.connect(self.clear)
        self.ui.da.clicked.connect(self.arrivalDate)
        self.ui.de.clicked.connect(self.expireDate)
        self.ui.update.clicked.connect(self.updateStock)
        self.ui.view.clicked.connect(self.viewStock)
        self.ui.product.clicked.connect(self.getStock)
        self.ui.delete_2.clicked.connect(self.deleteStock)
        self.ui.add.clicked.connect(self.bill)
        self.ui.exit.clicked.connect(self.exit)
        
        
        self.ui.comboBox.currentIndexChanged.connect(self.places)
        self.show()
    def exit(self):
        sys.exit()
    def places(self):
        self.place=self.ui.comboBox.currentText()
    def arrivalDate(self):
        self.date=self.ui.calendarWidget.selectedDate()
        self.ui.arrival.setText(self.date.toString("yyyy/MM/dd"))
    def expireDate(self):
        self.date=self.ui.calendarWidget.selectedDate()
        self.ui.expire.setText(self.date.toString("yyyy/MM/dd"))
    def getStock(self):
        pid=int(self.ui.id.text())
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "sujith",database = "organic")  
        cur = myconn.cursor()
        sql='select * from stock where pid=%s'
        val=[(pid)]
        cur.execute(sql,val)
        r=cur.fetchone()
        self.ui.id.setText(str(r[0]))
        self.ui.name.setText(str(r[1]))
        self.ui.quantity.setText(str(r[2]))
        self.ui.price.setText(str(r[3]))
        self.ui.vendname.setText(str(r[4]))
        self.ui.vendnumber.setText(str(r[5]))
        
        
        self.ui.arrival.setText(date.isoformat(r[7]))
        self.ui.expire.setText(date.isoformat(r[8]))
    def updateStock(self):
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "sujith",database = "organic")  
        cur = myconn.cursor()
        P_id=int(self.ui.id.text())
        P_name=self.ui.name.text()
        P_qty=int(self.ui.quantity.text())
        P_price=float(self.ui.price.text())
        
        vendor=self.ui.vendname.text()
        mobile=self.ui.vendnumber.text()
        mfg_place=self.place
        P_arrival=self.ui.arrival.text()
        P_exp=self.ui.expire.text()
        sql='update stock set pname=%s,quantity=%s,price=%s,seller_name=%s,seller_number=%s,place=%s,doa=%s,doe=%s where pid=%s'
        val=(P_name,P_qty,P_price,vendor,mobile,mfg_place,P_arrival,P_exp,P_id)
        cur.execute(sql,val)
        myconn.commit()
        myconn.close()
        QtWidgets.QMessageBox.about(self,"Success","Sucessfully Updated")
        self.statusBar().showMessage('Sucessfully Updated')
        self.clear()
    def submit(self):
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "Sujith",database = "organic")  
        cur = myconn.cursor()
        P_id=int(self.ui.id.text())
        P_name=self.ui.name.text()
        P_qty=int(self.ui.quantity.text())
        P_price=float(self.ui.price.text())
        
        vendor=self.ui.vendname.text()
        mobile=self.ui.vendnumber.text()
        mfg_place=self.place
        P_arrival=self.ui.arrival.text()
        P_exp=self.ui.expire.text()
        sql="insert into stock(pid,pname,quantity,price,seller_name,seller_number,place,doa,doe)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
        val=(P_id,P_name,P_qty,P_price,vendor,mobile,mfg_place,P_arrival,P_exp)
        cur.execute(sql,val)
        myconn.commit()
        myconn.close()
        QtWidgets.QMessageBox.about(self,"Success","Sucessfully Inserted")
        self.statusBar().showMessage('Sucessfully Inserted')
        self.clear()
    def viewStock(self):
        myconn=mysql.connector.connect(host="localhost", user="root",password="Sujith",database="organic")
        cur = myconn.cursor()
        cur.execute("select * from stock")
        res=cur.fetchall()
        #print(res)
        self.ui.tableWidget.setRowCount(0)
        for r_no, r_data in enumerate(res):
            self.ui.tableWidget.insertRow(r_no)
            for c_no, data in enumerate(r_data):
                self.ui.tableWidget.setItem(r_no,c_no,QtWidgets.QTableWidgetItem(str(data)))
        myconn.close()
    def deleteStock(self):
        P_id=int(self.ui.id.text())
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "sujith",database = "organic")  
        cur = myconn.cursor()
        sql='delete from stock where pid=%s'
        val=[(P_id)]
        cur.execute(sql,val)
        myconn.commit()
        myconn.close()
        QtWidgets.QMessageBox.about(self,"Success","Sucessfully Deleted")
        self.statusBar().showMessage('Sucessfully Deleted')
        self.clear()
    def clear(self):
        self.ui.id.clear()
        self.ui.name.clear()
        self.ui.quantity.clear()
        self.ui.price.clear()
        self.ui.vendname.clear()
        self.ui.vendnumber.clear()
        self.ui.arrival.clear()
        self.ui.expire.clear()
        
        self.ui.lineEdit_10.clear()
        self.ui.lineEdit_11.clear()
    def bill(self):
        global list_of_items
        global d
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "sujith",database = "organic")  
        cur = myconn.cursor()
        id=int(self.ui.lineEdit_10.text())
        quant=int(self.ui.lineEdit_11.text())
        sql='select * from stock where pid=%s'
        val=[(id)]
        cur.execute(sql,val)
        r=cur.fetchone()
        d[id]=r[3]*quant
        list_of_items+='{} \t\t {} \t {} \t {}\n'.format(r[1],r[3],quant,quant*r[3])
        self.ui.textEdit.setText('Name \t\t Price \t Quantity \t Total \n'+list_of_items)
        self.ui.label_13.setText(str(sum(d.values())))

        sql='update stock set quantity=quantity-%s where pid=%s'
        val=(quant,id)
        cur.execute(sql,val)
        myconn.commit()
        myconn.close()

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = SPM()
    list_of_items=''
    d={}
    myconn = mysql.connector.connect(host = "localhost", user = "root",password = "sujith",database = "organic")  
    cur = myconn.cursor()
    w.show()
    sys.exit(app.exec_())
