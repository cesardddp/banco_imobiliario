from enum import unique
from banco_imb import __version__
from banco_imb.db import Config, SqliteDatabase,Player
from banco_imb.db import PlayerOps
import peewee
import pytest


@pytest.fixture(autouse=False)
def db_test():
    # Setup DB here
    db_teste = SqliteDatabase(':memory:')
    class Player_teste(Player):

        class Meta:
            database = db_teste # This model uses the "people.db" database.
    class Config_teste(Config):

        class Meta:
            database = db_teste # This model uses the "people.db" database.
    
    setattr(db_teste,"Player", Player_teste)
    setattr(db_teste,"Config", Config_teste)
    
    try:
        Player_teste.create_table()
        Config_teste.create_table()
        Config_teste(state=False).save()

    except:
        breakpoint()
    else:
        print("Tabela 'Player_teste' criada com sucesso!")
        print("Tabela 'Config_teste' criada com sucesso!")


    # Yield some data, database connection or nothing at all
    yield db_teste

    # Delete DB here when the test ends
    db_teste.drop_tables([Player_teste,Config_teste])

@pytest.fixture(autouse=False)
def player_ops(db_test):
    return PlayerOps(db_test)


@pytest.fixture(autouse=False)
def player_teste(db_test):
    p_teste = db_test.Player(name="lara",cash=25000.0)
    p_teste.save()
    # grandma = db_test.Player.get(db_test.Player == p)
    return p_teste
    
@pytest.fixture(autouse=False)
def multiple_players_teste(db_test):
    players = [
        db_test.Player.create(**{'name': 'p_'+str(_),'cash': 25000.0})
        for _ in range(5)
    ]
    return players


def test_delete_player(db_test,player_ops:PlayerOps,player_teste):
    result = player_ops.delete_player(player_teste.id)
    assert result == player_teste.id
    with pytest.raises(peewee.DoesNotExist) as e_info:
        db_test.Player.get(db_test.Player.name==player_teste.name)

    result = player_ops.delete_player(5)
    assert result is 0

def test_game_is_runing(db_test,player_ops:PlayerOps):
    assert False == player_ops.game_is_runing()
    assert True == player_ops.game_is_runing(change=True)
    assert False == player_ops.game_is_runing(change=True)


def teste_unique_name_new_player_other_name(player_ops:PlayerOps):

    n = player_ops.new_player(name="testa",cash=25000.0)
    assert n > 0

def test_get_player_by_name_exist(player_ops:PlayerOps,player_teste):
    # breakpoint()
    player_finded = player_ops.get_player_by_name(player_teste.name)
    assert player_finded == player_teste

def test_get_player_by_name_dont_exist(player_ops:PlayerOps,player_teste):
    with pytest.raises(peewee.DoesNotExist) as e_info:
        player_finded = player_ops.get_player_by_name("NOONE")
        assert player_finded == player_teste

def test_load_jogadores(player_ops:PlayerOps,multiple_players_teste):

    for player in player_ops.load_jogadores():
        assert player in multiple_players_teste

def teste_unique_name_new_player_same_name(player_ops:PlayerOps,db_test):
    player_teste = db_test.Player(name="teste",cash=25000.0)
    player_teste.save()
    with pytest.raises(peewee.IntegrityError) as e_info:
        n = player_ops.new_player(name="teste",cash=25000.0)
        assert n > 0
