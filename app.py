import streamlit as st
from supabase import create_client, Client
import time


URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]


supabase: Client = create_client(URL, KEY)

# Criar registros
def add_alunos(nome, email, cidade):
    supabase.table("alunos").insert({
        "nome" : nome,
        "email": email,
        "cidade" :cidade
    }).execute()


# Ler os dados da tabela
def get_alunos():
    resposta = supabase.table("alunos").select("*").order("nome").execute()
    return resposta.data

# Updates na tabela
def update_alunos(id, nome, email, cidade):
    supabase.table("alunos").update({
        "nome" : nome,
        "email": email,
        "cidade" :cidade
    }).eq("id", id).execute()

# Delete
def delete_aluno(id):
    supabase.table("alunos").delete().eq("id", id).execute()
    
# Iniciando com o Streamlit
st.title("Aprendendo CRUD")

read_alunos, create_aluno, aba_editar, aba_excluir = st.tabs(["Ver Alunos", "Criar Aluno", "Editar Alunos", " Remover Alunos"])

with read_alunos:
    alunos = get_alunos()
    if alunos:
        for x in alunos:
            st.write(f"**{x["nome"]}**-- {x["email"]} -- {x["cidade"]}")

with create_aluno:
    with st.form("nome_aluno"):
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        cidade = st.text_input("Cidade")
        if st.form_submit_button("Adicionar"):
            if nome and email:
                add_alunos(nome, email, cidade)
                st.success(f"O {nome} foi salvo com sucesso!")
                time.sleep(20)
                st.rerun()
            else:
                st.warning("Nome e email são obrigatorios")
            
# --- UPDATE ---
with aba_editar:
    alunos = get_alunos()
    if alunos:
        opcoes = {f"{a['nome']} ({a['email']})": a for a in alunos}
        selecionado = st.selectbox("Selecione", list(opcoes.keys()), key="edit_select")
        aluno = opcoes[selecionado]

        with st.form("form_editar"):
            novo_nome = st.text_input("Nome", value=aluno["nome"])
            novo_email = st.text_input("Email", value=aluno["email"])
            nova_cidade = st.text_input("Cidade", value=aluno.get("cidade") or "")

            if st.form_submit_button("Salvar"):
                update_aluno(aluno["id"], novo_nome, novo_email, nova_cidade)
                st.success("Atualizado!")
                st.rerun()
    else:
        st.info("Nenhum aluno para editar.")

# --- DELETE ---
with aba_excluir:
    alunos = get_alunos()
    if alunos:
        opcoes = {f"{a['nome']} ({a['email']})": a for a in alunos}
        selecionado = st.selectbox("Selecione", list(opcoes.keys()), key="del_select")
        aluno = opcoes[selecionado]

        st.warning(f"Você está prestes a excluir: **{aluno['nome']}**")

        if st.button("Excluir", type="primary"):
            delete_aluno(aluno["id"])
            st.success("Excluído!")
            st.rerun()
    else:
        st.info("Nenhum aluno para excluir.")



       
    
        













