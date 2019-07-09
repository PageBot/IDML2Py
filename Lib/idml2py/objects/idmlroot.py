# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
# -----------------------------------------------------------------------------
#
#     idmlroot.py
#
# 

class IdmlRoot:
    def __init__(self):
        self.designMap = None
        self.xmlNodes = {}
        self.masterSpreads = []
        self.spreads = []
        self.stories = []
        self.resources = {}
        self.metaInfo = {}

if __name__ == "__main__":
    import sys
    import doctest
    sys.exit(doctest.testmod()[0])

