from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from pytube import YouTube

KV = '''
Screen: 
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: 'YT Downloader'
            #left_action_items: [["menu", lambda x: x]]
        Downloader:

<Downloader>:
    MDIconButton:
        pos_hint: {'center_x': .5, 'center_y': .90}
        icon: 'download'
        theme_icon_color: "Custom"
        icon_color: 'red'
        icon_size: '75sp' 

    MDLabel:
        text: 'DIGITE A URL DO VIDEO DO YOUTUBE'
        pos_hint: {'center_y': .75}
        halign: 'center'

    MDTextField:
        id: url_field
        hint_text: 'URL'
        helper_text: 'https://URL'
        helper_text_mode: 'persistent'
        pos_hint: {'center_x': .5, 'center_y': .65}
        size_hint_x: .8
        mode: "rectangle"
        line_color_focus: 'purple'

    MDRaisedButton:
        text: 'MP3'
        size_hint_x: .4
        size_hint_y: .12
        pos_hint: {'center_x': .25, 'center_y': .5}
        on_release: root.downloadMP3()

    MDRaisedButton:
        text: 'MP4'
        size_hint_x: .4
        size_hint_y: .12
        pos_hint: {'center_x': .75, 'center_y': .5}
        on_release: root.downloadMP4()

    MDIconButton:
        pos_hint: {'center_x': .5, 'center_y': .25}
        icon: 'invert-colors'
        icon_size: '75sp'
        on_release: app.changeColorTheme()

    MDRaisedButton:
        text: 'BOTÃO TESTE'
        size_hint_x: .4
        size_hint_y: .12
        pos_hint: {'center_x': .5, 'center_y': .1}
        on_release: root.open_dialog()

<CardDownloadCompleted>:     
    id: card
    orientation: 'vertical'
    size_hint: .6, .3
    pos_hint: {'center_x': .5, 'center_y': .5}

    MDBoxLayout:
        size_hint_y: .2
        padding: [25, 0, 25, 0]
        md_bg_color: app.theme_cls.accent_color   

        MDIconButton:
            theme_text_color: 'Custom'
            icon: 'close'
            text_color: 1, 1, 1, 1
            on_release: root.close()

        MDLabel:
            text: 'Download Realizado!'
            theme_text_color: 'Custom'
            text_color: 1, 1, 1, 1

<CardDownloadFailed>:     
    id: card
    orientation: 'vertical'
    size_hint: .6, .3
    pos_hint: {'center_x': .5, 'center_y': .5}

    MDBoxLayout:
        size_hint_y: .2
        padding: [25, 0, 25, 0]
        md_bg_color: app.theme_cls.accent_color   

        MDIconButton:
            theme_text_color: 'Custom'
            icon: 'close'
            text_color: 1, 1, 1, 1
            on_release: root.close()

        MDLabel:
            text: 'URL incorreta! Digite novamente...'
            theme_text_color: 'Custom'
            text_color: 1, 1, 1, 1

'''

class Downloader(FloatLayout):
    def open_dialog_completed(self):
        self.add_widget(CardDownloadCompleted())
    
    def open_dialog_failed(self):
        self.add_widget(CardDownloadFailed())

    def downloadMP3(self):
        try:
            print('download mp3')
            audio = YouTube(self.get_url())        
            audio.streams.filter(only_audio=True).first().download(
                output_path ="",
                filename=audio.title + ".mp3"
            )
            self.open_dialog_completed()
            
        except:
            print('URL inválida! Tente novamente')
            self.open_dialog_failed()

    def downloadMP4(self):
        try:
            print('download mp4')
            video = YouTube(self.get_url()) 
            video.streams.get_highest_resolution().download(
                output_path =""
            )
            self.open_dialog_completed()

        except:
            print('URL inválida! Tente novamente')
            self.open_dialog_failed()

    def get_url(self):
        print(self.ids.url_field.text)      #caminho do text field, neste caso o caminho é Downloader(self)>ids>id(url_fields), se estivesse no app, provavelmente o caminho deveria ser App(self)>Downloader(root)>ids>id(url_fields)
        return self.ids.url_field.text

class CardDownloadCompleted(MDCard):
    def close(self):
        self.parent.remove_widget(self)

class CardDownloadFailed(MDCard):
    def close(self):
        self.parent.remove_widget(self)

class App(MDApp):

    def build(self):
        self.theme_cls.primary_palette = 'Red'
        self.theme_cls.accent_palette = 'Purple'
        self.theme_cls.theme_style = 'Light'
        return Builder.load_string(KV)
           
    def changeColorTheme(self):
        if(self.theme_cls.theme_style == 'Light'):
            self.theme_cls.theme_style = 'Dark'
        else:
            self.theme_cls.theme_style = 'Light'

App().run()
