from zope.interface import Interface
from zope import schema

from zope.app.container.constraints import contains

from collective.sponsor import SponsorMessageFactory as _

class ISponsor(Interface):
    """Sponsor
    """
    
    title = schema.TextLine(title=_(u"Title"),
                            required=True)
    
    description = schema.Text(title=_(u"Description"),
                              description=_(u"Short Description of the Body Text."))
    
    text = schema.Text(title=_(u"Body Text"),
                       required=True)

    website = schema.TextLine(title=_(u"Website URL"),
                               description=_(u"Please enter a Website URL."),
                               required=True)

    category = schema.TextLine(title=_(u"Category"),
                               description=_(u"Please select a category."),
                               required=True)
    

class ISponsorFolder(Interface):
    """Sponsor Folder
    """
    
    title = schema.TextLine(title=_(u"Title"),
                            required=True)
    
    description = schema.Text(title=_(u"Description"),
                              description=_(u"Short Description of the Body Text."))
    
    text = schema.Text(title=_(u"Body Text"),
                       required=True)