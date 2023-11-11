"""
TJA Frame for displaying the prototype

Running Python 3.9

pip install -U wxPython
"""

import wx

import time

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

        self.MenuBarNew()

        panel.SetSizerAndFit(self.MainSizer)

        self.Show()
        self.MainSizer.Fit(self)
        self.Maximize(True)
        self.Center()

    def MenuBarNew(self):
        mMenuBar = wx.MenuBar()

        mFile = wx.Menu()
        mQuit = mFile.Append(wx.ID_EXIT, "&Quit")

        mChange = wx.Menu()
        mChange25 = mChange.Append(wx.ID_ANY, "Goal of 25")
        mChange50 = mChange.Append(wx.ID_ANY, "Goal of 50")
        mChange75 = mChange.Append(wx.ID_ANY, "Goal of 75")

        mDevs = wx.Menu()
        mShowDevs = mDevs.Append(wx.ID_ANY, "Show Developers")
        mShowClient = mDevs.Append(wx.ID_ANY, "Client Information")


        mMenuBar.Append(mFile, '&File')
        mMenuBar.Append(mChange, '&Change Distance Goal')
        mMenuBar.Append(mDevs, "&Developers")

        self.Bind(wx.EVT_MENU, self.OnChange25, mChange25)
        self.Bind(wx.EVT_MENU, self.OnChange50, mChange50)
        self.Bind(wx.EVT_MENU, self.OnChange75, mChange75)
        self.Bind(wx.EVT_MENU, self.OnDevs, mShowDevs)
        self.Bind(wx.EVT_MENU, self.OnClient, mShowClient)
        self.Bind(wx.EVT_MENU, self.OnClose, mQuit)

        self.SetMenuBar(mMenuBar)
        self.SetSize((350, 250))
        self.Centre()
        self.Show(True)

    def OnChange25(self, event):
        self.GamePanel.OnAdjustDistanceGoal(25)

    def OnChange50(self, event):
        self.GamePanel.OnAdjustDistanceGoal(50)

    def OnChange75(self, event):
        self.GamePanel.OnAdjustDistanceGoal(75)

    def OnDevs(self, event):
        wx.MessageBox("TJA Developers:\n\nProject Manager: Ryan Le"
                      "\nFacilitator: Ethan Silver\nWeb Manager: Bryce Cooperkawa"
                      "\nCustomer Liaison: Matt Zaleski\nAssurance Manager: Alvin Hoang", "Developers")

    def OnClient(self, event):
        wx.MessageBox("Client:\n\nMr. William Milam"
                      "\n \n Wmilam Consulting, LLC", "Client")

    def OnClose(self, event):
        self.Close()


class MainPanel(wx.Panel):
    """
    Main panel where everything is done
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        wid, hei = wx.DisplaySize()
        self.SetBackgroundColour((128,128,128))
        self.MainFont = wx.Font(pointSize=20, family=wx.FONTFAMILY_ROMAN, style=wx.RAISED_BORDER, weight=90)
        self.MainFont.MakeBold()
        self.OffColor = wx.Colour(255,0,0)
        self.OnColor = wx.Colour(0,255,0)


        self.MyCarSpeed = 25
        self.TargetCarSpeed = 20
        self.TargetDistance = 200
        self.ClosingRate = self.MyCarSpeed - self.TargetCarSpeed
        self.CurrentTime = 0
        self.TJAIsActive = False
        self.isStarted = False
        self.DistanceGoal = 25

        self.GameLayout()

    def GameLayout(self):
        self.FullPage = wx.BoxSizer(wx.VERTICAL)

        self.StartButtonSizer = wx.BoxSizer(wx.HORIZONTAL)

        # sizer for top area where car display will be
        self.TopArea = wx.BoxSizer(wx.HORIZONTAL)

        # sizer for mid area with statistics
        self.MidArea = wx.BoxSizer(wx.HORIZONTAL)

        # sizer for bottom area with buttons
        self.ButtonArea = wx.BoxSizer(wx.HORIZONTAL)

        # initialize the cars
        redcar = wx.Image("resources/download.png", wx.BITMAP_TYPE_ANY)
        pinkcar = wx.Image("resources/pink.png", wx.BITMAP_TYPE_ANY)


        self.RedCarDisplay = wx.StaticBitmap(self, wx.ID_ANY, redcar.ConvertToBitmap())
        self.PinkCarDisplay = wx.StaticBitmap(self, wx.ID_ANY, pinkcar.ConvertToBitmap())

        self.DistanceText = wx.StaticText(self, label="Distance: {}".format(self.TargetDistance))
        self.DistanceText.SetFont(self.MainFont)


        # Add the car images to the top sizer
        self.TopArea.Add(self.RedCarDisplay, 1, wx.ALL | wx.CENTER, 20)
        self.TopArea.Add(self.DistanceText, 0, wx.ALL | wx.CENTER, 20)
        self.TopArea.Add(self.PinkCarDisplay, 1, wx.ALL | wx.CENTER, 20)

        # Initialize stats and button
        self.Stats()
        self.Bottom()
        self.UpdateLabels()
        self.InitStartButton()

        # Add top middle, and bottom sizers to full page
        self.FullPage.Add(self.StartButtonSizer, 1, wx.CENTER | wx.EXPAND)
        self.FullPage.Add(self.TopArea, 2, wx.CENTER | wx.EXPAND)
        self.FullPage.Add(self.MidArea, 2, wx.CENTER | wx.EXPAND)
        self.FullPage.Add(self.ButtonArea, 2, wx.CENTER| wx.EXPAND)

        self.SetSizer(self.FullPage)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer, self.timer)


    def InitStartButton(self):
        self.DistanceVariableText = wx.StaticText(self, label="Input distance:")
        self.DistanceVariableText.SetFont(self.MainFont)
        self.StartButtonSizer.Add(self.DistanceVariableText, 0, wx.ALL | wx.CENTER, 5)

        self.SetDistanceVariable = wx.TextCtrl(self, value="200", style = wx.TE_PROCESS_ENTER)
        self.StartButtonSizer.Add(self.SetDistanceVariable, 0, wx.ALL | wx.CENTER, 5)
        self.SetDistanceVariable.Bind(wx.EVT_TEXT_ENTER, self.OnChangeDistance)

        self.StartButton = wx.Button(self, label="START SIMULATION", size=(100,50))
        self.StartButton.SetFont(self.MainFont)
        self.StartButtonSizer.Add(self.StartButton, 1, wx.ALL | wx.CENTER, 5)
        self.StartButton.Bind(wx.EVT_BUTTON, self.OnStart)

        self.MergeButton = wx.Button(self, label="ADD MERGING CAR", size=(100,50))
        self.MergeButton.SetFont(self.MainFont)
        self.StartButtonSizer.Add(self.MergeButton, 1, wx.ALL | wx.CENTER, 5)
        self.MergeButton.Bind(wx.EVT_BUTTON, self.OnMerge)


    def OnStart(self, event):
        self.isStarted = not self.isStarted

        if self.isStarted == True:
            self.StartButton.SetLabel("STOP SIMULATION")
            self.timer.Start(1000)
        else:
            self.StartButton.SetLabel("START SIMULATION")
            self.timer.Stop()

            # Reset everything
            self.MyCarSpeed = 25
            self.TargetCarSpeed = 20
            self.TargetDistance = int(self.SetDistanceVariable.GetValue())
            self.ClosingRate = self.MyCarSpeed - self.TargetCarSpeed
            self.CurrentTime = 0
            self.isStarted = False
            self.DistanceGoal = 25
            self.SetTJAStatus(False)
            self.UpdateLabels()
            self.UpdateMyText(0)
            self.UpdateDistanceText()


    def Stats(self):
        """
        Initializes the info in the middle sizer
        :return:
        """

        # Text variables - changed using SetLabel
        self.YourSpeed = wx.StaticText(self, label="Your speed is: {}mph".format(self.MyCarSpeed))
        self.CarSpeed = wx.StaticText(self, label="Tracking car's speed is: {}mph".format(self.TargetCarSpeed))
        self.ClosingRateText = wx.StaticText(self, label="The closing rate is: {}mph".format(self.ClosingRate))
        self.TimeText = wx.StaticText(self, label="The current time is: {}s".format(self.CurrentTime))

        # Set our font to text
        self.YourSpeed.SetFont(self.MainFont)
        self.ClosingRateText.SetFont(self.MainFont)
        self.CarSpeed.SetFont(self.MainFont)
        self.TimeText.SetFont(self.MainFont)

        # Add the activate TJA button
        self.ActivateButton = wx.Button(self, label="ACTIVATE TJA", size=(100,50))
        self.ActivateButton.SetFont(self.MainFont)
        self.ActivateButton.Bind(wx.EVT_BUTTON, self.OnActivateTJA)


        # Add text to sizer
        self.MidArea.Add(self.YourSpeed, 1, wx.ALL | wx.CENTER, 30)
        self.MidArea.Add(self.TimeText, 1, wx.ALL | wx.CENTER, 30)
        self.MidArea.Add(self.ActivateButton, 1, wx.ALL | wx.CENTER, 10)
        self.MidArea.Add(self.ClosingRateText, 1, wx.ALL | wx.CENTER, 30)
        self.MidArea.Add(self.CarSpeed, 1, wx.ALL | wx.CENTER, 30)

    def Bottom(self):

        self.IncreaseMySpeed = wx.Button(self, label="Increase my speed 1mph", size=(200, 50))
        self.IncreaseMySpeed.SetFont(self.MainFont)
        self.IncreaseMySpeed.Bind(wx.EVT_BUTTON, self.OnIncreaseMySpeed)
        self.ButtonArea.Add(self.IncreaseMySpeed, 1, wx.ALL | wx.CENTER, 20)

        self.DecreaseMySpeed = wx.Button(self, label="Decrease my speed 1mph", size=(200,50))
        self.DecreaseMySpeed.SetFont(self.MainFont)
        self.DecreaseMySpeed.Bind(wx.EVT_BUTTON, self.OnDecreaseMySpeed)
        self.ButtonArea.Add(self.DecreaseMySpeed, 1, wx.ALL | wx.CENTER, 20)

        self.IncreaseTargetSpeed = wx.Button(self, label="Increase target speed 1mph", size=(200, 50))
        self.IncreaseTargetSpeed.SetFont(self.MainFont)
        self.IncreaseTargetSpeed.Bind(wx.EVT_BUTTON, self.OnIncreaseTargetSpeed)
        self.ButtonArea.Add(self.IncreaseTargetSpeed, 1, wx.ALL | wx.CENTER, 20)

        self.DecreaseTargetSpeed = wx.Button(self, label="Decrease target speed 1mph", size=(200,50))
        self.DecreaseTargetSpeed.SetFont(self.MainFont)
        self.DecreaseTargetSpeed.Bind(wx.EVT_BUTTON, self.OnDecreaseTargetSpeed)
        self.ButtonArea.Add(self.DecreaseTargetSpeed, 1, wx.ALL | wx.CENTER, 20)


    def OnChangeDistance(self, event):
        if not self.isStarted:
            dist = int(self.SetDistanceVariable.GetValue())
            self.TargetDistance = dist
            self.UpdateDistanceText()

    def OnAdjustDistanceGoal(self, value):
        print(value)
        self.DistanceGoal = value


    def OnDecreaseMySpeed(self, event):
        self.UpdateMyText(-1)
        self.SetTJAStatus(False)

    def OnDecreaseTargetSpeed(self, event):
        self.UpdateTargetText(-1)

    def OnIncreaseMySpeed(self, event):
        self.UpdateMyText(1)

    def OnIncreaseTargetSpeed(self, event):
        self.UpdateTargetText(1)

    def OnActivateTJA(self, event):
        if self.TJAIsActive:
            self.SetTJAStatus(False)
        else:
            if self.MyCarSpeed <= 40:
                self.SetTJAStatus(True)

        self.UpdateLabels()

    def UpdateLabels(self):

        if self.TJAIsActive:
            self.YourSpeed.SetForegroundColour(self.OnColor)
            self.CarSpeed.SetForegroundColour(self.OnColor)
            self.ClosingRateText.SetForegroundColour(self.OnColor)
            self.TimeText.SetForegroundColour(self.OnColor)
        else:
            self.YourSpeed.SetForegroundColour(self.OffColor)
            self.CarSpeed.SetForegroundColour(self.OffColor)
            self.ClosingRateText.SetForegroundColour(self.OffColor)
            self.TimeText.SetForegroundColour(self.OffColor)
        self.Refresh()

    def UpdateMyText(self, value):
        self.TimeText.SetLabel("The current time is: {}s".format(self.CurrentTime))
        self.MyCarSpeed += value
        self.YourSpeed.SetLabel("Your speed is: {}mph".format(self.MyCarSpeed))

        if self.MyCarSpeed > 40 or self.MyCarSpeed < 0:
            self.SetTJAStatus(False)
        self.UpdateClosingRateText()

    def UpdateTargetText(self, value):
        self.TargetCarSpeed += value
        self.CarSpeed.SetLabel("Tracking car's speed is: {}mph".format(self.TargetCarSpeed))
        self.UpdateClosingRateText()

    def UpdateClosingRateText(self):
        self.UpdateClosingRate()
        self.ClosingRateText.SetLabel("The closing rate is: {}".format(self.ClosingRate))

    def UpdateDistanceText(self):
        self.DistanceText.SetLabel("Distance: {}".format(self.TargetDistance))

    def UpdateClosingRate(self):
        self.ClosingRate = self.TargetCarSpeed - self.MyCarSpeed

    def SetTJAStatus(self, value):
        self.TJAIsActive = value
        if value:
            self.ActivateButton.SetLabel("DEACTIVATE TJA")
        else:
            self.ActivateButton.SetLabel("ACTIVATE TJA")

        self.UpdateLabels()

    def CalculateDistance(self):
        self.TargetDistance += self.ClosingRate
        self.UpdateDistanceText()

    def IncrementTime(self):
        self.CalculateDistance()

    def onTimer(self, event):
        self.CurrentTime += 1
        self.CalculateDistance()
        self.UpdateMyText(0)
        if self.TJAIsActive:
            if self.TargetDistance > (self.DistanceGoal + self.MyCarSpeed*2) and self.MyCarSpeed < 40:
                self.UpdateMyText(1)
                print("Accelerating option 1", self.TargetDistance)

            elif self.TargetDistance < self.DistanceGoal and self.ClosingRate <= 0:
                self.UpdateMyText(-1)
                print("Slightly Decelerating to increase distance.")

            elif self.TargetDistance > self.DistanceGoal and self.ClosingRate == 0:
                self.UpdateMyText(1)
                print("Slow, get fast")
            elif self.TargetDistance > self.DistanceGoal and self.ClosingRate > 0:
                self.UpdateMyText(1)
                print("Go back")

            elif self.TargetDistance <= (self.DistanceGoal + self.MyCarSpeed*2) and self.ClosingRate != 0:
                # Going too fast! Start slowing down
                if int(self.ClosingRate/2)/2 < -1:
                    # Decelerates by fraction of 4 of closing rate
                    self.UpdateMyText(int(self.ClosingRate/4))
                    print("Decelerating by 4 option 2", self.TargetDistance)
                elif self.TargetDistance > self.DistanceGoal and self.ClosingRate < -1:
                    # Decelerates by 1
                    self.UpdateMyText(-1)
                    print("Decelerating by 1 option 3", self.TargetDistance)
                elif self.TargetDistance <= 10 and self.ClosingRate <= 0:
                    if self.ClosingRate <= -5:
                        self.UpdateMyText(-5)
                    else:
                        self.UpdateMyText(self.ClosingRate)
                    print("Target vehicle too close, engaging brakes.")
                elif self.TargetDistance == self.DistanceGoal and self.ClosingRate == -1:
                    # Target Reached
                    self.UpdateMyText(-1)
                    print("Target Reached", self.TargetDistance)
                elif self.ClosingRate > 0 and self.TargetDistance == self.DistanceGoal:
                    self.UpdateMyText(1)

    def OnMerge(self, event):
        if self.TargetDistance >= 35:
            self.TargetDistance = 25

if __name__ == '__main__':

    app = wx.App()
    frm = MainFrame(None, title='TJA')
    frm.Show()
    app.MainLoop()
