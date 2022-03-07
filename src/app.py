from datetime import timedelta
import json
from time import strftime
from flask import Flask, redirect,render_template, request,g,flash, session
# from an import Tuple

config = {
    "SECRET_KEY":"afas34$$56sad9}{`0df",
    "PERMANENT_SESSION_LIFETIME": timedelta(hours=5),
    }


app = Flask(__name__)

app.config.from_mapping(config)

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
    jogadores = load_jogadores()
    if nome in jogadores:
        flash("jogador "+nome+" já existe!","info")
        return redirect("/")

    if old_nome:=session.get("nome"):
        session.pop("nome")
        jogadores.pop(old_nome)
        flash(f"{old_nome} retirado","info")
    
    session.update({"nome":nome})

    jogadores.update({nome:25000})
    save_jogadores(jogadores)

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
        jogadores.pop('start')
        return render_template(
            "jogo.html",
            jogadores=jogadores,
            me=session.get('nome',False) 
        )
    else:
        jogadores.pop('start')
        return render_template(
            "index.html",
            jogadores=jogadores,
            me=session.get('nome',False) 
        )


def load_jogadores()->dict:
    
    jogdores:dict
    
    with open("bd.json") as file:
        jogadores = json.loads(
            file.read()
    )
    return jogadores

def load_history()->list:
    
    hisory:dict
    
    with open("history.json") as file:
        history = json.loads(
            file.read()
    )
    return history

def save_jogadores(jogadores:dict):    
    with open("bd.json",'w') as file:
        return file.write(
            json.dumps(jogadores)
        )

def save_jogo():
    jogadores = load_jogadores()
    history = load_history()
    jogadores.update(
        {"datetime":strftime("%d/%m/%Y - %H:%M:%S")}
    )
    history.append(jogadores)
    with open("history.json",'w') as file:
        return file.write(
            json.dumps(history)
        )


