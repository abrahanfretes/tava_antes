'''
Created on 06/09/2014

@author: arsenioferreira
'''
import wx
import wx.wizard as wizmod
from wx.lib.itemspicker import ItemsPicker, IP_SORT_CHOICES, IP_SORT_SELECTED,\
                               IP_REMOVE_FROM_CHOICES, EVT_IP_SELECTION_CHANGED
import py.una.pol.tava.view.vimages as images
from py.una.pol.tava.presenter.ptest import WizardFirstPagePresenter
import wx.dataview as dv

padding = 5

graphList = ["Parallel Coordinates",
              "Scatter Plot",
              "Som"]


class GraphicWizard(wizmod.Wizard):
    '''Add pages to this wizard object to make it useful.'''
    def __init__(self, project):

        self.project = project

        wizmod.Wizard.__init__(self, None, -1, title="New")
        self.SetPageSize((500, 380))
        wx.DefaultSize
        self.pages = []

        # Create a first page
        page1 = WizardFirstPage(self)
        self.page1 = page1
        self.add_page(page1)

        # Add second page
        self.page2 = WizardSecondPage(self)
        self.add_page(self.page2)

        # Add third page
        self.add_page(WizardThirdPage(self))

        self.Bind(wizmod.EVT_WIZARD_PAGE_CHANGED, self.on_page_changed)
        self.Bind(wizmod.EVT_WIZARD_FINISHED, self.on_finished)

        self.FitToPage(page1)

        # Show the main window
        self.run()

        # Cleanup
        self.Destroy()

    def add_page(self, page):
        '''Add a wizard page to the list.'''
        if self.pages:
            previous_page = self.pages[-1]
            page.SetPrev(previous_page)
            previous_page.SetNext(page)
        self.pages.append(page)

    def on_page_changed(self, evt):
        page = evt.GetPage()
        forward_btn = self.FindWindowById(wx.ID_FORWARD)
        if not (page is self.pages[2]) and evt.GetDirection():
            forward_btn.Disable()
        else:
            forward_btn.Enable(True)

        page = evt.GetPage()
        if page is self.pages[1]:
            if not hasattr(self.page2, 'ldv'):
                # construir diccionario
                files = {
                    1: ("Iterarion 1", "1-NSGA2-RANDOM-EpsDOM-Po1-R1"),
                    2: ("Iterarion 2", "1-NSGA2-RANDOM-EpsDOM-Po1-R1"),
                    3: ("Iterarion 1",
                       "1-NSGA2-RANDOM-EpsDOM-Ps800-DTLZ1-Obj10-C1S1P1-Po1-R1")
                    }
                for selection in self.page1.ip.GetSelections():
                    files = {key: value for key, value in files.items()
                             if value[1] == selection}
                ldv = TestPanel(self.page2, files)
                self.page2.sizer.Add(ldv, 1, wx.EXPAND)
                self.page2.ldv = ldv

    def run(self):
        self.RunWizard(self.pages[0])

    def on_finished(self, evt):
        '''Finish button has been pressed.  Clean up and exit.'''
        print "OnWizFinished\n"
#         print self.pages[1].gl.GetSelection()


class WizardFirstPage(wizmod.PyWizardPage):
    ''' An extended panel obj with a few methods to keep track of its siblings.
        This should be modified and added to the wizard.  Season to taste.'''
    def __init__(self, parent):
        wizmod.PyWizardPage.__init__(self, parent)

        self.presenter = WizardFirstPagePresenter(self)

        self.next = self.prev = None
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, -1, "Tava Test")
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.AddWindow(title, 0, wx.ALIGN_LEFT | wx.ALL, padding)
        self.sizer.AddWindow(wx.StaticLine(self, -1), 0, wx.EXPAND |
                             wx.ALL, padding)

        panel = wx.Panel(self)

        sizer = wx.GridBagSizer(5, 5)

        text2 = wx.StaticText(panel, label="Test Name")
        sizer.Add(text2, pos=(1, 0), flag=wx.LEFT, border=10)

        name_value_text = wx.TextCtrl(panel)
        sizer.Add(name_value_text, pos=(1, 1), span=(1, 4), flag=wx.TOP |
                  wx.EXPAND)

        # Definicion del text para el label de nombre de proyecto
        project_text = wx.StaticText(panel, label="Project")
        sizer.Add(project_text, pos=(2, 0), flag=wx.LEFT, border=10)

        # Definicion del text para el valor del nombre de proyecto
        project_value_text = wx.StaticText(panel, label=parent.project.name)

        # Desabilitamos el componente text
        project_value_text.Disable()

        # Agregamos el componente text al sizer principal
        sizer.Add(project_value_text, pos=(2, 1), span=(1, 4), flag=wx.RIGHT |
                  wx.EXPAND)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        self.ip = ItemsPicker(self, -1, self.GetListItems(), 'Files:',
                              'Selected Files:', ipStyle=IP_SORT_CHOICES |
                              IP_SORT_SELECTED | IP_REMOVE_FROM_CHOICES)
        self.ip._source.SetMinSize((-1, 150))
        self.ip.Bind(EVT_IP_SELECTION_CHANGED, self.OnSelectionChange)
        vbox2.Add(self.ip, 1, wx.EXPAND | wx.ALL, 3)

        sizer.Add(vbox2, pos=(6, 0), span=(1, 5),
                  flag=wx.EXPAND | wx.ALL)

        sizer.AddGrowableCol(2)

        panel.SetSizer(sizer)

        self.sizer.Add(panel, 0, wx.EXPAND | wx.ALL, padding)
        self.SetSizer(self.sizer)
        self.Fit()

    def SetNext(self, next_):
        '''Set the next page'''
        self.next = next_

    def SetPrev(self, prev):
        '''Set the previous page'''
        self.prev = prev

    def GetNext(self):
        '''Return the next page'''
        return self.next

    def GetPrev(self):
        '''Return the previous page'''
        return self.prev

    def GetListItems(self):
        return self.presenter.GetListItems()

    def OnSelectionChange(self, e):
        forward_btn = self.GetParent().FindWindowById(wx.ID_FORWARD)
        if e.GetItems():
            forward_btn.Enable(True)
        else:
            forward_btn.Disable()


class WizardSecondPage(wizmod.PyWizardPage):
    ''' An extended panel obj with a few methods to keep track of its siblings.
        This should be modified and added to the wizard.  Season to taste.'''
    def __init__(self, parent):
        wizmod.PyWizardPage.__init__(self, parent)
        self.next = self.prev = None
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, -1, "Tava Test")
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.AddWindow(title, 0, wx.ALIGN_LEFT | wx.ALL, padding)
        self.sizer.AddWindow(wx.StaticLine(self, -1), 0, wx.EXPAND |
                             wx.ALL, padding)

#         ldv = TestPanel(self)
#         self.sizer.Add(ldv, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

    def SetNext(self, next_):
        '''Set the next page'''
        self.next = next_

    def SetPrev(self, prev):
        '''Set the previous page'''
        self.prev = prev

    def GetNext(self):
        '''Return the next page'''
        return self.next

    def GetPrev(self):
        '''Return the previous page'''
        return self.prev


class WizardThirdPage(wizmod.PyWizardPage):
    ''' An extended panel obj with a few methods to keep track of its siblings.
        This should be modified and added to the wizard.  Season to taste.'''
    def __init__(self, parent):
        wizmod.PyWizardPage.__init__(self, parent)
        self.next = self.prev = None
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, -1, "Tava Test")
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.AddWindow(title, 0, wx.ALIGN_LEFT | wx.ALL, padding)
        self.sizer.AddWindow(wx.StaticLine(self, -1), 0, wx.EXPAND |
                             wx.ALL, padding)
        self.gl = GraphicList(self)
        self.sizer.Add(self.gl, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

    def SetNext(self, next_):
        '''Set the next page'''
        self.next = next_

    def SetPrev(self, prev):
        '''Set the previous page'''
        self.prev = prev

    def GetNext(self):
        '''Return the next page'''
        return self.next

    def GetPrev(self):
        '''Return the previous page'''
        return self.prev


class ColoredPanel(wx.Window):
    def __init__(self, parent, color):
        wx.Window.__init__(self, parent, -1, style=wx.SIMPLE_BORDER)
        self.SetBackgroundColour(color)
        if wx.Platform == '__WXGTK__':
            self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)


class GraphicList(wx.Listbook):
    def __init__(self, parent):
        wx.Listbook.__init__(self, parent, id=-1, style=wx.BK_DEFAULT)

        il = wx.ImageList(64, 64)
        obj = getattr(images, 'parallel_ico')
        bmp = obj.GetBitmap()
        il.Add(bmp)
        obj = getattr(images, 'scatterplot_ico')
        bmp = obj.GetBitmap()
        il.Add(bmp)
        obj = getattr(images, 'som_ico')
        bmp = obj.GetBitmap()
        il.Add(bmp)
        self.AssignImageList(il)

        win = self.makeColorPanel("Aquamarine")
        self.AddPage(win, graphList[0], imageId=0)

        win = self.makeColorPanel("Red")
        self.AddPage(win, graphList[1], imageId=1)

        win = self.makeColorPanel("Blue")
        self.AddPage(win, graphList[2], imageId=2)

        self.SetSelection(0)

        self.Bind(wx.EVT_LISTBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_LISTBOOK_PAGE_CHANGING, self.OnPageChanging)

    def makeColorPanel(self, color):
        p = wx.Panel(self, -1)
        win = ColoredPanel(p, color)
        p.win = win

        def OnCPSize(evt, win=win):
            win.SetPosition((0, 0))
            win.SetSize(evt.GetSize())
        p.Bind(wx.EVT_SIZE, OnCPSize)
        return p

    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print('OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

#----------------------------------------------------------------------
# We'll use instaces of these classes to hold our music data. Items in the
# tree will get associated back to the coresponding Song or Genre object.


class Iteration(object):
    def __init__(self, id_, label, result_file):
        self.id = id_
        self.label = label
        self.result_file = result_file
        self.check = False

    def __repr__(self):
        return 'Iteration %s-%s' % (self.label, self.result_file)


class ResultFile(object):
    def __init__(self, name):
        self.name = name
        self.iterations = []

    def __repr__(self):
        return 'ResultFile: ' + self.name

#----------------------------------------------------------------------

# This model acts as a bridge between the DataViewCtrl and the music data, and
# organizes it hierarchically as a collection of Genres, each of which is a
# collection of songs. We derive the class from PyDataViewCtrl, which knows
# how to reflect the C++ virtual methods to the Python methods in the derived
# class.

# This model provides these data columns:
#
#     0. File :  string
#     1. Iteration:  string
#     2. Select:   bool
#


class MyTreeListModel(dv.PyDataViewModel):
    def __init__(self, data):
        dv.PyDataViewModel.__init__(self)
        self.data = data

        # The objmapper is an instance of DataViewItemObjectMapper and is used
        # to help associate Python objects with DataViewItem objects. Normally
        # a dictionary is used so any Python object can be used as data nodes.
        # If the data nodes are weak-referencable then the objmapper can use a
        # WeakValueDictionary instead. Each PyDataViewModel automagically has
        # an instance of DataViewItemObjectMapper preassigned. This
        # self.objmapper is used by the self.ObjectToItem and
        # self.ItemToObject methods used below.
        self.objmapper.UseWeakRefs(True)

    # Report how many columns this model provides data for.
    def GetColumnCount(self):
        return 3

    # Map the data column numbers to the data type
    def GetColumnType(self, col):
        mapper = {0: 'string',
                   1: 'string',
                   2: 'bool'
                   }
        return mapper[col]

    def GetChildren(self, parent, children):
        # The view calls this method to find the children of any node in the
        # control. There is an implicit hidden root node, and the top level
        # item(s) should be reported as children of this node. A List view
        # simply provides all items as children of this hidden root. A Tree
        # view adds additional items as children of the other items, as needed,
        # to provide the tree hierachy.
        ##self.log.write("GetChildren\n")

        # If the parent item is invalid then it represents the hidden root
        # item, so we'll use the genre objects as its children and they will
        # end up being the collection of visible roots in our tree.
        if not parent:
            for genre in self.data:
                children.append(self.ObjectToItem(genre))
            return len(self.data)

        # Otherwise we'll fetch the python object associated with the parent
        # item and make DV items for each of it's child objects.
        node = self.ItemToObject(parent)
        if isinstance(node, ResultFile):
            for itr in node.iterations:
                children.append(self.ObjectToItem(itr))
            return len(node.iterations)
        return 0

    def IsContainer(self, item):
        # Return True if the item has children, False otherwise.
        ##self.log.write("IsContainer\n")

        # The hidden root is a container
        if not item:
            return True
        # and in this model the genre objects are containers
        node = self.ItemToObject(item)
        if isinstance(node, ResultFile):
            return True
        # but everything else (the song objects) are not
        return False

    #def HasContainerColumns(self, item):
    #    self.log.write('HasContainerColumns\n')
    #    return True

    def GetParent(self, item):
        # Return the item which is this item's parent.
        ##self.log.write("GetParent\n")

        if not item:
            return dv.NullDataViewItem

        node = self.ItemToObject(item)
        if isinstance(node, ResultFile):
            return dv.NullDataViewItem
        elif isinstance(node, Iteration):
            for rf in self.data:
                if rf.name == node.result_file:
                    return self.ObjectToItem(rf)

    def GetValue(self, item, col):
        # Return the value to be displayed for this item and column. For this
        # example we'll just pull the values from the data objects we
        # associated with the items in GetChildren.

        # Fetch the data object for this item.
        node = self.ItemToObject(item)

        if isinstance(node, ResultFile):
            # We'll only use the first column for the Genre objects,
            # for the other columns lets just return empty values
            mapper = {0: node.name,
                       1: "",
                       2: False      # some way to indicate a null value...
                       }
            return mapper[col]

        elif isinstance(node, Iteration):
            mapper = {0: "",
                       1: node.label,
                       2: node.check}
            return mapper[col]

        else:
            raise RuntimeError("unknown node type")

    def GetAttr(self, item, col, attr):
        ##self.log.write('GetAttr')
        node = self.ItemToObject(item)
        if isinstance(node, ResultFile):
            attr.SetColour('blue')
            attr.SetBold(True)
            return True
        return False

    def SetValue(self, value, item, col):
        print("SetValue: %s\n" % value)
        node = self.ItemToObject(item)
        if isinstance(node, Iteration):
            if col == 2:
                node.check = value
#----------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, data=None, model=None):
        wx.Panel.__init__(self, parent, -1)

        filedatas = data.items()
        filedatas.sort()

        # our data structure will be a collection of Genres, each of which is a
        # collection of Songs
        data = dict()
        for key, val in filedatas:
            itr = Iteration(str(key), val[0], val[1])
            result_file = data.get(itr.result_file)
            if result_file is None:
                result_file = ResultFile(itr.result_file)
                data[itr.result_file] = result_file
            result_file.iterations.append(itr)
        data = data.values()

        # Create a dataview control
        self.dvc = dv.DataViewCtrl(self, style=wx.BORDER_THEME
                    | dv.DV_ROW_LINES | dv.DV_VERT_RULES | dv.DV_MULTIPLE)
        # Create an instance of our model...
        if model is None:
            self.model = MyTreeListModel(data)
        else:
            self.model = model

        self.data = data

        # Tel the DVC to use the model
        self.dvc.AssociateModel(self.model)

        # Define the columns that we want in the view.  Notice the
        # parameter which tells the view which col in the data model to pull
        # values from for each view column.
        if 1:
            self.tr = tr = dv.DataViewTextRenderer()
            c0 = dv.DataViewColumn("File",   # title
                                   tr,        # renderer
                                   0,         # data model column
                                   width=500)
            self.dvc.AppendColumn(c0)
        else:
            self.dvc.AppendTextColumn("File",   0, width=500)

        c1 = self.dvc.AppendTextColumn("Iteration",   1, width=120)
        c1.Alignment = wx.ALIGN_CENTRE

        self.dvc.AppendToggleColumn("Select",   2, width=20,
                                    mode=dv.DATAVIEW_CELL_ACTIVATABLE)

        # Set some additional attributes for all the columns
        for c in self.dvc.Columns:
            c.Sortable = True
            c.Reorderable = True

        self.dvc.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED,
                      self.OnSelectionChange)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.dvc, 1, wx.EXPAND)

    def OnSelectionChange(self, e):
        page_wizard = self.GetParent()
        forward_btn = page_wizard.GetParent().FindWindowById(wx.ID_FORWARD)
        if forward_btn:
            if self.isSomeSelection():
                forward_btn.Enable(True)
            else:
                forward_btn.Disable()

    def isSomeSelection(self):
        for result in self.data:
            for itr in result.iterations:
                if itr.check:
                    return True
        return False
