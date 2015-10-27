#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
from models import initialisedb
from models import Player, DBSession, Movement
from utils import pay_money, add_money, subtract_money
import money


@click.group()
def cli():
    pass


@cli.command(name='initialisedb')
def initialisedb_command():
    initialisedb()


@cli.command(name='add_players')
@click.argument('num_of_players')
def add_players_command(num_of_players):
    for p in range(int(num_of_players)):
        player_name = 'Player {}'.format(p + 1)
        player = Player(player_name=player_name)
        DBSession.add(player)

    player = Player(player_name='Banqueiro', balance=float(1000000.00))
    DBSession.add(player)
    DBSession.flush()
    DBSession.commit()


@cli.command(name='start_game')
@click.argument('num_of_players')
def start_game_command(num_of_players):
    print "Iniciando novo jogo com {} jogadores".format(num_of_players)
    initialisedb()
    for p in range(int(num_of_players)):
        print "Inserindo jogador {} com BI$ 25.000,00".format(p + 1)
        player_name = 'Player {}'.format(p + 1)
        player = Player(player_name=player_name)
        DBSession.add(player)

    print "Inserindo Banqueiro"
    player = Player(player_name='Banqueiro', balance=float(1000000.0))
    DBSession.add(player)
    DBSession.flush()
    DBSession.commit()


@cli.command(name='list_balance')
@click.argument('players', default='ALL')
def list_balance_command(players):
    rs_players = Player.query.filter(Player.player_name != 'Banqueiro')
    if players != 'ALL':
        rs_players = rs_players.filter(Player.id == players).first()

    for player in rs_players:
        print "Player: {0} - Balance: BI$ {1}".format(player.player_name, money.format_money(player.balance))


@cli.command(name='list_movement')
@click.argument('players', default='ALL')
def list_movement(players):
    banqueiro = Player.query.filter(Player.player_name == 'Banqueiro').first()
    movements = Movement.query.filter(Movement.player_id != banqueiro.id)

    if players != 'ALL':
        player = Player.query.filter(Player.id == int(players)).first()
        movements = movements.filter(Movement.player_id == player.id).all()

    for movement in movements:
        movement_type = Movement.VERBOSE_TYPES[Movement.REV_TYPES[movement.move_type]]
        print "Player: {0} - Tipo: {1} - Valor: BI$ {2}".format(movement.player.player_name, movement_type, movement.amount)


# movement IN player valor
# movement OUT player valor
# movement PAY player OUT player IN valor
@cli.command(name='movement')
@click.argument('mov_type')
@click.argument('player_out', default=None)
@click.argument('player_in', default=None)
@click.argument('amount')
def movement_command(mov_type, player_out=None, player_in=None, amount=0.0):
    if mov_type == 'IN':
        print "Player {0} recebendo {1}".format(player_in, amount)
        add_money(player_in, float(amount))
    elif mov_type == 'OUT':
        print "Player {0} pagando {1}".format(player_out, amount)
        subtract_money(player_out, float(amount))
    elif mov_type == 'PAY':
        print "Player {0} pagando {1} para Player {2}".format(player_out, amount, player_in)
        pay_money(player_in, player_out, float(amount))

if __name__ == '__main__':
    cli()
