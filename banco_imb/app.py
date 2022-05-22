from copy import copy, deepcopy
from datetime import timedelta
import json
import logging
import os
from time import strftime
from flask import Flask, jsonify, redirect,render_template, request,g,flash, session
from .db import save_jogadores,get_ops_instance,main as db_main
import peewee
import error_classes

config = {
    "SECRET_KEY":"afas34$$56sad9}{`0df",
    "PERMANENT_SESSION_LIFETIME": timedelta(hours=5),
    }


app = Flask(__name__)

SESSION_NAME = "name"

app.config.from_mapping(config)
db = get_ops_instance()

@app.before_first_request
def set_database():
    db_main()
# @app.before_first_request
# def cria_db_and_hist():
#     os.path.exists()

@app.before_request
def check():
    name = session.get(SESSION_NAME,"")
    try:
        db.get_player_by_name(name)
    except peewee.DoesNotExist as dne:
        if name: session.pop(SESSION_NAME)


@app.post("/pagar")
def pagar():
    
    jogadores = db.load_jogadores()
    aviso = ""

    pagador_nome = request.form.get("pagador","")
    recebedor_nome = request.form.get("recebedor","")
    valor:int = int(request.form.get("valor",0))


    breakpoint()
    if pagador_nome:
        try:
            db.cash_transition(pagador_nome,recebedor_nome,valor)
        except error_classes.PlayerGoingBankrupt:
            flash(f"{pagador_nome.capitalize()}: JOGADOR SEM DINHEIRO","info")
        else:
            aviso += f"{pagador_nome.capitalize()} pagou ${valor}"

    if recebedor_nome:# or recebedor_nome=="banco":
        jogadores.update({
            recebedor_nome:jogadores[recebedor_nome]+valor
        }
    )
        aviso += f"\n{recebedor_nome.capitalize()} recebeu ${valor}"


    msg = save_jogadores(jogadores)

    flash(("Transeferencia realizada!\n" if msg else "Erro!\n") + aviso,'info')

    return redirect("/")
    

@app.route("/novo_jogador",methods=("POST",))
def novo_jogador():

    nome = request.form.get("nome","").strip()
    # jogadores = db.load_jogadores()
    try:
        db.new_player(name=nome,cash=25_000.00)
    except peewee.IntegrityError as ie:
        #pra pegar unique name pewe
        flash(f"{nome} já existe! Tente outro")
        return redirect("/")

    if old_nome:=session.get(SESSION_NAME):
        session.pop(SESSION_NAME)
        try:
            old_p = db.get_player_by_name(old_nome)
            old_p.delete_instance()
        except peewee.DoesNotExist as dne:
            logging.error("player saved in session do not exist in db!\nDetails: "+str(dne))

        flash(f"{old_nome} retirado","info")
    
    session.update({SESSION_NAME:nome})

    # jogadores.update({SESSION_NAME:nome,"cash":25000})
    # save_jogadores(jogadores)

    return redirect("/")


@app.route("/novo_jogo",methods=("GET","POST"))
def novo_jogo():
    nome = ""
    if request.method == "POST":
        nome = request.form.get("nome","").strip()
        session.setdefault(SESSION_NAME,nome)

    return render_template("novo_jogo.html",nome=nome)


@app.post("/start")
def start():
    state = db.game_is_runing()
    if not state:db.game_is_runing(change=True)
    return redirect("/")

@app.post("/end")
def end():
    state = db.game_is_runing()
    if state:db.game_is_runing(change=True)
    return redirect("/")


@app.get("/")
def index():
    jogadores=db.load_jogadores()
    if db.game_is_runing():
        jogadores_list=[
            {"name":j.name,"cash":j.cash,"id":j.id}
            for j in jogadores
            ]
        return render_template(
            "jogo.html",
            jogadores=jogadores_list,
            me=session.get('name',False) 
        )
    else:
        # jogadores_options = [
        #     {
        #         "value": j.id,
        #         "text": j.name
        #     } for j in 
        # ]
        return render_template(
            "index.html",
            jogadores=jogadores,
            me=session.get('name',False) 
        )


@app.delete("/delete/<int:pk>")
def delete_player(pk):
    
    if result:=db.delete_player(pk) > 0:
        return jsonify(id=result),200
    return "",404


