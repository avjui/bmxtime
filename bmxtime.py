#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import sys
import time
import wx
import wx.gizmos as gizmos
import wx.lib.mixins.listctrl as listmix
import threading

#Eigene Module
from connection import Connections,Ports
from database import Database
from driverlist import DriverList


class StartWindow(wx.Frame):
     
        def __init__(self, parent = None, id = -1, title = "BMX Bludenz - Zeitmessung"):
                # Init
                wx.Frame.__init__(
                        self, parent, id, title, size = (1000,500), 
                        style = wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
                self.panel = wx.Panel(self, -1)
                self.main()
                
        def main(self):

                # StatusBar
                self.CreateStatusBar()
                self.SetIcon(wx.Icon('icons/favicon.ico', wx.BITMAP_TYPE_ICO))

                # Filemenu
                filemenu = wx.Menu()

                # Bestenliste
                menuitem = wx.MenuItem(filemenu, -1, "&Bestenliste", "Bestenliste an Hand der gefahrenen Zeiten")
                filemenu.AppendItem(menuitem)
                self.Bind(wx.EVT_MENU, self.OnAbout, menuitem) # Hier wird der Event-Handler angegeben

                # Save
                menuitem = filemenu.Append(-1, "&Speichern", "Speichern der Ergebnise")
                self.Bind(wx.EVT_MENU, self.OnSave, menuitem) # Hier wird der Event-Handler angegeben
                
                # Filemenu - About
                menuitem = filemenu.Append(-1, "&About", "Informationen über das Programm")
                self.Bind(wx.EVT_MENU, self.OnAbout, menuitem) # Hier wird der Event-Handler angegeben
     
                # Filemenu - Separator
                filemenu.AppendSeparator()
     
                # Filemenu - Exit
                menuitem = wx.MenuItem(filemenu, -1, "E&xit", "Beenden des Programmes")
                menuitem.SetBitmap(wx.Bitmap('icons/exit.png'))
                filemenu.AppendItem(menuitem)
                self.Bind(wx.EVT_MENU, self.OnExit, menuitem) # Hier wird der Event-Handler angegeben

                # Filemenu 2 - Fahrer
                filemenu2 = wx.Menu()

                # Filemenu 2 Fahrerliste
                menuitem = filemenu2.Append(-1, "Fahrer&liste", "Bearbeitung der Liste der Fahrer")
                self.Bind(wx.EVT_MENU, self.OnDriversList, menuitem)

                #Filemenu 3 - Settings
                filemenu3 = wx.Menu()

                #Filemenu 3- Port
                menuitem = filemenu3.Append(-1, "&Port", "Einstellungen für die Schnittstellen")
                self.Bind(wx.EVT_MENU, self.OnPortConfiguration, menuitem)

                #Filemenu 3 - Messsstellen
                menuitem = filemenu3.Append(-1, "&Messstellen", "Einstellungen für die Zwischenzeiten")
                self.Bind(wx.EVT_MENU, self.OnTimeConfiguration, menuitem)
                
                # Menubar erstellen
                menubar = wx.MenuBar()
                menubar.Append(filemenu,"&Programm")
                menubar.Append(filemenu2,"&Fahrer")
                menubar.Append(filemenu3,"&Einstellungen")
                self.SetMenuBar(menubar)

                self.font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)
                labels = { 'Zwischenzeit 1' : (25,150),
                           'Zwischenzeit 2' : (25,280),
                           'Endzeit' : (25,20),
                           }

                self.horizontal = wx.BoxSizer()
                
                for key,value in labels.items():
                        self.CreatPanel(key, value)

                # Tabel
                self.CreatList()
                
                # Eingabefelder
                wx.StaticText(self.panel, -1, 'Nr.', pos=(225,280))
                self.number = wx.TextCtrl(self.panel, -1, pos=(220,300), size=(80,-1), style=wx.TE_READONLY)
                self.number.SetBackgroundColour('white')
                wx.StaticText(self.panel, -1, 'Nachname', pos=(315,280))
                self.firstname = wx.TextCtrl(self.panel, -1, pos=(310,300), size=(150,-1), style=wx.TE_READONLY)
                self.firstname.SetBackgroundColour('white')
                wx.StaticText(self.panel, -1, 'Vorame', pos=(475,280))
                self.secondname = wx.TextCtrl(self.panel, -1, pos=(470,300), size=(150,-1), style=wx.TE_READONLY)
                self.secondname.SetBackgroundColour('white')
                
                # Buttons
                self.buttonadd = wx.Button(self.panel, -1, label='Ready for Race', pos=(625,299))
                self.buttonadd.Bind(wx.EVT_BUTTON, self.SetReady)

                self.buttonload = wx.Button(self.panel, -1, label='Fahrerliste neu Laden', pos=(730,299))
                self.buttonload.Bind(wx.EVT_BUTTON, self.UpdateList)

                #gogogo
                self.Center()
                self.Show(True)

                
        def CreatPanel(self, label, position = (25,20)):

                self.boxx = position[0] - 10
                self.boxy = position[1] + 40

                current = time.localtime(time.time())
                # time string can have characters 0..9, -, period, or space
                ts = time.strftime("%H %M %S", current)

                pos = wx.DefaultPosition
                self.cpnl = wx.Panel(self.panel, pos=(self.boxx, self.boxy),size=(180, 40), style = wx.BORDER_SUNKEN)
                self.led = gizmos.LEDNumberCtrl(self.cpnl, -1, wx.DefaultPosition, size=(176,36))
                self.led.SetBackgroundColour('blue')
                self.led.SetForegroundColour('yellow')
                #self.led.SetValue(ts)
        
                self.tonetext = wx.StaticText(self.panel, -1, label, position, (160, -1), wx.ALIGN_CENTER)
                self.tonetext.SetFont(self.font)
                self.horizontal.Add(self.tonetext, flag=wx.CENTER)
                self.horizontal.Add(self.cpnl, flag=wx.CENTER)                
                

        def CreatList(self):

                self.lc = wx.ListCtrl(self.panel, -1, size=(640,250), pos=(220,20), style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SORT_ASCENDING)
                self.lc.InsertColumn(0, 'Nr.')
                self.lc.InsertColumn(1, 'Nachname')
                self.lc.InsertColumn(2, 'Vorname')
                self.lc.InsertColumn(3, 'Zwischenzeit1')
                self.lc.InsertColumn(4, 'Zwischenzeit1')
                self.lc.InsertColumn(5, 'Endzeit')
                self.lc.SetColumnWidth(0, 40)
                self.lc.SetColumnWidth(1, 150)
                self.lc.SetColumnWidth(2, 150)
                self.lc.SetColumnWidth(3, 100)
                self.lc.SetColumnWidth(4, 100)
                self.lc.SetColumnWidth(5, 100)
                self.UpdateList(self)
                self.lc.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.PopUpMenu, self.lc)
                self.lc.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.GetReady, self.lc)


        def PopUpMenu(self, event):
                popupmenu = wx.Menu()
                popupmenu.Append(1, 'Löschen')
                popupmenu.Append(2, 'Bearbeiten')
                popupmenu.Destroy()
                

        def UpdateList(self, event):
                
                self.lc.DeleteAllItems()
                data = Database().GetAllData('Fahrer')
                for i in data:
                     index = self.lc.InsertStringItem(sys.maxint, str(i[0]))
                     self.lc.SetStringItem(index, 1, i[1])
                     self.lc.SetStringItem(index, 2, i[2])
                return
                
                
        def GetReady(self,event):
                """
                Set values from list to the Ready Box
                """

                item = self.lc.GetFirstSelected() 
                self.nr = self.lc.GetItem(itemId=item, col=0)
                self.fname = self.lc.GetItem(itemId=item, col=1)
                self.sname = self.lc.GetItem(itemId=item, col=2)
                self.number.SetValue(self.nr.GetText())
                self.firstname.SetValue(self.fname.GetText())
                self.secondname.SetValue(self.sname.GetText())

        def SetReady(self, event):

                """
                Set arduion to ready
                """

                fieldlist =[self.number, self.firstname, self.secondname]
                for field in fieldlist:
                        field.SetBackgroundColour('green')
                        field.Refresh()

                serial_ready = True
                # Start the serial connection
                #time_datas = threading.Thread(target=Connections().read_data, args=(serial_ready,))
                #time_datas.start()

                
               
        def OnDriversList(self,event):
                """
                This create a Dialogbox for add end edit the drivers list
                """

                driverlist = DriverList(self)
                if (driverlist.ShowModal() == wx.ID_OK):
                        print "Done"
                driverlist.Destroy()
                                   

        def OnPortConfiguration(self,event):
                """
                Based on the wxPython demo - opens the MultiChoiceDialog
                """

                lst = Connections().get_serial_ports()
                
                if lst:
                        dlg = wx.MultiChoiceDialog( self, 
                                           "Bitte den Com Port auswählen",
                                           "Com Port Einstellungen", lst)
 
                        if (dlg.ShowModal() == wx.ID_OK):
                            selections = dlg.GetSelections()
                            strings = [lst[x] for x in selections]
                            # Debug
                            print "You chose:" + str(strings)
                        dlg.Destroy()
                else:
                        dlg = wx.MessageDialog( self, "Warnung kein Com Port verfügbar", "Schnittstellen Fehler", wx.ICON_ERROR)
                        if (dlg.ShowModal() == wx.ID_OK):
                                dlg.Destroy()

        def OnTimeConfiguration(self, event):

                timedlg = wx.Dialog( self, "parent", -1)
                timedlg.SetTitel('Zeitmessstellen')
                
                #self.cb = wx.CheckBox(timedlg, -1, 'Show Title', (10, 10))
                #self.cb.SetValue(True)


        def OnSave(self,event):
                return
        
        def OnAbout(self,event):

                """
                Shows the Aboutdialog
                """
                
                description = """\nEine simples Zeitmessungprogramm mit Hilfe von Ardurino UNO\nEs werden auch Zwischenzeiten unterstützt"""

                info = wx.AboutDialogInfo()
                info.SetIcon(wx.Icon('icons/bmx.png', wx.BITMAP_TYPE_PNG))
                info.SetName('\nZeitmessung')
                info.SetDescription(description)
                info.SetVersion('\n1.0 Beta')
                info.SetWebSite('http://bmx-bludenz.at' )

                wx.AboutBox(info)
     
     
        def OnExit(self,event):
                self.Close(True)  # Close the frame.
     

if __name__ == '__main__':
        
 
        app = wx.App(False)
        frame = StartWindow()
        app.MainLoop()
        

        # Zerstören der Objekte, damit dieses Beispiel
        # im IDLE nicht nur einmal funktioniert.
        del frame
        del app
