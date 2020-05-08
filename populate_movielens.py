# 添加和读取数据到数据库中
import csv
import os
import re

import django
from django.db.utils import IntegrityError

from populate_user_rate import random_user_name, random_phone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie.settings")

django.setup()
from user.models import Movie, Tags, Rate, User


def populate_movie():
    Movie.objects.all().delete()
    Tags.objects.all().delete()

    opener = open('movielens/movie.csv', 'r')
    csv_reader = csv.reader(opener)
    for line in csv_reader:
        movie_id = line[0]
        movie_name = line[1]
        image = line[2]
        print(movie_name)
        year = re.match(r'.*(\d{4}).*', movie_name)
        try:
            print(year[0])
            year = year[1]
        except TypeError:
            year = 'unknown'
        movie_name = movie_name.split('(')[0]
        try:
            movie = Movie.objects.create(name=movie_name, years=year, pic=image)
        except IntegrityError:
            pass


def populate_rate():
    Rate.objects.all().delete()
    with open('movielens/rrtotaltable.csv', 'r') as opener:
        csv_reader = csv.reader(opener)
        for line in csv_reader:
            user_id = line[0]
            movie_id = line[1]
            rate = line[2]
            user_name = random_user_name()
            while True:
                try:
                    user, created = User.objects.get_or_create(id=user_id,
                                                               defaults={'name': user_name, 'username': user_name, 'password': user_name, "phone": random_phone(), "address": random_user_name(), "email": random_user_name() + '@163.com'})
                    break
                except:
                    user_name = random_user_name()
                    print('trying again', user_name)
            print(movie_id)
            Rate.objects.create(user_id=user.id, movie_id=movie_id, mark=rate)


if __name__ == '__main__':
    populate_rate()
