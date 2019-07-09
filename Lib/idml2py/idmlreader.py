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
#     idmlreader.py
#
#     Takes an Adobe IDML file and answers a Python instance.
#
import zipfile
from lxml import etree

from objects.nodes import IdmlNode, NODE_CLASSES
from objects.idmlroot import IdmlRoot

DESIGN_MAP = 'designmap.xml'
FONTS = 'Resources/Fonts.xml'
GRAPHIC = 'Resources/Graphic.xml'
PREFERENCES = 'Resources/Preferences.xml'
STYLES = 'Resources/Styles.xml'

RESOURCES = [FONTS, GRAPHIC, PREFERENCES, STYLES]
META_INFO = ['META-INF/container.xml', 'META-INF/metadata.xml']

def path2Tag(path):
    return path.split('/')[-1].replace('.xml', '')

def tree2Py(fileName, root):
    tag = root.tag.split('}')[-1]
    nodeClass = NODE_CLASSES.get(tag, IdmlNode)
    e = nodeClass(fileName=fileName, name=tag, nsmap=root.nsmap, 
        attributes=root.items(),
        prefix=root.prefix, text=root.text, tail=root.tail, 
    )
    for child in root:
        eChild = tree2Py(fileName, child)
        if eChild is not None:
            e.elements.append(eChild)
    return e

def readIdml(path):
    """Read the IDML file, indicated by path, and answer a Python instance,
    that contains the whole (zip) file.

    >>> from idmlwriter import writeIdml
    >>> path = '../../Test/MagentaYellowRectangle.idml'
    >>> idml = readIdml(path)
    >>> idml.designMap
    <Document>

    >>> idml.resources['Styles'][1][0].attrs['ParagraphShadingWidth']
    'ColumnWidth'
    >>> idml.resources['Styles'][1][0].attrs['SplitColumnInsideGutter']
    6
    >>> sorted(idml.metaInfo.keys())
    ['container', 'metadata']
    >>> writeIdml(idml, path)
    
    """
    zf = zipfile.ZipFile(path, mode='r') # Open the file.sketch as Zip.
    zipInfo = zf.NameToInfo
    idml = IdmlRoot()
    if DESIGN_MAP in zipInfo:
        idml.designMap = tree2Py(DESIGN_MAP, etree.fromstring(zf.read(DESIGN_MAP)))
    for resource in RESOURCES:
        if resource in zipInfo:
            idml.resources[path2Tag(resource)] = tree2Py(resource, etree.fromstring(zf.read(resource)))
    for metaInfo in META_INFO:
        if metaInfo in zipInfo:
            idml.metaInfo[path2Tag(metaInfo)] = tree2Py(metaInfo, etree.fromstring(zf.read(metaInfo)))
    for story in zipInfo:
        if story.startswith('Stories/'):
            idml.stories.append(tree2Py(story, etree.fromstring(zf.read(story))))
    for spread in zipInfo:
        if spread.startswith('Spreads/'):
            idml.spreads.append(tree2Py(spread, etree.fromstring(zf.read(spread))))
    for masterSpread in zipInfo:
        if masterSpread.startswith('MasterSpreads/'):
            idml.masterSpreads.append(tree2Py(masterSpread, etree.fromstring(zf.read(masterSpread))))
    for xmlNode in zipInfo:
        if xmlNode.startswith('XML/'):
            idml.xmlNodes[path2Tag(xmlNode)] = tree2Py(xmlNode, etree.fromstring(zf.read(xmlNode)))
    return idml

if __name__ == "__main__":
    import sys
    import doctest
    sys.exit(doctest.testmod()[0])

