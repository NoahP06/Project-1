from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QPixmap
from gui import Ui_MainWindow
from PyQt6.QtCore import QTimer

class Television:
    """
    Simulates basic elements of a television
    """
    MIN_VOLUME = 0
    MAX_VOLUME = 2
    MIN_CHANNEL = 0
    MAX_CHANNEL = 3

    def __init__(self) -> None: 
        """
        Initializes the television
        """
        self.__status = False
        self.__muted = False
        self.__volume = self.MIN_VOLUME
        self.__channel = self.MIN_CHANNEL

    def power(self) -> None:
        """
        Toggles the power status
        """
        self.__status = not self.__status

    def mute(self) -> None:
        """
        Toggles the mute status if television is on
        """
        if self.__status:
            self.__muted = not self.__muted

    def channel_up(self) -> None:
        """
        Increases the channel number, going back to if at max
        """
        if self.__status:
            self.__channel = (self.__channel + 1) % (self.MAX_CHANNEL + 1)

    def channel_down(self) -> None:
        """
        Decrease the channel number, going to max if at 0
        """
        if self.__status:
            self.__channel = (self.__channel - 1) % (self.MAX_CHANNEL + 1)

    def volume_up(self) -> None:
        """
        Increases the volume if the television is on, and not at MAX_VOLUME or muted 
        """
        if self.__status and not self.__muted and self.__volume < self.MAX_VOLUME:
            self.__volume += 1

    def volume_down(self) -> None:
        """
        Decreases the volume if the television is on, and not at MIN_VOLUME or muted
        """
        if self.__status and not self.__muted and self.__volume > self.MIN_VOLUME:
            self.__volume -= 1

    def get_channel(self) -> int:
        """
        Returns current channel number
        """
        return self.__channel

    def get_volume(self) -> int:
        """
        Returns the volume, 0 if muted
        """
        return 0 if self.__muted else self.__volume

    def is_on(self) -> bool:
        """
        Returns True if the television is on
        """
        return self.__status

    def is_muted(self) -> bool:
        """
        Returns True if the television is muted
        """
        return self.__muted


class MainTVApp(QMainWindow):
    """
    Controls the television using PYQT6,
    Handles all of the logic for the display 
    """
    def __init__(self) -> None:
        """
        Initializes the GUI window
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.ChannelNumber.hide()
        self.ui.VolumeContainer.hide()
        self.tv = Television()

        self.ui.ChannelUp.clicked.connect(self.channel_up)     # ↑
        self.ui.ChannelDown.clicked.connect(self.channel_down) # ↓
        self.ui.VolUp.clicked.connect(self.volume_up)    # +
        self.ui.VolDown.clicked.connect(self.volume_down)  # -
        self.ui.MuteButton.clicked.connect(self.mute_toggle)  # 🔇
        self.ui.PowerButton.clicked.connect(self.power_toggle) # ⏻
        
        try:
            self.__PowerOff_screen = QPixmap('poweroff.jpg')
            self.__Channel_imgs = [
                QPixmap('channel0.jpg'),
                QPixmap('channel1.jpg'),
                QPixmap('channel2.jpg'),
                QPixmap('channel3.jpg'),
            ]
        except Exception:
            return Exception
        
        self.update_display()
    

    def update_display(self) -> None:
        """
        Updates television image and channel number
        """
        if not self.tv.is_on():
            self.ui.TvDisplay.setPixmap(self.__PowerOff_screen)
            self.ui.VolumeBar.setValue(0)
            return

        channel = self.tv.get_channel()
        self.ui.TvDisplay.setPixmap(self.__Channel_imgs[channel])
        self.ui.TvDisplay.setScaledContents(True)
        self.ui.ChannelNumber.display(channel)

        try:
            pixmap = QPixmap(f'channel{channel}.jpg')
            if not pixmap.isNull():
                self.ui.TvDisplay.setPixmap(pixmap.scaled(self.ui.TvDisplay.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.update_volume_bar()
        except Exception:
            return Exception

    def channel_up(self) -> None:
        """
        Increases the channel by 1, shows the channel number for 2 sec after
        """
        if not self.tv.is_on():
            return
        self.tv.channel_up()
        self.update_display()
        self.ui.ChannelNumber.show()
        QTimer.singleShot(2000, self.ui.ChannelNumber.hide)

    def channel_down(self) -> None:
        """
        Decreases the channel by 1, shows the channel number for 2 sec after
        """
        if not self.tv.is_on():
            return
        self.tv.channel_down()
        self.update_display()
        self.ui.ChannelNumber.show()
        QTimer.singleShot(2000, self.ui.ChannelNumber.hide)

    def volume_up(self) -> None:
        """
        Increases the volume by 1, shows the volume bar for 2 sec after
        """
        if not self.tv.is_on():
            return
        self.tv.volume_up()
        self.update_volume_bar()
        self.ui.VolumeContainer.show()
        QTimer.singleShot(2000, self.ui.VolumeContainer.hide)

    def volume_down(self) -> None:
        """
        Decreases the volume by 1, shows the volume bar for 2 sec after
        """
        if not self.tv.is_on():
            return
        self.tv.volume_down()
        self.update_volume_bar()
        self.ui.VolumeContainer.show()
        QTimer.singleShot(2000, self.ui.VolumeContainer.hide)
        

    def mute_toggle(self) -> None:
        """
        Toggles mute and changes the volum icon if the television is on
        """
        if not self.tv.is_on():
            return
        self.tv.mute()
        self.update_volume_bar()
        self.ui.VolumeContainer.show()
        QTimer.singleShot(2000, self.ui.VolumeContainer.hide)


    def power_toggle(self) -> None:
        """
        Toggles the power, and updates the display
        """
        self.tv.power()
        self.update_display()

    def update_volume_bar(self) -> None:
        """
        Updates the volume bar, volume number, and the volume icon
        """
        if self.tv.is_on():
            volume = self.tv.get_volume()
            self.ui.VolumeBar.setValue(volume)
            self.ui.VolumeNumber.display(volume)
            self.ui.VolumeIcon.setText('🔇' if self.tv.is_muted() else '🔊')
        else:
            self.ui.VolumeBar.setValue(0)
            self.ui.VolumeNumber.display(0)
            self.ui.VolumeIcon.setText('🔇')