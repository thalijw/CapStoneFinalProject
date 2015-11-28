#!/usr/bin/env python
# encoding: utf-8

import npyscreen

class TestApp(npyscreen.NPSApp):
    def main(self):
        F = npyscreen.Form(name= "Welcome to Npyscreen",)
        t = F.add(npyscreen.TitleText, name = "Text:",)
        fn = F.add(npyscreen.TitleFilename, name = "Filename:")
        fn2 = F.add(npyscreen.TitleDateCombo, name = "Date:")
        s = F.add(npyscreen.TitleSlider, out_of=12, name = "Slider")
        
        F.edit()

if __name__ == "__main__":
    App = TestApp()
    App.run()
