'''
Created on 1/5/2015

@author: abrahan
'''

import wx


# -------------------         Panel Splitter           ------------------------
# -------------------                                  ------------------------
class PageAndrewsCurves(wx.SplitterWindow):
    def __init__(self, parent, test):
        wx.SplitterWindow.__init__(self, parent)

        #  ------ self customize ----------------------------------------
        self.SetMinimumPaneSize(3)
        self.SetBorderSize(1)

        #  ------ self components --------------------------------------
        self.top_panel = TopPanel(self, test)
        self.footer = BottomPanel(self, test)
        high = int(round(self.GetParent().GetSize().GetWidth() * 0.50))
        self.SplitHorizontally(self.top_panel, self.footer, high)
        # ------ self controls -----------------------------------------


# -------------------         Panel for top            ------------------------
# -------------------                                  ------------------------
class TopPanel(wx.SplitterWindow):
    def __init__(self, parent, test):
        wx.SplitterWindow.__init__(self, parent)

        # ------ self customize ----------------------------------------
        self.SetMinimumPaneSize(3)
        # ------ self components --------------------------------------
        self.parent = parent


# -------------------         Panel for botton         ------------------------
# -------------------                                  ------------------------
class BottomPanel(wx.Panel):

    def __init__(self, parent, test):
        wx.Panel.__init__(self, parent)

        # ------ self customize ---------------------------------------
    # ------ self controls --------------------------------------------
