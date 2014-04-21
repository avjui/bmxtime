# -*- coding: iso-8859-1 -*-

import wx
import sys

from database import Database

class DriverList(wx.Dialog):
     
        def __init__(self, parent):

                wx.Dialog.__init__(self, parent, -1, "Fahrerliste", size=(900,400),
                                style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|
                                wx.TAB_TRAVERSAL)

                self.__CreateDriversList()
                
                
        def __CreateDriversList(self):

                self.DropDownList = ['test1', 'Test2', 'Test3']                 
                wx.StaticText(self, -1, 'Nr.', pos=(20,20))
                self.nbr = wx.TextCtrl(self, -1, pos=(20,45), size=(40,-1))
                wx.StaticText(self, -1, 'Vorname.', pos=(20,70))
                self.name = wx.TextCtrl(self, -1, size=(150,-1), pos=(20,95))
                wx.StaticText(self, -1, 'Nachname', pos=(20,120))
                self.famname = wx.TextCtrl(self, -1, size=(150,-1), pos=(20,145))
                wx.StaticText(self, -1, 'Geburtsdatum', pos=(20,170))
                self.date = wx.TextCtrl(self, -1, size=(150,-1), pos=(20,195))
                wx.StaticText(self, -1, 'Klasse', pos=(20,220))
                self.clas = wx.ComboBox(self, value="Klasse Auswählen", choices=self.DropDownList, size=(150,-1), pos=(20,245))
                self.buttonsave = wx.Button(self, -1, label='Hinzufügen', pos=(650,290), size=(100,25))
                self.buttondelete = wx.Button(self, -1, label='Löschen', pos=(760,290), size=(100,25))
                self.buttonadd_class = wx.Button(self, -1, label='Klasse hinzufügen', pos=(650,320), size=(210,25))
                self.buttonsave.Bind(wx.EVT_BUTTON , self.__save)
                self.buttondelete.Bind(wx.EVT_BUTTON , self.__delete)
                self.buttonadd_class.Bind(wx.EVT_BUTTON , self.__add_class)

                # create the list
                
                self.dl = wx.ListCtrl(self, -1, size=(640,250), pos=(220,20), style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SORT_ASCENDING)
                self.dl.InsertColumn(0, 'Nr')
                self.dl.InsertColumn(1, 'Nachname')
                self.dl.InsertColumn(2, 'Vorname')
                self.dl.InsertColumn(3, 'Geburtsdatum')
                self.dl.InsertColumn(4, 'Klasse')
                self.dl.SetColumnWidth(0, 40)
                self.dl.SetColumnWidth(1, 150)
                self.dl.SetColumnWidth(2, 150)
                self.dl.SetColumnWidth(3, 100)
                self.dl.SetColumnWidth(4, 100)

                # add lines from database
                self.__update_list()
                

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
                pass

        def __add_class(self, event):
                """
                Add ne class to database
                """
                pass


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
