# -*- coding: iso-8859-1 -*-

import wx
import sys

from database import Database
from logger import Log

log = Log()
class DriverList(wx.Dialog):
     
        def __init__(self, parent):

                wx.Dialog.__init__(self, parent, -1, "Fahrerliste", size=(900,473),
                                style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|
                                wx.TAB_TRAVERSAL)

                self.__CreateDriversList()
                
                
        def __CreateDriversList(self):
                
                hbox = wx.BoxSizer(wx.HORIZONTAL)
                inbox = wx.BoxSizer(wx.VERTICAL)

                buttonbox1 = wx.BoxSizer(wx.HORIZONTAL)

                hbox.Add((25,-1))
                self.DropDownList = Database().GetAllData('Klassen', convert=True)                
                self.nbrhead = wx.StaticText(self, -1, 'Nr.')
                self.nbr = wx.TextCtrl(self, -1, size=(40,-1))
                inbox.Add(self.nbrhead, flag=wx.TOP, border=10)
                inbox.Add(self.nbr, flag=wx.TOP, border=8)
                self.namehead = wx.StaticText(self, -1, 'Vorname.')
                self.name = wx.TextCtrl(self, -1, size=(150,-1))
                inbox.Add(self.namehead, flag=wx.TOP, border=10)
                inbox.Add(self.name, flag=wx.TOP, border=8)
                self.famnamehead = wx.StaticText(self, -1, 'Nachname')
                self.famname = wx.TextCtrl(self, -1, size=(150,-1))
                inbox.Add(self.famnamehead, flag=wx.TOP, border=10)
                inbox.Add(self.famname, flag=wx.TOP, border=8)
                self.datehead = wx.StaticText(self, -1, 'Geburtsdatum')
                self.date = wx.TextCtrl(self, -1, size=(150,-1))
                inbox.Add(self.datehead, flag=wx.TOP, border=10)
                inbox.Add(self.date, flag=wx.TOP, border=8)
                self.clashead = wx.StaticText(self, -1, 'Klasse')
                self.clas = wx.ComboBox(self, value="Klasse Auswählen", choices=self.DropDownList, size=(150,-1), style=wx.CB_SORT)
                inbox.Add(self.clashead, flag=wx.TOP, border=10)
                inbox.Add(self.clas, flag=wx.TOP, border=8)

                # create the list
                
                self.dl = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
                self.dl.InsertColumn(0, 'Nr')
                self.dl.InsertColumn(1, 'Nachname')
                self.dl.InsertColumn(2, 'Vorname')
                self.dl.InsertColumn(3, 'Geburtsdatum')
                self.dl.InsertColumn(4, 'Klasse')
                self.dl.SetColumnWidth(0, 40)
                self.dl.SetColumnWidth(1, 150)
                self.dl.SetColumnWidth(2, 150)
                self.dl.SetColumnWidth(3, 100)
                self.dl.SetColumnWidth(4, 150)
              

                # buttons
                self.buttonsave = wx.Button(self, -1, label='Hinzufügen', size=(100,25))
                buttonbox1.Add(self.buttonsave)
                self.buttondelete = wx.Button(self, -1, label='Löschen', size=(100,25))
                buttonbox1.Add(self.buttondelete)
                self.buttonadd_class = wx.Button(self, -1, label='Klasse hinzufügen', size=(200,25))
                inbox.Add((-1,75))
                inbox.Add(buttonbox1)
                inbox.Add(self.buttonadd_class)
                hbox.Add(inbox, flag=wx.BOTTOM, border=25)
                hbox.Add(self.dl, flag=wx.LEFT|wx.GROW|wx.ALL, border=25)  

                # Events
                self.buttonsave.Bind(wx.EVT_BUTTON , self.__save)
                self.buttondelete.Bind(wx.EVT_BUTTON , self.__delete)
                self.buttonadd_class.Bind(wx.EVT_BUTTON , self.__add_class)
                

                self.SetSizer(hbox)
                self.SetAutoLayout(True)

                
                # add lines from database
                self.__update_list()
                
                # Event for sorting list
                self.dl.Bind(wx.EVT_LIST_COL_CLICK, self.__OnColClick, self.dl)

        def __save(self, event):
                """
                Save data to database
                """

                self.databaselst = []
                self.databaselist = [int(self.nbr.GetValue()),self.name.GetValue(),self.famname.GetValue(),self.date.GetValue(), self.clas.GetValue()]
                Database().AddData('Fahrer', self.databaselist)

                self.__update_list()
                

        def __delete(self, event):
                """
                Delet selected data from database
                """
                item = self.dl.GetFirstSelected() 
                nr = self.dl.GetItem(itemId=item, col=0)
                print(nr.GetText())
                # Delete data from database
                Database().RemoveDataById(nr.GetText())

                #Update the list
                self.__update_list()
                return
        

        def __add_class(self, event):
                """
                Add ne class to database
                """
                classdlg = wx.TextEntryDialog(None, 'Geben Sie eine neue Klasse an')
                ret = classdlg.ShowModal()
                if ret == wx.ID_OK:
                    Database().AddClass(classdlg.GetValue())

                classdlg.Destroy()

                # Clear and update combobox
                self.clas.Clear()                
                for item in Database().GetAllData('Klassen', convert=True):
                        self.clas.Append(item)

                # Readd Value
                self.clas.SetValue('Klasse Auswählen')
                return

        def __update_list(self):
                """
                Update the listctrl box
                """
                
                self.dl.DeleteAllItems()
                
                data = Database().GetAllData('Fahrer')
                for i in data:
                     index = self.dl.InsertStringItem(sys.maxint, str(i[0]))
                     self.dl.SetStringItem(index, 1, i[1])
                     self.dl.SetStringItem(index, 2, i[2])
                     self.dl.SetStringItem(index, 3, i[3])
                     self.dl.SetStringItem(index, 4, i[4])

        
        def __OnColClick(self, event):
                """
                Function when you click on list colum to sort the list
                """
                coln=event.GetColumn()
                log.debug('[Driverslist] List colum %d was be clicked' % coln)

                self.dl.DeleteAllItems()
                if coln ==0:
                        data = Database().GetAllData('Fahrer', 'FahrerNR')
                if coln ==1:
                        data = Database().GetAllData('Fahrer', 'Nachname')
                if coln ==2:
                        data = Database().GetAllData('Fahrer', 'Vorname')
                if coln ==3:
                        data = Database().GetAllData('Fahrer', 'Datum')
                if coln ==4:
                        data = Database().GetAllData('Fahrer', 'Klasse')

                for i in data:
                     index = self.dl.InsertStringItem(sys.maxint, str(i[0]))
                     self.dl.SetStringItem(index, 1, i[1])
                     self.dl.SetStringItem(index, 2, i[2])
                     self.dl.SetStringItem(index, 3, i[3])
                     self.dl.SetStringItem(index, 4, i[4])
                event.Skip()
                return

        
