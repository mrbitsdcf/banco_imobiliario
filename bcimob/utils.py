# -*- coding: utf-8 -*-

from models import Player, Movement, DBSession


def pay_money(player_out, player_in, amount):
    out_player = Player.query.filter(Player.id == int(player_out)).first()
    in_player = Player.query.filter(Player.id == int(player_in)).first()

    movement_out = Movement(player=out_player, amount=amount, move_type=Movement.TYPES['OUT'])
    DBSession.add(movement_out)

    movement_in = Movement(player=in_player, amount=amount, move_type=Movement.TYPES['IN'])
    DBSession.add(movement_in)

    out_player.update_balance(operation_type=Movement.TYPES['OUT'], amount=amount)
    in_player.update_balance(operation_type=Movement.TYPES['IN'], amount=amount)

    DBSession.flush()
    DBSession.commit()


def add_money(player_in, amount):
    in_player = Player.query.filter(Player.id == int(player_in)).first()

    movement_in = Movement(player=in_player, amount=amount, move_type=Movement.TYPES['IN'])
    DBSession.add(movement_in)

    in_player.update_balance(operation_type=Movement.TYPES['IN'], amount=amount)

    DBSession.flush()
    DBSession.commit()


def subtract_money(player_out, amount):
    out_player = Player.query.filter(Player.id == int(player_out)).first()

    movement_out = Movement(player=out_player, amount=amount, move_type=Movement.TYPES['OUT'])
    DBSession.add(movement_out)

    out_player.update_balance(operation_type=Movement.TYPES['OUT'], amount=amount)

    DBSession.flush()
    DBSession.commit()
