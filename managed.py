import npyscreen
import psycopg2



class dbSelect(npyscreen.MultiLineAction):
    def actionHighlighted(self, act_on_this, key_press):
        if act_on_this == 'PostgreSQL':
            #load postgres
            pass
        elif act_on_this == 'MySQL':
            #load mysql
            pass








class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', dbSelectForm, name="db select")

if __name__ == '__main__':
    TestApp = MyApplication().run()
    print "all objects"
