# vocabulary from https://boardgamegeek.com/boardgame/1465/wizard

from django.db import models


class Color(models.TextChoices):
    NONE = ''
    RED = 'R'
    GREEN = 'G'
    BLUE = 'B'
    YELLOW = 'Y'


class Card(models.Model):
    VALUE_JESTER = 0
    VALUE_WIZARD = 14

    color = models.CharField(max_length=1, choices=Color.choices)
    value = models.IntegerField()


class Game(models.Model):
    name = models.CharField(max_length=255)


class Player(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        order_with_respect_to = 'game'


class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    trump = models.CharField(max_length=1, choices=Color.choices, default=Color.NONE)

    class Meta:
        order_with_respect_to = 'game'


class RoundPlayer(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    expectedWins = models.IntegerField()
    hand = models.ManyToManyField(Card)

    class Meta:
        order_with_respect_to = 'round'


class Trick(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    leader = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='leader')
    winner = models.ForeignKey(Player, on_delete=models.PROTECT, null=True, default=None, related_name='winner')

    class Meta:
        order_with_respect_to = 'round'


class PlayedCard(models.Model):
    trick = models.ForeignKey(Trick, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.PROTECT)
    player = models.ForeignKey(Player, on_delete=models.PROTECT)

    class Meta:
        order_with_respect_to = 'trick'
