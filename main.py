import os

from kivymd.app import MDApp
from kivy.core.window import Window

from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.lang import Builder
from pytube import YouTube
from kivy.utils import platform             #VERIFICA PLATAFORMA

#IMPORT ABAIXO SERVE PARA QUE SEJA POSSÍVEL BAIXAR OS VÍDEO HTTPS
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#SOLICITAR PERMISSÃO DE MEMÓRIA NO ANDROID
if platform == "android":
     from android.permissions import request_permissions, Permission
     from android.storage import primary_external_storage_path
     primary_ext_storage = primary_external_storage_path()
     request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

elif platform == "linux":
    print("Olá, estou usandoz linux!")
elif platform == "windows":
    print("Olá, estou usando windows!")
elif platform == "macOS":
    print("Olá, estou usando macOS!")
else:
    print("Não foi possível reconhecer seu sistema operacional!")

#import certifi
#import os

#os.environ['SSL_CERT_FILE'] = certifi.where()

class ContentNavigationDrawer(MDBoxLayout):
    pass

class Downloader(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.path = "/"
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, 
            select_path=self.select_path
        )

    def open_dialog_completed(self):
        self.add_widget(CardDownloadCompleted())
    
    def open_dialog_failed(self):
        self.add_widget(CardDownloadFailed())

    def downloadMP3(self):
        try:               
            audio = YouTube(self.get_url())
            print("Baixando mp3 de "+ audio.title)    
            audio.streams.filter(only_audio=True).first().download(
                output_path =self.path,
                filename=audio.title + ".mp3"
            )
            print("Audio salvo em", self.path)
            self.open_dialog_completed()
            
        except:
            print(self.ids.label_caminho.text)
            self.ids.label_caminho.text = "Arquivo será salvo em " + self.path
            print(self.ids.label_caminho.text)
            print(self.path)
            print('URL inválida! Tente novamente')
            self.open_dialog_failed()

    def downloadMP4(self):
        try:
            video = YouTube(self.get_url()) 
            print("Baixando mp4 de "+ video.title)
            video.streams.get_highest_resolution().download(
                output_path = self.path
            )
            print("Video salvo em", self.path)
            self.open_dialog_completed()
        except: 
            print('URL inválida! Tente novamente')
            self.open_dialog_failed()

    def get_url(self):
        print(self.ids.url_field.text)      #caminho do text field, neste caso o caminho é Downloader(self)>ids>id(url_fields), se estivesse no app, provavelmente o caminho deveria ser App(self)>Downloader(root)>ids>id(url_fields)
        
        return self.ids.url_field.text

    def file_manager_open(self):
        #self.file_manager.show(os.path.expanduser("~"))        #PC
        self.file_manager.show(primary_ext_storage)             #android
        self.manager_open = True

    def select_path(self, path: str):
        self.path = path
        self.exit_manager()
        toast(self.path)
        print(self.path)
        self.ids.label_caminho.text = "Arquivo será salvo em " + self.path      #Altera texto de Label informando onde será salvo o arquivo

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

class CardDownloadCompleted(MDCard):
    def close(self):
        self.parent.remove_widget(self)

class CardDownloadFailed(MDCard):
    def close(self):
        self.parent.remove_widget(self)

class App(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)

    def build(self):
        self.theme_cls.primary_palette = 'Red'
        self.theme_cls.accent_palette = 'Purple'
        self.theme_cls.theme_style = 'Light'
        #return Builder.load_string(KV)
           
    def changeColorTheme(self):
        if(self.theme_cls.theme_style == 'Light'):
            self.theme_cls.theme_style = 'Dark'

        else:
            self.theme_cls.theme_style = 'Light'

if __name__ == '__main__':
    App().run()
