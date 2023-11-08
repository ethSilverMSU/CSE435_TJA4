"""
TJA Frame for displaying the prototype

Running Python 3.9

pip install -U wxPython
"""

import wx

class MainFrame(wx.Frame):
    """
    Main frame
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the frame
        :param args:
        :param kwargs:
        """
        super(MainFrame, self).__init__(*args, **kwargs)

        panel = wx.Panel(self)

        self.GamePanel = MainPanel(panel)

        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.MainSizer.Add(self.GamePanel, 1, wx.EXPAND)

        panel.SetSizerAndFit(self.MainSizer)

        self.Show()
        self.MainSizer.Fit(self)
        self.Maximize(True)
        self.Center()

    def MenuBar(self):
        MenuBar = wx.MenuBar

        FileMenu = wx.Menu()

        Close = FileMenu.Append(wx.ID_ANY, "Close")



        MenuBar.Append(FileMenu, "&File")

        self.Bind(wx.EVT_MENU, self.OnClose, Close)


    def OnClose(self, event):
        self.Close()


class MainPanel(wx.Panel):
    """
    Main panel where everything is done
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        wid, hei = wx.DisplaySize()
        self.SetBackgroundColour((100,100,100))

        self.GameLayout()

    def GameLayout(self):
        self.FullPage = wx.BoxSizer(wx.VERTICAL)

        # sizer for top area where car display will be
        self.TopArea = wx.BoxSizer(wx.HORIZONTAL)

        # sizer for mid area with statistics
        self.MidArea = wx.BoxSizer(wx.HORIZONTAL)

        # sizer for bottom area with buttons
        self.ButtonArea = wx.BoxSizer(wx.HORIZONTAL)

        # initialize the cars
        redcar = wx.Image("resources/download.png", wx.BITMAP_TYPE_ANY)
        pinkcar = wx.Image("resources/pink.png", wx.BITMAP_TYPE_ANY)

        self.RedCarDisplay = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(redcar))
        self.PinkCarDisplay = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(pinkcar))


        # Add the car images to the top sizer
        self.TopArea.Add(self.RedCarDisplay, 1, wx.ALL | wx.CENTER, 20)
        self.TopArea.Add(self.PinkCarDisplay, 1, wx.ALL | wx.CENTER, 20)

        self.Stats()
        self.Bottom()


        # Add top middle, and bottom sizers to full page
        self.FullPage.Add(self.TopArea, 1, wx.CENTER | wx.EXPAND)
        self.FullPage.Add(self.MidArea, 1, wx.CENTER | wx.EXPAND)
        self.FullPage.Add(self.ButtonArea, 1, wx.CENTER| wx.EXPAND)

        self.SetSizer(self.FullPage)


    def Stats(self):
        """
        Initializes the info in the middle sizer
        :return:
        """

        MainFont = wx.Font(pointSize=20, family=wx.FONTFAMILY_ROMAN, style=wx.RAISED_BORDER, weight=90)

        # Text variables - changed using SetLabel
        self.YourSpeed = wx.StaticText(self, label="Your speed is: ")
        self.CarSpeed = wx.StaticText(self, label="Tracking car's speed is: ")
        self.YourSpeed.SetFont(MainFont)
        self.CarSpeed.SetFont(MainFont)

        self.MidArea.Add(self.YourSpeed, 1, wx.ALL | wx.CENTER, 30)
        self.MidArea.Add(self.CarSpeed, 1, wx.ALL | wx.CENTER, 30)


    def Bottom(self):

        self.DecreaseSpeed = wx.Button(self, label="Decrease speed 5pmh", size=(200,50))
        self.DecreaseSpeed.Bind(wx.EVT_BUTTON, self.OnDecreaseSpeed)
        self.ButtonArea.Add(self.DecreaseSpeed, 0, wx.ALL | wx.CENTER, 20)


    def OnDecreaseSpeed(self, event):
        print("Button Pressed")



if __name__ == '__main__':

    app = wx.App()
    frm = MainFrame(None, title='TJA')
    frm.Show()
    app.MainLoop()
