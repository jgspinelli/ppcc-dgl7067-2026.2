import re
from pathlib import Path

import streamlit as st


# ============================================================
# CONFIGURAÇÃO
# ============================================================



REFERENCIAS = """
## REFERÊNCIAS

1. CARNEIRO, Celso Dal Ré; MIZUSAKI, Ana Maria Pimentel; ALMEIDA, Fernando Flávio Marques de. *A determinação da idade das rochas*. *Terræ Didatica*, Campinas, SP, v. 1, n. 1, p. 6–35, 2005. DOI: [https://doi.org/10.20396/td.v1i1.8637442](https://doi.org/10.20396/td.v1i1.8637442). Disponível em: [https://periodicos.sbu.unicamp.br/ojs/index.php/td/article/view/8637442](https://periodicos.sbu.unicamp.br/ojs/index.php/td/article/view/8637442).

2. INTERNATIONAL COMMISSION ON STRATIGRAPHY. *International Chronostratigraphic Chart: v2026/06*. [S. l.]: International Commission on Stratigraphy, 2026. Disponível em: [https://stratigraphy.org/chart/](https://stratigraphy.org/chart/).

3. NATIONAL PARK SERVICE. *Geologic Time Scale*. [S. l.]: U.S. National Park Service, 2018. Disponível em: [https://www.nps.gov/subjects/geology/time-scale.htm](https://www.nps.gov/subjects/geology/time-scale.htm).
"""

st.set_page_config(
    page_title="PPCC (DGL7067): ESCALA DE TEMPO GEOLÓGICO",
    page_icon=None,
    layout="wide",
)


# ============================================================
# IMAGENS CHAMATIVAS, TIRADAS DO CANVA
# ============================================================

st.markdown(
    """
    <style>
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
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DADOS DA ESCALA DO TEMPO GEOLÓGICO
# ============================================================
#
# Atenção: Idades em Ma antes do presente.
# (referência numérica geral da história da Terra usada para a
# proporção é 4,54 Ga (4540 Ma) - LEVAR EM CONSIDERAÇÃO PARA NÃO CONFUNDIR Ma COM Ga.
#
# Os limites simplificados para fins didáticos
# a escala internacional atual (ICS), mantendo a  classificação em Éo/Era/Período
#
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
#
# Os destaques são apresentados como acontecimentos associados
# ao intervalo geológico encontrado pelo cálculo.
# As idades são aproximadas e têm finalidade didática.
# 
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
    """Converte duração para segundos.

    Aceita:
    - HH:MM:SS
    - MM:SS
    - 2h07min31s
    - 2h 7min 31s
    - apenas número, interpretado como minutos
    """
    texto = texto.strip().lower()

    if not texto:
        return None

    # HH:MM:SS ou MM:SS
    if ":" in texto:
        partes = texto.split(":")
        try:
            if len(partes) == 3:
                horas = int(partes[0])
                minutos = int(partes[1])
                segundos = int(partes[2])

                if horas < 0 or minutos < 0 or segundos < 0:
                    return None
                if minutos >= 60 or segundos >= 60:
                    return None

                return horas * 3600 + minutos * 60 + segundos

            if len(partes) == 2:
                minutos = int(partes[0])
                segundos = int(partes[1])

                if minutos < 0 or segundos < 0 or segundos >= 60:
                    return None

                return minutos * 60 + segundos

        except ValueError:
            return None

    # Formatos textuais
    padrao = re.fullmatch(
        r"\s*(?:(\d+(?:[.,]\d+)?)\s*h)?\s*"
        r"(?:(\d+(?:[.,]\d+)?)\s*min)?\s*"
        r"(?:(\d+(?:[.,]\d+)?)\s*s)?\s*",
        texto,
    )

    if padrao and any(padrao.groups()):
        try:
            horas = float((padrao.group(1) or "0").replace(",", "."))
            minutos = float((padrao.group(2) or "0").replace(",", "."))
            segundos = float((padrao.group(3) or "0").replace(",", "."))

            if horas < 0 or minutos < 0 or segundos < 0:
                return None
            if minutos >= 60 or segundos >= 60:
                return None

            total = horas * 3600 + minutos * 60 + segundos
            return total if total > 0 else None

        except ValueError:
            return None

    # Apenas número = minutos
    try:
        minutos = float(texto.replace(",", "."))
        if minutos > 0:
            return minutos * 60
    except ValueError:
        pass

    return None


def formatar_tempo(segundos):
    """Converte segundos para HH:MM:SS."""
    segundos = int(round(segundos))
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos_restantes = segundos % 60
    return f"{horas:02d}:{minutos:02d}:{segundos_restantes:02d}"


def formatar_idade(idade_ma):
    """Formata a idade na unidade geológica mais adequada."""
    if idade_ma >= 1000:
        return f"{idade_ma / 1000:.3f} Ga"
    if idade_ma >= 1:
        return f"{idade_ma:.2f} Ma"
    if idade_ma >= 0.001:
        return f"{idade_ma * 1000:.1f} ka"

    anos = idade_ma * 1_000_000
    return f"{anos:,.0f} anos".replace(",", ".")


def formatar_anos(idade_ma):
    """Converte milhões de anos para anos."""
    anos = round(idade_ma * 1_000_000)
    return f"{anos:,}".replace(",", ".") + " anos"


def calcular_idade(duracao_total, momento):
    """Mapeia linearmente o filme para 4540 Ma -> 0 Ma."""
    proporcao = momento / duracao_total
    return max(0.0, 4540.0 * (1.0 - proporcao))


def localizar_tempo_geologico(idade_ma):
    """Localiza a idade em um intervalo geológico."""
    for intervalo in INTERVALOS:
        if intervalo["fim"] < idade_ma <= intervalo["inicio"]:
            return intervalo

    # Presente: 0 Ma
    if idade_ma == 0:
        return INTERVALOS[-1]

    return None



def obter_destaques(intervalo):
    """Retorna os destaques didáticos associados ao período/era encontrado."""
    if intervalo is None:
        return []

    periodo = intervalo.get("período")
    era = intervalo.get("era")

    if periodo and periodo != "—" and periodo in DESTAQUES:
        return DESTAQUES[periodo]

    if periodo and periodo != "—":
        return []

    if era in DESTAQUES:
        return DESTAQUES[era]

    eon = intervalo.get("éon")
    return DESTAQUES.get(eon, [])


# ============================================================
# CABEÇALHO
# ============================================================

st.title("PPCC (DGL7067): ESCALA DE TEMPO GEOLÓGICO")

st.markdown(
    """

    Uma proposta de representação proporcional da história da Terra através da duração de um evento ou produção audiovisual. Veja o que está acontecendo na história da Terra em determinado momento do filme, série ou jogo esportiva!
    """
)

# Banner visual do programa, mantido separado das imagens usadas na aba "Sobre".
imagem_banner = Path("imagens") / "banner_cabecalho.png"
if imagem_banner.exists():
    st.markdown('<div class="cabecalho-banner">', unsafe_allow_html=True)
    st.image(str(imagem_banner), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("O banner do cabeçalho não foi encontrado na pasta 'imagens'.")

st.divider()



# ============================================================
# ENTRADAS
# ============================================================

st.subheader("Informações da obra ou partida")

nome_filme = st.text_input(
    "1. QUAL É A OBRA OU PARTIDA QUE VOCÊ ESTÁ ANALISANDO?",
    help="Informe o nome do filme, da série ou da partida esportiva que será usada como referência para a escala do tempo geológico.",
    placeholder="Ex.: Senhor dos Anéis, Stranger Things ou uma partida de futebol",
)

duracao_texto = st.text_input(
    "2. QUAL É A DURAÇÃO TOTAL?",
    help="Informe quanto tempo dura o filme, episódio, série ou partida completa. Use o formato horas:minutos:segundos.",
    placeholder="Ex.: 02:07:31",
)

momento_texto = st.text_input(
    "3. EM QUAL MOMENTO DA OBRA OU PARTIDA VOCÊ QUER FAZER A COMPARAÇÃO?",
    help="Informe o tempo exato em que o acontecimento escolhido ocorre. Esse momento será convertido proporcionalmente em uma idade da história da Terra.",
    placeholder="Ex.: 01:07:31",
)

descricao = st.text_input(
    "4. O QUE ESTÁ ACONTECENDO NESSE MOMENTO?",
    help="Descreva de forma breve o acontecimento que está ocorrendo no momento escolhido. Ex.: Neo morre, começa uma batalha ou ocorre um gol.",
    placeholder="Ex.: O personagem principal morre",
)

st.write("")

calcular = st.button(
    "CALCULAR CORRESPONDÊNCIA",
    type="primary",
    use_container_width=True,
)


# ============================================================
# RESULTADO
# ============================================================

if calcular:
    erros = []

    nome_filme = nome_filme.strip()
    descricao = descricao.strip()

    if not nome_filme:
        erros.append("Informe o nome do filme, série ou partida esportiva.")

    duracao = converter_duracao(duracao_texto)

    if duracao is None:
        erros.append(
            "Informe uma duração válida. Ex.: 02:07:31 ou 2h07min31s."
        )

    momento = None

    if duracao is not None:
        momento = converter_duracao(momento_texto)

        if momento is None:
            erros.append(
                "Informe um momento válido. Ex.: 01:07:31."
            )
        elif momento > duracao:
            erros.append(
                "O momento informado está depois do final da obra ou partida."
            )

    if erros:
        st.error("Não foi possível realizar o cálculo.")
        for erro in erros:
            st.write(f"• {erro}")

    else:
        idade_ma = calcular_idade(duracao, momento)
        intervalo = localizar_tempo_geologico(idade_ma)

        st.divider()

        # ----------------------------------------------------
        # IDENTIFICAÇÃO DO MOMENTO
        # ----------------------------------------------------

        st.subheader("Momento avaliado")

        evento = descricao if descricao else "Evento não especificado"

        st.markdown(
            f"""
            <div class="momento-box">
                <p><strong>MOMENTO</strong> {formatar_tempo(momento)} — {evento}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # ESCALA DE TEMPO GEOLÓGICO
        # ----------------------------------------------------

        if intervalo:
            st.markdown("#### Escala de Tempo Geológico")

            st.markdown(
                f"""
                <div class="escala-box">
                    <table>
                        <thead>
                            <tr><th>Nível</th><th>Correspondência</th></tr>
                        </thead>
                        <tbody>
                            <tr><td>Éon</td><td>{intervalo["éon"]}</td></tr>
                            <tr><td>Era</td><td>{intervalo["era"]}</td></tr>
                            <tr><td>Período</td><td>{intervalo["período"]}</td></tr>
                            <tr><td>Idade geológica</td><td>{formatar_idade(idade_ma)} antes do presente</td></tr>
                        </tbody>
                    </table>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ------------------------------------------------
            # CONTEXTO PALEONTOLÓGICO E GEOLÓGICO
            # ------------------------------------------------

            st.markdown("#### O que estava acontecendo nesse intervalo?")

            st.markdown(
                "<div class=\"contexto-box\"><p>Os acontecimentos apresentados a seguir estão associados ao intervalo geológico identificado e são utilizados como contexto para a comparação.</p></div>",
                unsafe_allow_html=True,
            )

            destaques = obter_destaques(intervalo)

            if destaques:
                for titulo, texto in destaques:
                    st.markdown(f"**{titulo}**")
                    st.write(texto)
            else:
                st.write(
                    "Não há destaques cadastrados para este intervalo."
                )

        # ----------------------------------------------------
        # CÁLCULO
        # ----------------------------------------------------

        with st.expander("Como o cálculo foi realizado"):
            proporcao = momento / duracao

            st.write(
                f"O momento analisado corresponde a "
                f"**{proporcao * 100:.2f}%** da duração da obra ou partida."
            )

            st.write(
                "Essa mesma proporção é aplicada à história da Terra."
            )

            st.code(
                "idade = 4540 Ma × (1 − momento / duração)"
            )

            st.write(
                f"Resultado: aproximadamente "
                f"**{idade_ma:.2f} Ma antes do presente**."
            )

            st.info(
                "Esta correspondência é uma representação matemática "
                "e didática. Ela não significa que o acontecimento "
                "da obra ou partida tenha ocorrido historicamente "
                "nessa idade geológica."
            )


# ============================================================
# SOBRE A ESCALA GEOCINÉFILA
# ============================================================

st.divider()

tab_sobre, tab_referencias, tab_codigo = st.tabs(["SOBRE O A PPCC", "REFERÊNCIAS", "ACESSO AO CÓDIGO FONTE"])

with tab_sobre:

        col_texto, col_imagem = st.columns([1.35, 1])

        with col_texto:
            st.markdown(
                """
                Esse programa simples é uma proposta de ferramenta didática/Artefato
                pedagógico que utiliza a duração de obras e gravações
                audiovisuais como uma representação proporcional da história
                da Terra. Idealizado como material didático sujeito a avaliação
                da disciplina Paleontologia DGL7067-07110 (2026.2) do currículo
                de Licenciatura em Ciências Biológicas da Universidade Federal
                de Santa Catarina.

                #### COMO FUNCIONA?

                A duração total da obra/partida é considerada como uma
                representação da história da Terra, desde sua formação
                até o presente momento.

                Assim, cada instante corresponde proporcionalmente a uma
                determinada idade geológica, calculada matematicamente
                pelo algoritmo.

                #### OBJETIVOS

                A proposta é utilizar uma referência familiar para ajudar
                a visualizar a dimensão da escala temporal geológica.

                #### IMPORTANTE

                A correspondência produzida pelo programa é uma
                representação matemática e didática, com aproximações e
                valores arredondados, a fim de se tornar mais fácil a
                interpretação para estudantes do Ensino Médio.

                O resultado deve ser interpretado como uma analogia entre
                duas escalas temporais.
                """
            )

        with col_imagem:
            imagem_programa = Path("imagens") / "sobre_o_programa.png"

            if imagem_programa.exists():
                st.image(
                    str(imagem_programa),
                    caption="Escala Geocinéfila",
                    use_container_width=True,
                )
            else:
                st.warning(
                    "A imagem principal não foi encontrada na pasta 'imagens'."
                )

with tab_codigo:
    st.markdown(
        """
        O código-fonte da Escala Geocinéfila será disponibilizado nesta seção.

        A proposta é disponibilizar futuramente o projeto por meio de um
        repositório no GitHub e/ou de uma página pública no Streamlit, permitindo
        que estudantes, docentes e outras pessoas interessadas possam consultar
        o funcionamento do programa e acompanhar suas atualizações.
        """
    )

    st.info("O acesso público ao código pode ser consultado em https://github.com/jgspinelli/ppcc-dgl7067-2026.2.")

with tab_referencias:
    st.markdown(REFERENCIAS)


# ============================================================
# RODAPÉ
# ============================================================

st.caption(
    "PPCC (DGL7067): ESCALA DE TEMPO GEOLÓGICO."
)

