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

def asNumber(v):
    try:
        vInt = int(v)
        vFloat = float(v)
        if vInt == vFloat:
            v = vInt
        else:
            v = vFloat
    except ValueError:
        pass
    return v

class IdmlNode:
    def __init__(self, fileName=None, name=None, nsmap=None, prefix=None, 
            text=None, tail=None, attributes=None, **kwargs):
        if name is None:
            name = self.__class__.__name__
        self.fileName = fileName
        self.name = name
        self.nsmap = nsmap
        self.prefix = prefix
        self.elements = []
        self.text = text
        self.tail = tail
        self.attrs = {}
        if attributes is None:
            attributes = {}
        for attrName, value in attributes:
            if value == 'true':
                value = True
            elif value == 'false':
                value = False
            else:
                value = asNumber(value)
            self.attrs[attrName] = value

    def __getitem__(self, index):
        return self.elements[index]

    def __repr__(self):
        return '<%s>' % self.name

    def writeXml(self, f, tab=0):
        s = '%s<' % (tab*'\t')
        if self.prefix:
            s += self.prefix + ':'
        s += self.name
        if tab == 0 and self.nsmap:
            for nsKey, nsValue in self.nsmap.items():
                if nsKey is None:
                    s += ' xmlns="%s"' % nsValue
                else:
                    s += ' xmlns:%s="%s"' % (nsKey, nsValue)
        for attrName, value in self.attrs.items():
            if isinstance(value, bool):
                value = {True:'true',False:'false'}[value]
            elif isinstance(value, str):
                value = value.replace('&','&amp;') # Order matters
                value = value.replace('"','&quot;')  
                value = value.replace('<','&lt;')  
                value = value.replace('>','&gt;')  
            s += ' %s="%s"' % (attrName, value)
        if self.text or self.elements:
            s += '>'
            f.write(s)
            if self.text is not None:
                f.write(self.text.strip())
            for e in self.elements:
                e.writeXml(f, tab+1)
            if self.elements:
                s = tab*'\t'
            else:
                s = ''
            s += '</'
            if self.prefix:
                s += self.prefix + ':'
            s += '%s>' % self.name
            f.write(s)
        else:
            s += '/>'
            f.write(s)
        if self.tail is not None:
            f.write(self.tail) 

class Page(IdmlNode):
    def __init__(self, **kwargs):
        #print(fileName, name)
        IdmlNode.__init__(self,  **kwargs)

NODE_CLASSES = {
    # Expanding set of IdmlNode classes, that know more about their
    # content so the can generate, manipulate and validate. 
    'IdmlNode': IdmlNode,
    'Page': Page,
}

