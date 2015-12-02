import npyscreen
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extensions import AsIs
from psycopg2 import connect
from psycopg2 import extras
import sys
import getpass

user = ""
class LoginForm(npyscreen.ActionForm, npyscreen.SplitForm):
    CANCEL_BUTTON_TEXT = "EXIT"
    def create(self):
	self.show_atx = 25
        self.show_aty = 10
        self.username = self.add(npyscreen.TitleText, name = "Username: ")
        self.nextrely += 4
        self.database = self.add(npyscreen.TitleSelectOne, name = "Choose One:",
            values = ["PostgreSQL Database", "MySQL Database"], scroll_exit = True)

    def on_ok(self):
        if ''.join(self.database.get_selected_objects()) == "PostgreSQL Database":
            self.parentApp.dbset.user = ''.join(self.username.value)
            self.parentApp.myDatabase.create(self.parentApp.dbset.user)
            self.parentApp.dbset.dbSelection = 'PostgreSQL'
            change_to = "TABLESELECTION"
            self.parentApp.change_form(change_to)
        if ''.join(self.database.get_selected_objects()) == "MySQL Database":
            change_to = "MYSQLDB" #MySQL Identifier
            self.parentApp.change_form(change_to)

    def on_cancel(self):
        self.parentApp.change_form(None)

class DBSettings(object):
    def __init__(self):
        self.user = ''
        self.tableName = ''
        self.dbSelection = ''
        self.table_rows = []
        self.headers = []

class DBTables(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(DBTables, self).__init__(*args, **keywords)

    def display_value(self, value):
        return "%s" % (value[0])

    def actionHighlighted(self, act_on_this, keypress):
        # get name of selected tab
        tableSelection = act_on_this[0]
        del self.parent.parentApp.TableForm

        self.parent.parentApp.TableForm = self.parent.parentApp.addForm('TESTDISPLAY', RecordListDisplay)
        self.parent.parentApp.dbset.tableName = tableSelection
        self.parent.parentApp.getForm('TESTDISPLAY').value = tableSelection
        self.parent.parentApp.switchForm('TESTDISPLAY')

    def getTablename():
        return tableSelection

class DisplayTables(npyscreen.ActionFormMinimal):
    OK_BUTTON_TEXT = "Back"

    def create(self):
        self.action = self.add(DBTables, name='Select Table', scroll_exit = True)

        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE]  = self.on_ok

    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        if self.parentApp.dbset.dbSelection == 'PostgreSQL':
            self.action.values = self.parentApp.myDatabase.list_all_tables(self.parentApp.dbset.tableName)
            self.action.display()

    def on_ok(self):
        self.parentApp.switchForm('MAIN')
        self.parentApp.switchFormNow()

class TableManipulation(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(TableManipulation, self).__init__(*args, **keywords)

    def display_value(self, value):
        return "%s" % value

    def actionHighlighted(self, act_on_this, keypress):
        # get name of selected table
        selectedTableName = act_on_this[0]
        self.parent.parentApp.dbset.tableName = selectedTableName

class PostgreSQL(object):
    def create(self, userName):
        con = None
        self.dbname = "postgres"
        self.user = userName
        self.con = connect(dbname = self.dbname , user = self.user)
        self.con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("select * from pg_database where datname = %(dname)s", {'dname': self.dbname })
        answer = cur.fetchall()

        if len(answer) <= 0:
            PostgreSQL.cur.execute('CREATE DATABASE ' + dbname + " OWNER " + user)

        # query = "DROP TABLE states;"
        # cur.execute(query)
        # query = "DROP TABLE weather;"
        # cur.execute(query)
        # query = "DROP TABLE states;"
        # cur.execute(query)

        query = "CREATE TABLE IF NOT EXISTS weather ( ID   SERIAL PRIMARY KEY, city varchar(80), temp int, prcp real, day date);"
        cur.execute(query)
        query = "CREATE TABLE IF NOT EXISTS cars ( ID   SERIAL PRIMARY KEY,  name varchar(80), model int, year int);"
        cur.execute(query)
        query = "CREATE TABLE IF NOT EXISTS states ( ID   SERIAL PRIMARY KEY,  name varchar(80), population int, capital varchar(80));"
        cur.execute(query)
        self.con.commit()
        cur.close()

    def list_all_tables(self, table_name):
        cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT table_name FROM information_schema.tables \
                    WHERE \
                    table_type = 'BASE TABLE' AND table_schema = 'public' \
                    ORDER BY table_type, table_name")
        answer = cur.fetchall()
        cur.close()
        return answer

    def view_table(self, table_name):
        cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT * FROM " + table_name
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        return rows

    def add_record(self, record_id, city='', temp='', prcp='', day=''):
        c = self.con.cursor()
        c.execute('INSERT INTO weather (city,temp,prcp,day) VALUES (%s,%s,%s,%s)', (city, temp, prcp, day,))
        self.con.commit()
        c.close()

    def add_record_cars(self, record_id, name='', model='', year=''):
        c = self.con.cursor()
        c.execute('INSERT INTO cars (name, model, year) VALUES (%s,%s,%s)', (name, model, year))
        self.con.commit()
        c.close()

    def add_record_states(self, record_id, name='', population='', capital=''):
        c = self.con.cursor()
        c.execute('INSERT INTO states (name, population, capital) VALUES (%s,%s,%s)', (name, population, capital))
        self.con.commit()
        c.close()

    def update_record(self, record_id, city='', temp='', prcp='', day=''):
        c = self.con.cursor()
        c.execute('UPDATE weather SET city=%s, temp=%s, prcp=%s, day=%s \
                    WHERE id=%s', (city, temp, prcp, day, record_id,))
        self.con.commit()
        c.close()

    def update_record_cars(self, record_id, name='', model='', year=''):
        c = self.con.cursor()
        c.execute('UPDATE cars SET name=%s, model=%s, year=%s \
                    WHERE id=%s', (name, model, year, record_id,))
        self.con.commit()
        c.close()
    def update_record_states(self, record_id, name='', population='', capital=''):
        c = self.con.cursor()
        c.execute('UPDATE states SET name=%s, population=%s, capital=%s \
                    WHERE id=%s', (name, population, capital, record_id,))
        self.con.commit()
        c.close()

    def delete_record(self, record_id,table_name ):
        c = self.con.cursor()
        query = "DELETE FROM " + table_name + " WHERE id=" + str(record_id)
        c.execute(query)
        #c.execute('DELETE FROM weather WHERE id=%s', (record_id,))
        self.con.commit()
        c.close()

    def list_all_records(self, table_name):
        c = self.con.cursor()
        c.execute('SELECT * from ' + table_name)
        records = c.fetchall()
        c.close()
        return records

    def get_record(self, record_id, table_name):
        c = self.con.cursor()
        query = "SELECT * from " + table_name + " WHERE id=" + str(record_id)
        #c.execute('SELECT * from %s WHERE id=%s', (table_name,record_id,))
        c.execute(query)
        records = c.fetchall()
        c.close()
        return records[0]

class RecordList(npyscreen.MultiLineAction):
    CANCEL_BUTTON_TEXT = "Back"
    def __init__(self, *args, **keywords):
        super(RecordList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record
        })

    def display_value(self, vl):
        return "%s, %s, %s, %s" % (vl[0], vl[1], vl[2], vl[3])

    def actionHighlighted(self, act_on_this, keypress):
        if self.parent.parentApp.dbset.tableName == "weather":
            self.parent.parentApp.getForm('EDITRECORDFM').value =act_on_this[0]
            self.parent.parentApp.switchForm('EDITRECORDFM')
        elif self.parent.parentApp.dbset.tableName == "cars":
            self.parent.parentApp.getForm('EDITRECORDFMCAR').value =act_on_this[0]
            self.parent.parentApp.switchForm('EDITRECORDFMCAR')
        elif self.parent.parentApp.dbset.tableName == "states":
            self.parent.parentApp.getForm('EDITRECORDFMSTATE').value =act_on_this[0]
            self.parent.parentApp.switchForm('EDITRECORDFMSTATE')

    def when_add_record(self, *args, **keywords):
        if self.parent.parentApp.dbset.tableName == "weather":
            self.parent.parentApp.getForm('EDITRECORDFM').value = None
            self.parent.parentApp.switchForm('EDITRECORDFM')
        elif self.parent.parentApp.dbset.tableName == "cars":
            self.parent.parentApp.getForm('EDITRECORDFMCAR').value = None
            self.parent.parentApp.switchForm('EDITRECORDFMCAR')
        elif self.parent.parentApp.dbset.tableName == "states":
            self.parent.parentApp.getForm('EDITRECORDFMSTATE').value = None
            self.parent.parentApp.switchForm('EDITRECORDFMSTATE')

    def when_delete_record(self, *args, **keywords):
        if self.parent.parentApp.dbset.tableName == "weather":
            self.parent.parentApp.myDatabase.delete_record(self.values[self.cursor_line][0], "weather")
            self.parent.update_list()
        if self.parent.parentApp.dbset.tableName == "cars":
            self.parent.parentApp.myDatabase.delete_record(self.values[self.cursor_line][0], "cars")
            self.parent.update_list()
        if self.parent.parentApp.dbset.tableName == "states":
            self.parent.parentApp.myDatabase.delete_record(self.values[self.cursor_line][0], "states")
            self.parent.update_list()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

class RecordListDisplay(npyscreen.FormMutt, npyscreen.FormWithMenus, npyscreen.SplitForm):
    CANCEL_BUTTON_TEXT = "Back"
    MAIN_WIDGET_CLASS = RecordList
    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wMain.values = self.parentApp.myDatabase.list_all_records(self.parentApp.dbset.tableName)
        self.wMain.display()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

class EditRecord(npyscreen.ActionForm):
    CANCEL_BUTTON_TEXT = "Back"
    def create(self):
        self.value = None
        self.wgCity    = self.add(npyscreen.TitleText, name = "City:",)
        self.wgTemp    = self.add(npyscreen.TitleText, name = "Temperature:")
        self.wgPrcp    = self.add(npyscreen.TitleText, name = "Precipitation:")
        self.wgDay    = self.add(npyscreen.DateCombo, name = "Date:")

    def beforeEditing(self):
        self.wgParam = []
        self.wgtable = ''
        if self.value:
            record = self.parentApp.myDatabase.get_record(self.value, "weather")
            self.name = "Record id : %s" % record[0]
            self.record_id          = record[0]
            self.wgCity.value       = record[1]
            self.wgTemp.value       = str(record[2])
            self.wgPrcp.value       = str(record[3])
            self.wgDay.value        = record[4]

        else:
            self.name = "New Record"
            self.record_id          = ''
            self.wgCity.value       = ''
            self.wgTemp.value       = ''
            self.wgPrcp.value       = ''
            self.wgDay.value        = ''

    def on_ok(self):
        if self.record_id: # We are editing an existing record
            self.parentApp.myDatabase.update_record(self.record_id,
                                            city = self.wgCity.value,
                                            temp = str(self.wgTemp.value),
                                            prcp = str(self.wgPrcp.value),
                                            day = self.wgDay.value,
                                            )
        else: # We are adding a new record.
            self.parentApp.myDatabase.add_record(self.record_id,
            city = self.wgCity.value,
            temp = self.wgTemp.value,
            prcp = self.wgPrcp.value,
            day = self.wgDay.value,
            )
        self.parentApp.switchFormPrevious()

class EditRecordCars(npyscreen.ActionForm):
    CANCEL_BUTTON_TEXT = "Back"
    def create(self):
        self.value = None
        self.wgName    = self.add(npyscreen.TitleText, name = "Name:",)
        self.wgModel    = self.add(npyscreen.TitleText, name = "Model:")
        self.wgYear    = self.add(npyscreen.TitleText, name = "Year:")

    def beforeEditing(self):
        if self.value:
            record = self.parentApp.myDatabase.get_record(self.value, 'cars')
            self.name = "Record id : %s" % record[0]
            self.record_id          = record[0]
            self.wgName.value       = record[1]
            self.wgModel.value       = str(record[2])
            self.wgYear.value       = str(record[3])

        else:
            self.name = "New Record"
            self.record_id          = ''
            self.wgName.value       = ''
            self.wgModel.value       = ''
            self.wgYear.value       = ''

    def on_ok(self):
        if self.record_id: # We are editing an existing record
            self.parentApp.myDatabase.update_record_cars(self.record_id,
                                            name = self.wgName.value,
                                            model = str(self.wgModel.value),
                                            year = str(self.wgYear.value),
                                            )
        else: # We are adding a new record.
            self.parentApp.myDatabase.add_record_cars(self.record_id,
            name = self.wgName.value,
            model = self.wgModel.value,
            year = self.wgYear.value,
            )
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

class EditRecordStates(npyscreen.ActionForm):
    CANCEL_BUTTON_TEXT = "Back"
    def create(self):
        self.value = None
        self.wgName    = self.add(npyscreen.TitleText, name = "Name:",)
        self.wgPopulation  = self.add(npyscreen.TitleText, name = "Population:")
        self.wgCapital     = self.add(npyscreen.TitleText, name = "Capital:")


    def beforeEditing(self):
        if self.value:
            record = self.parentApp.myDatabase.get_record(self.value, 'states')
            self.name = "Record id : %s" % record[0]
            self.record_id          = record[0]
            self.wgName.value       = record[1]
            self.wgPopulation.value = str(record[2])
            self.wgCapital.value    = record[3]

        else:
            self.name = "New Record"
            self.record_id              = ''
            self.wgName.value           = ''
            self.wgPopulation.value     = ''
            self.wgCapital.value        = ''

    def on_ok(self):
        if self.record_id: # We are editing an existing record
            self.parentApp.myDatabase.update_record_states(self.record_id,
                                            name = self.wgName.value,
                                            population = str(self.wgPopulation.value),
                                            capital = self.wgCapital.value ,
                                            )
        else: # We are adding a new record.
            self.parentApp.myDatabase.add_record_states(self.record_id,
            name = self.wgName.value,
            population = str(self.wgPopulation.value),
            capital = self.wgCapital.value ,
            )
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

class DatabasesApplication(npyscreen.NPSAppManaged):
    def onStart(self):
    	npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.myDatabase = PostgreSQL()
    	self.dbset = DBSettings()
    	self.addForm("MAIN", LoginForm, name = "Database Application", lines = 13, columns = 50)
    	self.addForm("TABLESELECTION", DisplayTables)
        self.addForm("POSTGRES", RecordListDisplay, draw_line_at = 4)
    	#self.addForm("MYSQLDB", MySQLClassHere)
        self.addForm("EDITRECORDFM", EditRecord)
        self.addForm("EDITRECORDFMCAR", EditRecordCars)
        self.addForm("EDITRECORDFMSTATE", EditRecordStates)
    	self.TableForm = self.addForm("TESTDISPLAY", RecordListDisplay)

    # This function switches screens in the interface
    def change_form(self, name):
        self.switchForm(name)

if __name__ == '__main__':
    myApp = DatabasesApplication()
    myApp.run()
