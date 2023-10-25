# coding: utf8
import wx
import time
from time import gmtime, strftime
import os
from os.path import *
from os import getcwd
import subprocess
import shlex
import wx.lib.agw.hyperlink as hl
import wx.media
import threading

#Threads wrapper
def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, None, id, title, wx.DefaultPosition, wx.Size(515, 780),style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX|wx.STAY_ON_TOP)

        #Panel pour affichage
        self.panel = wx.Panel(self,-1)
        self.panel.Fit()
        self.panel.Show()
        #On capture l'event de fermeture de l'app
        self.Bind(wx.EVT_CLOSE,self.on_close,self)

        #Crée la barre d'état (en bas).
        self.CreerBarreEtat()

        #Loader
        self.loader = Loader(self,-1,"Loading...")
        self.loader.Centre()
        
        #Musique Player
        self.player = wx.media.MediaCtrl(self, szBackend=wx.media.MEDIABACKEND_WMP10)
        self.player.Load("zik.mp3")
        self.Bind(wx.media.EVT_MEDIA_LOADED,self.button_play,self.player)
        
        #Boutons
        self.PIP_install_verif = wx.Button(self.panel,-1,"Verify if PIP is UpToDate")
        self.Bind(wx.EVT_BUTTON, self.PIPinstall_verif, self.PIP_install_verif)

        self.MOD_uninstall = wx.Button(self.panel,-1,"Uninstall ?")
        self.Bind(wx.EVT_BUTTON, self.MODuninstall, self.MOD_uninstall)
        self.MOD_uninstall.Disable()
        self.MOD_uninstall.SetForegroundColour("RED")
        self.MOD_uninstall.SetFont(wx.Font(12, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False, "Impact" ))

        #Auto update (all libs !)
        self.up_all = wx.Button(self.panel,-1,"Update ALL libraries ?")
        self.Bind(wx.EVT_BUTTON, self.upall, self.up_all)
        self.up_all.SetForegroundColour("ORANGE")
        self.up_all.SetFont(wx.Font(12, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False, "Impact" ))

        #Boutons musique
        self.buttonZik = wx.Button(self.panel,-1,"Play/Pause")
        self.Bind(wx.EVT_BUTTON, self.button_play, self.buttonZik)

        self.buttonZikStop = wx.Button(self.panel,-1,"Stop")
        self.Bind(wx.EVT_BUTTON, self.button_stop, self.buttonZikStop)

        #widgets vides
        self.txtVideMemo = wx.StaticText(self.panel,-1,"")
        self.txtVideMemo.SetFont(wx.Font(18, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False, "Impact" ))
        self.txtVideMemo.SetForegroundColour("RED")
        
        self.txtVidePIP = wx.StaticText(self.panel,-1,"")
        self.txtVidePIP.SetFont(wx.Font(10, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False, "Impact" ))
        
        #widgets
        self.txtMod = wx.StaticText(self.panel,-1,"Library to install :")
        
        self.txtBox = wx.TextCtrl(self.panel,-1,size=(300,20),style=wx.TE_PROCESS_ENTER)
        self.txtBox.SetHint("Type library name here...")
        self.Bind(wx.EVT_TEXT_ENTER,self.Get_Mod,self.txtBox)
        
        self.AffichTxt=wx.TextCtrl(self.panel,-1,size=(450,300),style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.AffichTxt.SetBackgroundColour('BLACK')
        self.AffichTxt.SetFont(wx.Font(10, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False ))
        self.AffichTxt.SetForegroundColour("FOREST GREEN")

        self.txtMajPip = wx.StaticText(self.panel,-1,"Link to Dev's Paypal.me :")

        self.LienPip = hl.HyperLinkCtrl(self.panel, wx.ID_ANY, 'Thanks if you donate <3',URL="paypal.me/noobpythondev")
        self.LienPip.SetLinkCursor(wx.CURSOR_HAND)
        self.LienPip.SetUnderlines(False, False, True)
        self.LienPip.EnableRollover(True)
        self.LienPip.SetColours("BLUE", "ORANGE", "BLUE")
        self.LienPip.SetBold(True)
        self.LienPip.SetToolTip(wx.ToolTip('Donation link to the no0b Dev ;)'))
        self.LienPip.UpdateLink()
        
        #Sizer install
        gbox0 = wx.GridBagSizer(10,10)
        gbox0.SetEmptyCellSize((10,10))
        gbox0.Add(self.PIP_install_verif,(0,0))
        gbox0.Add(self.txtVidePIP,(0,1))
        gbox0.Add(self.txtMajPip,(1,0))
        gbox0.Add(self.LienPip,(1,1))
        
        #Sizer gestion
        gbox1 = wx.GridBagSizer(10,10)
        gbox1.SetEmptyCellSize((2,2))
        gbox1.Add(self.txtMod,(0,0))
        gbox1.Add(self.txtBox,(0,1))
        gbox1.Add(self.txtVideMemo,(1,1))
        gbox1.Add(self.MOD_uninstall,(2,0))
        gbox1.Add(self.up_all,(2,1))

        #Sizer affichage
        gbox2 = wx.GridBagSizer(10,10)
        gbox2.SetEmptyCellSize((10,10))
        gbox2.Add(self.AffichTxt,(0,0))

        #Sizer zik
        gbox3 = wx.GridBagSizer(10,10)
        gbox3.SetEmptyCellSize((10,10))
        gbox3.Add(self.buttonZik,(0,0))
        gbox3.Add(self.buttonZikStop,(0,1))
        
        #PIP
        box0 = wx.StaticBox(self.panel, -1, "PIP Settings :")
        bsizer0 = wx.StaticBoxSizer(box0, wx.HORIZONTAL)
        sizerH0 = wx.BoxSizer(wx.VERTICAL)
        sizerH0.Add(gbox0, 0, wx.ALL|wx.CENTER, 10)
        bsizer0.Add(sizerH0, 1, wx.EXPAND, 0)
        
        #Modules
        box1 = wx.StaticBox(self.panel, -1, "Librairies Tool :")
        bsizer1 = wx.StaticBoxSizer(box1, wx.HORIZONTAL)
        sizerH1 = wx.BoxSizer(wx.VERTICAL)
        sizerH1.Add(gbox1, 0, wx.ALL|wx.CENTER, 10)
        bsizer1.Add(sizerH1, 1, wx.EXPAND, 0)

        #Affichage
        box2 = wx.StaticBox(self.panel, -1, "Output :")
        bsizer2 = wx.StaticBoxSizer(box2, wx.HORIZONTAL)
        sizerH2 = wx.BoxSizer(wx.VERTICAL)
        sizerH2.Add(gbox2, 0, wx.ALL|wx.CENTER, 10)
        bsizer2.Add(sizerH2, 1, wx.EXPAND, 0)

        #Zik
        box3 = wx.StaticBox(self.panel, -1, "Music :")
        bsizer3 = wx.StaticBoxSizer(box3, wx.HORIZONTAL)
        sizerH3 = wx.BoxSizer(wx.VERTICAL)
        sizerH3.Add(gbox3, 0, wx.ALL|wx.CENTER, 10)
        bsizer3.Add(sizerH3, 1, wx.EXPAND, 0)

        #--------Ajustement du sizer----------
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(bsizer0, 0,wx.ALL|wx.EXPAND, 10)
        mainSizer.Add(bsizer1, 0,wx.ALL|wx.EXPAND, 10)
        mainSizer.Add(bsizer2, 0,wx.ALL|wx.EXPAND, 10)
        mainSizer.Add(bsizer3, 0,wx.ALL|wx.EXPAND, 10)
        self.panel.SetSizerAndFit(mainSizer)

        #couleur bouton zik
        self.buttonZik.SetBackgroundColour(wx.GREEN)
    
    @threaded
    def upall(self,evt):
        global process
        self.AffichTxt.Clear()
        self.show_loader()
        process = subprocess.Popen(shlex.split('pip-review --auto'),encoding ="utf-8", text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        self.get_data()
        if outs:
            self.upall_out()
        if errs:
            self.upall_err()

    def upall_out(self):
        self.hide_loader()
        self.txtVideMemo.SetLabel("ALL Libraries updates done !")
        self.txtVideMemo.SetForegroundColour("FOREST GREEN")
        self.up_all.Disable()

    def upall_err(self):
        self.hide_loader()
        self.txtVideMemo.SetLabel("Update not done !")
        self.txtVideMemo.SetForegroundColour("RED")
        
    def button_play(self,evt):
        colorpause=self.buttonZik.GetBackgroundColour()
        if colorpause==(wx.GREEN):
            self.player.Pause()
            self.buttonZik.SetBackgroundColour("")
        else:#sinon on play
            self.player.Play()
            self.buttonZikStop.SetBackgroundColour("")
            self.buttonZik.SetBackgroundColour(wx.GREEN)
        evt.Skip()

    def button_stop(self,evt):
        self.buttonZikStop.SetBackgroundColour(wx.RED)
        self.buttonZik.SetBackgroundColour("")
        self.player.Stop()
        evt.Skip()
        
    @threaded
    def show_loader(self):
        self.loader.Show()

    @threaded
    def hide_loader(self):
        self.loader.Hide()

    @threaded
    def PIPinstall_verif(self,evt):
        global process
        self.AffichTxt.Clear()
        self.show_loader()
        process = subprocess.Popen(shlex.split('python -m pip install --upgrade pip'),encoding ="utf-8", text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        self.get_data()
        if outs:
            self.PIP_verif_out()
        if errs:
            self.PIP_verif_err()
        evt.Skip()

    def get_data(self):
        global outs,errs
        outs,errs = process.communicate()
        if outs:
            self.AffichTxt.SetForegroundColour("FOREST GREEN")
            self.AffichTxt.AppendText(outs + "\n")
        if errs:
            self.AffichTxt.SetForegroundColour("RED")
            self.AffichTxt.AppendText(errs + "\n")

    #Kinda deprecated as it's not supposed to be possible...
    def PIP_verif_err(self):
        self.hide_loader()
        self.txtVidePIP.SetLabel('PIP not installed !')
        self.txtVidePIP.SetForegroundColour("RED")
        self.PIP_install.Enable()
        self.PIP_install_verif.Disable()
        
    def PIP_verif_out(self):
        self.hide_loader()
        self.txtVidePIP.SetLabel('PIP is Up To Date !')
        self.txtVidePIP.SetForegroundColour("FOREST GREEN")
        self.PIP_install_verif.Disable()

    @threaded     
    def Get_Mod(self,evt):
        global exception,process
        exception=0
        self.AffichTxt.Clear()
        mod_to_install=self.txtBox.GetValue()
        self.show_loader()
        process = subprocess.Popen(shlex.split('python -m pip install '+mod_to_install),encoding ="utf-8", text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        self.get_data()
        if outs:
            txt_except="Requirement already satisfied: "+mod_to_install
            if txt_except in outs:
                exception=1    
            self.MOD_out()
        if errs:
            self.MOD_err()
        evt.Skip()
        
    def MOD_out(self):
        self.hide_loader()
        if exception==1:
            self.txtVideMemo.SetForegroundColour("RED")
            self.txtVideMemo.SetLabel("Library already installed !")
            self.MOD_uninstall.Enable()
        else:
            self.txtVideMemo.SetLabel("Library installation done !")
            self.txtVideMemo.SetForegroundColour("FOREST GREEN")

    def MOD_err(self):
        self.hide_loader()
        self.txtVideMemo.SetForegroundColour("RED")
        self.txtVideMemo.SetLabel("Library not found ! >_<")
        self.MOD_uninstall.Enable()

    @threaded
    def MODuninstall(self,evt):
        global process
        self.AffichTxt.Clear()
        mod_to_uninstall=self.txtBox.GetValue()
        self.show_loader()
        process = subprocess.Popen(shlex.split('python -m pip uninstall -y '+mod_to_uninstall),encoding ="utf-8", text=True, stdout=subprocess.PIPE,shell=True)
        self.get_data()
        if outs:
            self.MOD_uninstall_out()
        evt.Skip()

    def MOD_uninstall_out(self):
        self.hide_loader()
        self.txtVideMemo.SetLabel("")
        self.txtVideMemo.SetLabel("Library successfully uninstalled !")
        self.txtVideMemo.SetForegroundColour("FOREST GREEN")
        self.MOD_uninstall.Disable()
    
    def Chrono(self):#Chronometre (date )
        stemps = time.strftime("%A %d/%m/%Y") #Definit le format voulu
        self.SetStatusText(stemps,1) #Affiche a droite.
    
    def CreerBarreEtat(self):#Creation de la barre d'etat du bas avec l'affichage de la date
        self.CreateStatusBar(2) #Cree une barre de statut (en bas) de deux parties.
        self.SetStatusWidths([-1,150]) #Definit la taille.
        self.Chrono()#Affiche.

    def on_close(self,evt):#On detruit tout :)
        try:
            self.player.Stop()
        except:
            pass
        finally:
            self.loader.Destroy()
            self.Destroy()

class Loader(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, None, id, title, wx.DefaultPosition, wx.Size(300, 200),style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX|wx.STAY_ON_TOP)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self,-1)
        self.panel.Fit()
        self.panel.Show()

        self.txt = wx.StaticText(self.panel,-1,"Verifying Libraries Please Wait...")
        self.spinner = wx.ActivityIndicator(self.panel, size=(35, 35))

        sizer.AddStretchSpacer(1)
        sizer.Add(self.txt, 0, wx.ALIGN_CENTER)
        sizer.Add(self.spinner, 1, wx.ALIGN_CENTER)
        sizer.AddStretchSpacer(1)

        self.panel.SetSizerAndFit(sizer)
        self.spinner.Start()

        #usage : put in wx.Frame class, then call Show/Hide or Destroy
        
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, "PIP_GUI_V1.0 by François GARBEZ")
        frame.Show(True)
        frame.Centre()
        return True
 
if __name__=='__main__':    
 
    app = MyApp(0)
    app.MainLoop()


### PIP_GUI_V1.0 by François GARBEZ 25/10/2023 Tested on python 3.12 Win10 ###
