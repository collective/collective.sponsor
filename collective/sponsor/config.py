from Products.Archetypes.atapi import DisplayList

PROJECTNAME = "collective.sponsor"

ADD_PERMISSIONS = {
    "Sponsor"         : "collective.sponsor: Add Sponsor",
    "Sponsor Folder"  : "collective.sponsor: Add Sponsor Folder",
}

CATEGORIES = DisplayList((
    ('platinum', 'Platinum'),
    ('gold', 'Gold'),
    ('silver', 'Silver'),
    ('bronze', 'Bronze'),
    ('media', 'Mediapartner'),
    ))