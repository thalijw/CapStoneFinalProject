import npyscreen
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extensions import AsIs
from psycopg2 import connect
from psycopg2 import extras
import sys
import getpass

user = ""
password = ""

# First Page - Login Page
'''class LoginForm(npyscreen.SplitForm, npyscreen.ActionForm):
    def create(self):
        self.show_atx = 25
        self.show_aty = 10
        self.username = self.add(npyscreen.TitleText, name = "Username:")
        self.nextrely += 1
        self.password = self.add(npyscreen.TitlePassword, name = "Password:")
        self.nextrely += 3
        self.database = self.add(npyscreen.TitleSelectOne, name = "Choose One:",
            values = ["PostgreSQL Database", "MySQL Database"])

    def on_ok(self):
        user = ''.join(self.username.value)
        password = ''.join(self.password.value)

       #DO NOT TOUCH THIS CODE... IT IS VITAL:
        if ''.join(self.database.get_selected_objects()) == "PostgreSQL Database":
            change_to = "TABLEACTION"
            self.parentApp.change_form(change_to)
        if ''.join(self.database.get_selected_objects()) == "MySQL Database":
            change_to = "THIRD"
            self.parentApp.change_form(change_to)

    def on_cancel(self): 
        self.parentApp.change_form(None)'''

class DBSettings(object):
    def __init__(self):
        self.tableName = ''
        self.dbSelection = ''

# Page One show shelection of the database
class DBSelector(npyscreen.SplitForm, npyscreen.ActionFormMinimal):
    OK_BUTTON_TEXT = "Exit Application"
    def create(self):
        self.show_atx = 25
        self.show_aty = 10
        self.action = self.add(DBChoice, max_height = 3, name = "Select Database Type",
        values = ["PostgreSQL", "MySQL", "Exit"], scroll_exit = True)
        self.nextrely += 1
    def on_ok(self):
        self.parentApp.switchForm(None)
        self.parentApp.switchFormNow()

class DBChoice(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(DBChoice, self).__init__(*args, **keywords)
    
    def display_value(self, value):
        return "%s" % value
    
    def actionHighlighted(self, act_on_this, keypress):
        if act_on_this == 'MySQL':
            self.parent.parentApp.dbset.dbSelection = 'MySQL'
        #self.parent.parentApp.switchForm('TableSelect')
            
        elif act_on_this == 'PostgreSQL':
            self.parent.parentApp.dbset.dbSelection = 'PostgreSQL'
            self.parent.parentApp.switchForm('TABLESELECTION')
        elif act_on_this == 'Exit Application':
            self.parent.parentApp.exit_application()
        else:
            self.parent.parentApp.switchForm(None)

class DBTables(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(DBTables, self).__init__(*args, **keywords)
    
    def display_value(self, value):
        return "%s" % (value[0])
    
    def actionHighlighted(self, act_on_this, keypress):
        # get name of selected table
        selectedTableName = act_on_this[0]
        self.parent.parentApp.dbset.tableName = act_on_this[0]
        self.parent.parentApp.switchForm('TESTDISPLAY')


class DisplayTables(npyscreen.ActionFormMinimal):
    OK_BUTTON_TEXT = "Back"
        
    def create(self):
        self.action = self.add(DBTables, name='Select Table', scroll_exit = True)

        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE]  = self.on_ok
        
    def beforeEditing(self):
        self.update_list()
        
    def update_list(self):
        if self.parentApp.dbset.dbSelection == 'PostgreSQL':
            self.action.values = self.parentApp.PostgreDB.list_all_tables()
            #self.action.display()
        
    def on_ok(self):
        self.parentApp.switchForm('MAIN')
        self.parentApp.switchFormNow()


class DBTableValues(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(DBTableValues, self).__init__(*args, **keywords)
    
    def display_value(self, value):
        return "%s" % value
    
    def actionHighlighted(self, act_on_this, keypress):
        # get name of selected table
        selectedTableName = act_on_this[0]
        del  self.parent.parentApp.self.showTableForm
        self.parent.parentApp.self.showTableForm = self.addForm("TESTDISPLAY", DisplayTableValues, name = "Display Table")
class DisplayTableValues(npyscreen.ActionFormMinimal):
    OK_BUTTON_TEXT = "Back"
    
    def create(self):
        self.action = self.add(DBTableValues, name='Select Table', scroll_exit = True)
        self.action.values = self.parentApp.PostgreDB.view_table(self.parentApp.dbset.tableName )
        self.action.display()
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE]  = self.on_ok

def on_ok(self):
    self.parentApp.switchForm('MAIN')
    self.parentApp.switchFormNow()

# Second Page - PostgreSQL option
class PostgreSQL(object):
    def __init__(self, databaseName = "postgres"):
        con = None
        self.dbname = databaseName
        self.user = "wisam"
        self.con = connect(dbname = self.dbname , user = self.user)
        self.con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("select * from pg_database where datname = %(dname)s", {'dname': self.dbname })
        answer = cur.fetchall()

        if len(answer) <= 0:
            PostgreSQL.cur.execute('CREATE DATABASE ' + dbname + " OWNER " + user)
        
            query = "CREATE TABLE IF NOT EXISTS weather ( ID   SERIAL PRIMARY KEY, city varchar(80), temp int, prcp real, date date);"
            cur.execute(query)
            query = "INSERT INTO weather (city,temp,prcp,date) VALUES ('San Fransisco', 30, 0.10, '2005-10-09')"
            cur.execute(query)
            self.con.commit()
            cur.close()

    def list_all_tables(self):
        cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT table_name FROM information_schema.tables \
                    WHERE \
                    table_type = 'BASE TABLE' AND table_schema = 'public' \
                    ORDER BY table_type, table_name")
        answer = cur.fetchall()
        cur.close()
        return answer
    
    def create_table(self):
        pass

    def view_table(self, table_name):
        cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if table_name != "":
            npyscreen.notify_confirm(table_name)
            query = "SELECT * FROM " + table_name
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            return rows
        else:
            npyscreen.notify_confirm("Table name is empty")
        #cur.execute("execute viewTables (%s)", (table_name))
        #cur.execute("SELECT * from %s;", (table_name))
            

    def edit_table(self):
        pass

    def delete_table(self):
        #possibly only need a submenu or popup for this since it's a rather simple command...
        pass

    def exit_program(self):
        #To exit the program
        self.parentApp.switchForm( None )

    def exit_form(self):
        #To go back to previous screen
        self.parentApp.setNextFormPrevious()
        
# Third Page - MySQL option
# This will be very similar to PostgreSQL when that is done
class MySQL(npyscreen.SplitForm, npyscreen.FormWithMenus):
    pass
        #def create(self):
# self.test = self.add(npyscreen.TitleText, name = "MySQL")
	# Menu Items:
	# Select a table
	# Create a table
	# Exit

# Fourth Page - Possibly?

# Application level - controls the different screens
class App(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.PostgreDB = PostgreSQL()
        self.dbset = DBSettings()
	# self.mysql_db = MySQL_DB()
    #   self.addForm("MAIN", LoginForm, name = "Login Page", lines = 13, columns = 50, draw_line_at = 6)
        self.selectDBForm = self.addForm("MAIN", DBSelector, name = "Select Database", lines = 13, columns = 50, draw_line_at = 6)
        self.selectTableForm = self.addForm("TABLESELECTION", DisplayTables, name = "Select Table")
        self.showTableForm = self.addForm("TESTDISPLAY", DisplayTableValues, name = "Display Table")
        
        #self.addForm("TABLEACTION", EditTables)
        #self.addForm("THIRD", MySQL, name = "MySQL Database", draw_line_at = 5)
        #self.addForm("SECOND", PostgreSQL, name = "PostgreSQL Database", draw_line_at = 5)
	#Add more forms for more pages

    # This function switches screens in the interface
    def change_form(self, name):
        self.switchForm(name)

# Launches ncurses environment
if __name__ == '__main__':
    Program = App().run()
