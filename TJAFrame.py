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
        self.MainFont = wx.Font(pointSize=20, family=wx.FONTFAMILY_ROMAN, style=wx.RAISED_BORDER, weight=90)

        self.MyCarSpeed = 25
        self.TargetCarSpeed = 20
        self.TargetDistance = 25
        self.ClosingRate = 0
        self.TJAIsActive = False

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

        self.DistanceText = wx.StaticText(self, label="Distance: {}".format(self.TargetDistance))
        self.DistanceText.SetFont(self.MainFont)


        # Add the car images to the top sizer
        self.TopArea.Add(self.RedCarDisplay, 1, wx.ALL | wx.CENTER, 20)
        self.TopArea.Add(self.DistanceText, 0, wx.ALL | wx.CENTER, 20)
        self.TopArea.Add(self.PinkCarDisplay, 1, wx.ALL | wx.CENTER, 20)

        # Initialize stats and button
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

        # Text variables - changed using SetLabel
        self.YourSpeed = wx.StaticText(self, label="Your speed is: {}".format(self.MyCarSpeed))
        self.CarSpeed = wx.StaticText(self, label="Tracking car's speed is: {}".format(self.TargetCarSpeed))
        self.ClosingRateText = wx.StaticText(self, label="The closing rate is: {}".format(self.ClosingRate))

        self.YourSpeed.SetFont(self.MainFont)
        self.ClosingRateText.SetFont(self.MainFont)
        self.CarSpeed.SetFont(self.MainFont)

        self.MidArea.Add(self.YourSpeed, 1, wx.ALL | wx.CENTER, 30)
        self.MidArea.Add(self.ClosingRateText, 1, wx.ALL | wx.CENTER, 30)
        self.MidArea.Add(self.CarSpeed, 1, wx.ALL | wx.CENTER, 30)

    def Bottom(self):

        self.DecreaseMySpeed = wx.Button(self, label="Decrease my speed 1pmh", size=(200,50))
        self.DecreaseMySpeed.Bind(wx.EVT_BUTTON, self.OnDecreaseMySpeed)
        self.ButtonArea.Add(self.DecreaseMySpeed, 1, wx.ALL | wx.CENTER, 20)

        self.DecreaseTargetSpeed = wx.Button(self, label="Decrease target speed 1mph", size=(200,50))
        self.DecreaseTargetSpeed.Bind(wx.EVT_BUTTON, self.OnDecreaseTargetSpeed)
        self.ButtonArea.Add(self.DecreaseTargetSpeed, 1, wx.ALL | wx.CENTER, 20)

        self.IncreaseMySpeed = wx.Button(self, label="Increase my speed 1mph", size=(200,50))
        self.IncreaseMySpeed.Bind(wx.EVT_BUTTON, self.OnIncreaseMySpeed)
        self.ButtonArea.Add(self.IncreaseMySpeed, 1, wx.ALL | wx.CENTER, 20)

        self.IncreaseTargetSpeed = wx.Button(self, label="Increase my speed 1mph", size=(200, 50))
        self.IncreaseTargetSpeed.Bind(wx.EVT_BUTTON, self.OnIncreaseTargetSpeed)
        self.ButtonArea.Add(self.IncreaseTargetSpeed, 1, wx.ALL | wx.CENTER, 20)


    def OnDecreaseMySpeed(self, event):
        self.UpdateMyText(-1)

    def OnDecreaseTargetSpeed(self, event):
        self.UpdateTargetText(-1)

    def OnIncreaseMySpeed(self, event):
        self.UpdateMyText(1)

    def OnIncreaseTargetSpeed(self, event):
        self.UpdateTargetText(1)

    def UpdateMyText(self, value):
        self.MyCarSpeed += value
        self.YourSpeed.SetLabel("Your speed is: {}".format(self.MyCarSpeed))

    def UpdateTargetText(self, value):
        self.TargetCarSpeed += value
        self.CarSpeed.SetLabel("Tracking car's speed is: {}".format(self.TargetCarSpeed))

    def TJAStatusSwitch(self):
        self.TJAIsActive = not self.TJAIsActive
        print(self.TJAIsActive)

    def CalculateDistance(self):
        self.TargetDistance = self.TargetCarSpeed - self.CarSpeed

if __name__ == '__main__':

    app = wx.App()
    frm = MainFrame(None, title='TJA')
    frm.Show()
    app.MainLoop()
