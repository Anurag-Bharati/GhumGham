from django.contrib.auth.models import AnonymousUser
from django.db import models
from users.models import User


class Adventure(models.Model):
    ADVENTURE = (
        ("other", "Other"),
        ("rafting", "Rafting"),
        ("camping", "Camping"),
        ("trekking", "Trekking"),
        ("canoeing", "Canoeing"),
        ("ziplining", "Ziplining"),
        ("sky diving", "Sky Diving"),
        ("paragliding", "Paragliding"),
        ("rock climbing", "Rock Climbing"),
        ("mountaineering", "Mountaineering"),
        ("bungee jumping", "Bungee Jumping"),
        ("mountain biking", "Mountain Biking")
    )
    name = models.CharField(max_length=120, unique=False)
    adventure = models.CharField(max_length=200, null=True, choices=ADVENTURE)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=120, unique=False)
    breakfast = models.BooleanField(null=True, default=False)
    lunch = models.BooleanField(null=True, default=False)
    snacks = models.BooleanField(null=True, default=False)
    dinner = models.BooleanField(null=True, default=False)

    def __str__(self):
        result = ""
        if self.breakfast:
            result += "breakfast"
        if self.lunch:
            result += " lunch"
        if self.snacks:
            result += " snacks"
        if self.dinner:
            result += " dinner"
        if result:
            return result.strip().capitalize().replace(" ", ", ") + ' @ ' + self.name
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=120, unique=False)
    image = models.ImageField(null=True, blank=True, default="../../static/images/default_package.png")
    cover_image = models.ImageField(null=True, blank=True, default="../../static/images/default_package.png")
    coordinate = models.CharField(max_length=300, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    adventures = models.ManyToManyField(Adventure, blank=True)
    food = models.ForeignKey(Food, null=True, on_delete=models.SET_NULL, blank=True)
    date_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class Itinerary(models.Model):
    name = models.CharField(max_length=120, unique=False)
    duration = models.PositiveSmallIntegerField(null=True)
    places = models.ManyToManyField(Place, blank=True)

    def __str__(self):
        return self.name


class Package(models.Model):
    STATUS = (
        ("available", "Available"),
        ("unavailable", "Unavailable"),
        ("booked", "Booked"),
        ("ongoing", "Ongoing"),
    )
    name = models.CharField(max_length=120, unique=False, null=False, blank=False)
    type = models.CharField(max_length=120, unique=False, null=True)
    itinerary = models.ForeignKey(Itinerary, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.PositiveSmallIntegerField(null=False)
    image = models.ImageField(null=True, blank=True, default="../../static/assets/images/default_package.png")
    cover_image = models.ImageField(null=True, blank=True, default="../../static/assets/images/default_package.png")
    desc = models.CharField(max_length=200, unique=False, null=True, blank=True)
    duration = models.PositiveSmallIntegerField(null=True)
    is_featured = models.BooleanField(null=True, default=False)
    status = models.CharField(max_length=120, choices=STATUS, default=STATUS[1][0])
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class ActivityLog(models.Model):
    ACTION = (
        ("added", "Added"),
        ("updated", "Updated"),
        ("deleted", "Deleted"),
        ("logged-in", "Logged In"),
        ("logged-out", "Logged Out"),
        ("banned", "Banned"),
        ("unbanned", "Unbanned"),
    )
    THING = (
        ("food", "Food"),
        ("event", "Event"),
        ("place", "Place"),
        ("package", "Package"),
        ("itinerary", "Itinerary")
    )
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=AnonymousUser)
    target = models.CharField(max_length=120, null=True, blank=True)
    action = models.CharField(max_length=120, choices=ACTION)
    thing = models.CharField(max_length=120, choices=THING, null=True, blank=True)
    more = models.CharField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, )

    def __str__(self):
        vowel = ['a', 'e', 'i', 'o', 'u']
        article_thing = " a "
        if self.target:
            return self.action + ' ' + self.target.capitalize()
        if not self.thing and not self.target:
            return self.action + " to the system"
        if self.thing[0].lower() in vowel:
            article_thing = " an "
        if self.more:
            return self.action.capitalize() + article_thing + self.thing.lower() + self.more

        return self.action.capitalize() + article_thing + self.thing.lower()

    def getTime(self):
        return self.timestamp.date().__str__() + " at " + \
               self.timestamp.time().hour.__str__() + ":" + \
               self.timestamp.time().minute.__str__() + ":" + \
               self.timestamp.time().second.__str__()
