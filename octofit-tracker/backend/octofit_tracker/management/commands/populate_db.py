from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Données de test pour OctoFit
        users = [
            User(_id=ObjectId(), username='superman', email='superman@octofit.edu', password='superpassword'),
            User(_id=ObjectId(), username='wonderwoman', email='wonderwoman@octofit.edu', password='wonderpassword'),
            User(_id=ObjectId(), username='batman', email='batman@octofit.edu', password='batpassword'),
            User(_id=ObjectId(), username='flash', email='flash@octofit.edu', password='flashpassword'),
            User(_id=ObjectId(), username='aquaman', email='aquaman@octofit.edu', password='aquapassword'),
        ]
        User.objects.bulk_create(users)

        teams = [
            Team(_id=ObjectId(), name='Justice League'),
            Team(_id=ObjectId(), name='Avengers')
        ]
        Team.objects.bulk_create(teams)

        for team in teams:
            team.members.set(users)

        activities = [
            Activity(_id=ObjectId(), user=users[0], activity_type='Flying', duration=timedelta(hours=2)),
            Activity(_id=ObjectId(), user=users[1], activity_type='Strength Training', duration=timedelta(hours=1, minutes=30)),
            Activity(_id=ObjectId(), user=users[2], activity_type='Martial Arts', duration=timedelta(hours=1)),
            Activity(_id=ObjectId(), user=users[3], activity_type='Running', duration=timedelta(minutes=45)),
            Activity(_id=ObjectId(), user=users[4], activity_type='Swimming', duration=timedelta(hours=1, minutes=15)),
        ]
        Activity.objects.bulk_create(activities)

        leaderboard_entries = [
            Leaderboard(_id=ObjectId(), user=users[0], score=120),
            Leaderboard(_id=ObjectId(), user=users[1], score=110),
            Leaderboard(_id=ObjectId(), user=users[2], score=115),
            Leaderboard(_id=ObjectId(), user=users[3], score=105),
            Leaderboard(_id=ObjectId(), user=users[4], score=100),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        workouts = [
            Workout(_id=ObjectId(), name='Flight Training', description='Training for aerial maneuvers'),
            Workout(_id=ObjectId(), name='Strength Training', description='Building super strength'),
            Workout(_id=ObjectId(), name='Combat Training', description='Improving combat skills'),
            Workout(_id=ObjectId(), name='Speed Training', description='Enhancing running speed'),
            Workout(_id=ObjectId(), name='Aquatic Training', description='Mastering underwater techniques'),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))