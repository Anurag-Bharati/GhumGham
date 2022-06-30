from django.contrib.auth.models import AnonymousUser
from django.db import models
from users.models import User


class Event(models.Model):
    EVENTS = (
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
    event = models.CharField(max_length=200, null=True, choices=EVENTS)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=120, unique=False)
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    snacks = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)

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
    image = models.ImageField(null=True, default="../../static/images/default_package.png")
    duration = models.PositiveSmallIntegerField(null=True)
    coordinate = models.CharField(max_length=300, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    events = models.ManyToManyField(Event, blank=True)
    food = models.ForeignKey(Food, null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return self.name


class Itinerary(models.Model):
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    place = models.ForeignKey(Place, null=True, on_delete=models.SET_NULL)


class Package(models.Model):
    STATUS = (
        ("unavailable", "Unavailable"),
        ("available", "Available"),
        ("ongoing", "Ongoing"),
        ("booked", "Booked"),
    )
    name = models.CharField(max_length=120, unique=False)
    type = models.CharField(max_length=120, unique=False, null=True)
    itinerary = models.ManyToManyField(Itinerary)
    price = models.PositiveSmallIntegerField(null=False)
    image = models.ImageField(null=True, default="../../static/images/default_package.png")
    cover_image = models.ImageField(null=True, default="../../static/images/default_package.png")
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

class Order(models.Model):
    STATUS = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("declined", "Declined"),
        ("canceled", "Canceled"),
    )
    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, null=True, on_delete=models.CASCADE)
    staff = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='assignee')
    customer_phone = models.CharField(max_length=120)
    status = models.CharField(max_length=120, choices=STATUS, default=STATUS[0][0])
    created_date = models.DateField(auto_now_add=True)
    date = models.DateField()

    def __str__(self):
        return self.customer.username + f"({self.created_date})"
