from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    name_cn = models.CharField(max_length=50)
    location_cn = models.CharField(max_length=50)
    gym = models.CharField(max_length=50)
    logo = models.TextField(null=True)


class User(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    profile_photo = models.TextField(null=True)


class Player(models.Model):
    id = models.Autofild(primary_key=True)
    name = models.CharField(max_length=50)
    name_cn = models.CharField(max_length=50)
    age = models.IntegerField()
    hight = models.IntegerField()
    weight = models.IntegerField()
    position = models.CharField(max_length=50)
    number = models.IntegerField()
    photo = models.TextField()
    team = models.ForeignKey(Team,on_delete=models.SET_NULL)


class Coach(models.Model):
    id = models.ForeignKey(primary_key=True)
    name = models.CharField(max_length=50)
    name_cn = models.CharField(max_length=50)
    age = models.IntegerField()
    photo = models.TextField()
    team = models.ForeignKey(Team,on_delete=models.SET_NULL)


class Game(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.CharField(max_length=50)
    host = models.ForeignKey(Team,on_delete=models.CASCADE)
    guest = models.ForeignKey(Team,on_delete=models.CASCADE)
    time = models.DateTimeField()
    host_score = models.IntegerField()
    host_score = models.IntegerField()


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    create_by = models.ForeignKey(User,on_delete=models.SET_NULL)
    belong_to = models.ForeignKey(Game,on_delete=models.SET_NULL)
    create_time = models.DateTimeField(auto_now=True)
    text = models.TextField()


class CommentStar(models.Model):
    id = models.AutoField(primary_key=True)
    create_by = models.ForeignKey(User,on_delete=models.SET_NULL)
    belong_to = models.ForeignKey(Game,on_delete=models.SET_NULL)
    create_time = models.DateTimeField(auto_now=True)
    score = models.IntegerField()


class TeamStats(models.Model):
    id = models.AutoField(primary_key=True)
    belong_to_player = models.ForeignKey(Team,on_delete=models.SET_NULL)
    belong_to_game = models.ForeignKey(Game,on_delete=models.SET_NULL)

    #赛场数据
    score = models.IntegerField()
    rebound = models.IntegerField()
    o_rebound = models.IntegerField()
    d_rebound = models.IntegerField()
    assist = models.IntegerField()
    steal = models.IntegerField()
    block = models.IntegerField()
    foul = models.IntegerField()
    turnover = models.IntegerField()
    field_goals_attempted = models.IntegerField()
    field_goals_made = models.IntegerField()
    three_points_attempt = models.IntegerField()
    three_points_made = models.IntegerField()
    free_throws_attempted = models.IntegerField()
    free_throws_made = models.IntegerField()

class PlayerStats(models.Model):
    id = models.AutoField(primary_key=True)
    belong_to_player = models.ForeignKey(Player,on_delete=models.SET_NULL)
    belong_to_game = models.ForeignKey(Game,on_delete=models.SET_NULL)

    #赛场数据
    minute = models.IntegerField()
    score = models.IntegerField()
    rebound = models.IntegerField()
    o_rebound = models.IntegerField()
    d_rebound = models.IntegerField()
    assist = models.IntegerField()
    steal = models.IntegerField()
    block = models.IntegerField()
    foul = models.IntegerField()
    turnover = models.IntegerField()
    field_goals_attempted = models.IntegerField()
    field_goals_made = models.IntegerField()
    three_points_attempt = models.IntegerField()
    three_points_made = models.IntegerField()
    free_throws_attempted = models.IntegerField()
    free_throws_made = models.IntegerField()
    plus_minus = models.IntegerField()
