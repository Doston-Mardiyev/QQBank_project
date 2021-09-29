# QQBank_project
QQBank desktop application in python 
def search_data(self):
        
        con = cx_Oracle.connect("ibs", "ibs", "172.16.49.218/iabs")
        cur = con.cursor()
        cur.execute(f"select id, lead_last_date, code_filial, code, name, turnover_all_debit, turnover_all_credit, owned_employee from accounts where ROWNUM < 100")
        rows=cur.fetchall()
       
        
        self.Bank_table.delete(*self.Bank_table.get_children())
        
        for row in rows:
            print(rows)
            self.Bank_table.insert('',END, values=row)
            
        con.commit()
        con.close()
