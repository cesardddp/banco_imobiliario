from datetime import timedelta
import json
import logging
import os
from time import strftime
from flask import Flask, redirect,render_template, request,g,flash, session
from .db import load_history,load_jogadores,save_jogadores,save_jogo,get_ops_instance
import peewee
config = {
    "SECRET_KEY":"afas34$$56sad9}{`0df",
    "PERMANENT_SESSION_LIFETIME": timedelta(hours=5),
    }


app = Flask(__name__)

app.config.from_mapping(config)
db = get_ops_instance()

# @app.before_first_request
# def cria_db_and_hist():
#     os.path.exists()

@app.before_request
def check():
    if load_jogadores(): ...

@app.post("/pagar")
def pagar():
    
    jogadores = load_jogadores()
    aviso = ""

    pagador_nome = request.form.get("pagador","")
    recebedor_nome = request.form.get("recebedor","")
    valor:int = int(request.form.get("valor",0))


    
    if pagador_nome:
        if (jogadores.get(pagador_nome) - valor) < 0 :
                flash(f"{pagador_nome.capitalize()}: JOGADOR SEM DINHEIRO","info")
                return redirect("/")
        jogadores.update({pagador_nome:jogadores[pagador_nome]-valor})
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
    # jogadores = load_jogadores()
    try:
        db.new_player(name=nome,cash=25_000.00)
    except peewee.IntegrityError as ie:
        #pra pegar unique name pewe
        flash(f"{nome} já existe! Tente outro")
        return redirect("/")

    if old_nome:=session.get("nome"):
        session.pop("nome")
        try:
            db.get_player_by_name(old_nome)
        except peewee.DoesNotExist as dne:
            logging.error("player saved in session do not exist in db!\nDetails: "+str(dne))
            
        flash(f"{old_nome} retirado","info")
    
    session.update({"nome":nome})

    # jogadores.update({"name":nome,"cash":25000})
    # save_jogadores(jogadores)

    return redirect("/")


@app.route("/novo_jogo",methods=("GET","POST"))
def novo_jogo():
    nome = ""
    if request.method == "POST":
        nome = request.form.get("nome","").strip()
        session.setdefault("nome",nome)

    return render_template("novo_jogo.html",nome=nome)


@app.post("/start")
def start():
    j = load_jogadores()
    j.update({"start":True})
    save_jogadores(j)
    return redirect("/")

@app.post("/end")
def end():
    j = load_jogadores()
    j.update({"start":False})
    save_jogadores(j)
    save_jogo()
    return redirect("/")


@app.get("/")
def index():
    jogadores=load_jogadores()

    if jogadores.get('start'):
        try:
            jogadores.pop('start')
        except KeyError:
            logging.error("no start set")
        return render_template(
            "jogo.html",
            jogadores=jogadores,
            me=session.get('nome',False) 
        )
    else:
        try:
            jogadores.pop('start')
        except KeyError:
            logging.error("no start set")
        return render_template(
            "index.html",
            jogadores=jogadores,
            me=session.get('nome',False) 
        )



