from Acquisition import aq_inner
from zope.component import getMultiAdapter

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from collective.sponsor.interfaces import ISponsor

class SponsorView(BrowserView):
    
    __call__ = ViewPageTemplateFile('templates/sponsor.pt')
    
    def anonymous(self):
        """ return the anonymous state
        """
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        
        return portal_state.anonymous()
    