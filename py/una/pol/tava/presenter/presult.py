'''
Created on 30/08/2014

@author: abrahan
'''

import  os


class AddFileDialogPresenter():
    def __init__(self, iview):
        self.iview = iview
        self.countItem = 0

    def addListPath(self):

        for path in self.iview.dlg.GetPaths():
            dir_name = os.path.split(path)
            dir_name_add = list(dir_name)
            dir_name_add.reverse()
            self.iview.dvlc.AppendItem(dir_name_add)
            self.countItem += 1

        self.iview.o_button.Enable(True)
        self.iview.rb.EnableItem(0, True)

    def Close(self):
        self.iview.Close(True)

    def AddFile(self):
        list_path = []
        for i in range(self.countItem):
            list_path.append(self.getPath(i))

        print list_path
        self.Close()

    def getPath(self, row):

        return os.path.join(self.iview.dvlc.GetTextValue(row, 1),
            self.iview.dvlc.GetTextValue(row, 0))

    def deletedOneFile(self):
        self.iview.dvlc.DeleteItem(self.iview.dvlc.GetSelectedRow())
        self.countItem -= 1
        if self.countItem == 0:
            self.iview.o_button.Enable(False)
            self.iview.rb.EnableItem(0, False)

    def deletedAllFile(self):
        self.iview.dvlc.DeleteAllItems()
        self.countItem = 0
        self.iview.o_button.Enable(False)
        self.iview.rb.EnableItem(0, False)
