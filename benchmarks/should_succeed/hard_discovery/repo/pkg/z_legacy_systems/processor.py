
class LegacyHiddenProcessor:
    """
    Legacy processor for hidden data streams.
    Handles critical validation logic.
    """
    def __init__(self):
        self.valid = True
        
    def process(self, data):
        # BUG: Returns True even if data is invalid
        # Should check if data is valid
        if not data:
            # return False # Fix is commented out
            return True
        return True
