from zope.interface import implements
from zope.component import adapts

from Products.Archetypes.atapi import *

from Products.Archetypes.interfaces import IObjectPostValidation

from Products.validation import V_REQUIRED

from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from collective.sponsor.interfaces import ISponsorFolder
from collective.sponsor.config import PROJECTNAME

from collective.sponsor import SponsorMessageFactory as _

schema = Schema((

    TextField('text',
        required=False,
        searchable=True,
        storage=AnnotationStorage(),
        validators=('isTidyHtmlWithCleanup',),
        default_output_type='text/x-html-safe',
        widget=RichWidget(label=_(u"Body Text"),
                          description=_(u""),
                          rows=25,
                          allow_file_upload=False)   
        ),
    ))

SponsorFolderSchema = ATFolderSchema.copy() + schema.copy()

SponsorFolderSchema['title'].storage = AnnotationStorage()
SponsorFolderSchema['description'].storage = AnnotationStorage()

finalizeATCTSchema(SponsorFolderSchema, folderish=True, moveDiscussion=False)

class SponsorFolder(ATFolder):
    """Sponsor Folder
    """

    implements(ISponsorFolder)

    portal_type = "Sponsor Folder"
    _at_rename_after_creation = True

    schema = SponsorFolderSchema
    
    title = ATFieldProperty('title')
    description = ATFieldProperty('description')
    text = ATFieldProperty('text')
    
registerType(SponsorFolder, PROJECTNAME)