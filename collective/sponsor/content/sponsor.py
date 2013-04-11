from Products.CMFCore.permissions import View
from AccessControl import ClassSecurityInfo

from zope.interface import implements

try:
    from Products.LinguaPlone.public import *
except ImportError:
    from Products.Archetypes.atapi import *

from Products.Archetypes.atapi import DisplayList

from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.newsitem import ATNewsItem, ATNewsItemSchema

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.validation import V_REQUIRED

from collective.sponsor.interfaces import ISponsor
from collective.sponsor.config import PROJECTNAME, CATEGORIES

from collective.sponsor import SponsorMessageFactory as _

from urllib import quote

schema = Schema((
                 
    StringField('website',
        required = True,
        searchable = True,
        default = "http://",
        validators = (),
        storage = AnnotationStorage(),
        widget = StringWidget(label = _(u'Website URL'),
                              description = _(u"Please enter a Website URL."),
                              ),
        ),

    BooleanField('external',
        storage=AnnotationStorage(),
        widget=BooleanWidget(label=_(u"External link"),
                            description=_(u"Check to use external links on spnsor logos."),
                            ),
        ),

    StringField('category',
        storage = AnnotationStorage(),
        vocabulary = CATEGORIES,
        widget = MultiSelectionWidget(label=_(u"Category"),
                                      description=_(u"Please select a category."),
                                      ),     
        ),
                 
    ))

SponsorSchema = ATNewsItemSchema.copy() + schema.copy()

SponsorSchema['title'].storage = AnnotationStorage()
SponsorSchema['description'].storage = AnnotationStorage()
SponsorSchema['text'].storage = AnnotationStorage()
SponsorSchema['image'].widget.description = _(u'label_image_field', default = u'Logo or image of the sponsor')
SponsorSchema['imageCaption'].widget.visible = {"edit": "invisible", "view": "invisible"}
SponsorSchema['excludeFromNav'].default = True

finalizeATCTSchema(SponsorSchema, folderish=False, moveDiscussion=False)

class Sponsor(ATNewsItem):
    """Sponsor
    """

    implements(ISponsor)

    portal_type = "Sponsor"
    _at_rename_after_creation = True

    schema = SponsorSchema
    
    title = ATFieldProperty('title')
    description = ATFieldProperty('description')
    text = ATFieldProperty('text')
    website = ATFieldProperty('website')
    external = ATFieldProperty('external')
    category = ATFieldProperty('category')
    
    security = ClassSecurityInfo()
        
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        return self.getField('image').tag(self, **kwargs)

    
    security.declareProtected(View, 'website')
    def getRemoteUrl(self):
        """Sanitize output
        """
        value = self.Schema()['website'].get(self)
        if not value: value = '' # ensure we have a string
        return quote(value, safe='?$#@/:=+;$,&%')

    
    def __bobo_traverse__(self, REQUEST, name):
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                return image
        return super(Sponsor, self).__bobo_traverse__(REQUEST, name)


registerType(Sponsor, PROJECTNAME)