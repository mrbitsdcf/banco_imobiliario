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
    click.secho('Banco Imobiliario - Movimentação de Jogo', fg='green', bold=True)
    click.secho('========================================\n\n', fg='green', bold=True)
    pass


@cli.command(name='initialisedb', short_help="Inicia o banco de dados")
def initialisedb_command():
    click.secho('Criando banco de dados vazio', fg='blue')
    initialisedb()
    click.secho('[OK]', fg='green', bold=True)


@cli.command(name='add_players', short_help="Adiciona jogadores")
@click.argument('num_of_players')
def add_players_command(num_of_players):
    '''num_of_players: Numero de jogadores'''
    for p in range(int(num_of_players)):
        player_name = 'Jogador {}'.format(p + 1)
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
    click.secho("Iniciando novo jogo com {} jogadores\n".format(num_of_players), fg='yellow', bold=True)
    initialisedb()
    with click.progressbar(range(int(num_of_players))) as players:
        for p in players:
            player_name = 'Jogador {}'.format(p + 1)
            click.secho(' Inserindo jogador {0}'.format(player_name), fg='blue')
            player = Player(player_name=player_name)
            DBSession.add(player)

    player = Player(player_name='Banqueiro', balance=float(1000000.0))
    DBSession.add(player)

    DBSession.flush()
    DBSession.commit()
    click.secho('[OK]', fg='green', bold=True)


@cli.command(name='list_balance', short_help="Lista dinheiro dos jogadores")
@click.argument('players', default='ALL')
def list_balance_command(players):
    '''players: Nome do jogador. Deixar sem valor para listar todos'''
    click.secho('Listando balanco de jogadores\n', fg='yellow', bold=True)
    rs_players = Player.query.filter(Player.player_name != 'Banqueiro')
    if players != 'ALL':
        rs_players = rs_players.filter(Player.id == players).first()

    click.secho('Jogador     Balance', fg='red', bold=True)
    click.secho('=========================', fg='red')
    for player in rs_players:
        click.secho("{0} - BI${1:>10}".format(player.player_name, money.format_money(player.balance)))

    print


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
        print "Jogador: {0} - Tipo: {1} - Valor: BI$ {2}".format(movement.player.player_name, movement_type, movement.amount)


@cli.command(name='movement', short_help='Movimenta dinheiro')
@click.argument('mov_type')
@click.argument('player_out', default=None)
@click.argument('player_in', default=None)
@click.argument('amount')
def movement_command(mov_type, player_out=None, player_in=None, amount=0.0):
    """\b
    mov_type: Tipo de movimento. Recebe 'in' para entrada, 'out' para saida e 'pay' para pagamento

    player_out: Numero do jogador que pagara

    player_in: Numero do jogador que recebera

    amount: Valor da movimentacao


    Exemplos de uso:

    \b
        $ bcimob movement in 1 1 2000       # Jogador 1 receberá do banco BI$ 2.000,00

    \b
        $ bcimob movement out 2 2 2000      # Jogador 2 pagará ao banco BI$ 2.000,00

    \b
        $ bcimob movement pay 1 2 2000      # Jogador 1 pagará BI$ 2.000,00 ao jogador 2

    """

    click.secho('Movimentacao de dinheiro\n', fg='yellow', bold=True)
    fmt_amount = money.format_money(money.Decimal(amount))
    if mov_type == 'in':
        print "Jogador {0} recebendo BI$ {1}".format(player_in, fmt_amount)
        add_money(player_in, float(amount))
    elif mov_type == 'out':
        print "Jogador {0} pagando {1}".format(player_out, fmt_amount)
        subtract_money(player_out, float(amount))
    elif mov_type == 'pay':
        print "Jogador {0} pagando {1} para Jogador {2}".format(player_out, fmt_amount, player_in)
        pay_money(player_out, player_in, float(amount))

    click.secho('[OK]', fg='green', bold=True)

if __name__ == '__main__':
    cli()
