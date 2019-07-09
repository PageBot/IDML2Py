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
import codecs
import os, shutil
import zipfile
from lxml import etree

def writeIdml(idml, path):
    """Write the IDML file from idmlRoot, indicated by path.

    >>> from idmlreader import readIdml
    >>> path = '../../Test/MagentaYellowRectangle.idml'
    >>> idml = readIdml(path)
    >>> print(idml.resources['Styles'][1][0].attrs['ParagraphShadingWidth'])
    ColumnWidth
    >>> print(idml.resources['Styles'][1][0].attrs['SplitColumnInsideGutter'])
    6
    >>> writeIdml(idml, path)
    
    """
    tmpPath = path.replace('.idml', '.tmp')
    if os.path.exists(tmpPath):
        shutil.rmtree(tmpPath)
    os.mkdir(tmpPath)

    zf = zipfile.ZipFile(tmpPath + '.idml', mode='w') # Open export as Zip.

    filePath = '/mimetype'
    f = codecs.open(tmpPath + filePath, 'w', encoding='utf-8')
    f.write('application/vnd.adobe.indesign-idml-package')
    f.close()
    zf.write(tmpPath + filePath, arcname=filePath)

    #shutil.copy('../../Test/MagentaYellowRectangle/designmap.xml', tmpPath + '/designmap.xml')
    
    filePath = '/designmap.xml'
    f = codecs.open(tmpPath + filePath, 'w', encoding='utf-8')
    f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
    f.write('<?aid style="50" type="document" readerVersion="6.0" featureSet="257" product="14.0(324)" ?>\n')
    idml.designMap.writeXml(f)
    f.close()
    zf.write(tmpPath + filePath, arcname=filePath)
    
    os.mkdir(tmpPath + '/META-INF')

    for infoName in idml.metaInfo.keys():
        filePath = '/META-INF/%s.xml' % infoName
        f = codecs.open(tmpPath + filePath, 'w', encoding='utf-8')
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
        idml.metaInfo[infoName].writeXml(f)
        f.close()
        zf.write(tmpPath + filePath, arcname=filePath)

    os.mkdir(tmpPath + '/XML')

    for fileName in ('Tags', 'BackingStory'):
        filePath = '/XML/%s.xml' % fileName
        f = codecs.open(tmpPath + filePath, 'w', encoding='utf-8')
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
        idml.xmlNodes[fileName].writeXml(f)
        f.close()
        zf.write(tmpPath + filePath, arcname=filePath)

    os.mkdir(tmpPath + '/Spreads')

    #shutil.copy('../../Test/MagentaYellowRectangle/Spreads/Spread_udc.xml', tmpPath + '/Spreads/Spread_udc.xml')
    for spread in idml.spreads:
        filePath = '/' + spread.fileName
        f = codecs.open(tmpPath + filePath, 'w', encoding='utf-8')
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
        spread.writeXml(f)
        f.close()
        zf.write(tmpPath + filePath, arcname=filePath)
    
    os.mkdir(tmpPath + '/MasterSpreads')

    for masterSpread in idml.masterSpreads:
        filePath = '/' + masterSpread.fileName
        f = codecs.open(tmpPath + filePath, 'w', encoding='utf-8')
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
        masterSpread.writeXml(f)
        f.close()
        zf.write(tmpPath + filePath, arcname=filePath)

    os.mkdir(tmpPath + '/Resources')

    for fileName in ('Fonts', 'Graphic', 'Preferences', 'Styles'):
        filePath = '/Resources/%s.xml' % fileName
        f = codecs.open(tmpPath + filePath, 'w', encoding='utf-8')
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
        idml.resources[fileName].writeXml(f)
        f.close()
        zf.write(tmpPath + filePath, arcname=filePath)

    os.mkdir(tmpPath + '/Stories')

    for story in idml.stories:
        filePath = '/' + story.fileName
        f = codecs.open(tmpPath + filePath, 'w', encoding='utf-8')
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
        story.writeXml(f)
        f.close()
        zf.write(tmpPath + filePath, arcname=filePath)
    zf.close()

if __name__ == "__main__":
    import sys
    import doctest
    sys.exit(doctest.testmod()[0])

