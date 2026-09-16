import re
import json
from pathlib import Path
import requests
import streamlit as st

REFERENCIAS = """## REFERÊNCIAS

1. CARNEIRO, Celso Dal Ré; MIZUSAKI, Ana Maria Pimentel; ALMEIDA, Fernando Flávio Marques de. *A determinação da idade das rochas*. *Terræ Didatica*, Campinas, SP, v. 1, n. 1, p. 6–35, 2005. DOI: [https://doi.org/10.20396/td.v1i1.8637442](https://doi.org/10.20396/td.v1i1.8637442). Disponível em: [https://periodicos.sbu.unicamp.br/ojs/index.php/td/article/view/8637442](https://periodicos.sbu.unicamp.br/ojs/index.php/td/article/view/8637442).

2. INTERNATIONAL COMMISSION ON STRATIGRAPHY. *International Chronostratigraphic Chart: v2026/06*. [S. l.]: International Commission on Stratigraphy, 2026. Disponível em: [https://stratigraphy.org/chart/](https://stratigraphy.org/chart/).

3. NATIONAL PARK SERVICE. *Geologic Time Scale*. [S. l.]: U.S. National Park Service, 2018. Disponível em: [https://www.nps.gov/subjects/geology/time-scale.htm](https://www.nps.gov/subjects/geology/time-scale.htm)."""

st.set_page_config(page_title="PPCC (DGL7067): ESCALA DE TEMPO GEOLÓGICO", page_icon=None, layout="wide")

st.markdown("""<style>
    .cabecalho-banner {
        width: 100%;
        border-radius: 6px;
        overflow: hidden;
        margin: 0.5rem 0 1.25rem 0;
        border: 1px solid #63806F;
    }
    .momento-box {
        background-color: #285A63;
        color: #FFFFFF;
        padding: 0.9rem 1.1rem;
        border-radius: 6px;
        margin: 0.5rem 0 1.2rem 0;
        border: 1px solid #3B747D;
    }
    .momento-box p {
        margin: 0;
        color: #FFFFFF;
        font-size: 1.15rem;
        line-height: 1.5;
    }
    .escala-box {
        background-color: #3F6254;
        color: #FFFFFF;
        border: 1px solid #63806F;
        border-radius: 6px;
        padding: 0.25rem 0.8rem;
        margin: 0.4rem 0 1rem 0;
    }
    .escala-box table {
        width: 100%;
        border-collapse: collapse;
        color: #FFFFFF;
    }
    .escala-box th, .escala-box td {
        padding: 0.55rem 0.7rem;
        text-align: left;
        color: #FFFFFF;
        border-bottom: 1px solid #63806F;
    }
    .escala-box tr:last-child td {
        border-bottom: none;
    }
    .escala-box th {
        font-weight: 600;
    }
    .contexto-box {
        background-color: #6B6248;
        color: #FFFFFF;
        border: 1px solid #847858;
        border-radius: 6px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0 1rem 0;
    }
    .contexto-box p {
        margin: 0;
        color: #FFFFFF;
        line-height: 1.5;
    }
    </style>""", unsafe_allow_html=True)

# ============================================================
# DADOS DA ESCALA DO TEMPO GEOLÓGICO
# ============================================================
INTERVALOS = [
    # Éon Hadeano
    {
        "inicio": 4540.0,
        "fim": 4031.0,
        "éon": "Hadeano",
        "era": "—",
        "período": "—",
    },

    # Éon Arqueano
    {
        "inicio": 4031.0,
        "fim": 3600.0,
        "éon": "Arqueano",
        "era": "Eoarqueano",
        "período": "—",
    },
    {
        "inicio": 3600.0,
        "fim": 3200.0,
        "éon": "Arqueano",
        "era": "Paleoarqueano",
        "período": "—",
    },
    {
        "inicio": 3200.0,
        "fim": 2800.0,
        "éon": "Arqueano",
        "era": "Mesoarqueano",
        "período": "—",
    },
    {
        "inicio": 2800.0,
        "fim": 2500.0,
        "éon": "Arqueano",
        "era": "Neoarqueano",
        "período": "—",
    },

    # Éon Proterozoico
    # Os períodos abaixo seguem as subdivisões cronológicas usadas pela ICS.
    {
        "inicio": 2500.0,
        "fim": 2300.0,
        "éon": "Proterozoico",
        "era": "Paleoproterozoico",
        "período": "Sideriano",
    },
    {
        "inicio": 2300.0,
        "fim": 2050.0,
        "éon": "Proterozoico",
        "era": "Paleoproterozoico",
        "período": "Riaciano",
    },
    {
        "inicio": 2050.0,
        "fim": 1800.0,
        "éon": "Proterozoico",
        "era": "Paleoproterozoico",
        "período": "Orosiriano",
    },
    {
        "inicio": 1800.0,
        "fim": 1600.0,
        "éon": "Proterozoico",
        "era": "Paleoproterozoico",
        "período": "Estateriano",
    },
    {
        "inicio": 1600.0,
        "fim": 1400.0,
        "éon": "Proterozoico",
        "era": "Mesoproterozoico",
        "período": "Calimiano",
    },
    {
        "inicio": 1400.0,
        "fim": 1200.0,
        "éon": "Proterozoico",
        "era": "Mesoproterozoico",
        "período": "Ectasiano",
    },
    {
        "inicio": 1200.0,
        "fim": 1000.0,
        "éon": "Proterozoico",
        "era": "Mesoproterozoico",
        "período": "Esteniano",
    },
    {
        "inicio": 1000.0,
        "fim": 720.0,
        "éon": "Proterozoico",
        "era": "Neoproterozoico",
        "período": "Toniano",
    },
    {
        "inicio": 720.0,
        "fim": 635.0,
        "éon": "Proterozoico",
        "era": "Neoproterozoico",
        "período": "Criogeniano",
    },
    {
        "inicio": 635.0,
        "fim": 538.8,
        "éon": "Proterozoico",
        "era": "Neoproterozoico",
        "período": "Ediacarano",
    },

    # Éon Fanerozoico — Paleozoico
    {
        "inicio": 538.8,
        "fim": 486.85,
        "éon": "Fanerozoico",
        "era": "Paleozoico",
        "período": "Cambriano",
    },
    {
        "inicio": 486.85,
        "fim": 443.1,
        "éon": "Fanerozoico",
        "era": "Paleozoico",
        "período": "Ordoviciano",
    },
    {
        "inicio": 443.1,
        "fim": 419.6,
        "éon": "Fanerozoico",
        "era": "Paleozoico",
        "período": "Siluriano",
    },
    {
        "inicio": 419.6,
        "fim": 358.9,
        "éon": "Fanerozoico",
        "era": "Paleozoico",
        "período": "Devoniano",
    },
    {
        "inicio": 358.9,
        "fim": 298.9,
        "éon": "Fanerozoico",
        "era": "Paleozoico",
        "período": "Carbonífero",
    },
    {
        "inicio": 298.9,
        "fim": 251.9,
        "éon": "Fanerozoico",
        "era": "Paleozoico",
        "período": "Permiano",
    },

    # Fanerozoico — Mesozoico
    {
        "inicio": 251.9,
        "fim": 201.4,
        "éon": "Fanerozoico",
        "era": "Mesozoico",
        "período": "Triássico",
    },
    {
        "inicio": 201.4,
        "fim": 143.1,
        "éon": "Fanerozoico",
        "era": "Mesozoico",
        "período": "Jurássico",
    },
    {
        "inicio": 143.1,
        "fim": 66.0,
        "éon": "Fanerozoico",
        "era": "Mesozoico",
        "período": "Cretáceo",
    },

    # Fanerozoico — Cenozoico
    {
        "inicio": 66.0,
        "fim": 23.04,
        "éon": "Fanerozoico",
        "era": "Cenozoico",
        "período": "Paleógeno",
    },
    {
        "inicio": 23.04,
        "fim": 2.58,
        "éon": "Fanerozoico",
        "era": "Cenozoico",
        "período": "Neógeno",
    },
    {
        "inicio": 2.58,
        "fim": 0.0,
        "éon": "Fanerozoico",
        "era": "Cenozoico",
        "período": "Quaternário",
    },
]

# ============================================================
# DESTAQUES DA HISTÓRIA DA TERRA
# ============================================================
DESTAQUES = {
    "Hadeano": [
        ("Formação da Terra", "A Terra se formou há cerca de 4,54 bilhões de anos."),
        ("Formação da crosta", "Começaram a se formar os primeiros materiais rochosos e a diferenciação do planeta."),
        ("Primeiros ambientes aquosos", "Há evidências de que água líquida já estava presente muito cedo na história da Terra."),
    ],

    "Eoarqueano": [
        ("Evidências antigas de vida", "O registro geológico preserva algumas das evidências mais antigas de atividade biológica durante o Arqueano."),
        ("Estromatólitos", "Estruturas associadas a comunidades microbianas aparecem no registro geológico."),
        ("Atmosfera sem oxigênio livre", "A atmosfera terrestre ainda apresentava condições muito diferentes das atuais."),
    ],

    "Paleoarqueano": [
        ("Vida microbiana", "Organismos procariontes já faziam parte dos ecossistemas terrestres."),
        ("Estromatólitos", "Comunidades microbianas produziram estruturas que ficaram preservadas no registro geológico."),
        ("Primeiros continentes", "Núcleos continentais antigos começaram a se estabilizar."),
    ],

    "Mesoarqueano": [
        ("Diversificação microbiana", "Microrganismos continuaram ocupando e transformando ambientes aquáticos."),
        ("Estromatólitos abundantes", "Estruturas produzidas por comunidades microbianas são importantes registros da vida arqueana."),
        ("Atmosfera anóxica", "O oxigênio livre ainda não dominava a atmosfera."),
    ],

    "Neoarqueano": [
        ("Grande desenvolvimento da vida microbiana", "Comunidades microbianas eram amplamente distribuídas."),
        ("Cianobactérias e fotossíntese", "A fotossíntese oxigênica contribuiu para a transformação gradual da atmosfera."),
        ("Continentes mais estáveis", "Grandes blocos continentais começaram a adquirir maior estabilidade geológica."),
    ],

    "Paleoproterozoico": [
        ("Grande Evento de Oxidação", "O oxigênio passou a se acumular significativamente na atmosfera, transformando os oceanos e a biosfera."),
        ("Grandes glaciações", "O Paleoproterozoico inclui importantes episódios de glaciação em escala global."),
        ("Transformação dos oceanos", "O aumento do oxigênio alterou profundamente a química dos ambientes marinhos."),
    ],

    "Sideriano": [
        ("Oxigenação da atmosfera", "O intervalo inclui parte importante do processo de aumento do oxigênio atmosférico e mudanças na química dos oceanos."),
        ("Formações ferríferas bandadas", "Depósitos ricos em ferro registram mudanças na química dos oceanos associadas à oxigenação do sistema terrestre."),
    ],

    "Riaciano": [
        ("Grande Evento de Oxidação", "O aumento do oxigênio atmosférico transformou progressivamente os oceanos e criou novas condições para a biosfera."),
        ("Glaciações paleoproterozoicas", "O intervalo inclui importantes episódios de glaciação, entre eles os eventos associados às glaciações huronianas."),
    ],

    "Orosiriano": [
        ("Transformações tectônicas", "O Paleoproterozoico foi marcado por intensa atividade tectônica e formação de grandes cinturões orogênicos."),
        ("Mudanças na biosfera", "A oxigenação iniciada anteriormente continuou alterando as condições ambientais disponíveis para a vida."),
    ],

    "Estateriano": [
        ("Oceanos e atmosfera em transformação", "Mudanças na química dos oceanos e da atmosfera acompanharam a evolução da biosfera proterozoica."),
        ("Evidências antigas de eucariotos", "O final do Paleoproterozoico e a transição para o Mesoproterozoico incluem alguns dos registros mais antigos de eucariotos."),
    ],

    "Calimiano": [
        ("Diversificação dos eucariotos", "O registro geológico preserva evidências de organismos eucarióticos durante o Mesoproterozoico."),
        ("Supercontinentes", "Grandes massas continentais passaram por ciclos de agregação e fragmentação durante o Mesoproterozoico."),
    ],

    "Ectasiano": [
        ("Diversificação eucariótica", "Organismos eucarióticos aparecem em registros fósseis e microfósseis cada vez mais diversos."),
        ("Ecossistemas marinhos", "Ambientes marinhos proterozoicos sustentavam comunidades microbianas e eucarióticas diversificadas."),
    ],

    "Esteniano": [
        ("Diversificação dos eucariotos", "O Mesoproterozoico tardio registra diversidade crescente de organismos eucarióticos."),
        ("Formação e fragmentação continental", "Grandes blocos continentais participaram de ciclos tectônicos que antecederam a reorganização do Neoproterozoico."),
    ],

    "Toniano": [
        ("Diversificação eucariótica", "O Neoproterozoico inicial preserva uma diversidade crescente de organismos eucarióticos e formas multicelulares."),
        ("Mudanças ambientais", "O intervalo foi marcado por mudanças tectônicas, químicas e ambientais que antecederam as grandes glaciações do Criogeniano."),
    ],

    "Criogeniano": [
        ("Glaciações criogenianas", "O planeta passou por episódios de glaciação extremamente intensos durante o Criogeniano."),
        ("Mudanças nos oceanos", "Os episódios glaciais alteraram profundamente as condições ambientais e a química dos oceanos."),
    ],

    "Ediacarano": [
        ("Biota de Ediacara", "Organismos multicelulares, muitos de corpo mole, são preservados em diversos depósitos do período."),
        ("Diversificação da vida", "Mudanças ambientais e biológicas do Ediacarano antecederam a grande diversificação registrada no Cambriano."),
    ],

    "Mesoproterozoico": [
        ("Diversificação dos eucariotos", "Organismos eucarióticos tornaram-se mais diversos e importantes nos ecossistemas durante o Proterozoico."),
        ("Vida multicelular", "O registro geológico preserva evidências de formas multicelulares cada vez mais complexas."),
        ("Supercontinentes", "Grandes massas continentais se organizaram e se fragmentaram ao longo do intervalo."),
    ],

    "Neoproterozoico": [
        ("Diversificação de organismos multicelulares", "A diversidade e a complexidade da vida aumentaram nos oceanos."),
        ("Glaciações criogenianas", "O planeta passou por episódios de glaciação extremamente intensos, associados à hipótese de uma Terra quase totalmente congelada."),
        ("Biota de Ediacara", "Organismos multicelulares de corpo mole aparecem no registro fossilífero do final do Proterozoico."),
        ("Preparação para o Fanerozoico", "Mudanças ambientais e biológicas antecederam a grande diversificação registrada no Cambriano."),
    ],

    "Cambriano": [
        ("Grande diversificação do Cambriano", "O registro fóssil mostra uma rápida diversificação de muitos grandes grupos de animais."),
        ("Artrópodes e trilobitas", "Trilobitas e outros artrópodes tornaram-se componentes importantes dos mares."),
        ("Primeiros vertebrados", "Os primeiros representantes do grupo dos vertebrados aparecem no registro cambriano."),
    ],

    "Ordoviciano": [
        ("Diversificação marinha", "Houve grande diversificação de organismos marinhos, incluindo braquiópodes, moluscos e outros grupos."),
        ("Origem dos vertebrados mandibulados", "A origem dos vertebrados mandibulados remonta ao Paleozoico inicial, com evidências importantes no final do Ordoviciano e no Siluriano."),
        ("Primeiras plantas terrestres", "Evidências indicam a presença de plantas muito simples ocupando ambientes terrestres."),
        ("Extinção do Ordoviciano", "Uma das grandes extinções em massa ocorreu no final do período."),
    ],

    "Siluriano": [
        ("Expansão da vida terrestre", "Plantas vasculares e artrópodes passaram a ocupar ambientes terrestres de maneira mais significativa."),
        ("Peixes com mandíbulas", "Peixes mandibulados diversificaram-se nos ambientes aquáticos."),
        ("Primeiros ecossistemas terrestres", "Comunidades terrestres tornaram-se progressivamente mais complexas."),
    ],

    "Devoniano": [
        ("Diversificação dos peixes", "O Devoniano é conhecido pela grande diversificação de peixes."),
        ("Primeiras florestas", "Florestas complexas se desenvolveram e transformaram os ambientes terrestres."),
        ("Primeiros tetrápodes", "Os primeiros vertebrados com características associadas à vida terrestre surgiram."),
        ("Crise do Devoniano", "O final do período foi marcado por importantes eventos de extinção."),
    ],

    "Carbonífero": [
        ("Grandes florestas", "Extensas florestas pantanosas contribuíram para a formação de importantes depósitos de carvão."),
        ("Diversificação dos tetrápodes", "Anfíbios e répteis diversificaram-se em diferentes ambientes."),
        ("Insetos gigantes", "Alguns artrópodes atingiram tamanhos muito superiores aos encontrados atualmente."),
    ],

    "Permiano": [
        ("Pangeia", "Os continentes estavam reunidos no supercontinente Pangeia."),
        ("Diversificação dos amniotas", "Répteis e sinapsídeos tornaram-se importantes componentes dos ecossistemas terrestres."),
        ("Grande Extinção do Permiano", "A maior extinção em massa conhecida encerrou o período e remodelou a vida na Terra."),
    ],

    "Triássico": [
        ("Primeiros dinossauros", "Os primeiros dinossauros surgiram durante o Triássico."),
        ("Primeiros mamíferos", "Os primeiros mamíferos apareceram no Triássico."),
        ("Pangeia começa a se fragmentar", "A fragmentação do supercontinente começou durante o Mesozoico."),
        ("Extinção do Triássico", "Uma importante extinção em massa ocorreu no final do período."),
    ],

    "Jurássico": [
        ("Diversificação dos dinossauros", "Dinossauros tornaram-se muito diversos e abundantes nos ecossistemas terrestres."),
        ("Primeiras aves", "As primeiras aves conhecidas surgiram durante o Jurássico."),
        ("Grandes répteis marinhos", "Ictiossauros e plesiossauros eram componentes importantes dos mares."),
        ("Fragmentação de Pangeia", "A abertura de novos oceanos avançou e aproximou os continentes de suas configurações modernas."),
    ],

    "Cretáceo": [
        ("Plantas com flores", "As angiospermas se diversificaram e passaram a ocupar papel importante nos ecossistemas."),
        ("Diversificação dos dinossauros", "Dinossauros continuaram a ocupar grande diversidade de nichos terrestres."),
        ("Diversificação de aves e mamíferos", "Aves e mamíferos passaram por importantes diversificações."),
        ("Extinção Cretáceo–Paleógeno", "Há cerca de 66 milhões de anos ocorreu uma grande extinção, associada ao impacto de um asteroide e a outros fatores ambientais."),
    ],

    "Paleógeno": [
        ("Diversificação dos mamíferos", "Após a extinção do fim do Cretáceo, mamíferos e aves passaram por importante diversificação."),
        ("Primeiros primatas", "Primatas aparecem e se diversificam durante o Cenozoico inicial."),
        ("Novos ecossistemas", "Florestas e outros ambientes terrestres passaram por grandes mudanças."),
    ],

    "Neógeno": [
        ("Expansão das gramíneas", "Ecossistemas de campos e savanas se expandiram em várias regiões."),
        ("Diversificação dos hominínios", "A linhagem evolutiva que inclui os seres humanos passou por importantes mudanças."),
        ("Grandes mamíferos", "Diversos grupos de mamíferos modernos se diversificaram."),
    ],

    "Quaternário": [
        ("Glaciações", "Grandes ciclos glaciais modificaram paisagens, oceanos e ecossistemas."),
        ("Evolução e dispersão do gênero Homo", "Diferentes espécies humanas ocuparam e posteriormente se dispersaram por várias regiões."),
        ("Homo sapiens", "Nossa espécie surgiu durante o Pleistoceno e posteriormente se espalhou pelo planeta."),
        ("Holoceno", "O intervalo atual começou após a última grande fase glacial e inclui o desenvolvimento das sociedades humanas."),
    ],
}

# ============================================================
# FUNÇÕES
# ============================================================
def converter_duracao(texto):
    texto = str(texto).strip().lower()
    if not texto: return None
    if ":" in texto:
        partes = texto.split(":")
        try:
            if len(partes) == 3:
                h,m,s = map(int,partes)
                if h < 0 or m < 0 or s < 0 or m >= 60 or s >= 60: return None
                return h*3600+m*60+s
            if len(partes) == 2:
                m,s = map(int,partes)
                if m < 0 or s < 0 or s >= 60: return None
                return m*60+s
        except ValueError: return None
    p = re.fullmatch(r"\s*(?:(\d+(?:[.,]\d+)?)\s*h)?\s*(?:(\d+(?:[.,]\d+)?)\s*min)?\s*(?:(\d+(?:[.,]\d+)?)\s*s)?\s*",texto)
    if p and any(p.groups()):
        try:
            h=float((p.group(1) or "0").replace(",",".")); m=float((p.group(2) or "0").replace(",",".")); s=float((p.group(3) or "0").replace(",","."))
            if h<0 or m<0 or s<0 or m>=60 or s>=60: return None
            return int(round(h*3600+m*60+s))
        except ValueError: return None
    try:
        m=float(texto.replace(",",".")); return int(round(m*60)) if m>=0 else None
    except ValueError: return None

def formatar_tempo(segundos):
    segundos=int(round(segundos)); h=segundos//3600; m=(segundos%3600)//60; s=segundos%60
    return f"{h:02d}:{m:02d}:{s:02d}"

def formatar_idade(idade_ma):
    if idade_ma >= 1000: return f"{idade_ma/1000:.3f} Ga"
    if idade_ma >= 1: return f"{idade_ma:.2f} Ma"
    if idade_ma >= 0.001: return f"{idade_ma*1000:.1f} ka"
    return f"{idade_ma*1_000_000:,.0f} anos".replace(",", ".")

def localizar_tempo_geologico(idade_ma):
    for intervalo in INTERVALOS:
        if intervalo["fim"] < idade_ma <= intervalo["inicio"]: return intervalo
    if idade_ma == 0: return INTERVALOS[-1]
    return None

def eventos_do_intervalo(intervalo):
    periodo=intervalo.get("período"); era=intervalo.get("era"); eon=intervalo.get("éon")
    if periodo and periodo != "—" and periodo in DESTAQUES: eventos=DESTAQUES[periodo]
    elif era in DESTAQUES: eventos=DESTAQUES[era]
    else: eventos=DESTAQUES.get(eon, [])
    return eventos[:2]

def extrair_json(texto):
    texto=texto.strip()
    if texto.startswith("```"):
        texto=re.sub(r"^```(?:json)?\s*","",texto); texto=re.sub(r"\s*```$","",texto)
    i=texto.find("{"); j=texto.rfind("}")
    if i==-1 or j==-1: return None
    try: return json.loads(texto[i:j+1])
    except json.JSONDecodeError: return None

def consultar_duracao_ia(nome_obra):
    api_key=st.secrets.get("GEMINI_API_KEY","")
    if not api_key:
        return {"ok":False,"erro":"A consulta automática não está configurada. Adicione GEMINI_API_KEY aos Secrets do Streamlit."}
    prompt = """
Pesquise na Web a duração da obra chamada: "__OBRA__".
Identifique a obra correta, incluindo ano quando necessário.
Para filme, use a duração do longa correspondente.
Para episódio de série, use a duração do episódio.
Não invente a duração.
Retorne SOMENTE JSON válido:
{
  "obra_identificada": "string",
  "ano": "string",
  "duracao_minutos": 127,
  "fonte_principal": "string",
  "url_fonte": "https://...",
  "observacao": "string"
}
""".replace("__OBRA__", nome_obra)

    url="https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key="+api_key
    payload={"contents":[{"parts":[{"text":prompt}]}],"tools":[{"google_search":{}}]}
    try:
        r=requests.post(url,json=payload,timeout=45); r.raise_for_status(); data=r.json()
        candidates=data.get("candidates",[])
        if not candidates: return {"ok":False,"erro":"A consulta não retornou uma resposta."}
        parts=candidates[0].get("content",{}).get("parts",[])
        text="\n".join(p.get("text","") for p in parts if p.get("text"))
        result=extrair_json(text)
        if not result: return {"ok":False,"erro":"A resposta da consulta não pôde ser interpretada."}
        try: minutos=int(round(float(result.get("duracao_minutos"))))
        except (TypeError,ValueError): return {"ok":False,"erro":"A consulta não forneceu uma duração numérica válida."}
        if minutos<=0 or minutos>10000: return {"ok":False,"erro":"A duração retornada parece inválida."}
        fontes=[]
        gm=candidates[0].get("groundingMetadata",{})
        for chunk in gm.get("groundingChunks",[]):
            web=chunk.get("web",{})
            if web.get("uri"): fontes.append({"titulo":web.get("title") or web["uri"],"url":web["uri"]})
        if fontes: fonte,url_fonte=fontes[0]["titulo"],fontes[0]["url"]
        else: fonte,url_fonte=result.get("fonte_principal") or "Fonte retornada pela consulta",result.get("url_fonte") or ""
        return {"ok":True,"obra":result.get("obra_identificada") or nome_obra,"ano":result.get("ano",""),"duracao_minutos":minutos,"fonte":fonte,"url":url_fonte,"observacao":result.get("observacao","")}
    except requests.RequestException as exc: return {"ok":False,"erro":f"Não foi possível consultar a IA: {exc}"}
    except Exception as exc: return {"ok":False,"erro":f"Erro inesperado na consulta: {exc}"}

def tempo_da_idade(idade_ma,duracao):
    return max(0,min(1,1-idade_ma/4540.0))*duracao

# ============================================================
# INTERFACE
# ============================================================
st.title("PPCC (DGL7067): ESCALA DE TEMPO GEOLÓGICO")
st.markdown("Uma proposta de representação proporcional da história da Terra através da duração de uma obra audiovisual. Consulte uma obra, obtenha sua duração e observe como toda a escala de tempo geológico pode ser representada dentro dela.")

imagem_banner=Path("imagens")/"banner_cabecalho.png"
if imagem_banner.exists():
    st.markdown('<div class="cabecalho-banner">',unsafe_allow_html=True); st.image(str(imagem_banner),use_container_width=True); st.markdown("</div>",unsafe_allow_html=True)

st.divider()
st.subheader("Consulta de uma obra")
nome_obra=st.text_input("NOME DA OBRA PARA CONSULTA:",placeholder="Ex.: Jurassic Park")
consultar=st.button("CONSULTAR DURAÇÃO E GERAR ESCALA",type="primary",use_container_width=True)

if consultar:
    nome_obra=nome_obra.strip()
    if not nome_obra: st.error("Informe o nome de uma obra."); st.stop()
    with st.spinner("Consultando a obra e verificando sua duração..."): consulta=consultar_duracao_ia(nome_obra)
    if not consulta["ok"]:
        st.error(consulta["erro"]); st.info("O programa não faz o cálculo quando não consegue obter uma duração consultável."); st.stop()
    duracao=consulta["duracao_minutos"]*60
    st.divider(); st.subheader("Obra consultada")
    ano=f' ({consulta["ano"]})' if consulta["ano"] else ""
    st.markdown(f'<div class="momento-box"><p><strong>{consulta["obra"]}{ano}</strong></p><p style="font-size:1.05rem;margin-top:0.35rem;">Duração utilizada pelo algoritmo: <strong>{formatar_tempo(duracao)}</strong></p></div>',unsafe_allow_html=True)
    st.caption(f"Primeira fonte retornada pela consulta com busca na Web: {consulta['fonte']}")
    if consulta.get("url"): st.markdown(f"Fonte: {consulta['url']}")
    if consulta.get("observacao"): st.caption(consulta["observacao"])
    st.markdown('<div class="contexto-box">A duração acima é a entrada do algoritmo. A identificação de éon, era, período e idade geológica é feita pelo programa a partir da duração consultada e dos limites cadastrados da escala geológica.</div>',unsafe_allow_html=True)

    st.subheader("A obra representada como escala de tempo geológico")
    st.write("A tabela divide proporcionalmente toda a duração da obra entre os intervalos geológicos cadastrados. Os horários indicam em que ponto da obra cada limite geológico seria alcançado.")

    linhas=[]
    for intervalo in INTERVALOS:
        inicio_obra=tempo_da_idade(intervalo["inicio"],duracao); fim_obra=tempo_da_idade(intervalo["fim"],duracao)
        eventos=eventos_do_intervalo(intervalo)
        eventos_html="<br>".join(f"• <strong>{titulo}</strong>: {texto}" for titulo,texto in eventos)
        linhas.append(f'<tr><td>{formatar_tempo(inicio_obra)} – {formatar_tempo(fim_obra)}</td><td>{formatar_idade(intervalo["inicio"])} – {formatar_idade(intervalo["fim"])}</td><td>{intervalo["éon"]}</td><td>{intervalo["era"]}</td><td>{intervalo["período"]}</td><td>{eventos_html or "Sem acontecimentos cadastrados."}</td></tr>')

    st.markdown(f'<div class="escala-box"><table><thead><tr><th>Momento na obra</th><th>Idade geológica</th><th>Éon</th><th>Era</th><th>Período</th><th>Acontecimentos de contexto</th></tr></thead><tbody>{"".join(linhas)}</tbody></table></div>',unsafe_allow_html=True)
    st.markdown('<div class="contexto-box">Os acontecimentos apresentados nas tabelas são associados aos respectivos intervalos geológicos e servem como contexto didático. Eles não significam que tenham ocorrido exatamente no instante da obra indicado pela analogia.</div>',unsafe_allow_html=True)

    with st.expander("Como o cálculo foi realizado"):
        st.code("idade = 4540 Ma × (1 − momento / duração)")
        st.write("A IA é utilizada somente para localizar a duração da obra e fornecer uma fonte consultada. A classificação geológica é realizada pelo algoritmo local.")

st.divider()
tab_sobre,tab_referencias,tab_codigo=st.tabs(["SOBRE O PPCC","REFERÊNCIAS","ACESSO AO CÓDIGO FONTE"])
with tab_sobre:
    col_texto,col_imagem=st.columns([1.35,1])
    with col_texto:
        st.markdown("""Esse programa simples é uma proposta de ferramenta didática/Artefato pedagógico que utiliza a duração de obras e gravações audiovisuais como uma representação proporcional da história da Terra. Idealizado como material didático sujeito a avaliação da disciplina Paleontologia DGL7067-07110 (2026.2) do currículo de Licenciatura em Ciências Biológicas da Universidade Federal de Santa Catarina.

#### COMO FUNCIONA?

A duração total da obra é considerada como uma representação da história da Terra, desde sua formação até o presente momento.

A duração é consultada automaticamente e depois utilizada pelo algoritmo. A inteligência artificial não determina a idade geológica nem a classificação do intervalo: essas etapas são calculadas pelo programa.

#### OBJETIVOS

A proposta é utilizar uma referência familiar para ajudar a visualizar a dimensão da escala temporal geológica.

#### IMPORTANTE

A correspondência produzida pelo programa é uma representação matemática e didática, com aproximações e valores arredondados, a fim de se tornar mais fácil a interpretação para estudantes do Ensino Médio.

O resultado deve ser interpretado como uma analogia entre duas escalas temporais.""")
    with col_imagem:
        imagem_programa=Path("imagens")/"sobre_o_programa.png"
        if imagem_programa.exists(): st.image(str(imagem_programa),caption="PPCC (DGL7067): Escala de Tempo Geológico",use_container_width=True)
with tab_referencias: st.markdown(REFERENCIAS)
with tab_codigo:
    st.markdown("O código-fonte do artefato será disponibilizado nesta seção.\n\nA consulta automática utiliza a API Gemini com busca na Web. A chave da API deve ser armazenada nos Secrets do Streamlit e não deve ser colocada no código ou publicada no GitHub.")
    st.info("O acesso público ao código pode ser consultado, baixado e modificado em https://github.com/jgspinelli/ppcc-dgl7067-2026.2.")
st.caption("PPCC (DGL7067): ESCALA DE TEMPO GEOLÓGICO.")
