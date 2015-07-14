'''
Created on 7/6/2015

@author: abrahan
'''
import wx


class TComboBox(wx.Panel):
    def __init__(self, parent, label='Label Combo', values=[], back_g='#AABBCC'):
        wx.Panel.__init__(self, parent)

        self.SetBackgroundColour('#AABBCC')
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
        self.combo.Set([str(v) for v in values])


class TSpinCtrlDouble(wx.Panel):
    def __init__(self, parent, label='Tava Spin', back_g='#AABBCC'):
        wx.Panel.__init__(self, parent)

        self.SetBackgroundColour('#AABBCC')
        label = wx.StaticText(self, -1, label)
        spin = wx.SpinCtrlDouble(self)
        spin.SetValue(0.05)
        spin.SetIncrement(0.01)
        spin.SetMin(0)
        spin.SetMax(1)
        spin.SetDigits(2)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(label, 0)
        sizer.Add(spin, 0)
        self.SetSizer(sizer)

    def getTSeleccion(self):
        return self.combo.GetSelection()


class TChoice(wx.Panel):
    def __init__(self, parent, label='Select one:', values=[], back_g='#AABBCC'):
        wx.Panel.__init__(self, parent)

        self.SetBackgroundColour('#AABBCC')
        label = wx.StaticText(self, -1, label)
        self.choice = wx.Choice(self, -1, (100, 50), choices=values)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(label, 0)
        sizer.Add(self.choice, 0)
        self.SetSizer(sizer)

    def getTSeleccion(self):
        return self.choice.GetCurrentSelection()

    def tappend(self, values):
        self.choice.Set([str(v) for v in values])
