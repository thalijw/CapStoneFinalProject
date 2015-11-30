import sqlite3
import npyscreen
import psycopg2

class PostgreSQL(object):
    def __init__(self, databaseIn="postgres", userIn="wisam", passwordIn="wisam"):
        con = None
        self.dbname = databaseIn
        self.user = userIn
        self.password = passwordIn
        try:
            self.con = psycopg2.connect(dbname=self.dbname, user=self.user, host='localhost', password=self.password)
            self.con.set_isolation_level(psycopg2.ISOLATION_LEVEL_AUTOCOMMIT)
        except:
            print "I am unable to connect to the database"
        c = self.con.cursor()
        # dropQuery = "DROP TABLE weather;"
        c.execute(dropQuery)
        # c.execute("select * from pg_database where datname = %(dname)s", {'dname': self.dbname })
        createQuery = "CREATE TABLE IF NOT EXISTS weather ( ID SERIAL PRIMARY KEY, city varchar(80), temp int, prcp real, day date);"
        c.execute(createQuery)
        c.close()

    def add_record(self, city='', temp='', prcp='', day=''):
        # db = connect(self.dbfilename)
        c = self.con.cursor()
        c.execute('INSERT INTO weather (city,temp,prcp,day) VALUES (%s,%s,%s,%s)', (city, temp, prcp, day,))
        self.con.commit()
        c.close()

    def update_record(self, record_id, city='', temp='', prcp='', day=''):
        # db = sqlite3.connect(self.dbfilename)
        c = self.con.cursor()
        c.execute('UPDATE weather SET city=%s, temp=%s, prcp=%s, day=%s \
                    WHERE id=%s', (city, temp, prcp, day, record_id,))
        self.con.commit()
        c.close()

    def delete_record(self, record_id):
        # db = sqlite3.connect(self.dbfilename)
        c = self.con.cursor()
        c.execute('DELETE FROM weather WHERE id=%s', (record_id,))
        self.con.commit()
        c.close()

    def list_all_records(self, ):
        # db = sqlite3.connect(self.dbfilename)
        c = self.con.cursor()
        c.execute('SELECT * from weather')
        records = c.fetchall()
        c.close()
        return records

    def get_record(self, record_id):
        # db = sqlite3.connect(self.dbfilename)
        c = self.con.cursor()
        c.execute('SELECT * from weather WHERE id=%s', (record_id,))
        records = c.fetchall()
        c.close()
        return records[0]

class RecordList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(RecordList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record
        })

    def display_value(self, vl):
        return "%s, %s, %s, %s" % (vl[0], vl[1], vl[2], vl[3])

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('EDITRECORDFM').value =act_on_this[0]
        self.parent.parentApp.switchForm('EDITRECORDFM')

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EDITRECORDFM').value = None
        self.parent.parentApp.switchForm('EDITRECORDFM')

    def when_delete_record(self, *args, **keywords):
        self.parent.parentApp.myDatabase.delete_record(self.values[self.cursor_line][0])
        self.parent.update_list()

class RecordListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = RecordList
    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wMain.values = self.parentApp.myDatabase.list_all_records()
        self.wMain.display()

class EditRecord(npyscreen.ActionForm):
    def create(self):
        self.value = None
        self.wgCity    = self.add(npyscreen.TitleText, name = "City:",)
        self.wgTemp    = self.add(npyscreen.TitleText, name = "Temperature:")
        self.wgPrcp    = self.add(npyscreen.TitleText, name = "Precipitation:")
        self.wgDay    = self.add(npyscreen.DateCombo, name = "Date:")

    def beforeEditing(self):
        if self.value:
            record = self.parentApp.myDatabase.get_record(self.value)
            self.name = "Record id : %s" % record[0]
            self.record_id          = record[0]
            self.wgCity.value       = record[1]
            self.wgTemp.value       = str(record[2])
            self.wgPrcp.value       = str(record[3])
            self.wgDay.value       = record[4]
        else:
            self.name = "New Record"
            self.record_id          = ''
            self.wgCity.value       = ''
            self.wgTemp.value       = ''
            self.wgPrcp.value       = ''
            self.wgDay.value       = ''

    def on_ok(self):
        if self.record_id: # We are editing an existing record
            self.parentApp.myDatabase.update_record(self.record_id,
                                            city = self.wgCity.value,
                                            temp = str(self.wgTemp.value),
                                            prcp = str(self.wgPrcp.value),
                                            day = self.wgDay.value,
                                            )
        else: # We are adding a new record.
            self.parentApp.myDatabase.add_record(
            city = self.wgCity.value,
            temp = self.wgTemp.value,
            prcp = self.wgPrcp.value,
            day = self.wgDay.value,
            )
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

class AddressBookApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.myDatabase = PostgreSQL()
        self.addForm("MAIN", RecordListDisplay)
        self.addForm("EDITRECORDFM", EditRecord)

if __name__ == '__main__':
    myApp = AddressBookApplication()
    myApp.run()
