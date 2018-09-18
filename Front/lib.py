class LEDObject():
    """Koreisai StageBack LED-Logo Object
    """
    now_status = 'off' #ON or OFF
    now_pattern = None #animation pattern
    def on(self):
        """turn all LED ON"""
        pass

    def off(self):
        """"turn all LED OFF"""
        pass

    def color(self, hex: str, *position: int):
        """set LED color with hex
        default: ALL LEDs color turns hex value
        if you set potition, only a LED in the position turns hex value"""
        pass

    def animation(self, pattern: str):
        """set animation
        Return:
            1 or -1 (Success or Failure)
        """
        pass

    
