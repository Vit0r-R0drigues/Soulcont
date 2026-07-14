from __future__ import annotations

import csv
import re
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "marketing" / "instagram"

LOGO_BRANCA = "../../../../assets/img/logo/vl_logo_horizontal_branca.svg"
LOGO_PRIMARIA = "../../../../assets/img/logo/vl_logo_horizontal_primaria.svg"
LIONCIO = "../../../../assets/img/lioncio.png"
LIONCIO_DIREITA = "../../../../assets/img/lionciocaminhandoparaoladodireito.png"


def slugify(text: str) -> str:
    replacements = str.maketrans(
        "áàãâéêíóôõúüçÁÀÃÂÉÊÍÓÔÕÚÜÇ",
        "aaaaeeiooouucAAAAEEIOOOUUC",
    )
    text = text.translate(replacements).lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def md_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def html_list(items: list[str]) -> str:
    return "\n".join(f"<li>{escape(item)}</li>" for item in items)


CTA_BANK = [
    "Chame a VL no WhatsApp e entenda os próximos passos.",
    "Solicite um diagnóstico contábil inicial.",
    "Antes de abrir empresa, fale com quem entende do processo.",
    "Quer trocar de contador com segurança? Fale com a VL.",
    "Sua empresa cresceu? Vamos analisar o melhor caminho.",
    "Prestador de serviço, sua tributação merece atenção.",
    "Organize sua empresa com orientação contábil clara.",
    "Peça uma análise inicial antes de decidir no achismo.",
    "Quer revisar o enquadramento da empresa? Converse com a VL.",
    "Fale com a VL e veja como organizar sua rotina contábil.",
    "Conte com uma contabilidade consultiva para a próxima fase.",
    "Chame no WhatsApp e explique o momento da sua empresa.",
    "Vamos avaliar se sua empresa está no caminho certo.",
    "Abra seu CNPJ com mais clareza desde o começo.",
    "Receba orientação para emitir notas com mais segurança.",
    "Entenda quais documentos sua contabilidade precisa acompanhar.",
    "Planeje a saída do MEI antes que vire urgência.",
    "Peça apoio para separar finanças pessoais e empresariais.",
    "Converse com a VL antes de mudar seu regime ou enquadramento.",
    "Transforme dúvida contábil em decisão mais segura.",
    "Fale com a VL para entender sua situação sem compromisso de publicação.",
    "Leve sua dúvida para uma análise responsável e individualizada.",
]

HASHTAG_GROUPS = {
    "base": ["#vlcontabilidade", "#contabilidade", "#contabilidadeconsultiva", "#contabilidadedigital"],
    "abertura": ["#aberturadeempresa", "#cnpj", "#empreendedorismo", "#pequenasempresas", "#saopaulo"],
    "troca": ["#trocadecontador", "#gestaoempresarial", "#pequenasempresas", "#atendimentoconsultivo"],
    "simples": ["#simplesnacional", "#fatorr", "#prestadoresdeservico", "#profissionalliberal"],
    "mei": ["#mei", "#meiemcrescimento", "#microempresa", "#empreendedorismo"],
    "organizacao": ["#gestaofinanceira", "#organizacaofinanceira", "#prolabore", "#pequenasempresas"],
    "autoridade": ["#contabilidadeempresarial", "#gestaoempresarial", "#tecnologia", "#atendimentohumanizado"],
    "conversao": ["#diagnosticocontabil", "#prestadoresdeservico", "#simplesnacional", "#saopaulo"],
}


def hashtags(*groups: str) -> list[str]:
    result: list[str] = []
    for tag in HASHTAG_GROUPS["base"]:
        if tag not in result:
            result.append(tag)
    for group in groups:
        for tag in HASHTAG_GROUPS[group]:
            if tag not in result:
                result.append(tag)
    return result[:9]


POSTS = [
    {
        "title": "Vai abrir empresa? Não escolha CNAE no chute",
        "slug": "abertura_empresa_cnae",
        "pilar": "Abertura de empresa",
        "funil": "topo",
        "format": "vertical",
        "variant": "dark",
        "icon": "CNAE",
        "subtitle": "O código da atividade influencia nota, tributação e obrigações.",
        "bullets": ["Atividade exercida", "Tipo de cliente", "Forma de emissão de nota", "Regime mais coerente"],
        "cta": "Antes de abrir CNPJ, fale com a VL.",
        "objective": "Educar sobre a importância do enquadramento antes da abertura.",
        "publico": "Prestadores de serviço e profissionais que querem abrir empresa.",
        "body": "O CNAE não é um detalhe burocrático. Ele ajuda a definir como a empresa será enquadrada, quais notas poderá emitir e quais obrigações precisam ser acompanhadas. Escolher no improviso pode gerar retrabalho e dúvidas logo nos primeiros meses.",
        "note": "A escolha correta depende da atividade real, do modelo de faturamento e da análise documental.",
        "groups": ["abertura"],
    },
    {
        "title": "MEI crescendo: quando virar ME?",
        "slug": "mei_crescendo_quando_virar_me",
        "pilar": "MEI em crescimento",
        "funil": "meio",
        "format": "square",
        "variant": "light",
        "icon": "MEI",
        "subtitle": "Crescer é bom. Crescer sem planejar pode virar dor de cabeça.",
        "bullets": ["Faturamento perto do limite", "Mais notas fiscais", "Clientes maiores", "Necessidade de estrutura"],
        "cta": "Sua empresa cresceu? Vamos analisar o melhor caminho.",
        "objective": "Mostrar sinais de transição do MEI para ME.",
        "publico": "MEIs em crescimento e prestadores de serviço.",
        "body": "Quando o MEI começa a emitir mais notas, atender clientes maiores ou se aproximar do limite anual, é hora de olhar a próxima etapa com calma. A transição para ME deve ser planejada para evitar desenquadramento desorganizado e decisões feitas na pressa.",
        "note": "Cada caso precisa considerar faturamento, atividade, emissão de notas e estrutura da operação.",
        "groups": ["mei"],
    },
    {
        "title": "Seu contador só manda guia?",
        "slug": "contador_so_manda_guia",
        "pilar": "Troca de contador",
        "funil": "meio",
        "format": "vertical",
        "variant": "gold",
        "icon": "GUIA",
        "subtitle": "Guia é obrigação. Orientação é o que ajuda sua empresa a decidir.",
        "bullets": ["Você entende o que paga?", "Recebe retorno com clareza?", "Tem análise do seu momento?", "Sabe quais documentos enviar?"],
        "cta": "Quer uma contabilidade mais consultiva? Fale com a VL.",
        "objective": "Ativar dor de falta de orientação e posicionar a VL como consultiva.",
        "publico": "Empresários insatisfeitos com atendimento contábil operacional.",
        "body": "Receber guias em dia é importante, mas a contabilidade não deveria parar aí. O empresário precisa entender o que está pagando, quais riscos existem e como a rotina contábil apoia decisões de crescimento.",
        "note": "A troca de contador deve ser feita com organização, documentos e análise do cenário atual.",
        "groups": ["troca"],
    },
    {
        "title": "Prestador de serviço: Anexo III ou Anexo V?",
        "slug": "anexo_iii_anexo_v",
        "pilar": "Simples Nacional e Fator R",
        "funil": "topo",
        "format": "square",
        "variant": "dark",
        "icon": "%",
        "subtitle": "No Simples Nacional, a atividade e o Fator R podem influenciar o anexo.",
        "bullets": ["Depende da atividade", "Depende da folha", "Depende do faturamento", "Precisa de acompanhamento"],
        "cta": "Prestador de serviço, peça uma análise responsável.",
        "objective": "Explicar a dúvida comum de enquadramento sem prometer redução.",
        "publico": "Prestadores de serviço no Simples Nacional.",
        "body": "Muitos prestadores de serviço têm dúvida sobre Anexo III e Anexo V. Essa análise envolve atividade, folha, pró-labore, faturamento e acompanhamento mensal. Decidir só pela alíquota aparente pode gerar uma leitura incompleta.",
        "note": "O enquadramento tributário depende de análise individual e documentos atualizados.",
        "groups": ["simples"],
    },
    {
        "title": "O que é Fator R?",
        "slug": "fator_r_explicado",
        "pilar": "Simples Nacional e Fator R",
        "funil": "topo",
        "format": "vertical",
        "variant": "light",
        "icon": "R",
        "subtitle": "Uma relação entre folha/pró-labore e faturamento que merece atenção.",
        "bullets": ["Afeta alguns prestadores", "Exige acompanhamento mensal", "Não deve ser decidido no achismo"],
        "cta": "Chame a VL para entender se isso se aplica à sua empresa.",
        "objective": "Educar sobre Fator R com linguagem simples.",
        "publico": "Prestadores de serviço e profissionais liberais.",
        "body": "Fator R é uma relação usada em algumas atividades do Simples Nacional para verificar a proporção entre folha/pró-labore e faturamento. Em determinados casos, ele pode influenciar o anexo aplicável.",
        "note": "A aplicação depende da atividade, dos valores do período e da documentação contábil.",
        "groups": ["simples"],
    },
    {
        "title": "Pró-labore errado pode afetar sua empresa",
        "slug": "pro_labore_errado",
        "pilar": "Organização financeira e contábil",
        "funil": "meio",
        "format": "square",
        "variant": "slate",
        "icon": "PL",
        "subtitle": "A retirada do sócio precisa ter critério contábil e financeiro.",
        "bullets": ["Organiza a remuneração", "Ajuda na leitura da empresa", "Pode influenciar análises tributárias"],
        "cta": "Revise sua rotina de pró-labore com orientação.",
        "objective": "Mostrar importância do pró-labore para organização e análise.",
        "publico": "Sócios de pequenas empresas e prestadores PJ.",
        "body": "Pró-labore não é apenas uma retirada mensal. Ele ajuda a separar a remuneração do sócio do resultado da empresa e pode ter impacto em análises contábeis e tributárias, especialmente para prestadores de serviço.",
        "note": "O valor adequado deve considerar realidade financeira, legislação e contexto da empresa.",
        "groups": ["organizacao", "simples"],
    },
    {
        "title": "5 sinais de que está na hora de trocar de contador",
        "slug": "sinais_trocar_contador",
        "pilar": "Troca de contador",
        "funil": "meio",
        "format": "vertical",
        "variant": "dark",
        "icon": "5",
        "subtitle": "A troca começa quando a falta de clareza atrapalha sua gestão.",
        "bullets": ["Pouco retorno", "Guias sem explicação", "Sem análise do regime", "Documentos sempre confusos"],
        "cta": "Quer trocar com segurança? Fale com a VL.",
        "objective": "Gerar identificação em leads que querem trocar de contador.",
        "publico": "Empresários com baixa satisfação no atendimento contábil.",
        "body": "A troca de contador costuma ser considerada quando a empresa cresce, mas o atendimento continua apenas operacional. Falta de retorno, ausência de orientação e pouca clareza sobre impostos são sinais de alerta.",
        "note": "A transição deve ser organizada para reduzir ruído e preservar a rotina fiscal e contábil.",
        "groups": ["troca"],
    },
    {
        "title": "Trocar de contador é mais simples do que parece",
        "slug": "trocar_contador_simples",
        "pilar": "Troca de contador",
        "funil": "fundo",
        "format": "square",
        "variant": "light",
        "icon": "OK",
        "subtitle": "Com checklist e onboarding, a transição fica mais clara.",
        "bullets": ["Mapeamento inicial", "Documentos necessários", "Prioridades do mês", "Acompanhamento da entrada"],
        "cta": "A VL te orienta na transição.",
        "objective": "Reduzir objeção de medo da troca.",
        "publico": "Empresários que desejam trocar de contador.",
        "body": "Muita gente adia a troca de contador por medo de bagunçar a rotina. Com um processo claro, lista de documentos e revisão do cenário atual, a transição pode ser feita com muito mais segurança.",
        "note": "Antes da troca, vale entender pendências, obrigações em andamento e prazos próximos.",
        "groups": ["troca"],
    },
    {
        "title": "Sua empresa fatura, mas você sabe se lucra?",
        "slug": "empresa_fatura_mas_lucra",
        "pilar": "Organização financeira e contábil",
        "funil": "meio",
        "format": "vertical",
        "variant": "gold",
        "icon": "R$",
        "subtitle": "Entrada de dinheiro não é a mesma coisa que resultado.",
        "bullets": ["Controle entradas e saídas", "Separe custos e retiradas", "Acompanhe margem", "Use dados para decidir"],
        "cta": "Organize sua empresa com a VL.",
        "objective": "Conectar dor financeira com necessidade de análise contábil.",
        "publico": "Pequenos empresários e prestadores de serviço.",
        "body": "Faturamento mostra quanto entrou. Lucro da operação mostra o que sobra depois de custos, despesas, impostos e retiradas. Sem essa leitura, decisões importantes acabam sendo tomadas no escuro.",
        "note": "A análise financeira precisa ser feita com dados atualizados e rotina de acompanhamento.",
        "groups": ["organizacao"],
    },
    {
        "title": "Misturar dinheiro pessoal e da empresa trava o crescimento",
        "slug": "separar_contas_pessoal_empresa",
        "pilar": "Organização financeira e contábil",
        "funil": "topo",
        "format": "square",
        "variant": "dark",
        "icon": "2X",
        "subtitle": "Quando tudo passa pela mesma conta, ninguém enxerga o resultado.",
        "bullets": ["Crie conta PJ", "Defina pró-labore", "Registre entradas e saídas", "Acompanhe o caixa"],
        "cta": "Peça apoio para organizar sua rotina financeira.",
        "objective": "Educar sobre separação financeira.",
        "publico": "MEIs, autônomos e pequenos empresários.",
        "body": "Misturar conta pessoal com conta da empresa parece prático no começo, mas dificulta a leitura do caixa, do lucro e das retiradas. A empresa precisa de rotina própria para crescer com mais clareza.",
        "note": "A organização deve respeitar o porte, a atividade e a realidade financeira do negócio.",
        "groups": ["organizacao"],
    },
    {
        "title": "Simples Nacional não significa simples sem análise",
        "slug": "simples_nacional_com_analise",
        "pilar": "Simples Nacional e Fator R",
        "funil": "topo",
        "format": "vertical",
        "variant": "slate",
        "icon": "SN",
        "subtitle": "O regime pode ser prático, mas o enquadramento exige acompanhamento.",
        "bullets": ["Anexo correto", "Faturamento acumulado", "Atividade exercida", "Folha e pró-labore"],
        "cta": "Revise seu Simples Nacional com critério.",
        "objective": "Reforçar que o Simples exige leitura mensal.",
        "publico": "Empresas do Simples Nacional e prestadores.",
        "body": "O Simples Nacional facilita a rotina de muitas empresas, mas não elimina a necessidade de análise. Atividade, faturamento acumulado, anexo e folha podem mudar a interpretação do cenário.",
        "note": "A avaliação correta depende dos documentos e do histórico da empresa.",
        "groups": ["simples"],
    },
    {
        "title": "Antes de emitir nota, entenda sua atividade",
        "slug": "emitir_nota_entenda_atividade",
        "pilar": "Abertura de empresa",
        "funil": "topo",
        "format": "square",
        "variant": "light",
        "icon": "NF",
        "subtitle": "Nota fiscal precisa conversar com CNAE, serviço e município.",
        "bullets": ["Descrição do serviço", "CNAE coerente", "Cadastro municipal", "Tributos envolvidos"],
        "cta": "Tenha orientação antes da primeira nota.",
        "objective": "Prevenir erros de emissão de nota.",
        "publico": "Prestadores abrindo empresa ou começando a emitir notas.",
        "body": "Emitir nota fiscal sem entender a atividade pode gerar dúvida sobre código de serviço, descrição e tributação. O ideal é organizar isso antes da primeira emissão, especialmente para prestadores de serviço.",
        "note": "As regras podem variar conforme atividade, município e cadastro da empresa.",
        "groups": ["abertura"],
    },
    {
        "title": "Abertura de empresa com segurança",
        "slug": "abertura_empresa_segura",
        "pilar": "Abertura de empresa",
        "funil": "fundo",
        "format": "vertical",
        "variant": "dark",
        "icon": "CNPJ",
        "subtitle": "CNPJ bem aberto evita retrabalho depois.",
        "bullets": ["Atividade correta", "Regime adequado", "Documentos organizados", "Orientação para notas"],
        "cta": "Abra sua empresa com a VL.",
        "objective": "Converter interessados em abertura de empresa.",
        "publico": "Pessoas que querem abrir CNPJ.",
        "body": "Abrir empresa envolve mais do que preencher cadastro. A escolha da atividade, a análise do regime, a orientação para notas e a organização dos documentos ajudam a começar com menos improviso.",
        "note": "O processo deve considerar o serviço prestado, a previsão de faturamento e a estrutura inicial.",
        "groups": ["abertura", "conversao"],
    },
    {
        "title": "Documentos que sua contabilidade precisa receber",
        "slug": "documentos_contabilidade_mensal",
        "pilar": "Organização financeira e contábil",
        "funil": "topo",
        "format": "square",
        "variant": "light",
        "icon": "DOC",
        "subtitle": "Documentos certos deixam a rotina mais rápida e confiável.",
        "bullets": ["Notas emitidas", "Extratos", "Comprovantes", "Folha e pró-labore"],
        "cta": "Organize sua rotina mensal com a VL.",
        "objective": "Educar sobre rotina documental.",
        "publico": "Pequenos empresários, MEIs e prestadores.",
        "body": "A contabilidade trabalha melhor quando recebe informações completas e no prazo. Notas, extratos, comprovantes e dados de folha ajudam a manter obrigações em dia e a gerar análises mais úteis.",
        "note": "A lista exata pode variar conforme porte, regime e atividade da empresa.",
        "groups": ["organizacao"],
    },
    {
        "title": "Por que sua empresa precisa de rotina contábil?",
        "slug": "rotina_contabil_empresa",
        "pilar": "Autoridade e confiança",
        "funil": "topo",
        "format": "vertical",
        "variant": "slate",
        "icon": "ROT",
        "subtitle": "Organização mensal evita decisões feitas no susto.",
        "bullets": ["Prazos acompanhados", "Documentos em ordem", "Indicadores atualizados", "Menos improviso"],
        "cta": "Conte com uma contabilidade que acompanha sua empresa.",
        "objective": "Mostrar valor recorrente da contabilidade.",
        "publico": "Pequenos empresários buscando organização.",
        "body": "A rotina contábil cria previsibilidade. Em vez de resolver tudo quando aparece um problema, a empresa acompanha documentos, obrigações e indicadores com mais método.",
        "note": "Cada rotina deve ser ajustada ao volume de documentos e ao momento da empresa.",
        "groups": ["autoridade", "organizacao"],
    },
    {
        "title": "Contabilidade consultiva: o que muda?",
        "slug": "contabilidade_consultiva_o_que_muda",
        "pilar": "Autoridade e confiança",
        "funil": "meio",
        "format": "square",
        "variant": "dark",
        "icon": "VL",
        "subtitle": "Você recebe orientação, não apenas obrigações.",
        "bullets": ["Explicação clara", "Análise do cenário", "Apoio para decisão", "Acompanhamento próximo"],
        "cta": "Conheça a visão consultiva da VL.",
        "objective": "Diferenciar a VL de contabilidades apenas operacionais.",
        "publico": "Empresários que valorizam orientação.",
        "body": "Na contabilidade consultiva, a entrega não se limita a guias e declarações. O foco é traduzir números, explicar impactos e apoiar decisões dentro do que pode ser analisado com segurança.",
        "note": "Orientações específicas exigem dados, documentos e contexto da empresa.",
        "groups": ["autoridade"],
    },
    {
        "title": "MEI pode contratar funcionário?",
        "slug": "mei_pode_contratar_funcionario",
        "pilar": "MEI em crescimento",
        "funil": "topo",
        "format": "vertical",
        "variant": "light",
        "icon": "MEI",
        "subtitle": "Pode, mas existem limites e obrigações que precisam ser acompanhados.",
        "bullets": ["Limite de contratação", "Folha e encargos", "Rotina trabalhista", "Planejamento de crescimento"],
        "cta": "Antes de contratar, converse com a VL.",
        "objective": "Educar MEIs sobre contratação e crescimento.",
        "publico": "MEIs que precisam ampliar estrutura.",
        "body": "O MEI pode contratar dentro de regras específicas, mas isso traz obrigações e aumenta a necessidade de organização. Antes de crescer a equipe, vale entender se o formato atual ainda atende à empresa.",
        "note": "A decisão deve considerar faturamento, atividade e obrigações trabalhistas aplicáveis.",
        "groups": ["mei"],
    },
    {
        "title": "Estourou o limite do MEI? Atenção ao próximo passo",
        "slug": "limite_mei_desenquadramento",
        "pilar": "MEI em crescimento",
        "funil": "meio",
        "format": "square",
        "variant": "gold",
        "icon": "LIM",
        "subtitle": "O desenquadramento precisa ser tratado com orientação.",
        "bullets": ["Verifique o faturamento", "Entenda o impacto", "Organize documentos", "Planeje a transição"],
        "cta": "Fale com a VL antes que vire urgência.",
        "objective": "Captar MEIs em risco de desenquadramento.",
        "publico": "MEIs próximos ou acima do limite.",
        "body": "Quando o faturamento passa do limite do MEI, a empresa precisa avaliar os próximos passos com cuidado. Ignorar o tema pode gerar correções, dúvidas e uma transição mais trabalhosa.",
        "note": "O tratamento depende do valor faturado, do período e da situação cadastral da empresa.",
        "groups": ["mei", "conversao"],
    },
    {
        "title": "Você sabe quanto sua empresa paga de imposto?",
        "slug": "quanto_empresa_paga_imposto",
        "pilar": "Simples Nacional e Fator R",
        "funil": "meio",
        "format": "vertical",
        "variant": "dark",
        "icon": "%",
        "subtitle": "Mais importante que olhar a guia é entender o motivo dela.",
        "bullets": ["Regime aplicado", "Faturamento do período", "Atividade e anexo", "Histórico da empresa"],
        "cta": "Peça uma explicação clara sobre seus impostos.",
        "objective": "Incentivar revisão e entendimento tributário.",
        "publico": "Empresários que pagam guias sem entender composição.",
        "body": "Não basta saber o valor da guia. É importante entender de onde ele vem, qual regime está sendo aplicado e se o enquadramento faz sentido para o momento da empresa.",
        "note": "Nem todo imposto alto está errado, mas precisa ser explicado com base em dados.",
        "groups": ["simples"],
    },
    {
        "title": "Seu enquadramento tributário está atualizado?",
        "slug": "enquadramento_tributario_atualizado",
        "pilar": "Simples Nacional e Fator R",
        "funil": "fundo",
        "format": "square",
        "variant": "slate",
        "icon": "REV",
        "subtitle": "Empresa muda. A análise contábil precisa acompanhar.",
        "bullets": ["Mudança de faturamento", "Nova atividade", "Contratação", "Pró-labore e folha"],
        "cta": "Solicite um diagnóstico contábil com a VL.",
        "objective": "Converter para diagnóstico de enquadramento.",
        "publico": "Prestadores e empresas pequenas com cenário em mudança.",
        "body": "Uma empresa que mudou de faturamento, serviço, equipe ou retirada dos sócios pode precisar revisar o enquadramento. O que fazia sentido no início nem sempre continua adequado.",
        "note": "A revisão depende de documentos, histórico e análise individual do cenário.",
        "groups": ["simples", "conversao"],
    },
    {
        "title": "Fisioterapeuta precisa de contador?",
        "slug": "fisioterapeuta_precisa_contador",
        "pilar": "Abertura de empresa",
        "funil": "topo",
        "format": "vertical",
        "variant": "light",
        "icon": "SAÚDE",
        "subtitle": "Atendimento, nota e enquadramento precisam estar alinhados.",
        "bullets": ["CNPJ ou pessoa física", "Emissão de nota", "CNAE adequado", "Rotina de documentos"],
        "cta": "Fale com a VL antes de estruturar seu atendimento PJ.",
        "objective": "Atrair profissionais de saúde prestadores de serviço.",
        "publico": "Fisioterapeutas e profissionais da saúde.",
        "body": "Fisioterapeutas que atendem como PJ precisam olhar emissão de nota, atividade correta e rotina fiscal. A formalização ajuda a atender clientes e clínicas com mais organização.",
        "note": "O melhor formato depende da forma de atendimento, faturamento e exigências dos contratantes.",
        "groups": ["abertura"],
    },
    {
        "title": "Psicólogo PJ: cuidados contábeis",
        "slug": "psicologo_pj_cuidados_contabeis",
        "pilar": "Abertura de empresa",
        "funil": "topo",
        "format": "square",
        "variant": "dark",
        "icon": "PJ",
        "subtitle": "A rotina profissional precisa de organização fiscal e financeira.",
        "bullets": ["Atividade correta", "Nota fiscal", "Separação financeira", "Pró-labore"],
        "cta": "Estruture seu CNPJ com orientação.",
        "objective": "Atrair psicólogos que atuam ou querem atuar como PJ.",
        "publico": "Psicólogos e profissionais liberais.",
        "body": "Para psicólogos PJ, a contabilidade ajuda a organizar abertura, emissão de notas, documentos mensais e separação entre conta pessoal e empresarial. Isso evita improviso na rotina.",
        "note": "A análise deve considerar forma de atendimento, município, faturamento e obrigações profissionais.",
        "groups": ["abertura", "organizacao"],
    },
    {
        "title": "Dentista PJ: atenção ao enquadramento",
        "slug": "dentista_pj_enquadramento",
        "pilar": "Simples Nacional e Fator R",
        "funil": "meio",
        "format": "vertical",
        "variant": "gold",
        "icon": "OD",
        "subtitle": "Serviços de saúde exigem cuidado com atividade, notas e regime.",
        "bullets": ["CNAE e serviço", "Emissão de nota", "Fator R quando aplicável", "Pró-labore"],
        "cta": "Peça uma análise antes de decidir sozinho.",
        "objective": "Atrair dentistas e clínicas pequenas para diagnóstico.",
        "publico": "Dentistas PJ e pequenos consultórios.",
        "body": "Dentistas que atuam como PJ precisam manter atividade, nota e regime tributário alinhados. Em alguns cenários, análises como Fator R e pró-labore podem ser relevantes.",
        "note": "O enquadramento depende do serviço prestado, estrutura e documentos da empresa.",
        "groups": ["simples", "abertura"],
    },
    {
        "title": "Agência de marketing: cuidado com CNAE e nota",
        "slug": "agencia_marketing_cnae_nota",
        "pilar": "Abertura de empresa",
        "funil": "topo",
        "format": "square",
        "variant": "light",
        "icon": "MKT",
        "subtitle": "Serviços diferentes podem exigir descrições e códigos diferentes.",
        "bullets": ["Gestão de tráfego", "Consultoria", "Criação", "Serviços recorrentes"],
        "cta": "Organize sua agência com apoio contábil.",
        "objective": "Atrair agências prestadoras de serviço.",
        "publico": "Agências de marketing e profissionais de mídia.",
        "body": "Agências costumam vender serviços variados. Por isso, CNAE, descrição de nota e rotina documental precisam refletir a realidade do que é prestado, sem deixar tudo genérico demais.",
        "note": "A orientação deve considerar contratos, município e forma de faturamento.",
        "groups": ["abertura"],
    },
    {
        "title": "Profissional de TI: como organizar sua empresa",
        "slug": "profissional_ti_organizar_empresa",
        "pilar": "Organização financeira e contábil",
        "funil": "topo",
        "format": "vertical",
        "variant": "slate",
        "icon": "TI",
        "subtitle": "Contrato, nota e retirada precisam funcionar juntos.",
        "bullets": ["CNPJ adequado", "Notas recorrentes", "Conta PJ", "Pró-labore com critério"],
        "cta": "A VL ajuda a estruturar sua rotina PJ.",
        "objective": "Atrair profissionais de tecnologia PJ.",
        "publico": "Desenvolvedores, consultores de TI e prestadores tech.",
        "body": "Profissionais de TI que trabalham como PJ precisam organizar contrato, emissão de nota, conta empresarial e retirada mensal. A rotina fica mais clara quando os números deixam de ficar misturados.",
        "note": "A estrutura ideal depende do serviço, faturamento, clientes e forma de contratação.",
        "groups": ["organizacao", "abertura"],
    },
    {
        "title": "Clínica de estética: contabilidade além da guia",
        "slug": "clinica_estetica_contabilidade",
        "pilar": "Autoridade e confiança",
        "funil": "meio",
        "format": "square",
        "variant": "dark",
        "icon": "CLÍN",
        "subtitle": "Crescimento exige controle de serviço, caixa, documentos e tributos.",
        "bullets": ["Notas e serviços", "Equipe e pró-labore", "Custos da operação", "Indicadores financeiros"],
        "cta": "Tenha uma contabilidade que acompanhe sua clínica.",
        "objective": "Atrair clínicas pequenas para atendimento consultivo.",
        "publico": "Clínicas de estética e saúde.",
        "body": "Uma clínica de estética não precisa apenas de guias. Precisa acompanhar serviços, documentos, equipe, retiradas e indicadores para entender se o crescimento está organizado.",
        "note": "Cada clínica deve ser analisada conforme estrutura, atividades e modelo de atendimento.",
        "groups": ["autoridade", "organizacao"],
    },
    {
        "title": "Arquiteto ou engenheiro PJ: atenção fiscal",
        "slug": "arquiteto_engenheiro_pj",
        "pilar": "Abertura de empresa",
        "funil": "topo",
        "format": "vertical",
        "variant": "light",
        "icon": "PROJ",
        "subtitle": "Projetos, consultorias e obras podem ter tratamentos diferentes.",
        "bullets": ["Atividade exercida", "Contrato", "Nota fiscal", "Regime tributário"],
        "cta": "Estruture seu CNPJ com a VL.",
        "objective": "Atrair arquitetos e engenheiros prestadores.",
        "publico": "Arquitetos, engenheiros e consultores técnicos.",
        "body": "Arquitetos e engenheiros PJ precisam descrever corretamente seus serviços e manter nota, contrato e atividade alinhados. Essa organização ajuda a reduzir dúvidas fiscais e contábeis.",
        "note": "O enquadramento depende do tipo de serviço, local de prestação e documentação.",
        "groups": ["abertura"],
    },
    {
        "title": "Pequena empresa precisa de análise financeira",
        "slug": "pequena_empresa_analise_financeira",
        "pilar": "Organização financeira e contábil",
        "funil": "meio",
        "format": "square",
        "variant": "slate",
        "icon": "DRE",
        "subtitle": "Sem dados, crescimento vira sensação.",
        "bullets": ["Margem", "Caixa", "Custos", "Resultado da operação"],
        "cta": "Transforme números em decisões com a VL.",
        "objective": "Conectar contabilidade com gestão financeira.",
        "publico": "Micro e pequenas empresas.",
        "body": "Pequenas empresas também precisam analisar margem, caixa, custos e resultado. A contabilidade pode apoiar essa leitura quando os documentos estão organizados e os números são acompanhados.",
        "note": "A análise deve partir de demonstrativos, extratos e informações consistentes.",
        "groups": ["organizacao", "autoridade"],
    },
    {
        "title": "O barato na contabilidade pode sair caro",
        "slug": "barato_contabilidade_pode_sair_caro",
        "pilar": "Troca de contador",
        "funil": "meio",
        "format": "vertical",
        "variant": "gold",
        "icon": "VALOR",
        "subtitle": "Preço importa, mas falta de orientação também tem custo.",
        "bullets": ["Dúvidas sem resposta", "Enquadramento sem revisão", "Documentos desorganizados", "Decisões no escuro"],
        "cta": "Escolha uma contabilidade que acompanhe sua empresa.",
        "objective": "Reposicionar valor sem parecer serviço barato.",
        "publico": "Empresários sensíveis a preço, mas com dor de atendimento.",
        "body": "Contratar contabilidade olhando só o menor preço pode deixar a empresa sem orientação quando mais precisa. O custo aparece em retrabalho, dúvidas recorrentes e decisões sem base.",
        "note": "A escolha deve considerar atendimento, clareza, processo e capacidade de análise.",
        "groups": ["troca", "autoridade"],
    },
    {
        "title": "Diagnóstico contábil: o primeiro passo para organizar sua empresa",
        "slug": "diagnostico_contabil_prestadores",
        "pilar": "Conversão",
        "funil": "fundo",
        "format": "square",
        "variant": "dark",
        "icon": "DIAG",
        "subtitle": "Antes de decidir, entenda onde sua empresa está hoje.",
        "bullets": ["Enquadramento", "Notas fiscais", "Pró-labore", "Rotina contábil"],
        "cta": "Solicite um diagnóstico contábil para prestadores de serviço.",
        "objective": "Converter leads para a oferta central da campanha.",
        "publico": "Prestadores de serviço, MEIs em crescimento e pequenas empresas.",
        "body": "O diagnóstico contábil ajuda a olhar o momento atual da empresa: enquadramento, emissão de notas, pró-labore, documentos e clareza da rotina. É o primeiro passo para sair do achismo.",
        "note": "A análise é individual e depende das informações apresentadas pela empresa.",
        "groups": ["conversao", "simples", "organizacao"],
    },
]


CAROUSELS = [
    {
        "title": "5 sinais de que está na hora de trocar de contador",
        "slug": "5_sinais_trocar_contador",
        "pilar": "Troca de contador",
        "funil": "meio",
        "objective": "Gerar identificação e demanda por transição organizada.",
        "publico": "Empresários insatisfeitos com a contabilidade atual.",
        "cta": "Quer trocar com segurança? Fale com a VL.",
        "groups": ["troca"],
        "slides": [
            ("5 sinais de que está na hora de trocar de contador", "A falta de clareza começa pequena, mas pesa na gestão."),
            ("Seu contador não responde com clareza", "Você pergunta, espera e continua sem entender o próximo passo."),
            ("Você só recebe guias, sem orientação", "Cumprir obrigação é importante. Explicar o impacto também."),
            ("Não existe análise do regime tributário", "A empresa muda e o enquadramento precisa ser acompanhado."),
            ("Você não sabe se está pagando imposto corretamente", "Nem todo imposto alto está errado, mas precisa ser explicado."),
            ("Sua empresa cresceu, mas a contabilidade não acompanhou", "Crescimento exige método, documentos e leitura consultiva."),
            ("Quer trocar com segurança? Fale com a VL", "A transição pode ser organizada com checklist e diagnóstico inicial."),
        ],
        "caption": "Se a contabilidade atual não explica, não acompanha e não ajuda você a entender a rotina da empresa, talvez seja hora de avaliar uma troca. A mudança não precisa ser feita no susto: com documentos, levantamento inicial e onboarding, a transição fica mais segura. Cada empresa deve revisar sua situação antes de migrar. Quer entender como fazer isso com clareza? Fale com a VL.",
    },
    {
        "title": "MEI crescendo: quando virar ME?",
        "slug": "mei_crescendo_quando_virar_me",
        "pilar": "MEI em crescimento",
        "funil": "meio",
        "objective": "Orientar MEIs sobre sinais de transição.",
        "publico": "MEIs próximos do limite ou com operação maior.",
        "cta": "Fale com a VL antes de tomar decisão.",
        "groups": ["mei"],
        "slides": [
            ("MEI crescendo? Atenção a estes sinais", "Crescer é ótimo. Planejar a próxima fase é essencial."),
            ("Faturamento perto do limite", "Acompanhe o acumulado antes que a decisão vire urgência."),
            ("Necessidade de contratar mais estrutura", "Equipe, ferramentas e rotina podem pedir outro formato."),
            ("Mais notas fiscais e clientes maiores", "Clientes maiores costumam exigir mais organização."),
            ("Risco de desenquadramento", "Ignorar o limite pode gerar ajustes e retrabalho."),
            ("Planejar antes evita dor de cabeça", "Organize documentos, emissão de notas e projeção de receita."),
            ("Fale com a VL antes de tomar decisão", "A transição para ME deve ser analisada caso a caso."),
        ],
        "caption": "O MEI que cresce precisa olhar para a próxima fase antes do problema aparecer. Faturamento, contratação, volume de notas e clientes maiores são sinais de que talvez seja hora de planejar a mudança para ME. A decisão depende da realidade da empresa e deve ser analisada com documentos. A VL te ajuda a entender os próximos passos.",
    },
    {
        "title": "Fator R explicado de forma simples",
        "slug": "fator_r_forma_simples",
        "pilar": "Simples Nacional e Fator R",
        "funil": "topo",
        "objective": "Educar prestadores sobre Fator R sem promessas tributárias.",
        "publico": "Prestadores de serviço no Simples Nacional.",
        "cta": "Solicite uma análise com a VL.",
        "groups": ["simples"],
        "slides": [
            ("Fator R: por que prestadores de serviço precisam entender?", "Ele pode influenciar a leitura tributária de algumas atividades."),
            ("Ele relaciona folha/pró-labore com faturamento", "A proporção entre esses valores entra na análise."),
            ("Pode influenciar o Anexo do Simples", "Em certos casos, pode afetar Anexo III ou Anexo V."),
            ("Depende da atividade da empresa", "Nem toda empresa usa a mesma regra."),
            ("Precisa de acompanhamento mensal", "A análise muda conforme faturamento e folha variam."),
            ("Não decida no achismo", "Alíquota aparente não substitui análise técnica."),
            ("Solicite uma análise com a VL", "Cada caso precisa ser avaliado com documentos atualizados."),
        ],
        "caption": "Fator R é um tema importante para muitos prestadores de serviço, mas não deve ser tratado como fórmula automática. Ele depende da atividade, do faturamento, da folha e do pró-labore. Acompanhamento mensal ajuda a entender o cenário com mais segurança. Para saber se isso se aplica à sua empresa, é preciso analisar o caso individualmente.",
    },
    {
        "title": "Abrir empresa sem análise pode sair caro",
        "slug": "abrir_empresa_sem_analise",
        "pilar": "Abertura de empresa",
        "funil": "topo",
        "objective": "Prevenir erros comuns na abertura de CNPJ.",
        "publico": "Pessoas que querem abrir empresa.",
        "cta": "Abra sua empresa com orientação.",
        "groups": ["abertura"],
        "slides": [
            ("Vai abrir empresa? Cuidado com estes erros", "O CNPJ começa certo quando a análise vem antes do cadastro."),
            ("Escolher CNAE no chute", "A atividade precisa refletir o serviço prestado."),
            ("Não analisar regime tributário", "O regime deve conversar com faturamento e operação."),
            ("Não entender emissão de notas", "Nota fiscal envolve serviço, município e descrição correta."),
            ("Misturar conta pessoal e empresarial", "Isso dificulta leitura de caixa e resultado."),
            ("Não definir pró-labore corretamente", "Retirada sem critério atrapalha a gestão."),
            ("Abra sua empresa com orientação", "A VL ajuda a organizar a abertura desde o início."),
        ],
        "caption": "Abrir empresa sem análise pode gerar ajustes depois. CNAE, regime, emissão de notas, conta PJ e pró-labore precisam ser pensados antes dos primeiros clientes. A orientação contábil ajuda a transformar a abertura em uma base mais segura para crescer.",
    },
    {
        "title": "Contabilidade não é só guia",
        "slug": "contabilidade_nao_e_so_guia",
        "pilar": "Autoridade e confiança",
        "funil": "meio",
        "objective": "Reforçar posicionamento consultivo da VL.",
        "publico": "Empresários que buscam mais orientação.",
        "cta": "Conte com a VL.",
        "groups": ["autoridade"],
        "slides": [
            ("Contabilidade não é só guia", "Guia é parte da rotina. Gestão precisa de leitura."),
            ("É orientação para decisão", "Você entende o que os números querem dizer."),
            ("É análise de regime tributário", "O enquadramento precisa acompanhar a empresa."),
            ("É organização financeira", "Documentos e caixa precisam conversar."),
            ("É acompanhamento do crescimento", "A rotina muda quando a empresa cresce."),
            ("É segurança para empreender", "Menos improviso, mais clareza."),
            ("Conte com a VL", "Contabilidade moderna, próxima e consultiva."),
        ],
        "caption": "Contabilidade não deveria ser lembrada apenas quando a guia chega. Uma rotina bem acompanhada ajuda o empresário a entender obrigações, documentos, resultados e próximos passos. É isso que a VL busca entregar: clareza, orientação e proximidade.",
    },
    {
        "title": "Anexo III ou Anexo V: o que observar?",
        "slug": "anexo_iii_ou_v_observar",
        "pilar": "Simples Nacional e Fator R",
        "funil": "topo",
        "objective": "Educar sobre variáveis de enquadramento no Simples.",
        "publico": "Prestadores de serviço no Simples.",
        "cta": "Peça uma análise individualizada.",
        "groups": ["simples"],
        "slides": [
            ("Anexo III ou Anexo V?", "A resposta não deve sair do achismo."),
            ("Comece pela atividade", "O serviço prestado direciona a análise."),
            ("Olhe faturamento acumulado", "A faixa do Simples importa no cálculo."),
            ("Acompanhe folha e pró-labore", "Esses dados podem influenciar o Fator R."),
            ("Evite comparar só alíquota inicial", "A leitura completa é mais importante."),
            ("Reveja quando a empresa mudar", "Crescimento altera o cenário."),
            ("Fale com a VL", "A análise precisa de dados atualizados."),
        ],
        "caption": "A dúvida entre Anexo III e Anexo V é comum entre prestadores de serviço. Mas a resposta depende de atividade, faturamento, folha, pró-labore e histórico. O melhor caminho é analisar o cenário completo, sem prometer resultado automático.",
    },
    {
        "title": "Separar conta pessoal e conta da empresa",
        "slug": "separar_contas",
        "pilar": "Organização financeira e contábil",
        "funil": "topo",
        "objective": "Ensinar organização financeira básica para pequenas empresas.",
        "publico": "MEIs e pequenos empresários.",
        "cta": "Organize sua rotina com a VL.",
        "groups": ["organizacao"],
        "slides": [
            ("Você mistura conta pessoal e da empresa?", "Esse hábito confunde o resultado do negócio."),
            ("O caixa fica sem leitura", "Você vê dinheiro entrando, mas não sabe o que sobra."),
            ("As retiradas perdem critério", "Pró-labore ajuda a organizar esse ponto."),
            ("Comprovantes se perdem", "A contabilidade fica sem base completa."),
            ("Decisões ficam emocionais", "Sem dados, tudo parece sensação."),
            ("Comece com uma conta PJ", "Depois crie rotina de extratos e comprovantes."),
            ("A VL ajuda a organizar", "Clareza financeira começa no básico bem feito."),
        ],
        "caption": "Separar conta pessoal e conta da empresa é um dos passos mais importantes para enxergar o resultado do negócio. Com conta PJ, pró-labore e documentos organizados, a análise fica mais clara e a tomada de decisão melhora.",
    },
    {
        "title": "Checklist mensal para não travar a contabilidade",
        "slug": "checklist_mensal_contabilidade",
        "pilar": "Organização financeira e contábil",
        "funil": "topo",
        "objective": "Orientar envio de documentos mensais.",
        "publico": "Empresários que querem melhorar rotina documental.",
        "cta": "Salve este checklist e fale com a VL.",
        "groups": ["organizacao"],
        "slides": [
            ("Checklist mensal da contabilidade", "O básico em dia evita correria."),
            ("Notas fiscais emitidas", "Separe notas de serviço e produtos, quando houver."),
            ("Extratos da conta PJ", "O financeiro precisa bater com a operação."),
            ("Comprovantes importantes", "Pagamentos, contratos e recibos relevantes."),
            ("Informações de folha e pró-labore", "Retiradas e equipe precisam estar atualizadas."),
            ("Dúvidas do mês", "Registre o que precisa de orientação."),
            ("Rotina clara, empresa mais organizada", "A VL ajuda a manter esse processo leve."),
        ],
        "caption": "A rotina contábil fica mais eficiente quando os documentos chegam completos e no prazo. Notas, extratos, comprovantes, folha e dúvidas do mês ajudam a contabilidade a orientar melhor a empresa.",
    },
    {
        "title": "Pró-labore para prestadores de serviço",
        "slug": "pro_labore_prestadores",
        "pilar": "Simples Nacional e Fator R",
        "funil": "meio",
        "objective": "Explicar a importância do pró-labore para prestadores PJ.",
        "publico": "Prestadores de serviço e profissionais liberais.",
        "cta": "Revise sua rotina de pró-labore com orientação.",
        "groups": ["simples", "organizacao"],
        "slides": [
            ("Pró-labore: por que prestadores devem olhar isso?", "Retirada do sócio precisa ter método."),
            ("Não é a mesma coisa que lucro", "Pró-labore remunera o trabalho do sócio."),
            ("Ajuda a separar pessoa física e empresa", "A rotina financeira fica mais clara."),
            ("Pode entrar em análises tributárias", "Em alguns casos, conversa com Fator R."),
            ("Precisa caber no caixa", "Não adianta definir valor fora da realidade."),
            ("Revise periodicamente", "A empresa muda, a retirada também pode mudar."),
            ("Fale com a VL", "Cada caso precisa ser analisado com documentos."),
        ],
        "caption": "Pró-labore é uma das peças de organização para prestadores de serviço PJ. Ele ajuda a separar a remuneração do sócio do resultado da empresa e pode ser relevante em análises tributárias. O valor deve ser definido com critério e documentação.",
    },
    {
        "title": "Diagnóstico contábil para prestadores de serviço",
        "slug": "diagnostico_contabil_prestadores",
        "pilar": "Conversão",
        "funil": "fundo",
        "objective": "Apresentar a oferta central da campanha.",
        "publico": "Prestadores, MEIs em crescimento e pequenas empresas.",
        "cta": "Solicite um diagnóstico inicial com a VL.",
        "groups": ["conversao"],
        "slides": [
            ("Diagnóstico contábil para prestadores", "Antes de mudar, entenda o cenário atual."),
            ("Enquadramento", "Sua empresa está no regime coerente para a operação?"),
            ("Notas fiscais", "A emissão conversa com atividade e serviço prestado?"),
            ("Fator R e pró-labore", "Esses pontos estão sendo acompanhados quando aplicáveis?"),
            ("Rotina documental", "A contabilidade recebe o que precisa para orientar?"),
            ("Clareza financeira", "Você sabe se a empresa fatura e lucra?"),
            ("Solicite uma análise inicial", "A VL te ajuda a enxergar o caminho com clareza."),
        ],
        "caption": "O diagnóstico contábil da VL foi pensado para prestadores de serviço que querem clareza antes de tomar decisões. A análise olha enquadramento, notas, Fator R quando aplicável, pró-labore, documentos e organização financeira. Cada caso precisa de avaliação individual.",
    },
]


STORIES = [
    ("Você sabe se sua empresa está no enquadramento correto?", "Enquadramento precisa acompanhar atividade, faturamento e rotina.", "Chame a VL para uma análise inicial.", "Simples Nacional e Fator R", "meio", "Fundo escuro, selo dourado e checklist de 3 pontos."),
    ("Seu contador te explica ou só manda boleto?", "Guia sem explicação deixa o empresário no escuro.", "Fale com a VL e entenda outra forma de atendimento.", "Troca de contador", "meio", "Pergunta grande com ícone de documento e balão de conversa."),
    ("Você é MEI e está crescendo?", "Faturamento, notas e estrutura podem indicar uma nova fase.", "Planeje a transição antes da urgência.", "MEI em crescimento", "meio", "Linha de crescimento com marcador MEI para ME."),
    ("Você sabe o que é Fator R?", "Ele pode influenciar a análise de alguns prestadores no Simples.", "Peça uma explicação simples para a VL.", "Simples Nacional e Fator R", "topo", "Card didático com fórmula visual folha/faturamento."),
    ("Você mistura conta pessoal e conta da empresa?", "Isso dificulta saber se o negócio realmente dá resultado.", "Comece a organizar com orientação.", "Organização financeira e contábil", "topo", "Duas colunas: pessoal e empresa."),
    ("Quer abrir CNPJ com segurança?", "CNAE, regime e notas precisam ser pensados antes.", "Fale com a VL antes de abrir.", "Abertura de empresa", "fundo", "Logo central e lista curta de abertura."),
    ("Já pensou em trocar de contador?", "Com checklist, a transição pode ser mais simples.", "Chame a VL para entender o processo.", "Troca de contador", "fundo", "Seta de transição entre dois cards."),
    ("Sua empresa fatura, mas você sabe se lucra?", "Faturamento não mostra sozinho o resultado da operação.", "Vamos organizar essa leitura?", "Organização financeira e contábil", "meio", "Gráfico simples com receita, custos e resultado."),
    ("Antes de emitir nota, confira sua atividade.", "A descrição do serviço precisa conversar com o cadastro.", "Peça orientação antes da primeira nota.", "Abertura de empresa", "topo", "Nota fiscal estilizada com marcação de atenção."),
    ("Pró-labore está definido ou sai no improviso?", "Retirada sem critério confunde empresa e sócio.", "Revise sua rotina com a VL.", "Organização financeira e contábil", "meio", "Controle de retirada mensal em mini tabela."),
    ("Simples Nacional também precisa de análise.", "Atividade, anexo e faturamento mudam a leitura.", "Peça uma revisão responsável.", "Simples Nacional e Fator R", "meio", "Selo SN com checklist lateral."),
    ("CNAE escolhido no chute pode gerar retrabalho.", "A atividade precisa refletir o serviço real.", "Abra empresa com orientação.", "Abertura de empresa", "topo", "Alvo com etiqueta CNAE."),
    ("MEI perto do limite?", "Esse é o momento de planejar a próxima fase.", "Fale com a VL antes de estourar.", "MEI em crescimento", "fundo", "Barra de progresso de faturamento."),
    ("Contabilidade consultiva muda a conversa.", "Você recebe explicação para decidir melhor.", "Conheça a VL.", "Autoridade e confiança", "meio", "Mesa de análise com gráficos abstratos."),
    ("Documentos atrasados atrapalham a análise.", "Notas, extratos e comprovantes contam a história do mês.", "Organize seu envio mensal.", "Organização financeira e contábil", "topo", "Checklist documental."),
    ("Profissional liberal também precisa de rotina contábil.", "CNPJ, nota e retirada precisam funcionar juntos.", "Fale com a VL.", "Abertura de empresa", "topo", "Ícones de saúde, TI e consultoria."),
    ("Imposto alto nem sempre está errado.", "Mas precisa ser explicado com clareza.", "Peça uma leitura técnica.", "Simples Nacional e Fator R", "meio", "Guia com lupa."),
    ("Sua empresa mudou este ano?", "Faturamento, equipe ou serviço novo pedem revisão.", "Solicite um diagnóstico contábil.", "Conversão", "fundo", "Antes/depois da empresa com seta."),
    ("Quer parar de decidir no escuro?", "Dados contábeis ajudam a enxergar o caminho.", "Converse com a VL.", "Autoridade e confiança", "fundo", "Lanterna sobre gráfico, sem exagero visual."),
    ("Diagnóstico contábil para prestadores.", "Enquadramento, notas, pró-labore e rotina em uma análise inicial.", "Chame a VL no WhatsApp.", "Conversão", "fundo", "Capa de oferta com selo Diagnóstico."),
]


STORY_CALLS = [
    "Sua empresa cresceu e a contabilidade acompanhou?",
    "Você entende a guia que paga todo mês?",
    "CNAE não é detalhe. Você revisou o seu?",
    "MEI perto do limite precisa de plano.",
    "Fator R parece complicado? A gente explica.",
    "Nota fiscal errada pode virar retrabalho.",
    "Conta pessoal e conta da empresa: ainda estão misturadas?",
    "Trocar de contador não precisa ser um caos.",
    "Pró-labore é organização, não burocracia.",
    "Simples Nacional também pede acompanhamento.",
    "Você sabe quais documentos enviar este mês?",
    "Empresa que fatura também precisa entender margem.",
    "Seu contador orienta ou só envia guia?",
    "Antes de abrir CNPJ, analise atividade e regime.",
    "Prestador de serviço: seu enquadramento merece atenção.",
    "Dentista PJ, sua nota conversa com sua atividade?",
    "Psicólogo PJ, sua rotina contábil está organizada?",
    "Profissional de TI, seu CNPJ está bem estruturado?",
    "Agência de marketing: cuidado com CNAE genérico.",
    "Clínica de estética precisa de análise além da guia.",
    "Imposto precisa ser explicado com clareza.",
    "Documentos certos deixam a contabilidade mais útil.",
    "Crescimento sem organização vira urgência.",
    "Diagnóstico contábil é o começo da clareza.",
    "Sua empresa tem conta PJ e retirada definida?",
    "Enquadramento muda quando a operação muda.",
    "Planeje antes de desenquadrar do MEI.",
    "A contabilidade deve apoiar decisão, não só obrigação.",
    "Quer abrir empresa sem improviso?",
    "Chame a VL para entender o próximo passo.",
]


WHATSAPP_MESSAGES = [
    ("Abertura de empresa", "Olá! Que bom falar com você. Para orientar a abertura do CNPJ, me conte qual serviço você pretende prestar, se já tem previsão de faturamento e se vai emitir nota para empresas ou pessoas físicas."),
    ("MEI em crescimento", "Perfeito. Para entender a transição do MEI, preciso saber seu faturamento aproximado dos últimos 12 meses, atividade exercida e se você já emite notas com frequência."),
    ("Troca de contador", "Entendi. A troca pode ser organizada com tranquilidade. Você consegue me dizer o que mais incomoda hoje: falta de retorno, pouca orientação, documentos ou dúvidas sobre impostos?"),
    ("Perguntou preço", "Consigo te orientar melhor depois de entender o cenário, porque o valor depende do tipo de empresa, regime, volume de notas e rotina necessária. Me passa esses dados para avaliarmos com responsabilidade?"),
    ("Fator R", "Boa pergunta. O Fator R depende de atividade, faturamento e folha/pró-labore. Para avaliar se se aplica ao seu caso, precisamos olhar os dados da empresa e o histórico recente."),
    ("Revisar imposto", "Vamos analisar com cuidado. Nem todo imposto alto está errado, mas ele precisa ser explicado. Você sabe qual regime sua empresa está hoje e consegue enviar uma visão do faturamento mensal?"),
    ("Lead sumiu", "Oi! Passando só para saber se ainda faz sentido te ajudar com essa análise. Se preferir, me envie o ponto principal da sua dúvida e retomamos por ali."),
    ("Pediu proposta", "Claro. Para preparar uma proposta coerente, preciso confirmar atividade, regime atual, quantidade média de notas, existência de folha/pró-labore e se há alguma pendência hoje."),
    ("Já tem contador", "Sem problema. Muitos clientes chegam já atendidos por outra contabilidade. A ideia é entender se você recebe a orientação que precisa e se a troca faria sentido para o seu momento."),
    ("Atendimento rápido", "Consigo te direcionar. Me diga em uma frase o que você precisa resolver agora: abrir empresa, trocar contador, MEI crescendo, nota fiscal, Fator R ou revisão de enquadramento?"),
]


def post_caption(post: dict) -> str:
    return (
        f"{post['title']}\n\n"
        f"{post['body']}\n\n"
        f"{post['note']}\n\n"
        f"{post['cta']}"
    )


def frame_class(format_key: str) -> str:
    return "frame-square" if format_key == "square" else "frame-vertical"


def format_label(format_key: str) -> str:
    return "Feed quadrado 1080x1080" if format_key == "square" else "Feed vertical 1080x1350"


def create_post_html(post: dict, index: int) -> str:
    logo = LOGO_PRIMARIA if post["variant"] == "light" else LOGO_BRANCA
    lioncio_html = ""
    if index in {5, 11, 17, 24}:
        lioncio_html = f'<img class="lioncio-mark" src="{LIONCIO}" alt="Mascote Lioncio">'
    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(post['title'])} | SoulCont</title>
  <link rel="stylesheet" href="../../06_templates/style.css">
</head>
<body class="preview-page">
  <main class="stage">
    <article class="creative-frame {frame_class(post['format'])} theme-{post['variant']}" data-export-name="post_{index:03d}_{post['slug']}.png">
      <div class="brand-row">
        <img src="{logo}" alt="SoulCont">
        <span>{escape(post['pilar'])}</span>
      </div>
      <div class="visual-symbol">{escape(post['icon'])}</div>
      {lioncio_html}
      <section class="copy-area">
        <p class="eyebrow">Conteúdo educativo</p>
        <h1>{escape(post['title'])}</h1>
        <p class="subtitle">{escape(post['subtitle'])}</p>
        <ul class="point-list">
          {html_list(post['bullets'])}
        </ul>
      </section>
      <footer class="frame-cta">
        <strong>{escape(post['cta'])}</strong>
        <span>@soulcontt</span>
      </footer>
    </article>
  </main>
</body>
</html>
"""


def create_carousel_html(carousel: dict, index: int) -> str:
    frames: list[str] = []
    for slide_index, (title, text) in enumerate(carousel["slides"], start=1):
        theme = ["dark", "light", "slate", "dark", "gold", "light", "dark"][(slide_index - 1) % 7]
        logo = LOGO_PRIMARIA if theme == "light" else LOGO_BRANCA
        lioncio_html = f'<img class="lioncio-corner" src="{LIONCIO_DIREITA}" alt="Mascote Lioncio">' if slide_index == 7 and index in {1, 3, 5, 10} else ""
        frames.append(
            f"""
    <article class="creative-frame frame-vertical theme-{theme} carousel-slide" data-export-name="carrossel_{index:03d}_slide_{slide_index:02d}_{carousel['slug']}.png">
      <div class="brand-row">
        <img src="{logo}" alt="SoulCont">
        <span>{slide_index:02d}/07</span>
      </div>
      <div class="slide-number">{slide_index:02d}</div>
      {lioncio_html}
      <section class="copy-area carousel-copy">
        <p class="eyebrow">{escape(carousel['pilar'])}</p>
        <h1>{escape(title)}</h1>
        <p class="subtitle">{escape(text)}</p>
      </section>
      <footer class="frame-cta">
        <strong>{escape(carousel['cta']) if slide_index == 7 else 'Arraste para continuar'}</strong>
        <span>@soulcontt</span>
      </footer>
    </article>
"""
        )
    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(carousel['title'])} | SoulCont</title>
  <link rel="stylesheet" href="../../06_templates/style.css">
</head>
<body class="preview-page">
  <main class="stage carousel-stage">
{''.join(frames)}
  </main>
</body>
</html>
"""


def create_story_html(story: tuple[str, str, str, str, str, str], index: int) -> str:
    title, explanation, cta, pilar, funil, visual = story
    theme = ["dark", "light", "gold", "slate"][index % 4]
    logo = LOGO_PRIMARIA if theme == "light" else LOGO_BRANCA
    lioncio_html = f'<img class="lioncio-story" src="{LIONCIO}" alt="Mascote Lioncio">' if index in {3, 9, 14, 20} else ""
    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Story {index:03d} | SoulCont</title>
  <link rel="stylesheet" href="../../06_templates/style.css">
</head>
<body class="preview-page">
  <main class="stage">
    <article class="creative-frame frame-story theme-{theme} story-frame" data-export-name="story_{index:03d}_{slugify(title)}.png">
      <div class="brand-row">
        <img src="{logo}" alt="SoulCont">
        <span>Story educativo</span>
      </div>
      <div class="story-pill">{escape(pilar)}</div>
      {lioncio_html}
      <section class="copy-area story-copy">
        <h1>{escape(title)}</h1>
        <p class="subtitle">{escape(explanation)}</p>
      </section>
      <footer class="frame-cta story-cta">
        <strong>{escape(cta)}</strong>
        <span>@soulcontt</span>
      </footer>
    </article>
  </main>
</body>
</html>
"""


STYLE_CSS = """
:root {
  --vl-navy: #0F2233;
  --vl-navy-2: #18354D;
  --vl-navy-3: #051937;
  --vl-gold: #C8A86B;
  --vl-gold-2: #E0C586;
  --vl-cream: #F4F1EA;
  --vl-white: #FFFFFF;
  --vl-muted: rgba(244, 241, 234, 0.74);
  --vl-ink: #101820;
  --vl-green: #2FAF7A;
  --vl-orange: #E38B29;
  --font-title: "Syne", "Outfit", "Inter", Arial, sans-serif;
  --font-body: "Inter", "Poppins", Arial, sans-serif;
}

* {
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  min-height: 100%;
}

body {
  font-family: var(--font-body);
  background: #e7ebef;
}

.preview-page {
  padding: 40px;
}

.stage {
  display: grid;
  gap: 40px;
  justify-content: center;
}

.carousel-stage {
  grid-template-columns: 1fr;
}

.creative-frame {
  position: relative;
  overflow: hidden;
  width: var(--frame-width);
  height: var(--frame-height);
  padding: 70px 72px 64px;
  color: var(--vl-cream);
  background:
    linear-gradient(135deg, rgba(200, 168, 107, 0.14), transparent 34%),
    linear-gradient(160deg, var(--vl-navy-3) 0%, var(--vl-navy) 45%, #111A25 100%);
  border: 1px solid rgba(200, 168, 107, 0.26);
  isolation: isolate;
}

.creative-frame::before {
  content: "";
  position: absolute;
  inset: 36px;
  border: 2px solid rgba(200, 168, 107, 0.22);
  pointer-events: none;
  z-index: -1;
}

.creative-frame::after {
  content: "";
  position: absolute;
  right: -120px;
  bottom: 110px;
  width: 520px;
  height: 520px;
  border: 80px solid rgba(200, 168, 107, 0.08);
  transform: rotate(18deg);
  z-index: -1;
}

.frame-square {
  --frame-width: 1080px;
  --frame-height: 1080px;
}

.frame-vertical {
  --frame-width: 1080px;
  --frame-height: 1350px;
}

.frame-story {
  --frame-width: 1080px;
  --frame-height: 1920px;
  padding: 92px 76px 84px;
}

.theme-light {
  color: var(--vl-navy);
  background:
    linear-gradient(145deg, rgba(200, 168, 107, 0.16), transparent 38%),
    linear-gradient(180deg, #fbf8f2 0%, #ffffff 100%);
  border-color: rgba(15, 34, 51, 0.12);
}

.theme-light::before {
  border-color: rgba(15, 34, 51, 0.13);
}

.theme-light::after {
  border-color: rgba(15, 34, 51, 0.05);
}

.theme-gold {
  color: #111111;
  background:
    linear-gradient(135deg, #F1DDAF 0%, var(--vl-gold) 48%, #B58F4D 100%);
  border-color: rgba(15, 34, 51, 0.22);
}

.theme-gold::before {
  border-color: rgba(15, 34, 51, 0.17);
}

.theme-gold::after {
  border-color: rgba(255, 255, 255, 0.16);
}

.theme-slate {
  color: var(--vl-cream);
  background:
    linear-gradient(145deg, rgba(47, 175, 122, 0.12), transparent 36%),
    linear-gradient(160deg, #10202F 0%, #18354D 58%, #253B4C 100%);
}

.brand-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
  min-height: 70px;
  position: relative;
  z-index: 2;
}

.brand-row img {
  display: block;
  width: 300px;
  height: auto;
  max-height: 78px;
  object-fit: contain;
}

.brand-row span {
  max-width: 420px;
  text-align: right;
  font-size: 24px;
  line-height: 1.2;
  font-weight: 700;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  color: currentColor;
  opacity: 0.78;
}

.copy-area {
  position: absolute;
  left: 72px;
  right: 72px;
  top: 245px;
  z-index: 2;
}

.frame-square .copy-area {
  top: 210px;
}

.eyebrow,
.story-pill {
  display: inline-flex;
  align-items: center;
  min-height: 46px;
  padding: 0 20px;
  margin: 0 0 26px;
  border: 1px solid rgba(200, 168, 107, 0.36);
  background: rgba(200, 168, 107, 0.13);
  color: currentColor;
  font-size: 20px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.theme-light .eyebrow,
.theme-light .story-pill {
  background: rgba(15, 34, 51, 0.06);
  border-color: rgba(15, 34, 51, 0.16);
}

h1 {
  max-width: 860px;
  margin: 0;
  font-family: var(--font-title);
  font-size: 74px;
  line-height: 0.98;
  letter-spacing: 0;
  font-weight: 800;
}

.frame-square h1 {
  font-size: 66px;
}

.carousel-copy h1 {
  font-size: 78px;
}

.story-copy h1 {
  font-size: 88px;
  line-height: 1;
}

.subtitle {
  max-width: 760px;
  margin: 32px 0 0;
  font-size: 34px;
  line-height: 1.28;
  font-weight: 600;
  color: currentColor;
  opacity: 0.86;
}

.frame-square .subtitle {
  font-size: 30px;
}

.story-copy .subtitle {
  margin-top: 42px;
  font-size: 40px;
  max-width: 780px;
}

.point-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  padding: 0;
  margin: 54px 0 0;
  list-style: none;
}

.frame-square .point-list {
  margin-top: 38px;
}

.point-list li {
  min-height: 82px;
  display: flex;
  align-items: center;
  padding: 18px 22px;
  border: 1px solid rgba(244, 241, 234, 0.16);
  background: rgba(244, 241, 234, 0.07);
  font-size: 25px;
  line-height: 1.18;
  font-weight: 750;
}

.theme-light .point-list li,
.theme-gold .point-list li {
  border-color: rgba(15, 34, 51, 0.15);
  background: rgba(15, 34, 51, 0.05);
}

.visual-symbol,
.slide-number {
  position: absolute;
  right: 74px;
  top: 355px;
  min-width: 190px;
  height: 190px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(200, 168, 107, 0.34);
  color: var(--vl-gold-2);
  font-family: var(--font-title);
  font-size: 52px;
  font-weight: 800;
  letter-spacing: 0;
  background: rgba(8, 20, 32, 0.22);
  z-index: 1;
}

.theme-light .visual-symbol,
.theme-light .slide-number,
.theme-gold .visual-symbol,
.theme-gold .slide-number {
  color: var(--vl-navy);
  border-color: rgba(15, 34, 51, 0.2);
  background: rgba(255, 255, 255, 0.28);
}

.frame-square .visual-symbol {
  top: 312px;
  right: 62px;
  min-width: 150px;
  height: 150px;
  font-size: 42px;
}

.slide-number {
  top: 270px;
  right: 78px;
  min-width: 170px;
  height: 170px;
  font-size: 58px;
  opacity: 0.78;
}

.frame-cta {
  position: absolute;
  left: 72px;
  right: 72px;
  bottom: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
  min-height: 104px;
  padding: 24px 28px;
  color: #111111;
  background: linear-gradient(135deg, #E7C982 0%, var(--vl-gold) 62%, #B58F4D 100%);
  z-index: 3;
}

.theme-gold .frame-cta {
  color: var(--vl-cream);
  background: linear-gradient(135deg, var(--vl-navy) 0%, #10202F 100%);
}

.theme-light .frame-cta {
  color: var(--vl-cream);
  background: linear-gradient(135deg, var(--vl-navy) 0%, var(--vl-navy-2) 100%);
}

.frame-cta strong {
  max-width: 690px;
  font-size: 27px;
  line-height: 1.12;
  font-weight: 850;
}

.frame-cta span {
  font-size: 22px;
  font-weight: 750;
  white-space: nowrap;
}

.lioncio-mark {
  position: absolute;
  right: 70px;
  bottom: 188px;
  width: 210px;
  height: auto;
  z-index: 2;
  filter: drop-shadow(0 18px 32px rgba(0, 0, 0, 0.22));
}

.lioncio-corner {
  position: absolute;
  right: 58px;
  bottom: 176px;
  width: 240px;
  z-index: 2;
}

.lioncio-story {
  position: absolute;
  right: 80px;
  bottom: 210px;
  width: 310px;
  z-index: 2;
}

.story-pill {
  position: absolute;
  left: 76px;
  top: 246px;
  max-width: 780px;
  line-height: 1.1;
}

.story-copy {
  top: 510px;
}

.story-cta {
  min-height: 150px;
  bottom: 84px;
}

.story-cta strong {
  font-size: 34px;
}

.story-cta span {
  font-size: 26px;
}

@media screen and (max-width: 1200px) {
  .preview-page {
    padding: 20px;
  }
}
"""


EXPORT_JS = r"""
const fs = require("fs");
const os = require("os");
const path = require("path");
const { pathToFileURL } = require("url");
const Module = require("module");

function addNodePath(modulePath) {
  if (!fs.existsSync(modulePath)) return;
  const current = process.env.NODE_PATH ? process.env.NODE_PATH.split(path.delimiter) : [];
  if (!current.includes(modulePath)) {
    process.env.NODE_PATH = [modulePath, ...current].join(path.delimiter);
    Module._initPaths();
  }
}

function loadPlaywright() {
  try {
    return require("playwright");
  } catch (firstError) {
    const runtimeNodeModules = path.join(
      os.homedir(),
      ".cache",
      "codex-runtimes",
      "codex-primary-runtime",
      "dependencies",
      "node",
      "node_modules"
    );

    addNodePath(runtimeNodeModules);

    const pnpmDir = path.join(runtimeNodeModules, ".pnpm");
    if (fs.existsSync(pnpmDir)) {
      const playwrightPkg = fs
        .readdirSync(pnpmDir)
        .find((name) => /^playwright@\d/.test(name));
      if (playwrightPkg) {
        addNodePath(path.join(pnpmDir, playwrightPkg, "node_modules"));
      }
    }

    try {
      return require("playwright");
    } catch {
      const fallback = path.join(runtimeNodeModules, "playwright", "index.js");
      if (fs.existsSync(fallback)) {
        return require(fallback);
      }
    }

    console.error("Playwright não foi encontrado.");
    console.error("Instale Playwright no ambiente Node ou execute com o NODE_PATH do runtime Codex.");
    throw firstError;
  }
}

function walk(dir, results = []) {
  if (!fs.existsSync(dir)) return results;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, results);
    if (entry.isFile() && entry.name === "arte.html") results.push(full);
  }
  return results;
}

async function launchBrowser(chromium) {
  const candidates = [
    { channel: "msedge" },
    { channel: "chrome" },
    { executablePath: "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe" },
    { executablePath: "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe" },
    { executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" },
    { executablePath: "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" },
    {},
  ];

  const errors = [];
  for (const candidate of candidates) {
    try {
      if (candidate.executablePath && !fs.existsSync(candidate.executablePath)) continue;
      return await chromium.launch({ headless: true, ...candidate });
    } catch (error) {
      errors.push(error.message);
    }
  }

  throw new Error(`Não foi possível abrir Edge, Chrome ou Chromium do Playwright.\n${errors.join("\n")}`);
}

(async () => {
  const { chromium } = loadPlaywright();
  const base = path.resolve(__dirname, "..");
  const outDir = path.join(base, "07_exportacao", "png");
  fs.mkdirSync(outDir, { recursive: true });

  const htmlFiles = [
    ...walk(path.join(base, "01_posts_feed")),
    ...walk(path.join(base, "02_carrosseis")),
    ...walk(path.join(base, "03_stories")),
  ];

  const browser = await launchBrowser(chromium);
  const page = await browser.newPage({ viewport: { width: 1280, height: 2200 }, deviceScaleFactor: 1 });

  let count = 0;
  for (const file of htmlFiles) {
    await page.goto(pathToFileURL(file).href, { waitUntil: "load" });
    await page.waitForTimeout(250);
    const frames = await page.locator(".creative-frame").all();

    for (let i = 0; i < frames.length; i++) {
      const frame = frames[i];
      const name = await frame.getAttribute("data-export-name");
      const fallbackName = `${path.basename(path.dirname(file))}_${String(i + 1).padStart(2, "0")}.png`;
      const outputPath = path.join(outDir, name || fallbackName);
      await frame.screenshot({ path: outputPath });
      count += 1;
    }
  }

  await browser.close();
  console.log(`Exportação concluída: ${count} PNGs em ${outDir}`);
})();
"""


def create_templates() -> None:
    write(BASE / "06_templates" / "style.css", STYLE_CSS)
    write(
        BASE / "06_templates" / "template_post_quadrado.html",
        """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Template Post Quadrado | VL</title>
  <link rel="stylesheet" href="style.css">
</head>
<body class="preview-page">
  <main class="stage">
    <article class="creative-frame frame-square theme-dark" data-export-name="template_post_quadrado.png">
      <div class="brand-row"><img src="../../../assets/img/logo/vl_logo_horizontal_branca.svg" alt="SoulCont"><span>Pilar do conteúdo</span></div>
      <div class="visual-symbol">VL</div>
      <section class="copy-area">
        <p class="eyebrow">Conteúdo educativo</p>
        <h1>Título forte e ético do post</h1>
        <p class="subtitle">Subtítulo curto com a ideia principal.</p>
        <ul class="point-list"><li>Ponto 1</li><li>Ponto 2</li><li>Ponto 3</li><li>Ponto 4</li></ul>
      </section>
      <footer class="frame-cta"><strong>CTA claro para WhatsApp ou diagnóstico.</strong><span>@soulcontt</span></footer>
    </article>
  </main>
</body>
</html>
""",
    )
    write(
        BASE / "06_templates" / "template_post_vertical.html",
        """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Template Post Vertical | VL</title>
  <link rel="stylesheet" href="style.css">
</head>
<body class="preview-page">
  <main class="stage">
    <article class="creative-frame frame-vertical theme-light" data-export-name="template_post_vertical.png">
      <div class="brand-row"><img src="../../../assets/img/logo/vl_logo_horizontal_primaria.svg" alt="SoulCont"><span>Pilar do conteúdo</span></div>
      <div class="visual-symbol">%</div>
      <section class="copy-area">
        <p class="eyebrow">Conteúdo educativo</p>
        <h1>Título forte e legível para celular</h1>
        <p class="subtitle">Subtítulo curto com contexto.</p>
        <ul class="point-list"><li>Ponto 1</li><li>Ponto 2</li><li>Ponto 3</li><li>Ponto 4</li></ul>
      </section>
      <footer class="frame-cta"><strong>CTA claro para WhatsApp ou diagnóstico.</strong><span>@soulcontt</span></footer>
    </article>
  </main>
</body>
</html>
""",
    )
    write(
        BASE / "06_templates" / "template_carrossel.html",
        """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Template Carrossel | VL</title>
  <link rel="stylesheet" href="style.css">
</head>
<body class="preview-page">
  <main class="stage carousel-stage">
    <article class="creative-frame frame-vertical theme-dark carousel-slide" data-export-name="template_carrossel_slide_01.png">
      <div class="brand-row"><img src="../../../assets/img/logo/vl_logo_horizontal_branca.svg" alt="SoulCont"><span>01/07</span></div>
      <div class="slide-number">01</div>
      <section class="copy-area carousel-copy"><p class="eyebrow">Pilar</p><h1>Gancho do carrossel</h1><p class="subtitle">Frase curta para abrir a sequência.</p></section>
      <footer class="frame-cta"><strong>Arraste para continuar</strong><span>@soulcontt</span></footer>
    </article>
  </main>
</body>
</html>
""",
    )
    write(
        BASE / "06_templates" / "template_story.html",
        """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Template Story | VL</title>
  <link rel="stylesheet" href="style.css">
</head>
<body class="preview-page">
  <main class="stage">
    <article class="creative-frame frame-story theme-slate story-frame" data-export-name="template_story.png">
      <div class="brand-row"><img src="../../../assets/img/logo/vl_logo_horizontal_branca.svg" alt="SoulCont"><span>Story educativo</span></div>
      <div class="story-pill">Pilar</div>
      <section class="copy-area story-copy"><h1>Pergunta curta para story?</h1><p class="subtitle">Explicação breve em uma frase.</p></section>
      <footer class="frame-cta story-cta"><strong>CTA claro para resposta ou WhatsApp.</strong><span>@soulcontt</span></footer>
    </article>
  </main>
</body>
</html>
""",
    )


def create_strategy_docs() -> None:
    write(
        BASE / "00_estrategia" / "estrategia_campanha.md",
        f"""
# Estratégia da campanha

Marca: **SoulCont**

Oferta central: **Diagnóstico Contábil para Prestadores de Serviço**

## Objetivo

Criar uma esteira de conteúdo para Instagram que atraia MEIs em crescimento, prestadores de serviço, profissionais liberais e pequenas empresas que precisam de abertura de empresa, revisão de enquadramento, troca de contador ou organização contábil.

## Posicionamento usado

A VL aparece como uma contabilidade moderna, consultiva, digital e próxima. A comunicação evita promessas absolutas sobre tributos e trabalha com clareza, análise individual e orientação responsável.

## Pilares

1. Abertura de empresa.
2. Troca de contador.
3. Simples Nacional e Fator R.
4. MEI em crescimento.
5. Organização financeira e contábil.
6. Autoridade e confiança.
7. Conversão para diagnóstico.

## Distribuição editorial

- Topo de funil: educação e descoberta.
- Meio de funil: dor, consideração e comparação.
- Fundo de funil: diagnóstico, WhatsApp e decisão assistida.

Nesta biblioteca foram criados {len(POSTS)} posts de feed, {len(CAROUSELS)} carrosséis e {len(STORIES)} stories.

## Assets encontrados e reaproveitados

- Logos oficiais em `assets/img/logo/`.
- Logo horizontal branca e primária.
- Favicon e monogramas oficiais.
- Mascote Lioncio em `assets/img/lioncio.png`.
- Variações do Lioncio caminhando.
- Paleta principal extraída do site: azul profundo `#0F2233`, azul secundário `#18354D`, dourado `#C8A86B`, creme `#F4F1EA`.
- Padrão visual já usado: fundos escuros, bordas douradas, layout consultivo e premium.

## Assets faltantes para revisão da marca

- Manual oficial de marca, se existir.
- Fotos autorais atuais da equipe ou escritório.
- Versões adicionais do Lioncio em alta resolução e poses específicas.
- Pacote oficial de ícones, caso a marca tenha um.
- Número de WhatsApp público definitivo para inserir nas artes, se for desejado.

## Observação ética

Todo conteúdo tributário usa linguagem de possibilidade e análise individual: "pode influenciar", "depende", "precisa ser analisado" e "cada caso deve ser avaliado".
""",
    )
    write(
        BASE / "00_estrategia" / "persona_publico_alvo.md",
        """
# Persona e público-alvo

## Persona principal

Prestador de serviço que abriu ou quer abrir CNPJ, emite nota fiscal, está no Simples Nacional ou saiu recentemente do MEI. Tem rotina corrida, entende pouco de contabilidade e sente falta de explicação clara.

## Segmentos prioritários

- MEIs em crescimento.
- Microempresas e pequenas empresas.
- Profissionais liberais.
- Profissionais da saúde, psicólogos, dentistas, fisioterapeutas e clínicas de estética.
- Agências de marketing.
- Profissionais de TI.
- Engenheiros, arquitetos e consultores.
- Empresas pequenas em São Paulo e região.

## Dores

- Contador que só envia guias.
- Dúvida sobre imposto e enquadramento.
- Medo de errar nota fiscal.
- MEI crescendo sem saber o próximo passo.
- Falta de clareza sobre lucro da operação.
- Mistura entre conta pessoal e empresarial.
- Insegurança para trocar de contador.
""",
    )
    write(
        BASE / "00_estrategia" / "tom_de_voz.md",
        """
# Tom de voz

## Direção

Claro, educativo, profissional, direto, consultivo e humano. A VL fala como quem orienta, traduz e acompanha, sem exagero e sem tom agressivo.

## Usar

- "Vamos analisar o cenário."
- "Depende da atividade, do faturamento e da rotina."
- "A empresa precisa de clareza para decidir."
- "Nem todo imposto alto está errado, mas precisa ser explicado."
- "A transição pode ser organizada."

## Evitar

- Promessas absolutas sobre economia tributária.
- Ataque direto a outros contadores.
- Linguagem de atalhos ou soluções milagrosas.
- Consultoria individual sem análise documental.
- Tom de urgência artificial ou sensacionalista.
""",
    )
    write(
        BASE / "00_estrategia" / "oferta_diagnostico_contabil.md",
        """
# Oferta: Diagnóstico Contábil para Prestadores de Serviço

## Promessa ética

Ajudar o prestador de serviço a entender se a empresa está organizada, se o enquadramento atual faz sentido e quais pontos precisam de atenção, sem transformar a análise em promessa de resultado.

## O que analisar

- Enquadramento e regime atual.
- CNAE e atividade exercida.
- Emissão de notas fiscais.
- Fator R quando aplicável.
- Pró-labore e rotina de retirada.
- Documentos enviados à contabilidade.
- Separação entre pessoa física e empresa.
- Clareza sobre resultado financeiro.

## CTA central

Quer entender se sua empresa está no caminho certo? Chame a SoulCont e solicite um diagnóstico inicial.
""",
    )
    write(
        BASE / "00_estrategia" / "banco_de_ctas.md",
        "# Banco de CTAs\n\n" + md_list(CTA_BANK),
    )
    hashtag_doc = ["# Banco de hashtags", "", "Recomendação: usar de 5 a 10 hashtags por post, priorizando relevância."]
    for group, tags in HASHTAG_GROUPS.items():
        hashtag_doc.append(f"\n## {group.capitalize()}\n")
        hashtag_doc.append(" ".join(tags))
    write(BASE / "00_estrategia" / "banco_de_hashtags.md", "\n".join(hashtag_doc))
    write(
        BASE / "00_estrategia" / "mensagens_whatsapp.md",
        "# Mensagens para WhatsApp Business\n\n"
        + "\n\n".join(f"## {title}\n\n{message}" for title, message in WHATSAPP_MESSAGES)
        + "\n\n## Respostas rápidas sugeridas\n\n"
        + md_list([f"/{slugify(title)} - {message}" for title, message in WHATSAPP_MESSAGES]),
    )


def create_posts() -> None:
    feed_caption_lines = ["# Legendas de feed\n"]
    for index, post in enumerate(POSTS, start=1):
        folder = BASE / "01_posts_feed" / f"post_{index:03d}_{post['slug']}"
        tags = hashtags(*post["groups"])
        caption = post_caption(post)
        write(folder / "arte.html", create_post_html(post, index))
        write(
            folder / "ficha.md",
            f"""
# {post['title']}

Objetivo:
{post['objective']}

Público:
{post['publico']}

Pilar:
{post['pilar']}

Formato:
{format_label(post['format'])}

Etapa do funil:
{post['funil']}

Texto da arte:
- Título: {post['title']}
- Subtítulo: {post['subtitle']}
{md_list(post['bullets'])}

Legenda:
{caption}

CTA:
{post['cta']}

Hashtags:
{" ".join(tags)}

Observações:
Revisar se o CTA deve incluir telefone, link ou apenas chamada para WhatsApp. Conteúdo educativo, sem promessa absoluta de resultado tributário.

Status: pronto para revisão humana
""",
        )
        feed_caption_lines.append(
            f"## Post {index:03d} - {post['title']}\n\n{caption}\n\nHashtags: {' '.join(tags)}\n"
        )
    write(BASE / "04_legendas" / "legendas_feed.md", "\n".join(feed_caption_lines))


def create_carousels() -> None:
    carousel_caption_lines = ["# Legendas de carrosséis\n"]
    for index, carousel in enumerate(CAROUSELS, start=1):
        folder = BASE / "02_carrosseis" / f"carrossel_{index:03d}_{carousel['slug']}"
        tags = hashtags(*carousel["groups"])
        slide_text = "\n".join(
            f"{slide_index}. **{title}**\n   {text}"
            for slide_index, (title, text) in enumerate(carousel["slides"], start=1)
        )
        write(folder / "arte.html", create_carousel_html(carousel, index))
        write(
            folder / "ficha.md",
            f"""
# {carousel['title']}

Objetivo:
{carousel['objective']}

Público:
{carousel['publico']}

Pilar:
{carousel['pilar']}

Formato:
Carrossel estático 1080x1350 por slide

Etapa do funil:
{carousel['funil']}

Texto da arte:
{slide_text}

Legenda:
{carousel['caption']}

CTA:
{carousel['cta']}

Hashtags:
{" ".join(tags)}

Observações:
Carrossel com 7 slides. Revisar se algum tema exige complemento jurídico/contábil antes da publicação.

Status: pronto para revisão humana
""",
        )
        carousel_caption_lines.append(
            f"## Carrossel {index:03d} - {carousel['title']}\n\n{carousel['caption']}\n\nHashtags: {' '.join(tags)}\n"
        )
    write(BASE / "04_legendas" / "legendas_carrosseis.md", "\n".join(carousel_caption_lines))


def create_stories() -> None:
    story_lines = ["# Legendas e chamadas para stories\n"]
    for index, story in enumerate(STORIES, start=1):
        title, explanation, cta, pilar, funil, visual = story
        folder = BASE / "03_stories" / f"story_{index:03d}_{slugify(title)}"
        write(folder / "arte.html", create_story_html(story, index))
        write(
            folder / "ficha.md",
            f"""
# {title}

Objetivo:
Gerar resposta, toque no link ou conversa no WhatsApp a partir de uma dor específica.

Público:
Prestadores de serviço, MEIs e pequenos empresários.

Pilar:
{pilar}

Formato:
Story estático 1080x1920

Etapa do funil:
{funil}

Texto da arte:
- Pergunta: {title}
- Explicação: {explanation}
- CTA: {cta}

Legenda interna:
{explanation}

CTA:
{cta}

Hashtags:
Não recomendado usar muitas hashtags em story. Se usar, manter 1 a 3 discretas.

Ideia visual:
{visual}

Observações:
Pode ser usado com sticker de pergunta, enquete ou link após revisão humana.

Status: pronto para revisão humana
""",
        )
        story_lines.append(f"## Story {index:03d} - {title}\n\nTexto curto: {explanation}\n\nCTA: {cta}\n\nIdeia visual: {visual}\n")
    story_lines.append("\n# 30 chamadas curtas extras para stories\n")
    story_lines.extend(f"{i:02d}. {call}" for i, call in enumerate(STORY_CALLS, start=1))
    write(BASE / "04_legendas" / "legendas_stories.md", "\n".join(story_lines))


def create_calendar() -> None:
    rows = []
    for day in range(1, 31):
        post = POSTS[day - 1]
        if day in {3, 6, 9, 12, 15, 18, 21, 24, 27, 30}:
            carousel_index = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30].index(day)
            item = CAROUSELS[carousel_index]
            formato = "Carrossel 1080x1350"
            legenda = f"legendas_carrosseis.md#carrossel-{carousel_index + 1:03d}"
            tema = item["title"]
            pilar = item["pilar"]
            objetivo = item["objective"]
            cta = item["cta"]
        else:
            formato = format_label(post["format"])
            legenda = f"legendas_feed.md#post-{day:03d}"
            tema = post["title"]
            pilar = post["pilar"]
            objetivo = post["objective"]
            cta = post["cta"]
        rows.append(
            {
                "dia": day,
                "tema": tema,
                "formato": formato,
                "pilar": pilar,
                "objetivo": objetivo,
                "cta": cta,
                "legenda_associada": legenda,
                "status": "pronto para revisão humana",
            }
        )

    csv_path = BASE / "05_calendario" / "calendario_30_dias.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md_rows = [
        "# Calendário editorial de 30 dias",
        "",
        "| Dia | Tema | Formato | Pilar | Objetivo | CTA | Legenda associada | Status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        md_rows.append(
            f"| {row['dia']} | {row['tema']} | {row['formato']} | {row['pilar']} | {row['objetivo']} | {row['cta']} | {row['legenda_associada']} | {row['status']} |"
        )
    write(BASE / "05_calendario" / "calendario_30_dias.md", "\n".join(md_rows))


def create_review_docs() -> None:
    matrix = [
        "# Matriz de conteúdo",
        "",
        "| ID | Tipo | Tema | Pilar | Funil | Formato |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for index, post in enumerate(POSTS, start=1):
        matrix.append(f"| post_{index:03d} | Feed | {post['title']} | {post['pilar']} | {post['funil']} | {format_label(post['format'])} |")
    for index, item in enumerate(CAROUSELS, start=1):
        matrix.append(f"| carrossel_{index:03d} | Carrossel | {item['title']} | {item['pilar']} | {item['funil']} | 7 slides 1080x1350 |")
    for index, story in enumerate(STORIES, start=1):
        matrix.append(f"| story_{index:03d} | Story | {story[0]} | {story[3]} | {story[4]} | 1080x1920 |")
    write(BASE / "08_revisao" / "matriz_de_conteudo.md", "\n".join(matrix))

    write(
        BASE / "08_revisao" / "checklist_revisao.md",
        """
# Checklist de revisão humana

- [ ] Conferir se todos os textos estão em português brasileiro.
- [ ] Validar se nenhum post promete resultado tributário absoluto.
- [ ] Confirmar que não há orientação individual sem análise documental.
- [ ] Revisar termos técnicos: CNAE, Fator R, Anexo III, Anexo V, pró-labore e MEI.
- [ ] Confirmar se o WhatsApp público e o arroba do Instagram estão corretos antes de publicar.
- [ ] Verificar se o logo usado é a versão atual da marca.
- [ ] Revisar uso do Lioncio e retirar se a marca preferir uma linha mais institucional.
- [ ] Exportar PNGs e conferir legibilidade no celular.
- [ ] Conferir calendário e alternância entre topo, meio e fundo de funil.
- [ ] Aprovar cada arte antes de publicar ou agendar em qualquer plataforma.
""",
    )
    write(
        BASE / "08_revisao" / "lista_de_pendencias.md",
        """
# Lista de pendências

- Confirmar telefone público de WhatsApp a ser usado em CTAs finais.
- Confirmar se o arroba `@soulcontt` é o perfil definitivo.
- Validar com o responsável técnico os textos sobre Fator R, Anexo III, Anexo V e desenquadramento do MEI.
- Definir se as artes devem levar CRC, site ou telefone na área visual.
- Revisar se o mascote Lioncio deve aparecer nas peças indicadas.
- Substituir identidade provisória por manual oficial, se houver.
- Inserir fotos autorais, caso a marca queira humanizar mais os posts.
""",
    )


def create_export_docs() -> None:
    write(BASE / "07_exportacao" / "exportar_posts.js", EXPORT_JS)
    write(
        BASE / "07_exportacao" / "instrucoes_exportacao.md",
        """
# Instruções de exportação

Os layouts editáveis estão em HTML/CSS. Cada arquivo `arte.html` contém uma ou mais áreas `.creative-frame` no tamanho correto para Instagram.

## Exportação automática

Use o script:

```powershell
& "C:\\Users\\vitor\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\node\\bin\\node.exe" "marketing\\instagram\\07_exportacao\\exportar_posts.js"
```

O script tenta carregar Playwright do ambiente local. Nesta máquina, o runtime do Codex contém Playwright em:

```text
C:\\Users\\vitor\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\node\\node_modules
```

Os PNGs serão criados em:

```text
marketing\\instagram\\07_exportacao\\png
```

## Exportação manual

1. Abra qualquer `arte.html` no navegador.
2. Confira se a arte carregou com logo e texto corretos.
3. Use captura do navegador, extensão de screenshot ou ferramenta de design para exportar o elemento no tamanho original.
4. Para carrosséis, exporte cada slide separadamente.

## Observação

Não publique nem agende a partir destes arquivos. Eles são materiais para revisão humana.
""",
    )


def create_readme() -> None:
    write(
        BASE / "README.md",
        f"""
# Biblioteca Instagram | SoulCont

Esta pasta reúne uma campanha pronta para revisão humana. Nada foi publicado, agendado ou enviado.

## Conteúdo criado

- {len(POSTS)} posts de feed.
- {len(CAROUSELS)} carrosséis completos, com 7 slides cada.
- {len(STORIES)} stories estáticos.
- 30 chamadas curtas extras para stories.
- 20+ CTAs.
- 10 mensagens de direcionamento para WhatsApp Business.
- Calendário editorial de 30 dias.
- Estratégia, persona, tom de voz, oferta, hashtags e revisão.
- Templates editáveis em HTML/CSS.
- Script de exportação em PNG.

## Estrutura

- `00_estrategia`: documentos estratégicos, CTAs, hashtags e WhatsApp.
- `01_posts_feed`: artes editáveis e fichas dos posts.
- `02_carrosseis`: carrosséis editáveis e fichas.
- `03_stories`: stories editáveis e fichas.
- `04_legendas`: legendas completas.
- `05_calendario`: calendário em CSV e Markdown.
- `06_templates`: templates e CSS compartilhado.
- `07_exportacao`: instruções e script de exportação.
- `08_revisao`: checklist, pendências e matriz de conteúdo.

## Assets de marca usados

- `assets/img/logo/vl_logo_horizontal_branca.svg`
- `assets/img/logo/vl_logo_horizontal_primaria.svg`
- `assets/img/logo/vl_favicon_primario.png`
- `assets/img/lioncio.png`
- `assets/img/lionciocaminhandoparaoladodireito.png`

## Como revisar

1. Abra as fichas Markdown de cada post.
2. Revise texto, CTA, hashtags e observações.
3. Abra o `arte.html` correspondente no navegador.
4. Verifique legibilidade no celular e aderência à marca.
5. Exporte somente depois de aprovação humana.

## Como exportar

Veja `07_exportacao/instrucoes_exportacao.md`.

## Pontos que exigem validação antes de publicar

- Revisão técnica dos conteúdos tributários.
- Confirmação de telefone, arroba e links públicos.
- Aprovação do uso do mascote Lioncio.
- Confirmação de que a identidade visual final está correta.
- Conferência de que não há dados reais ou informações sigilosas.
""",
    )


def create_extra_ideas() -> None:
    ideas = [
        "Checklist de documentos para abrir CNPJ como prestador de serviço.",
        "Quando vale revisar CNAE depois que a empresa muda de atividade.",
        "Como se preparar para contratar o primeiro funcionário.",
        "Diferença entre faturamento, caixa e lucro da operação.",
        "Como organizar notas fiscais recorrentes.",
        "O que muda quando o MEI passa a vender para empresas maiores.",
        "Perguntas para fazer antes de trocar de contador.",
        "Como a tecnologia ajuda na rotina contábil.",
        "Erros comuns ao definir pró-labore.",
        "Como ler uma demonstração contábil sem complicar.",
    ]
    write(
        BASE / "00_estrategia" / "ideias_extras_posts_futuros.md",
        "# 10 ideias extras de posts futuros\n\n" + md_list(ideas),
    )


def main() -> None:
    for folder in [
        "00_estrategia",
        "01_posts_feed",
        "02_carrosseis",
        "03_stories",
        "04_legendas",
        "05_calendario",
        "06_templates",
        "07_exportacao",
        "08_revisao",
    ]:
        (BASE / folder).mkdir(parents=True, exist_ok=True)

    create_strategy_docs()
    create_extra_ideas()
    create_templates()
    create_posts()
    create_carousels()
    create_stories()
    create_calendar()
    create_review_docs()
    create_export_docs()
    create_readme()
    print(f"Biblioteca criada em {BASE}")


if __name__ == "__main__":
    main()
