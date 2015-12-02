import npyscreen

def myFunction(*args):
    F = npyscreen.Form(name='My Test App')
    myFW = F.add(npyscreen.TitleText, name="First Widget")
    F.edit()
    return myFW.value
    
if __name__ == '__main__':
    print npyscreen.wrapper_basic(myFunction)

