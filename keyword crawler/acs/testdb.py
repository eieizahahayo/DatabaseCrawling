from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
connect('mongodb://a:a123456@ds125381.mlab.com:25381/crawlerdata')


class Journal(MongoModel):
    site = fields.CharField()
    link = fields.CharField()
    title = fields.CharField()
    journalName = fields.CharField()
    volume = fields.CharField()
    date = fields.CharField()
    doi = fields.CharField()
    keywords = fields.CharField()
    authors = fields.CharField()
    address = fields.CharField()
    contact = fields.CharField()



post = Journal(
    site = "webA",
    link = "www.google.co.th",
    title = "TitleA",
    journalName = "JournalA",
    volume = "VolumeA",
    date = "17/09/1995",
    doi = "doiA",
    keywords = ["A","B"],
    authors = "Mr.A",
    address = "AddressA",
    contact = "mrA@somemail.com"
).save()


# Find objects using familiar MongoDB-style syntax.
slideshows = Journal.objects.raw({'link': 'www.google.co.th'})
print(slideshows)
# Only retrieve the 'title' field.
slideshow_titles = slideshows.only('title')

# u'Five Crazy Health Foods Jabba Eats.'
print(slideshow_titles.first().title)

for each in Journal.objects.all():
    print(each.keywords[0])
