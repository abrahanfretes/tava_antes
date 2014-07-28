'''
Created on 18/07/2014

@author: aferreira
'''
import wx


class I18nLocale(wx.Locale):
    def __init__(self):
        super(I18nLocale, self).__init__(language=wx.LANGUAGE_DEFAULT)

        self.AddCatalogLookupPathPrefix('.')
        self.AddCatalog('tava_es')

    def setCatalog(self, catalog):
        self.AddCatalog(catalog)
