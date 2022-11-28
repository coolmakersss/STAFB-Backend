from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    name_cn = models.CharField(max_length=50)
    location_cn = models.CharField(max_length=50)
    division = models.CharField(max_length=50,null=True)
    subarea = models.CharField(max_length=50,null=True)
    gym = models.CharField(max_length=50)
    logo = models.TextField(null=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    profile_photo = models.TextField(null=True)


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    name_cn = models.CharField(max_length=50)
    age = models.IntegerField()
    hight = models.IntegerField()                                        # 单位cm
    weight = models.IntegerField()                                       # 单位kg
    position = models.CharField(max_length=50)
    number = models.IntegerField()
    photo = models.TextField(null=True)
    team = models.ForeignKey(Team,null=True,on_delete=models.SET_NULL)


class Coach(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    name_cn = models.CharField(max_length=50)
    age = models.IntegerField()
    photo = models.TextField()
    team = models.ForeignKey(Team,null=True,on_delete=models.SET_NULL)


class Game(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.CharField(max_length=50)
    host = models.ForeignKey(Team,on_delete=models.CASCADE,related_name="host_team")
    guest = models.ForeignKey(Team,on_delete=models.CASCADE,related_name="guest_team")
    time = models.DateTimeField()
    host_score = models.IntegerField(null=True)
    guest_score = models.IntegerField(null=True)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    create_by = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    belong_to = models.ForeignKey(Game,null=True,on_delete=models.SET_NULL)
    create_time = models.DateTimeField(auto_now=True)
    text = models.TextField()


class CommentStar(models.Model):
    id = models.AutoField(primary_key=True)
    create_by = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    belong_to = models.ForeignKey(Game,null=True,on_delete=models.SET_NULL)
    create_time = models.DateTimeField(auto_now=True)
    score = models.IntegerField()


class TeamStats(models.Model):
    id = models.AutoField(primary_key=True)
    belong_to_player = models.ForeignKey(Team,null=True,on_delete=models.SET_NULL)
    belong_to_game = models.ForeignKey(Game,null=True,on_delete=models.SET_NULL)

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
    belong_to_player = models.ForeignKey(Player,null=True,on_delete=models.SET_NULL)
    belong_to_game = models.ForeignKey(Game,null=True,on_delete=models.SET_NULL)

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


class PlayerHonors(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.CharField(max_length=50)
    mvp = models.ForeignKey(Player,null=True,on_delete=models.SET_NULL,related_name="mvp_player")
    dpoy = models.ForeignKey(Player,null=True,on_delete=models.SET_NULL,related_name="dpoy_player")
    smoy = models.ForeignKey(Player,null=True,on_delete=models.SET_NULL,related_name="smoy_player")
    amvp = models.ForeignKey(Player,null=True,on_delete=models.SET_NULL,related_name="amvp_player")
    first_team = models.CharField(max_length=50)        #Save player's id with "," for interval. Samlpe: 1,5,21,30,14
    second_team = models.CharField(max_length=50)       #Save player's id with "," for interval. Samlpe: 1,5,21,30,14
    third_team = models.CharField(max_length=50)        #Save player's id with "," for interval. Samlpe: 1,5,21,30,14
    d_first_team = models.CharField(max_length=50)      #Save player's id with "," for interval. Samlpe: 1,5,21,30,14
    d_second_team = models.CharField(max_length=50)     #Save player's id with "," for interval. Samlpe: 1,5,21,30,14
    d_third_team = models.CharField(max_length=50)      #Save player's id with "," for interval. Samlpe: 1,5,21,30,14

    #???
    score_king = models.ForeignKey(Player,null=True,on_delete=models.SET_NULL,related_name="score_king_player")
    rebound_king = models.ForeignKey(Player,null=True,on_delete=models.SET_NULL,related_name="rebound_king_player")
    assist_king = models.ForeignKey(Player,null=True,on_delete=models.SET_NULL,related_name="assist_king_player")
    steal_king = models.ForeignKey(Player,null=True,on_delete=models.SET_NULL,related_name="steal_king_player")
    block_king = models.ForeignKey(Player,null=True,on_delete=models.SET_NULL,related_name="block_king_player")


