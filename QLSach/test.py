
import mysql.connector


mydb = mysql.connector.connect(host='127.0.0.1', user='root', password='123456789', database='book01')
mycursor = mydb.cursor()

# code = 'insert into Author(name,product_id) values(%s,%s) '
# val=("Xuân Quỳnh","5")
#
# code2='select * from author'
# mycursor.execute(code,val)

# code="update chi_tiet_phieu_nhap set soLuong=150 where soLuong=200"
# mycursor.execute(code)
# mydb.commit()

# THỜI GIAN HỦY ĐƠN
# mycursor.execute('set global event_scheduler=on')
# code="create event if not exists delete_event ON schedule every 10 SECOND starts current_timestamp() do delete from book01.chi_tiet_phieu_nhap where soLuong="
# num='300'
# mycursor.execute(code+num)
#
code="create trigger soluongnhap insert on book01.chi_tiet_phieu_nhap" \
     "for insert, update" \
     "as" \
     "begin" \
     "ROLLBACK TRAN" \
     "if soLuong<150" \
     "end"
mycursor.execute(code)

