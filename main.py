from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
import requests
from bs4 import BeautifulSoup
from plyer import notification
kv = '''
<MyLabel>:
    size_hint: 0.5, 0.5
    text_size: self.size
    #color:(1,0,1,1)
    Label:
        id: left_label
    Label:
        id: right_label
'''
class MyLabel(Label):
    pass
class MyGrid(GridLayout):
    def __init__(self, **kwargs):# handle as many can com in **kwargs
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 1
        self.timer = None
        btn1 = Button(text='START', size_hint=(.1, .1),background_color = (0.0, 1.0, 0.0, 1.0),
                        pos_hint={'x': .0, 'y': .0})
        btn1.bind(state=self.callbackStart)
        btn1.bind(state=self.callbackStartt)
        btn2 = Button(text='STOP', size_hint=(.1, .1),background_color = (1.0, 0.0, 0.0, 1.0),
                      pos_hint={'x': .2, 'y': .2})
        btn2.bind(state=self.callbackStop)
        #btn3 = Button(text='Get Old Data', size_hint=(.1, .1),
                      #pos_hint={'x': .2, 'y': .2})
        #btn3.bind(state=self.callbackStartt)
        #self.add_widget(btn3)
        self.add_widget(btn1)
        self.add_widget(btn2)
        self.label1 = MyLabel(text='Old Updated data from GPSC site', color=(1, 0, 1, 1))
        self.add_widget(self.label1)
        self.label = MyLabel(text='Latest Retriving data from GPSC site Press Start Button', color=(1, 1, 0, 1))
        self.add_widget(self.label)
        self.label2 = MyLabel(text='Dev By P. A. RATHOD (STATE TAX INSPECTOR)', color=(1, 0, 0, 1))
        self.add_widget(self.label2)
    def callbackStart(self, instance, value):
        if self.timer is not None:
            Clock.unschedule(self.timer)
        self.timer = Clock.schedule_interval(self.timedAction, 5)
    def callbackStop(self, instance, value):
        Clock.unschedule(self.timer)
    def callbackStartt(self, instance, value):
        self.timedActionn()
    def timedActionn(self):
        url = 'https://gpsc.gujarat.gov.in/index'
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        lists = soup.find('div', {'class': 'cn_content'}).text
        new_string = lists[18:]
        getinf1 = new_string[:-30]
        self.label1.text = getinf1
        getinf2 = self.label1.text
        return getinf2
    def timedAction(self, dt):
        getinf2 = self.label1.text
        url = 'https://gpsc.gujarat.gov.in/index'
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        lists = soup.find('div', {'class': 'cn_content'}).text
        new_string = lists[18:]
        getinf = new_string[:-30]
        if getinf2 == getinf:
            #print(getinf)
            self.label.text = getinf
        else:
            self.label.text = getinf
            self.timedActionn()
            notification.notify(title='GPSC', message=getinf, app_icon = None, timeout = 5, toast = False)
class MyApp(App):
    def build(self):
        Builder.load_string(kv)
        return MyGrid()
if __name__ == "__main__":
    MyApp().run()
