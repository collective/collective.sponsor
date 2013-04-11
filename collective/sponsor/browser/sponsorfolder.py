from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize
from collective.sponsor.interfaces import ISponsorFolder

from collective.sponsor.config import CATEGORIES


class SponsorFolderView(BrowserView):
    __call__ = ViewPageTemplateFile('templates/sponsorfolder.pt')
    

    def _query(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        state = 'published'
        results = catalog(portal_type='Sponsor',
                          review_state=state,
                          sort_on='effective',
                          path=path)
        return results


    def _sponsors(self):
        result = self._query()
        
        sponsors = []
        for sponsor in result:
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
            sponsors[category] = list
        
        return sponsors

    
    def sponsors_listing(self):
        results = self._sponsors()
        
        return results