#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
from models import initialisedb
from models import Player, DBSession, Movement
from utils import pay_money, add_money, subtract_money
import money

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
click.clear()


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    '''Gerencia dinheiro de jogadores no Banco Imobiliario'''
    pass


@cli.command(name='initialisedb', short_help="Inicia o banco de dados")
def initialisedb_command():
    initialisedb()


@cli.command(name='add_players', short_help="Adiciona jogadores")
@click.argument('num_of_players')
def add_players_command(num_of_players):
    '''num_of_players: Numero de jogadores'''
    for p in range(int(num_of_players)):
        player_name = 'Player {}'.format(p + 1)
        player = Player(player_name=player_name)
        DBSession.add(player)

    player = Player(player_name='Banqueiro', balance=float(1000000.00))
    DBSession.add(player)
    DBSession.flush()
    DBSession.commit()


@cli.command(name='start_game', short_help="Inicia novo jogo")
@click.argument('num_of_players')
def start_game_command(num_of_players):
    '''num_of_players: Numero de jogadores'''
    click.echo("Iniciando novo jogo com {} jogadores".format(num_of_players))
    initialisedb()
    with click.progressbar(
        length=int(num_of_players) + 1,
        label="Inserindo {0} jogadores com BI$ 25.000,00 cada e banqueiro".format(num_of_players)
    ) as players:
        for p in players:
            player_name = 'Player {}'.format(p + 1)
            player = Player(player_name=player_name)
            DBSession.add(player)
            players.update(p)

        player = Player(player_name='Banqueiro', balance=float(1000000.0))
        DBSession.add(player)
        DBSession.flush()
        DBSession.commit()


@cli.command(name='list_balance', short_help="Lista dinheiro dos jogadores")
@click.argument('players', default='ALL')
def list_balance_command(players):
    '''players: Nome do jogador. Deixar sem valor para listar todos'''
    rs_players = Player.query.filter(Player.player_name != 'Banqueiro')
    if players != 'ALL':
        rs_players = rs_players.filter(Player.id == players).first()

    for player in rs_players:
        print "Player: {0} - Balance: BI$ {1}".format(player.player_name, money.format_money(player.balance))


@cli.command(name='list_movement', short_help="Lista movimentacao dos jogadores")
@click.argument('players', default='ALL')
def list_movement(players):
    '''players: Nome do jogador. Deixar sem valor para listar todos'''
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
@cli.command(name='movement', short_help='Movimenta dinheiro')
@click.argument('mov_type')
@click.argument('player_out', default=None)
@click.argument('player_in', default=None)
@click.argument('amount')
def movement_command(mov_type, player_out=None, player_in=None, amount=0.0):
    """mov_type: Tipo de movimento. Recebe IN para entrada, OUT para saida e PAY para pagamento

    player_out: Numero do jogador que pagara

    player_in: Numero do jogador que recebera

    amount: Valor da movimentacao


    Exemplos de uso:

    \b
        $ bcimob movement IN 1 1 2000       # Jogador 1 receberá do banco BI$ 2.000,00

    \b
        $ bcimob movement OUT 2 2 2000      # Jogador 2 pagará ao banco BI$ 2.000,00

    \b
        $ bcimob movement PAY 1 2 2000      # Jogador 1 pagará BI$ 2.000,00 ao jogador 2

    """
    if mov_type == 'IN':
        print "Player {0} recebendo {1}".format(player_in, amount)
        add_money(player_in, float(amount))
    elif mov_type == 'OUT':
        print "Player {0} pagando {1}".format(player_out, amount)
        subtract_money(player_out, float(amount))
    elif mov_type == 'PAY':
        print "Player {0} pagando {1} para Player {2}".format(player_out, amount, player_in)
        pay_money(player_out, player_in, float(amount))

if __name__ == '__main__':
    cli()
