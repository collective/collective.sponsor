from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize

from collective.sponsor.config import CATEGORIES

from random import shuffle


class SponsorboxViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/sponsorbox.pt')


    def _query(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        state = 'published'
        results = catalog(portal_type='Sponsor',
                          review_state=state,
                          sort_on='effective')
        return results


    def _sponsors(self):
        sponsors = []
        for sponsor in self._query():
            sponsors.append(sponsor.getObject())
            
        return sponsors
    

    def categories(self):
        c = []
        for category in CATEGORIES.keys():
            c.append(category)
        return c

    
    def filtered_categories(self):
        """return filtered list of categories, remove empty ones
        """
        categories = self.categories()
        sponsors = self.sponsors()
        
        filtered_categories = []
        for category in categories:
            if len(sponsors[category]):
                filtered_categories.append(category)
        return filtered_categories
        
    
    def sponsors(self):
        results = self._sponsors()
        sponsors = {}
        for category in self.categories():
            list = []
            for r in results:
                if category in r.getCategory():
                    list.append(r)
            shuffle(list)
            sponsors[category] = list
        return sponsors
