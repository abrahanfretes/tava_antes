'''
Created on 7/6/2015

@author: abrahan
'''
import wx


class TComboBox(wx.Panel):
    def __init__(self, parent, label='Label Combo', values=[]):
        wx.Panel.__init__(self, parent)

        label_combo = wx.StaticText(self, -1, label)
        self.combo = wx.ComboBox(self, 500, "default value", (90, 50),
                                 (160, -1), values,
                                 wx.CB_READONLY
                                 # |wx.CB_DROPDOWN
                                 # | wx.TE_PROCESS_ENTER
                                 # | wx.CB_SORT
                                 )

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(label_combo, 0)
        sizer.Add(self.combo, 0)
        self.SetSizer(sizer)

    def getTSeleccion(self):
        return self.combo.GetSelection()

    def tappend(self, values):
        for item in values:
            self.combo.Append(str(item), item)
