'''
Created on 18/07/2014

@author: aferreira
'''
import wx
import os


class I18nLocale(wx.Locale):
    def __init__(self):
        super(I18nLocale, self).__init__(language=wx.LANGUAGE_DEFAULT)

        self.MakeMO(os.getcwd(), applicationDomain="tava")
        self.AddCatalogLookupPathPrefix('./locale/es_PY/')
        self.AddCatalog('tava_es_PY')

    def SetCatalog(self, catalog):
        self.AddCatalog(catalog)

    def MakeMO(self, applicationDirectoryPath, targetDir='./locale',
               applicationDomain=None, verbose=0, forceEnglish=0):
        '''
        MakeMO converts all translated language-specific PO files located
        inside the  application directory into the binary .MO files stored
        inside the LC_MESSAGES sub-directory for the found locale files.

        MakeMO searches for all files that have a name of the form 'app_xx.po'
        inside the application directory specified by the first argument. The
        'app' is the application domain name (that can be specified by the
        applicationDomain argument or is taken from the directory name). The
        'xx' corresponds to one of the ISO 639 two-letter language codes.

        MakeMo stores the resulting files inside a sub-directory of `targetDir`
        called xx/LC_MESSAGES where 'xx' corresponds to the 2-letter language
        code.

        :param applicationDirectoryPath:
        :param targetDir:
        :param applicationDomain:
        :param verbose:
        :param forceEnglish:
        '''

        if targetDir is None:
            targetDir = './locale'
        if verbose:
            print "Target directory for .mo files is: %s" % targetDir

        if applicationDomain is None:
            applicationName = self.fileBaseOf(applicationDirectoryPath,
                                              withPath=0)
        else:
            applicationName = applicationDomain
        currentDir = os.getcwd()
        os.chdir(applicationDirectoryPath)

        languageDict = self.getlanguageDict()

        for langCode in languageDict.keys():
            if langCode == "es_PY":
                pass
            mo_targetDir = "%s/%s" % (targetDir, langCode)
            langPOfileName = mo_targetDir + "/%s_%s.po" % (
                                            applicationName, langCode)
            if os.path.exists(langPOfileName):
                if not os.path.exists(mo_targetDir):
                    self.mkdir(mo_targetDir)
                cmd = 'msgfmt --output-file="%s/%s_%s.mo" "%s/%s_%s.po"' % (
                mo_targetDir, applicationName, langCode, mo_targetDir,
                applicationName, langCode)
                if verbose:
                    print cmd
                os.system(cmd)
        os.chdir(currentDir)

    def fileBaseOf(self, filename, withPath=0):
        """fileBaseOf(filename,withPath) ---> string

        Return base name of filename.  The returned string never includes the
        extension. Use os.path.basename() to return the basename with the
        extension.  The second argument is optional.  If specified and if set
        to 'true' (non zero) the string returned contains the full path of the
        file name.  Otherwise the path is excluded.

        [Example]
        >>> fn = 'd:/dev/telepath/tvapp/code/test.html'
        >>> fileBaseOf(fn)
        'test'
        >>> fileBaseOf(fn)
        'test'
        >>> fileBaseOf(fn,1)
        'd:/dev/telepath/tvapp/code/test'
        >>> fileBaseOf(fn,0)
        'test'
        >>> fn = 'abcdef'
        >>> fileBaseOf(fn)
        'abcdef'
        >>> fileBaseOf(fn,1)
        'abcdef'
        >>> fn = "abcdef."
        >>> fileBaseOf(fn)
        'abcdef'
        >>> fileBaseOf(fn,1)
        'abcdef'
        """
        pos = filename.rfind('.')
        if pos > 0:
            filename = filename[:pos]
        if withPath:
            return filename
        else:
            return os.path.basename(filename)

    def mkdir(self, directory):
        """Create a directory (and possibly the entire tree).

        The os.mkdir() will fail to create a directory if one of the
        directory in the specified path does not exist.  mkdir()
        solves this problem.  It creates every intermediate directory
        required to create the final path. Under Unix, the function
        only supports forward slash separator, but under Windows and MacOS
        the function supports the forward slash and the OS separator (backslash
        under windows).
        """

        # translate the path separators
        directory = self.unixpath(directory)
        # build a list of all directory elements
        aList = filter(lambda x: len(x) > 0, directory.split('/'))
        theLen = len(aList)
        # if the first element is a Windows-style disk drive
        # concatenate it with the first directory
        if aList[0].endswith(':'):
            if theLen > 1:
                aList[1] = aList[0] + '/' + aList[1]
                del aList[0]
                theLen -= 1
        # if the original directory starts at root,
        # make sure the first element of the list
        # starts at root too
        if directory[0] == '/':
            aList[0] = '/' + aList[0]
        # Now iterate through the list, check if the
        # directory exists and if not create it
        theDir = ''
        for i in range(theLen):
            theDir += aList[i]
            if not os.path.exists(theDir):
                os.mkdir(theDir)
            theDir += '/'

    def unixpath(self, thePath):
        """Return a path name that contains Unix separator.
        [Example]
        >>> unixpath(r"d:\test")
        'd:/test'
        >>> unixpath("d:/test/file.txt")
        'd:/test/file.txt'
        >>>
        """
        thePath = os.path.normpath(thePath)
        if os.sep == '/':
            return thePath
        else:
            return thePath.replace(os.sep, '/')

    def getlanguageDict(self):
        languageDict = {}

        for lang in [x for x in dir(wx) if x.startswith("LANGUAGE")]:
            i = wx.Locale(wx.LANGUAGE_DEFAULT).GetLanguageInfo(getattr(wx,
                                                                       lang))
            if i:
                languageDict[i.CanonicalName] = i.Description

        return languageDict
