from __future__ import annotations

import html
from urllib.parse import quote
import json
from pathlib import Path

from cidades_config import (
    PROFESSIONALS,
    REGIONS,
    SITE,
    regionalize_city,
    validate_city_dataset,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "cidades"
TODAY = "2026-07-20"


CITIES = [
    {
        "slug": "ico",
        "name": "Icó",
        "mode": "presencial",
        "context_title": "Contabilidade com presença em Icó e acompanhamento próximo",
        "context": "Icó é a base da SoulCont. O escritório combina atendimento presencial com processos digitais para que documentos, prazos e decisões sejam acompanhados sem depender apenas de encontros físicos.",
        "focus": "Abertura, migração e rotina mensal",
        "focus_text": "Apoio para empresas que estão começando, trocando de contador ou organizando a operação contábil.",
        "audiences": [
            "Pequenas empresas de Icó que precisam organizar a rotina fiscal e contábil",
            "Prestadores de serviços e profissionais liberais que querem revisar imposto e retirada",
            "MEIs em crescimento que precisam avaliar limite, contratação ou mudança de regime",
            "Empresas com equipe que necessitam de folha e departamento pessoal organizados",
        ],
        "decisions": [
            "Escolher CNAE, natureza jurídica e regime antes de abrir o CNPJ",
            "Trocar de contador com checklist e continuidade da rotina",
            "Revisar enquadramento, pró-labore e distribuição de lucros",
            "Acompanhar caixa, margem e obrigações com mais previsibilidade",
        ],
        "faq_q": "Posso ser atendido presencialmente em Icó?",
        "faq_a": "Sim. A SoulCont está na Rua São José, 1245, Novo Centro, em Icó. O atendimento também pode continuar por canais digitais.",
    },
    {
        "slug": "cedro",
        "name": "Cedro",
        "mode": "digital",
        "context_title": "Acompanhamento contábil para empresas de Cedro sem deslocamentos constantes",
        "context": "O atendimento a empresas de Cedro é conduzido digitalmente a partir da base da SoulCont em Icó. A proposta é organizar documentos, calendário fiscal e decisões por um fluxo claro, mantendo contato direto com os responsáveis.",
        "focus": "Organização fiscal e crescimento",
        "focus_text": "Estrutura para pequenos negócios que precisam ganhar previsibilidade sem aumentar a complexidade da rotina.",
        "audiences": [
            "Empresas de serviços que precisam compreender imposto, retirada e margem",
            "Comércios e pequenos negócios que estão estruturando controles e equipe",
            "MEIs de Cedro que se aproximam do limite ou planejam crescer",
            "Empresas que desejam migrar de contador com documentação organizada",
        ],
        "decisions": [
            "Avaliar se o regime atual ainda acompanha o faturamento",
            "Organizar folha, encargos e admissões antes de ampliar a equipe",
            "Separar finanças pessoais e empresariais",
            "Criar uma rotina mensal com responsabilidades e prazos definidos",
        ],
        "faq_q": "Como funciona a contabilidade digital para uma empresa de Cedro?",
        "faq_a": "Documentos e solicitações seguem um fluxo digital, com orientação direta dos contadores. Quando necessário, o atendimento considera a proximidade da base em Icó.",
    },
    {
        "slug": "oros",
        "name": "Orós",
        "mode": "digital",
        "context_title": "Contabilidade para negócios de Orós que precisam sair do improviso",
        "context": "A SoulCont atende empresas de Orós por canais digitais, conectando rotina contábil, tributos e leitura financeira. O objetivo é transformar dúvidas recorrentes em processos e próximos passos compreensíveis.",
        "focus": "MEI, serviços e pequenas empresas",
        "focus_text": "Orientação para negócios que estão crescendo e precisam rever enquadramento, retirada ou controles.",
        "audiences": [
            "MEIs de Orós avaliando desenquadramento ou contratação",
            "Prestadores de serviços com dúvidas sobre Simples Nacional e pró-labore",
            "Pequenas empresas que precisam organizar obrigações mensais",
            "Empreendedores que pretendem abrir um CNPJ com análise prévia",
        ],
        "decisions": [
            "Entender o momento correto de migrar do MEI",
            "Definir retirada sem comprometer caixa e conformidade",
            "Comparar cenários tributários antes de decidir",
            "Organizar documentos para abertura ou troca de contador",
        ],
        "faq_q": "A SoulCont atende MEIs de Orós que estão crescendo?",
        "faq_a": "Sim. O atendimento pode avaliar limite, atividade, contratação e os custos de uma possível migração para outro regime.",
    },
    {
        "slug": "umari",
        "name": "Umari",
        "mode": "digital",
        "context_title": "Suporte contábil acessível para empreendedores de Umari",
        "context": "Empresas de Umari podem ser acompanhadas digitalmente pela equipe da SoulCont em Icó. O processo prioriza comunicação simples, organização documental e orientação antes de decisões tributárias ou trabalhistas.",
        "focus": "Formalização e rotina organizada",
        "focus_text": "Apoio para quem vai abrir empresa, formalizar uma operação ou colocar as obrigações em ordem.",
        "audiences": [
            "Empreendedores de Umari que precisam escolher como formalizar a atividade",
            "MEIs com dúvidas sobre limite e obrigações",
            "Pequenas empresas que desejam centralizar documentos e prazos",
            "Prestadores que precisam analisar imposto e retirada",
        ],
        "decisions": [
            "Verificar se MEI, Simples Nacional ou outra estrutura faz sentido",
            "Definir CNAE e forma de atuação antes da abertura",
            "Regularizar a rotina antes que pendências se acumulem",
            "Entender custos de contratação e folha de pagamento",
        ],
        "faq_q": "É necessário ir até Icó para contratar a SoulCont em Umari?",
        "faq_a": "Não. A análise inicial, o envio de documentos e o acompanhamento podem ser feitos digitalmente, com contato direto com a equipe.",
    },
    {
        "slug": "baixio",
        "name": "Baixio",
        "mode": "digital",
        "context_title": "Contabilidade digital para empresas de Baixio com orientação humana",
        "context": "A SoulCont atende negócios de Baixio a partir de Icó, utilizando um fluxo digital para documentos e acompanhamento. A tecnologia organiza a rotina, enquanto as decisões continuam sendo discutidas com os contadores responsáveis.",
        "focus": "Abertura e acompanhamento mensal",
        "focus_text": "Estrutura simples para começar corretamente e manter impostos, documentos e prazos acompanhados.",
        "audiences": [
            "Empreendedores de Baixio preparando a abertura do primeiro CNPJ",
            "Prestadores de serviços que precisam emitir notas e organizar tributos",
            "MEIs que querem verificar crescimento e mudança de porte",
            "Pequenas empresas insatisfeitas com falta de retorno contábil",
        ],
        "decisions": [
            "Abrir empresa sem escolher CNAE e regime por tentativa",
            "Estabelecer calendário para documentos e impostos",
            "Planejar retirada e distribuição de resultados",
            "Trocar de contador sem interromper o cumprimento das obrigações",
        ],
        "faq_q": "Quais documentos uma empresa de Baixio envia mensalmente?",
        "faq_a": "A lista depende da atividade, equipe e regime. A SoulCont define um checklist específico no início do atendimento para evitar pedidos soltos e atrasos.",
    },
    {
        "slug": "iguatu",
        "name": "Iguatu",
        "mode": "digital",
        "context_title": "Contabilidade consultiva para empresas de Iguatu em fase de estruturação",
        "context": "O atendimento a Iguatu é pensado para empresas que precisam ir além do cumprimento básico: revisar regime, organizar folha, compreender margem e transformar dados contábeis em decisões mais seguras.",
        "focus": "Tributos, equipe e gestão",
        "focus_text": "Acompanhamento para operações com maior volume de decisões fiscais, trabalhistas e financeiras.",
        "audiences": [
            "Empresas de serviços com faturamento crescente e dúvidas de enquadramento",
            "Profissionais liberais que estruturaram equipe ou ampliaram atendimento",
            "Pequenas empresas com folha, encargos e rotinas mais complexas",
            "Negócios de Iguatu avaliando uma troca de contador",
        ],
        "decisions": [
            "Comparar Simples Nacional e Lucro Presumido com dados do negócio",
            "Revisar pró-labore, distribuição e custo da equipe",
            "Ler fluxo de caixa, margem e ponto de equilíbrio",
            "Criar um plano de transição contábil com pendências identificadas",
        ],
        "faq_q": "A SoulCont realiza diagnóstico tributário para empresas de Iguatu?",
        "faq_a": "Sim. A análise compara o enquadramento atual com cenários possíveis, considerando atividade, faturamento, folha e forma de retirada.",
    },
    {
        "slug": "juazeiro-do-norte",
        "name": "Juazeiro do Norte",
        "mode": "digital",
        "context_title": "Contabilidade para empresas de serviços e profissionais de Juazeiro do Norte",
        "context": "A SoulCont atende digitalmente empresas de Juazeiro do Norte que buscam uma leitura conectada entre tributação, operação e finanças. O trabalho começa pelo contexto do negócio, não por uma solução pronta.",
        "focus": "Serviços, profissionais e expansão",
        "focus_text": "Apoio para estruturas que cresceram e precisam revisar regime, retirada, folha e indicadores.",
        "audiences": [
            "Empresas de serviços de Juazeiro do Norte com operação recorrente",
            "Profissionais liberais que precisam estruturar honorários e retirada",
            "Negócios com equipe que desejam organizar departamento pessoal",
            "Empresas em expansão que querem revisar enquadramento tributário",
        ],
        "decisions": [
            "Validar se a estrutura tributária acompanha o crescimento",
            "Organizar pró-labore e distribuição de lucros com documentação",
            "Acompanhar margem, caixa e custo da equipe",
            "Migrar de contador com continuidade e responsáveis definidos",
        ],
        "faq_q": "A SoulCont atende profissionais liberais de Juazeiro do Norte?",
        "faq_a": "Sim. O atendimento pode analisar enquadramento, pró-labore, distribuição, organização financeira e a rotina fiscal da empresa profissional.",
    },
    {
        "slug": "jucas",
        "name": "Jucás",
        "mode": "digital",
        "context_title": "Uma rotina contábil mais previsível para empresas de Jucás",
        "context": "Empreendedores de Jucás podem usar o atendimento digital da SoulCont para centralizar documentos, dúvidas e decisões. A base em Icó mantém a atuação conectada ao contexto regional sem prometer uma unidade física na cidade.",
        "focus": "Pequenas empresas e migração contábil",
        "focus_text": "Organização para negócios que precisam de retorno, calendário e clareza sobre responsabilidades.",
        "audiences": [
            "Pequenas empresas de Jucás com obrigações e documentos descentralizados",
            "MEIs que começaram a crescer ou contratar",
            "Prestadores que querem entender imposto e resultado",
            "Empresas considerando trocar de contador por falta de acompanhamento",
        ],
        "decisions": [
            "Mapear pendências antes da troca de contador",
            "Definir um fluxo mensal para notas, extratos e folha",
            "Verificar o impacto tributário do crescimento",
            "Separar retirada dos sócios e despesas da empresa",
        ],
        "faq_q": "Como é feita a troca de contador para uma empresa de Jucás?",
        "faq_a": "A SoulCont levanta pendências, orienta a documentação, organiza a comunicação de transição e implanta a nova rotina sem depender de presença física contínua.",
    },
    {
        "slug": "carius",
        "name": "Cariús",
        "mode": "digital",
        "context_title": "Orientação contábil para empresas e MEIs em crescimento em Cariús",
        "context": "O atendimento para Cariús combina processos digitais com análise individual do negócio. É uma alternativa para empreendedores que precisam entender o próximo passo antes de mudar porte, contratar ou assumir novas obrigações.",
        "focus": "Crescimento do MEI e pequenas empresas",
        "focus_text": "Avaliação de limites, custos e rotinas antes de uma mudança de estrutura.",
        "audiences": [
            "MEIs de Cariús próximos do limite de faturamento",
            "Empreendedores planejando contratar o primeiro funcionário",
            "Prestadores que desejam abrir uma empresa fora do MEI",
            "Pequenas empresas que precisam organizar impostos e caixa",
        ],
        "decisions": [
            "Comparar permanência no MEI e migração para microempresa",
            "Estimar custo de folha antes de contratar",
            "Escolher CNAE e regime coerentes com a atividade real",
            "Organizar capital de giro e calendário de tributos",
        ],
        "faq_q": "A SoulCont ajuda no desenquadramento do MEI em Cariús?",
        "faq_a": "Sim. A análise considera motivo, prazo, atividade, faturamento e custos da nova estrutura antes de orientar a migração.",
    },
    {
        "slug": "acopiara",
        "name": "Acopiara",
        "mode": "digital",
        "context_title": "Apoio contábil para empresas de Acopiara que precisam revisar escolhas",
        "context": "A SoulCont atende digitalmente negócios de Acopiara que desejam revisar regime, organizar equipe ou melhorar a leitura financeira. O acompanhamento busca antecipar decisões em vez de atuar apenas depois do problema.",
        "focus": "Diagnóstico tributário e operação",
        "focus_text": "Análise para empresas que mudaram de tamanho, equipe ou perfil de faturamento.",
        "audiences": [
            "Empresas de Acopiara que cresceram sem revisar o enquadramento",
            "Prestadores com dúvidas entre Simples e Lucro Presumido",
            "Negócios com equipe e rotinas trabalhistas recorrentes",
            "Empresas que precisam conectar contabilidade e controle financeiro",
        ],
        "decisions": [
            "Revisar regime com base em faturamento, atividade e folha",
            "Conferir se retirada e distribuição estão bem documentadas",
            "Organizar admissões, férias, rescisões e encargos",
            "Criar indicadores para caixa, margem e ponto de equilíbrio",
        ],
        "faq_q": "Quando uma empresa de Acopiara deve revisar o regime tributário?",
        "faq_a": "A revisão é especialmente importante após mudanças de faturamento, atividade, folha ou forma de retirada. A comparação deve usar dados da própria empresa.",
    },
    {
        "slug": "quixelo",
        "name": "Quixelô",
        "mode": "digital",
        "context_title": "Contabilidade digital para empreendedores de Quixelô com processo definido",
        "context": "Empresas de Quixelô podem ser atendidas pela SoulCont sem depender de deslocamentos para cada obrigação. O processo digital organiza documentos e prazos, enquanto dúvidas e escolhas são tratadas diretamente com a equipe.",
        "focus": "Rotina mensal e suporte ao empreendedor",
        "focus_text": "Fluxo claro para quem precisa saber o que enviar, quando pagar e como decidir.",
        "audiences": [
            "Empreendedores de Quixelô abrindo ou regularizando a empresa",
            "MEIs que precisam avaliar crescimento",
            "Prestadores com dúvidas sobre notas, imposto e retirada",
            "Pequenas empresas que buscam atendimento mais organizado",
        ],
        "decisions": [
            "Definir responsabilidades mensais entre empresa e contabilidade",
            "Organizar documentos digitais e calendário fiscal",
            "Avaliar porte e regime antes de crescer",
            "Trocar de contador com levantamento do cenário atual",
        ],
        "faq_q": "O atendimento para Quixelô é totalmente digital?",
        "faq_a": "A rotina pode ser conduzida digitalmente, incluindo envio de documentos, reuniões e acompanhamento. A SoulCont informa desde o início os canais e prazos do processo.",
    },
    {
        "slug": "ipaumirim",
        "name": "Ipaumirim",
        "mode": "digital",
        "context_title": "Abertura e contabilidade mensal para negócios de Ipaumirim",
        "context": "A SoulCont atende empreendedores de Ipaumirim que querem iniciar um CNPJ com análise ou organizar uma empresa já em funcionamento. O trabalho digital permite acompanhar documentos e decisões a partir da base em Icó.",
        "focus": "Abertura segura e conformidade",
        "focus_text": "Orientação para começar com escolhas coerentes e manter a rotina sem acúmulo de pendências.",
        "audiences": [
            "Empreendedores de Ipaumirim avaliando a abertura de empresa",
            "Prestadores que precisam definir CNAE e emissão de notas",
            "MEIs considerando mudança de porte",
            "Empresas que precisam retomar a organização fiscal e contábil",
        ],
        "decisions": [
            "Escolher natureza jurídica e regime com base na operação",
            "Planejar custos iniciais, retirada e obrigações",
            "Criar rotina para notas, extratos e documentos",
            "Identificar pendências antes de uma troca de contador",
        ],
        "faq_q": "A SoulCont abre empresas para empreendedores de Ipaumirim?",
        "faq_a": "Sim. O processo começa pela análise da atividade, CNAE, natureza jurídica, regime e documentos necessários para o novo CNPJ.",
    },
    {
        "slug": "jaguaribe",
        "name": "Jaguaribe",
        "mode": "digital",
        "context_title": "Contabilidade consultiva para empresas de Jaguaribe com operação em evolução",
        "context": "Empresas de Jaguaribe podem contar com acompanhamento digital da SoulCont para conectar fiscal, folha e finanças. A proposta é dar visibilidade aos efeitos das decisões antes que elas apareçam apenas nas guias ou no caixa.",
        "focus": "Fiscal, equipe e visão financeira",
        "focus_text": "Acompanhamento para negócios que precisam integrar obrigações e gestão.",
        "audiences": [
            "Empresas de Jaguaribe com equipe e folha recorrente",
            "Prestadores que desejam revisar tributação e retirada",
            "Pequenos negócios ampliando faturamento ou estrutura",
            "Empresas que precisam interpretar resultados contábeis",
        ],
        "decisions": [
            "Avaliar custo tributário junto com margem e caixa",
            "Planejar contratação, férias e encargos",
            "Revisar pró-labore e distribuição de lucros",
            "Estabelecer indicadores para decisões de crescimento",
        ],
        "faq_q": "A contabilidade para Jaguaribe inclui departamento pessoal?",
        "faq_a": "Sim, conforme a contratação. O suporte pode incluir admissões, férias, rescisões, folha, encargos e organização dos prazos trabalhistas.",
    },
    {
        "slug": "brejo-santo",
        "name": "Brejo Santo",
        "mode": "digital",
        "context_title": "Contabilidade para empresas e profissionais de Brejo Santo",
        "context": "O atendimento digital da SoulCont em Brejo Santo é voltado a negócios que querem discutir tributação, retirada, equipe e indicadores com mais profundidade. A análise considera o estágio e o modelo de cada empresa.",
        "focus": "Profissionais, serviços e estrutura empresarial",
        "focus_text": "Orientação para operações que precisam combinar conformidade com visão de crescimento.",
        "audiences": [
            "Profissionais liberais de Brejo Santo com empresa constituída",
            "Prestadores de serviços com faturamento recorrente",
            "Empresas com equipe e custos trabalhistas relevantes",
            "Negócios avaliando revisão tributária ou troca de contador",
        ],
        "decisions": [
            "Comparar regimes e impactos sobre a margem",
            "Estruturar pró-labore e distribuição de lucros",
            "Organizar a rotina de folha e documentos",
            "Usar fluxo de caixa e ponto de equilíbrio nas decisões",
        ],
        "faq_q": "Profissionais liberais de Brejo Santo podem contratar atendimento digital?",
        "faq_a": "Sim. A SoulCont atende empresas profissionais por reuniões e processos digitais, com orientação sobre enquadramento, retirada e rotina fiscal.",
    },
    {
        "slug": "jaguaribara",
        "name": "Jaguaribara",
        "mode": "digital",
        "context_title": "Uma contabilidade organizada para empreendedores de Jaguaribara",
        "context": "A SoulCont atende empresas de Jaguaribara por um processo digital que centraliza documentos, demandas e calendário. O objetivo é reduzir incerteza sobre obrigações e criar espaço para decisões planejadas.",
        "focus": "MEI, abertura e rotina mensal",
        "focus_text": "Suporte para negócios pequenos que precisam crescer com organização.",
        "audiences": [
            "MEIs de Jaguaribara avaliando limite ou contratação",
            "Empreendedores preparando a abertura de um CNPJ",
            "Prestadores que precisam organizar notas e tributos",
            "Pequenas empresas que desejam mais clareza no atendimento contábil",
        ],
        "decisions": [
            "Formalizar a atividade em uma estrutura adequada",
            "Planejar mudança de MEI para microempresa",
            "Organizar um calendário de documentos e impostos",
            "Separar finanças do negócio e dos sócios",
        ],
        "faq_q": "Uma empresa de Jaguaribara pode trocar de contador de forma digital?",
        "faq_a": "Sim. A SoulCont organiza checklist, levantamento de pendências e entrada dos documentos por canais digitais, mantendo a continuidade da rotina.",
    },
    {
        "slug": "solonopole",
        "name": "Solonópole",
        "mode": "digital",
        "context_title": "Acompanhamento contábil para pequenas empresas de Solonópole",
        "context": "Negócios de Solonópole podem utilizar o atendimento digital da SoulCont para organizar obrigações e discutir decisões com uma equipe identificada. A distância deixa de ser um obstáculo para reuniões, documentos e acompanhamento.",
        "focus": "Pequenas empresas e atendimento remoto",
        "focus_text": "Processo contábil estruturado para empresas que precisam de retorno e previsibilidade.",
        "audiences": [
            "Pequenas empresas de Solonópole com rotina fiscal recorrente",
            "Prestadores de serviços que precisam analisar retirada e imposto",
            "MEIs em crescimento",
            "Empresas insatisfeitas com comunicação ou falta de acompanhamento",
        ],
        "decisions": [
            "Definir um fluxo digital de documentos e solicitações",
            "Revisar regime e custo tributário",
            "Planejar contratação e encargos",
            "Trocar de contador com escopo e responsabilidades claros",
        ],
        "faq_q": "Como são realizadas reuniões com empresas de Solonópole?",
        "faq_a": "As reuniões podem ocorrer por vídeo ou telefone, apoiadas por documentos digitais e um fluxo definido de acompanhamento.",
    },
    {
        "slug": "varzea-alegre",
        "name": "Várzea Alegre",
        "mode": "digital",
        "context_title": "Contabilidade para empresas de Várzea Alegre que querem decidir com dados",
        "context": "A SoulCont atende digitalmente empresas de Várzea Alegre que buscam organizar a operação e compreender os números antes de crescer, contratar ou mudar de regime. O acompanhamento conecta obrigações e gestão.",
        "focus": "Serviços, profissionais e análise tributária",
        "focus_text": "Apoio para empresas que precisam revisar estrutura e transformar registros em decisões.",
        "audiences": [
            "Prestadores de serviços de Várzea Alegre",
            "Profissionais liberais com empresa ou preparando a abertura",
            "Negócios com aumento de faturamento e dúvidas tributárias",
            "Pequenas empresas que precisam organizar caixa e equipe",
        ],
        "decisions": [
            "Escolher estrutura para abrir uma empresa profissional",
            "Comparar regimes usando faturamento e folha",
            "Revisar retirada e distribuição de resultados",
            "Criar visão de caixa, margem e ponto de equilíbrio",
        ],
        "faq_q": "A SoulCont atende abertura de empresa em Várzea Alegre?",
        "faq_a": "Sim. A orientação é digital e cobre análise de atividade, CNAE, natureza jurídica, regime e documentação do novo CNPJ.",
    },
    {
        "slug": "lavras-da-mangabeira",
        "name": "Lavras da Mangabeira",
        "mode": "digital",
        "context_title": "Contabilidade para negócios de Lavras da Mangabeira em crescimento",
        "context": "Empresas de Lavras da Mangabeira podem ser acompanhadas pela SoulCont a partir de Icó. O processo digital facilita a rotina e permite discutir contratação, tributação e organização financeira antes de decisões importantes.",
        "focus": "Crescimento, equipe e previsibilidade",
        "focus_text": "Suporte para pequenos negócios que estão assumindo novas responsabilidades.",
        "audiences": [
            "Pequenas empresas de Lavras da Mangabeira em fase de crescimento",
            "MEIs planejando mudar de porte ou contratar",
            "Prestadores que precisam organizar impostos e pró-labore",
            "Empresas que desejam migrar de contador",
        ],
        "decisions": [
            "Calcular o efeito de uma contratação no caixa",
            "Revisar enquadramento antes de aumentar a operação",
            "Organizar folha, documentos e obrigações",
            "Planejar a transição para uma nova contabilidade",
        ],
        "faq_q": "Empresas de Lavras da Mangabeira precisam se deslocar para enviar documentos?",
        "faq_a": "Não. Os documentos podem seguir por canais digitais definidos no início do atendimento, reduzindo deslocamentos e pedidos dispersos.",
    },
    {
        "slug": "crato",
        "name": "Crato",
        "mode": "digital",
        "context_title": "Contabilidade consultiva para empresas e profissionais do Crato",
        "context": "O atendimento da SoulCont para o Crato é digital e voltado a empresas que querem avaliar tributação, retirada e desempenho com base em dados. Cada recomendação considera atividade, faturamento, equipe e objetivo do negócio.",
        "focus": "Profissionais, serviços e estratégia tributária",
        "focus_text": "Análise para operações que precisam alinhar conformidade, margem e crescimento.",
        "audiences": [
            "Profissionais liberais do Crato com empresa constituída",
            "Empresas de serviços com diferentes fontes de receita",
            "Negócios com equipe e custos operacionais crescentes",
            "Empresas avaliando diagnóstico tributário ou migração contábil",
        ],
        "decisions": [
            "Comparar regimes conforme receita, folha e atividade",
            "Estruturar pró-labore e distribuição de lucros",
            "Analisar margem, caixa e ponto de equilíbrio",
            "Organizar transição contábil sem perder continuidade",
        ],
        "faq_q": "A SoulCont faz planejamento tributário para empresas do Crato?",
        "faq_a": "A SoulCont realiza diagnóstico e comparação de cenários. A recomendação depende dos dados da empresa e não de uma promessa genérica de redução de impostos.",
    },
    {
        "slug": "barbalha",
        "name": "Barbalha",
        "mode": "digital",
        "context_title": "Contabilidade para profissionais e empresas de serviços de Barbalha",
        "context": "A SoulCont atende digitalmente empresas de Barbalha que precisam organizar enquadramento, retirada, equipe e indicadores. O processo é adequado a profissionais e prestadores que desejam uma orientação mais conectada à operação.",
        "focus": "Profissionais liberais e empresas de serviços",
        "focus_text": "Acompanhamento para estruturas com honorários, equipe e decisões tributárias recorrentes.",
        "audiences": [
            "Profissionais liberais de Barbalha que atuam por empresa",
            "Prestadores com faturamento recorrente e equipe",
            "Empresas que precisam rever regime ou pró-labore",
            "Negócios buscando mais organização financeira e fiscal",
        ],
        "decisions": [
            "Escolher o enquadramento compatível com a atividade profissional",
            "Organizar honorários, retirada e distribuição",
            "Planejar folha e contratação",
            "Integrar fluxo de caixa e margem à leitura contábil",
        ],
        "faq_q": "A SoulCont atende empresas de profissionais em Barbalha?",
        "faq_a": "Sim. O atendimento pode incluir análise de enquadramento, retirada, distribuição de lucros, folha e rotina fiscal da empresa profissional.",
    },
    {
        "slug": "sao-paulo",
        "name": "São Paulo",
        "region": "sao-paulo",
        "attendance_mode": "service_area",
        "service_areas": [
            "São Paulo",
            "Guarulhos",
            "Osasco",
            "Barueri",
            "Santo André",
            "São Bernardo do Campo",
        ],
        "context_title": (
            "Contabilidade consultiva para empresas de serviços em São Paulo"
        ),
        "context": (
            "O atendimento combina processos digitais, contato direto com o contador "
            "e análise da atividade, do faturamento, da folha e da forma de retirada. "
            "Reuniões presenciais externas podem ser combinadas mediante agendamento."
        ),
        "focus": "Prestadores de serviços e pequenas empresas",
        "focus_text": (
            "Abertura, troca de contador, revisão tributária e organização da rotina "
            "para empresas paulistanas."
        ),
        "audiences": [
            "Prestadores de serviços que precisam revisar regime, impostos e retirada",
            "Pequenas empresas que desejam trocar de contador com transição organizada",
            "Profissionais liberais que pretendem estruturar ou desenvolver seu CNPJ",
            "Empresas com equipe que precisam organizar folha e obrigações trabalhistas",
        ],
        "decisions": [
            "Planejar atividade, CNAE, natureza jurídica e tributação antes da abertura",
            "Comparar Simples Nacional e Lucro Presumido com dados da empresa",
            "Organizar pró-labore, distribuição de lucros, folha e calendário fiscal",
            "Trocar de contador com diagnóstico, documentos e responsáveis definidos",
        ],
        "faq_q": "A SoulCont possui escritório aberto ao público em São Paulo?",
        "faq_a": (
            "Não. O atendimento em São Paulo é prioritariamente on-line. Reuniões "
            "presenciais externas podem ser combinadas mediante agendamento e disponibilidade."
        ),
        "page_description": (
            "Contabilidade em São Paulo para prestadores de serviços e pequenas empresas. "
            "Abertura, troca de contador e gestão tributária com atendimento digital e humano."
        ),
    },
    {
        "slug": "guarulhos",
        "name": "Guarulhos",
        "region": "sao-paulo",
        "attendance_mode": "service_area",
        "address": None,
        "context_title": (
            "Contabilidade para empresas de Guarulhos que precisam organizar "
            "tributos, equipe e crescimento"
        ),
        "context": (
            "A SoulCont atende empresas de Guarulhos por canais digitais, com contato "
            "direto com o contador e encontros externos mediante agendamento e "
            "disponibilidade. O trabalho parte da atividade, do faturamento, da folha "
            "e das rotinas já existentes, sem indicar unidade física no município."
        ),
        "focus": "Serviços, comércio e empresas com equipe",
        "focus_text": (
            "Organização fiscal, trabalhista e financeira para negócios que precisam "
            "acompanhar o crescimento sem perder previsibilidade."
        ),
        "audiences": [
            "Prestadores de serviços de Guarulhos com faturamento recorrente",
            "Pequenas empresas com admissões, folha e encargos mensais",
            "Comércios que precisam separar rotina fiscal e controle financeiro",
            "Empresas que desejam trocar de contador com pendências mapeadas",
        ],
        "decisions": [
            "Revisar regime tributário conforme atividade, receita e folha",
            "Planejar contratação, pró-labore e distribuição de lucros",
            "Organizar notas, documentos e calendário de obrigações",
            "Conduzir a troca de contador com responsáveis e prazos definidos",
        ],
        "faq_q": "A SoulCont possui escritório aberto ao público em Guarulhos?",
        "faq_a": (
            "Não. O atendimento em Guarulhos é realizado on-line. Encontros presenciais "
            "externos podem ser avaliados mediante agendamento e disponibilidade."
        ),
        "page_description": (
            "Contabilidade em Guarulhos para prestadores de serviços, comércios e "
            "pequenas empresas. Atendimento on-line e encontros externos agendados."
        ),
    },
    {
        "slug": "osasco",
        "name": "Osasco",
        "title_override": "Contador em Osasco para Troca de Contador | SoulCont",
        "region": "sao-paulo",
        "attendance_mode": "service_area",
        "address": None,
        "context_title": (
            "Contabilidade consultiva para empresas de Osasco em fase de organização "
            "ou mudança"
        ),
        "context": (
            "Empresas de Osasco podem contratar a SoulCont por um processo digital que "
            "centraliza documentos, dúvidas e decisões. A análise considera regime, "
            "retirada, equipe e situação cadastral para estruturar a rotina ou preparar "
            "uma troca de contador sem prometer endereço comercial na cidade."
        ),
        "focus": "Troca de contador e rotina mensal",
        "focus_text": (
            "Diagnóstico, transição documental e implantação de um fluxo contábil mais "
            "claro para pequenas empresas e prestadores."
        ),
        "audiences": [
            "Empresas de Osasco insatisfeitas com falta de retorno ou acompanhamento",
            "Prestadores de serviços que precisam revisar impostos e retirada",
            "Pequenos negócios com documentos e obrigações descentralizados",
            "Profissionais liberais que pretendem abrir ou regularizar seu CNPJ",
        ],
        "decisions": [
            "Levantar pendências antes de trocar de contador",
            "Definir checklist para notas, extratos, folha e impostos",
            "Avaliar Simples Nacional ou Lucro Presumido com dados reais",
            "Estruturar pró-labore e distribuição de resultados com documentação",
        ],
        "faq_q": "Como uma empresa de Osasco pode trocar de contador para a SoulCont?",
        "faq_a": (
            "A transição começa com um diagnóstico e um checklist de documentos e "
            "pendências. O processo é conduzido on-line, com definição de responsáveis "
            "e continuidade das obrigações."
        ),
        "page_description": (
            "Contabilidade em Osasco para trocar de contador, abrir empresa e organizar "
            "tributos. Atendimento consultivo on-line para pequenas empresas."
        ),
    },
    {
        "slug": "barueri",
        "name": "Barueri",
        "title_override": "Contador em Barueri para Serviços Profissionais | SoulCont",
        "region": "sao-paulo",
        "attendance_mode": "service_area",
        "address": None,
        "context_title": (
            "Contabilidade para empresas de serviços e profissionais de Barueri"
        ),
        "context": (
            "O atendimento da SoulCont para Barueri conecta a rotina fiscal à leitura de "
            "margem, retirada e estrutura da operação. É indicado para empresas de "
            "serviços e profissionais que precisam comparar cenários antes de abrir, "
            "crescer ou rever o enquadramento, com atendimento on-line."
        ),
        "focus": "Serviços profissionais e análise tributária",
        "focus_text": (
            "Acompanhamento para operações baseadas em conhecimento que precisam alinhar "
            "tributação, pró-labore, distribuição e indicadores."
        ),
        "audiences": [
            "Consultorias e empresas de serviços empresariais de Barueri",
            "Profissionais liberais que atuam por pessoa jurídica",
            "Prestadores com faturamento crescente e estrutura enxuta",
            "Empresas que desejam integrar contabilidade e leitura financeira",
        ],
        "decisions": [
            "Escolher CNAE e estrutura tributária antes da abertura",
            "Comparar regimes conforme faturamento, atividade e folha",
            "Organizar pró-labore e distribuição de lucros",
            "Acompanhar margem, caixa e ponto de equilíbrio",
        ],
        "faq_q": "A SoulCont atende empresas de serviços estabelecidas em Barueri?",
        "faq_a": (
            "Sim. O atendimento é feito on-line e pode incluir abertura, rotina contábil, "
            "diagnóstico tributário, folha e apoio financeiro. Não há unidade física da "
            "SoulCont aberta ao público em Barueri."
        ),
        "page_description": (
            "Contabilidade em Barueri para consultorias, profissionais e empresas de "
            "serviços. Regime tributário, pró-labore e gestão com atendimento on-line."
        ),
    },
    {
        "slug": "santo-andre",
        "name": "Santo André",
        "title_override": "Contador em Santo André: Abertura e Rotina Fiscal | SoulCont",
        "region": "sao-paulo",
        "attendance_mode": "service_area",
        "address": None,
        "context_title": (
            "Contabilidade para prestadores e pequenas empresas de Santo André"
        ),
        "context": (
            "A SoulCont atende empresas de Santo André digitalmente, organizando "
            "documentos, tributos, retirada e obrigações trabalhistas em um fluxo "
            "acompanhado. As orientações são definidas a partir dos dados da empresa e "
            "das exigências aplicáveis à sua atividade."
        ),
        "focus": "Formalização, tributos e organização",
        "focus_text": (
            "Estrutura para quem vai abrir empresa, regularizar a rotina ou transformar "
            "informações contábeis em decisões práticas."
        ),
        "audiences": [
            "Prestadores de serviços de Santo André preparando a abertura do CNPJ",
            "Profissionais liberais com dúvidas sobre regime e retirada",
            "Pequenas empresas que precisam organizar notas e obrigações",
            "Negócios com equipe que desejam revisar folha e encargos",
        ],
        "decisions": [
            "Validar atividade, CNAE e regime antes de abrir a empresa",
            "Criar uma rotina para emissão de notas e envio de documentos",
            "Revisar pró-labore, impostos e distribuição de resultados",
            "Planejar admissões, férias e custo da equipe",
        ],
        "faq_q": "O atendimento contábil em Santo André é presencial?",
        "faq_a": (
            "O atendimento é prioritariamente on-line e a SoulCont não mantém escritório "
            "aberto ao público em Santo André. Encontros externos podem ser avaliados "
            "mediante agendamento e disponibilidade."
        ),
        "page_description": (
            "Contabilidade em Santo André para abrir empresa, organizar tributos e folha. "
            "Atendimento on-line para prestadores e pequenas empresas."
        ),
    },
    {
        "slug": "sao-bernardo-do-campo",
        "name": "São Bernardo do Campo",
        "region": "sao-paulo",
        "attendance_mode": "service_area",
        "address": None,
        "context_title": (
            "Contabilidade para empresas de São Bernardo do Campo com operação e equipe"
        ),
        "context": (
            "Empresas de São Bernardo do Campo podem ser acompanhadas pela SoulCont por "
            "processos digitais e contato direto com o contador. A análise reúne impacto "
            "tributário, folha, retiradas e visão financeira para apoiar decisões de "
            "contratação, reorganização ou crescimento."
        ),
        "focus": "Folha, tributação e visão financeira",
        "focus_text": (
            "Apoio para pequenas empresas que precisam compreender o custo da estrutura "
            "e manter as obrigações sob controle."
        ),
        "audiences": [
            "Empresas de serviços de São Bernardo do Campo com equipe própria",
            "Pequenos negócios avaliando contratação ou reorganização",
            "Prestadores que precisam revisar regime, margem e retirada",
            "Empresas que querem trocar de contador com continuidade operacional",
        ],
        "decisions": [
            "Calcular o custo de admissões, férias, encargos e rescisões",
            "Comparar carga tributária junto com margem e fluxo de caixa",
            "Organizar pró-labore, distribuição e documentos societários",
            "Planejar a transição contábil sem interromper obrigações",
        ],
        "faq_q": (
            "A SoulCont atende empresas com funcionários em São Bernardo do Campo?"
        ),
        "faq_a": (
            "Sim. Conforme o escopo contratado, o atendimento pode incluir folha, "
            "admissões, férias, rescisões e encargos. O processo é on-line e não indica "
            "uma unidade física da SoulCont no município."
        ),
        "page_description": (
            "Contabilidade em São Bernardo do Campo para empresas com equipe. Tributos, "
            "folha, troca de contador e gestão com atendimento consultivo on-line."
        ),
    },
]

CITIES = [regionalize_city(city) for city in CITIES]
validate_city_dataset(CITIES)


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def list_items(items: list[str]) -> str:
    return "\n".join(
        f'                        <li><i class="fi fi-rr-check-circle"></i> {esc(item)}</li>'
        for item in items
    )


def json_script(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=8)


def city_url(city: dict) -> str:
    return f"{SITE['base_url']}/cidades/{city['slug']}/"


def page_description(city: dict) -> str:
    return city.get(
        "page_description",
        (
            f"Contabilidade consultiva para empresas de {city['name']}, "
            f"{city['base_description']}."
        ),
    )


def professionals_for(city: dict) -> list[dict]:
    return [PROFESSIONALS[key] for key in city["professionals"]]


def page_title(city: dict) -> str:
    return city.get(
        "title_override",
        f"Contador em {city['name']} | Contabilidade consultiva | SoulCont",
    )


def page_og_title(city: dict) -> str:
    return city.get("title_override", f"Contador em {city['name']} | SoulCont")


def address_text(address: dict) -> str:
    parts = [
        address.get("streetAddress"),
        address.get("addressLocality"),
        address.get("addressRegion"),
    ]
    return " · ".join(str(part) for part in parts if part)


def attendance_copy(city: dict) -> dict[str, str]:
    name = city["name"]
    mode = city["attendance_mode"]
    if mode == "public_location":
        return {
            "title": city.get("presence_title", f"Atendimento presencial em {name}"),
            "text": city.get("presence_text", address_text(city["address"])),
            "hero": city.get(
                "hero_text",
                (
                    "A SoulCont conecta contabilidade, tributos e leitura financeira "
                    f"para empresas de {name}, com atendimento presencial e processos digitais."
                ),
            ),
            "faq": city.get(
                "attendance_faq",
                (
                    f"Sim. A SoulCont atende presencialmente em {name} e a rotina "
                    "também pode continuar por canais digitais."
                ),
            ),
            "note": city.get(
                "presence_note",
                (
                    f"A SoulCont possui atendimento presencial em {name} no endereço "
                    "informado nesta página, além de manter processos digitais."
                ),
            ),
        }
    if mode == "service_area":
        return {
            "title": city.get(
                "presence_title", f"Atendimento on-line e externo em {name}"
            ),
            "text": city.get(
                "presence_text",
                "Reuniões on-line e encontros presenciais externos mediante agendamento.",
            ),
            "hero": city.get(
                "hero_text",
                (
                    f"A SoulCont atende empresas de {name} on-line e pode realizar "
                    "encontros presenciais externos mediante agendamento."
                ),
            ),
            "faq": city.get(
                "attendance_faq",
                (
                    f"Sim. O atendimento para {name} acontece on-line, com possibilidade "
                    "de encontro presencial externo mediante agendamento."
                ),
            ),
            "note": city.get(
                "presence_note",
                (
                    f"A SoulCont atende empresas de {name} como prestadora de área de "
                    "atendimento e não divulga uma unidade aberta ao público na cidade."
                ),
            ),
        }
    return {
        "title": city.get("presence_title", f"Atendimento digital em {name}"),
        "text": city.get(
            "presence_text",
            f"Reuniões, documentos e acompanhamento digital, {city['base_description']}.",
        ),
        "hero": city.get(
            "hero_text",
            (
                f"A SoulCont atende empresas de {name} por processos digitais, com "
                f"orientação dos contadores responsáveis e {city['base_description']}."
            ),
        ),
        "faq": city.get(
            "attendance_faq",
            (
                f"Sim. O atendimento para {name} é digital e conduzido pela equipe "
                f"da SoulCont, {city['base_description']}."
            ),
        ),
        "note": city.get(
            "presence_note",
            (
                f"Esta página descreve o atendimento destinado a empresas de {name}. "
                f"A SoulCont não possui unidade física na cidade e atua {city['base_description']}."
            ),
        ),
    }


def page_schema(city: dict) -> dict:
    url = city_url(city)
    payload = {
        "@context": "https://schema.org",
        "@type": "AccountingService",
        "@id": f"{url}#accounting-service",
        "name": SITE["name"],
        "url": url,
        "logo": SITE["logo"],
        "image": SITE["og_image"],
        "description": page_description(city),
        "telephone": city["phone_e164"],
        "email": SITE["email"],
        "taxID": SITE["tax_id"],
        "areaServed": [
            {
                "@type": "City",
                "name": area,
                "containedInPlace": {
                    "@type": "State",
                    "name": city["state_name"],
                },
            }
            for area in city["service_areas"]
        ],
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "opens": "07:30",
                "closes": "18:00",
            },
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": "Saturday",
                "opens": "09:00",
                "closes": "15:00",
            },
        ],
        "sameAs": SITE["same_as"],
        "employee": [
            {
                "@type": "Person",
                "name": professional["name"],
                "jobTitle": professional["job_title"],
                "identifier": professional["registration"],
            }
            for professional in professionals_for(city)
        ],
    }
    if city.get("address"):
        payload["address"] = city["address"]
    return payload


def faq_schema(city: dict) -> dict:
    copy = attendance_copy(city)
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": city["faq_q"],
                "acceptedAnswer": {"@type": "Answer", "text": city["faq_a"]},
            },
            {
                "@type": "Question",
                "name": f"A SoulCont atende empresas de {city['name']}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": copy["faq"],
                },
            },
            {
                "@type": "Question",
                "name": "Quais serviços contábeis estão disponíveis?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Abertura de empresa, troca de contador, diagnóstico tributário, contabilidade fiscal, departamento pessoal e consultoria financeira e empresarial, conforme a necessidade do negócio.",
                },
            },
        ],
    }


PAGE_CSS = """
        html,body{max-width:100%;overflow-x:hidden}img{max-width:100%;height:auto}.detail-hero,.section-panel,.detail-card,.final-cta-panel{min-width:0}.detail-hero h1,.section-heading h2,.final-cta-panel h2{overflow-wrap:break-word}.cta-actions-v2{flex-wrap:wrap}.city-service-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:18px}.city-service-grid .detail-card{height:100%}.city-related-links{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:14px;margin-top:14px}.city-related-links+.section-heading{margin-top:26px}.city-related-links a{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:16px 18px;border:1px solid rgba(15,34,51,.1);border-radius:14px;background:#fff;color:#0f2233;font-weight:700;text-decoration:none}.city-related-links a:hover,.city-related-links a:focus-visible{border-color:#d99a3e;color:#2c6b57}.city-team-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:22px;margin-top:28px}.city-person{display:grid;grid-template-columns:100px minmax(0,1fr);gap:20px;align-items:center;padding:18px;border:1px solid rgba(15,34,51,.1);border-radius:20px;background:#fff;min-width:0}.city-person img{display:block;width:100px;aspect-ratio:3/4;object-fit:cover;border-radius:14px;background:#eef2f4}.city-person strong{display:block;font-family:Syne,sans-serif;color:#0f2233;overflow-wrap:anywhere}.city-person span{display:block;color:#66737d;margin-top:5px;font-size:.93rem}.city-link{color:#2c6b57;font-weight:700}.city-note{margin-top:22px;padding:18px 20px;border-left:4px solid #2c6b57;background:rgba(44,107,87,.07);border-radius:0 14px 14px 0}.city-note p{margin:0}.city-breadcrumb{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:18px;color:#66737d;font-size:.9rem}.city-breadcrumb a{color:#2c6b57;font-weight:700;text-decoration:none}.city-breadcrumb span{opacity:.7}@media(max-width:900px){.detail-hero{padding-left:clamp(22px,5vw,42px);padding-right:clamp(22px,5vw,42px)}}@media(max-width:640px){.cta-actions-v2>*{width:100%;justify-content:center;text-align:center}.city-person{grid-template-columns:78px minmax(0,1fr);gap:14px;padding:14px}.city-person img{width:78px}}@media(max-width:390px){.city-person{grid-template-columns:1fr;text-align:center}.city-person img{width:92px;margin:0 auto}.detail-hero h1{font-size:clamp(2rem,11vw,2.7rem)}}
""".strip()


def professional_image_variant(image: str, width: int) -> str:
    # Keep a cache-busting query (e.g. "?v=2") after the variant suffix.
    path, separator, query = image.partition("?")
    stem = path.removesuffix("-640w.webp").removesuffix(".webp")
    return f"{stem}-{width}w.webp{separator}{query}"


def render_professionals(city: dict) -> str:
    return "\n".join(
        (
            f'                <article class="city-person"><img src="{esc(professional_image_variant(professional["image"], 320))}" '
            f'srcset="{esc(professional_image_variant(professional["image"], 320))} 320w, '
            f'{esc(professional_image_variant(professional["image"], 640))} 640w" '
            'sizes="(max-width: 390px) 92px, (max-width: 640px) 78px, 100px" '
            f'alt="{esc(professional["name"])}, {esc(professional["job_title"])} da SoulCont" '
            'width="320" height="427" loading="lazy" decoding="async"><div>'
            f'<strong>{esc(professional["name"])}</strong>'
            f'<span>{esc(professional["job_title"])}<br>{esc(professional["registration"])}</span>'
            "</div></article>"
        )
        for professional in professionals_for(city)
    )


def related_links_section(city: dict) -> str:
    region = REGIONS[city["region"]]
    services = region.get("related_services") or []
    articles = region.get("related_articles") or []
    if not services and not articles:
        return ""

    def render_group(heading: str, icon: str, items: list[dict]) -> str:
        if not items:
            return ""
        links = "\n".join(
            f'                <a href="{esc(item["url"])}"><span>{esc(item["label"])}</span>'
            '<i class="fi fi-rr-arrow-right"></i></a>'
            for item in items
        )
        return (
            '<div class="section-heading"><span class="eyebrow-label">'
            f'<i class="fi fi-rr-{icon}"></i> {heading}</span></div>'
            f'\n            <div class="city-related-links">\n{links}\n            </div>'
        )

    blocks = "\n            ".join(
        part
        for part in (
            render_group("Serviços relacionados", "briefcase", services),
            render_group("Conteúdo relacionado", "document", articles),
        )
        if part
    )
    return (
        '\n        <section class="section-block"><div class="section-shell">'
        f'<div class="section-panel">\n            {blocks}\n        </div></div></section>'
    )


WHATSAPP_REGION_CODES = {"ceara": "ce", "sao-paulo": "sp"}


def whatsapp_url(phone_e164: str, place: str) -> str:
    text = f"Olá! Vim pela página de {place} no site da SoulCont e quero conversar sobre minha empresa."
    return f"https://wa.me/{phone_e164.lstrip('+')}?text={quote(text)}"


def render_city(city: dict) -> str:
    name = esc(city["name"])
    slug = city["slug"]
    copy = attendance_copy(city)
    presence_title = esc(copy["title"])
    presence_text = esc(copy["text"])
    hero_text = esc(copy["hero"])
    attendance_faq = esc(copy["faq"])
    presence_note = esc(copy["note"])
    description = esc(page_description(city))
    phone_e164 = esc(city["phone_e164"])
    phone_display = esc(city["phone_display"])
    whatsapp_href = esc(whatsapp_url(city["phone_e164"], city["name"]))
    whatsapp_region = WHATSAPP_REGION_CODES.get(city["region"], "")
    state_name = esc(city["state_name"])
    professional_summary = " · ".join(
        f"{professional['name']} · {professional['registration']}"
        for professional in professionals_for(city)
    )
    professional_heading = (
        "Profissional responsável pelo atendimento"
        if len(city["professionals"]) == 1
        else "Profissionais responsáveis pelo atendimento"
    )
    title = esc(page_title(city))
    og_title = esc(page_og_title(city))
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#0F2233">
    <meta name="description" content="{description}">
    <meta name="robots" content="index, follow">
    <meta name="author" content="SoulCont">
    <link rel="canonical" href="{city_url(city)}">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="pt_BR">
    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{SITE['og_image']}">
    <meta property="og:url" content="{city_url(city)}">
    <meta name="twitter:card" content="summary_large_image">
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Inter:wght@400;500;600;700&family=Poppins:wght@400;500;600;700&family=Syne:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn-uicons.flaticon.com/2.6.0/uicons-regular-rounded/css/uicons-regular-rounded.css">
    <link rel="icon" href="/assets/img/soulcont/favicon.svg?v=2" type="image/svg+xml">
    <link rel="apple-touch-icon" href="/assets/img/soulcont/apple-touch-icon.png" sizes="180x180">
    <link rel="stylesheet" href="/assets/css/main.css?v=3.7">
    <link rel="stylesheet" href="/assets/css/mediaquery.css?v=3.7">
    <link rel="stylesheet" href="/assets/css/site-v2.css?v=1.1">
    <link rel="stylesheet" href="/assets/css/motion.css?v=1.0">
    <link rel="stylesheet" href="/assets/css/soulcont-brand.css?v=1.5">
    <link rel="stylesheet" href="/assets/css/cookies.css?v=4.0">
    <style>{PAGE_CSS}</style>
    <script type="application/ld+json">
{json_script(page_schema(city))}
    </script>
    <script type="application/ld+json">
{json_script(faq_schema(city))}
    </script>
</head>
<body data-whatsapp-region="{whatsapp_region}">
    <header>
        <div class="logo"><a href="/"><img src="/assets/img/soulcont/wordmark.svg?v=2" alt="Logo SoulCont"></a></div>
        <nav role="navigation" aria-label="Menu principal"><ul class="menu">
            <li><a href="/" data-nav="home"><i class="fi fi-rr-home"></i> Home</a></li>
            <li><a href="/HTML/servicos.html" data-nav="services"><i class="fi fi-rr-briefcase"></i> Serviços</a></li>
            <li><a href="/HTML/ferramentas.html" data-nav="tools"><i class="fi fi-rr-calculator"></i> Ferramentas</a></li>
            <li><a href="/HTML/contatos.html" data-nav="contact"><i class="fi fi-rr-phone-call"></i> Contato</a></li>
        </ul></nav>
        <div class="menu-mobile"><button class="menu-toggle" aria-label="Abrir menu" aria-expanded="false" id="btn-mobile"><i class="fi fi-rr-menu-burger"></i></button></div>
    </header>
    <main class="site-main-v2">
        <section class="section-shell">
            <div class="detail-hero">
                <div class="city-breadcrumb"><a href="/cidades/">Cidades atendidas</a><span>/</span><strong>{name}</strong></div>
                <span class="eyebrow-label"><i class="fi fi-rr-marker"></i> Contabilidade em {name}, {state_name}</span>
                <h1>Contador em {name} para decisões empresariais mais claras e seguras</h1>
                <p>{hero_text}</p>
                <div class="cta-actions-v2"><a href="{whatsapp_href}" class="btn-v2 btn-v2-primary" target="_blank" rel="noopener noreferrer" data-direct-whatsapp="true" data-track-position="hero">Falar no WhatsApp</a><a href="tel:{phone_e164}" class="btn-v2 btn-v2-secondary" data-track-position="hero">Ligar para {phone_display}</a></div>
                <p class="hero-responsible-line">Atendimento conduzido por {esc(professional_summary)}</p>
            </div>
        </section>
        <section class="section-block"><div class="section-shell"><div class="detail-grid">
            <article class="detail-card"><span class="card-icon"><i class="fi fi-rr-marker"></i></span><h3>{presence_title}</h3><p>{presence_text}</p></article>
            <article class="detail-card"><span class="card-icon"><i class="fi fi-rr-phone-call"></i></span><h3>Telefone oficial</h3><p><a class="city-link" href="tel:{phone_e164}">{phone_display}</a></p></article>
            <article class="detail-card"><span class="card-icon"><i class="fi fi-rr-bulb"></i></span><h3>{esc(city['focus'])}</h3><p>{esc(city['focus_text'])}</p></article>
        </div></div></section>
        <section class="section-block"><div class="section-shell"><div class="section-panel">
            <div class="section-heading"><span class="eyebrow-label"><i class="fi fi-rr-chart-histogram"></i> Contexto do atendimento</span><h2>{esc(city['context_title'])}</h2><p>{esc(city['context'])}</p></div>
            <ul class="detail-list">
{list_items(city['audiences'])}
            </ul>
        </div></div></section>
        <section class="section-block" id="servicos"><div class="section-shell"><div class="section-panel">
            <div class="section-heading"><span class="eyebrow-label"><i class="fi fi-rr-briefcase"></i> Serviços contábeis para {name}</span><h2>Apoio para abrir, organizar e desenvolver sua empresa</h2><p>O escopo é definido após compreender atividade, regime, equipe, pendências e objetivos do negócio.</p></div>
            <div class="city-service-grid">
                <article class="detail-card"><span class="card-icon"><i class="fi fi-rr-apps-add"></i></span><h3>Abertura de empresa</h3><p>CNAE, natureza jurídica, regime tributário e documentação para iniciar o CNPJ com mais segurança.</p></article>
                <article class="detail-card"><span class="card-icon"><i class="fi fi-rr-refresh"></i></span><h3>Troca de contador</h3><p>Levantamento de pendências, checklist documental e transição organizada para manter a rotina.</p></article>
                <article class="detail-card"><span class="card-icon"><i class="fi fi-rr-chart-pie"></i></span><h3>Diagnóstico tributário</h3><p>Análise do enquadramento e comparação de cenários com dados da empresa.</p></article>
                <article class="detail-card"><span class="card-icon"><i class="fi fi-rr-document-signed"></i></span><h3>Contabilidade fiscal</h3><p>Apuração de tributos, acompanhamento de obrigações e prevenção de riscos fiscais.</p></article>
                <article class="detail-card"><span class="card-icon"><i class="fi fi-rr-users"></i></span><h3>Departamento pessoal</h3><p>Admissões, férias, rescisões, folha de pagamento e acompanhamento de encargos.</p></article>
                <article class="detail-card"><span class="card-icon"><i class="fi fi-rr-coins"></i></span><h3>Consultoria financeira</h3><p>Fluxo de caixa, margem, ponto de equilíbrio e indicadores para apoiar decisões.</p></article>
            </div>
        </div></div></section>{related_links_section(city)}
        <section class="section-block"><div class="section-shell"><div class="section-panel">
            <div class="section-heading"><span class="eyebrow-label"><i class="fi fi-rr-compass-alt"></i> Decisões que podemos organizar</span><h2>Próximos passos para empresas de {name}</h2><p>O atendimento consultivo transforma situações recorrentes em análises, responsáveis e prazos.</p></div>
            <ul class="detail-list">
{list_items(city['decisions'])}
            </ul>
            <div class="city-note"><p>{presence_note}</p></div>
        </div></div></section>
        <section class="section-block"><div class="section-shell"><div class="section-panel">
            <div class="section-heading"><span class="eyebrow-label"><i class="fi fi-rr-shield-check"></i> Responsáveis pelo atendimento</span><h2>{professional_heading}</h2><p>O acompanhamento é conduzido por profissionais identificados, com processos digitais e análise do momento de cada empresa.</p></div>
            <div class="city-team-grid">
{render_professionals(city)}
            </div>
        </div></div></section>
        <section class="section-block"><div class="section-shell"><div class="detail-grid">
            <article class="detail-card"><h3>1. Conversa inicial</h3><p>Entendemos atividade, situação atual e o que precisa ser resolvido primeiro.</p></article>
            <article class="detail-card"><h3>2. Análise e orientação</h3><p>Organizamos documentos e cenários para apresentar caminhos compatíveis com o negócio.</p></article>
            <article class="detail-card"><h3>3. Implantação e rotina</h3><p>Definimos responsabilidades, prazos e canais para manter o acompanhamento contínuo.</p></article>
        </div></div></section>
        <section class="section-block"><div class="section-shell"><div class="section-panel">
            <div class="section-heading"><span class="eyebrow-label"><i class="fi fi-rr-interrogation"></i> FAQ</span><h2>Perguntas frequentes sobre contabilidade em {name}</h2></div>
            <div class="faq-details">
                <details><summary>{esc(city['faq_q'])}</summary><p>{esc(city['faq_a'])}</p></details>
                <details><summary>A SoulCont atende empresas de {name}?</summary><p>{attendance_faq}</p></details>
                <details><summary>Quais serviços contábeis estão disponíveis?</summary><p>Abertura de empresa, troca de contador, diagnóstico tributário, contabilidade fiscal, departamento pessoal e consultoria financeira e empresarial, conforme a necessidade.</p></details>
            </div>
        </div></div></section>
        <section class="section-block"><div class="section-shell"><div class="final-cta-panel">
            <span class="eyebrow-label"><i class="fi fi-rr-headset"></i> Próximo passo</span><h2>Precisa de um contador para sua empresa em {name}?</h2><p>Converse com a SoulCont e explique o momento atual do negócio. A primeira orientação começa pelo seu contexto.</p>
            <div class="cta-actions-v2"><a href="{whatsapp_href}" class="btn-v2 btn-v2-primary" target="_blank" rel="noopener noreferrer" data-direct-whatsapp="true" data-track-position="final_cta">Falar no WhatsApp</a><a href="tel:{phone_e164}" class="btn-v2 btn-v2-secondary" data-track-position="final_cta">Ligar para {phone_display}</a></div>
        </div></div></section>
    </main>
    <footer class="site-footer-v2 footer-lean">
        <div class="footer-panel-v2">
            <div class="footer-lean__top">
                <div class="footer-lean__brand">
                    <a href="/" class="soulcont-wordmark" aria-label="SoulCont - página inicial"><span>SOUL</span><strong>CONT</strong></a>
                    <p>Contabilidade consultiva para empresas e profissionais.</p>
                </div>
                <div class="footer-lean__contact">
                    <a class="footer-lean__wa" href="https://wa.me/5588921791670?text=Ol%C3%A1%21%20Vim%20pelo%20site%20da%20SoulCont%20e%20quero%20conversar%20sobre%20minha%20empresa." target="_blank" rel="noopener noreferrer" data-direct-whatsapp="true" data-track-position="footer">WhatsApp Ceará · (88) 92179-1670</a>
                    <a class="footer-lean__wa" href="https://wa.me/5511916539680?text=Ol%C3%A1%21%20Vim%20pelo%20site%20da%20SoulCont%20e%20quero%20conversar%20sobre%20minha%20empresa." target="_blank" rel="noopener noreferrer" data-direct-whatsapp="true" data-track-position="footer">WhatsApp São Paulo · (11) 91653-9680</a>
                    <a class="footer-lean__mail" href="mailto:contato@soulcont.com">contato@soulcont.com</a>
                </div>
            </div>
            <nav class="footer-lean__links" aria-label="Links do rodapé">
                <a href="/HTML/servicos.html">Serviços</a>
                <a href="/HTML/abertura-de-empresa.html">Abrir empresa</a>
                <a href="/HTML/troca-de-contador.html">Trocar de contador</a>
                <a href="/HTML/ferramentas.html">Ferramentas</a>
                <a href="/BLOG/index.html">Blog</a>
                <a href="/cidades/">Cidades atendidas</a>
                <a href="/HTML/sobre.html">Sobre</a>
            </nav>
            <div class="footer-meta-v2 footer-lean__legal">
                <p>Vitor Rodrigues de Lima · CRC SP353836 · Leonardo Silva de Sousa · CRCCE 024206/O5</p>
                <p>&copy; <span id="current-year">2026</span> SoulCont · CNPJ 63.937.299/0001-25 · <a href="/HTML/politica-de-privacidade.html">Privacidade</a></p>
            </div>
        </div>
    </footer>
    <script src="/assets/js/menu.js?v=4.1" defer></script><script src="/assets/js/footer.js?v=3.7" defer></script><script src="/assets/js/motion.js?v=1.0" defer></script><script src="/assets/js/main.js?v=1.0" defer></script><script src="/assets/js/soulcont-brand.js?v=1.3" defer></script>
    <script src="/assets/js/cookies.js?v=4.1" defer></script>
</body>
</html>
'''


def render_hub() -> str:
    region_sections = []
    active_region_keys: list[str] = []
    for region_key, region in REGIONS.items():
        region_cities = [city for city in CITIES if city["region"] == region_key]
        if not region_cities:
            continue
        active_region_keys.append(region_key)
        cards = "\n".join(
            f'''                    <article class="detail-card"><span class="card-icon"><i class="fi fi-rr-marker"></i></span><h3>Contador em {esc(city['name'])}</h3><p>{esc(city['focus_text'])}</p><a class="text-link-v2" href="/cidades/{city['slug']}/">Ver atendimento em {esc(city['name'])} <i class="fi fi-rr-arrow-right"></i></a></article>'''
            for city in region_cities
        )
        region_sections.append(
            (
                '<section class="city-region" '
                f'aria-labelledby="region-{esc(region_key)}">'
                f'<h3 id="region-{esc(region_key)}">{esc(region["state_name"])}</h3>'
                f'<div class="cities-grid">\n{cards}\n                </div></section>'
            )
        )
    grouped_cards = "\n".join(region_sections)
    regional_contacts = "".join(
        (
            f'<li><a href="tel:{esc(REGIONS[key]["phone_e164"])}">'
            f'{esc(REGIONS[key]["state_code"])} · {esc(REGIONS[key]["phone_display"])}</a></li>'
        )
        for key in active_region_keys
    )
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Cidades atendidas pela SoulCont",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": city["name"],
                "url": city_url(city),
            }
            for index, city in enumerate(CITIES, 1)
        ],
    }
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="theme-color" content="#0F2233">
    <meta name="description" content="Conheça as cidades atendidas pela SoulCont. Contabilidade consultiva com atendimento presencial, externo ou on-line conforme a região.">
    <meta name="robots" content="index, follow"><meta name="author" content="SoulCont"><link rel="canonical" href="https://soulcontt.com.br/cidades/">
    <meta property="og:type" content="website"><meta property="og:locale" content="pt_BR"><meta property="og:title" content="Cidades atendidas | SoulCont"><meta property="og:description" content="Contabilidade consultiva com formas de atendimento transparentes para cada região."><meta property="og:image" content="https://soulcontt.com.br/assets/img/soulcont/og-soulcont.jpg"><meta property="og:url" content="https://soulcontt.com.br/cidades/">
    <title>Cidades atendidas | Contabilidade consultiva | SoulCont</title>
    <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Inter:wght@400;500;600;700&family=Poppins:wght@400;500;600;700&family=Syne:wght@400;500;600;700;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="https://cdn-uicons.flaticon.com/2.6.0/uicons-regular-rounded/css/uicons-regular-rounded.css">
    <link rel="icon" href="/assets/img/soulcont/favicon.svg?v=2" type="image/svg+xml"><link rel="stylesheet" href="/assets/css/main.css?v=3.7"><link rel="stylesheet" href="/assets/css/mediaquery.css?v=3.7"><link rel="stylesheet" href="/assets/css/site-v2.css?v=1.1"><link rel="stylesheet" href="/assets/css/motion.css?v=1.0"><link rel="stylesheet" href="/assets/css/soulcont-brand.css?v=1.5"><link rel="stylesheet" href="/assets/css/cookies.css?v=4.0">
    <style>html,body{{max-width:100%;overflow-x:hidden}}.city-region+.city-region{{margin-top:36px}}.city-region>h3{{margin:0 0 16px;color:#0f2233;font-family:Syne,sans-serif}}.cities-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:18px}}.cities-grid .detail-card{{height:100%;display:flex;flex-direction:column}}.cities-grid .text-link-v2{{margin-top:auto;padding-top:18px}}.hub-note{{margin-top:24px;padding:20px;border-left:4px solid #2c6b57;background:rgba(44,107,87,.07);border-radius:0 14px 14px 0}}.hub-note p{{margin:0}}@media(max-width:640px){{.cta-actions-v2>*{{width:100%;justify-content:center;text-align:center}}}}</style>
    <script type="application/ld+json">
{json_script(item_list)}
    </script>
</head>
<body>
    <header><div class="logo"><a href="/"><img src="/assets/img/soulcont/wordmark.svg?v=2" alt="Logo SoulCont"></a></div><nav role="navigation" aria-label="Menu principal"><ul class="menu"><li><a href="/"><i class="fi fi-rr-home"></i> Home</a></li><li><a href="/HTML/servicos.html"><i class="fi fi-rr-briefcase"></i> Serviços</a></li><li><a href="/HTML/ferramentas.html"><i class="fi fi-rr-calculator"></i> Ferramentas</a></li><li><a href="/HTML/contatos.html"><i class="fi fi-rr-phone-call"></i> Contato</a></li></ul></nav><div class="menu-mobile"><button class="menu-toggle" aria-label="Abrir menu" aria-expanded="false" id="btn-mobile"><i class="fi fi-rr-menu-burger"></i></button></div></header>
    <main class="site-main-v2">
        <section class="section-shell"><div class="detail-hero"><span class="eyebrow-label"><i class="fi fi-rr-marker"></i> Presença regional</span><h1>Contabilidade consultiva para empresas em diferentes regiões</h1><p>A SoulCont informa em cada página se o atendimento é presencial em endereço público, externo mediante agendamento ou inteiramente on-line.</p><div class="cta-actions-v2"><a href="/HTML/contatos.html" class="btn-v2 btn-v2-primary">Falar com a SoulCont</a><a href="#cidades" class="btn-v2 btn-v2-secondary">Ver cidades atendidas</a></div></div></section>
        <section class="section-block" id="cidades"><div class="section-shell"><div class="section-panel"><div class="section-heading"><span class="eyebrow-label"><i class="fi fi-rr-map"></i> Cidades atendidas</span><h2>Escolha a cidade da sua empresa</h2><p>As páginas apresentam situações e prioridades comuns ao atendimento em cada localidade. O diagnóstico final sempre depende dos dados reais da empresa.</p></div>
{grouped_cards}
            <div class="hub-note"><p>A presença de uma cidade nesta lista não significa que exista uma unidade física no local. Consulte a página da cidade para conhecer a forma de atendimento disponível.</p></div></div></div></section>
        <section class="section-block"><div class="section-shell"><div class="final-cta-panel"><span class="eyebrow-label"><i class="fi fi-rr-headset"></i> Atendimento consultivo</span><h2>Sua cidade não está na lista?</h2><p>A SoulCont pode avaliar atendimento on-line para empresas de outras localidades. O primeiro passo é entender a atividade e a necessidade do negócio.</p><div class="cta-actions-v2"><a href="/HTML/contatos.html" class="btn-v2 btn-v2-primary">Consultar atendimento</a></div></div></div></section>
    </main>
    <footer class="site-footer-v2 footer-lean">
        <div class="footer-panel-v2">
            <div class="footer-lean__top">
                <div class="footer-lean__brand">
                    <a href="/" class="soulcont-wordmark" aria-label="SoulCont - página inicial"><span>SOUL</span><strong>CONT</strong></a>
                    <p>Contabilidade consultiva para empresas e profissionais.</p>
                </div>
                <div class="footer-lean__contact">
                    <a class="footer-lean__wa" href="https://wa.me/5588921791670?text=Ol%C3%A1%21%20Vim%20pelo%20site%20da%20SoulCont%20e%20quero%20conversar%20sobre%20minha%20empresa." target="_blank" rel="noopener noreferrer" data-direct-whatsapp="true" data-track-position="footer">WhatsApp Ceará · (88) 92179-1670</a>
                    <a class="footer-lean__wa" href="https://wa.me/5511916539680?text=Ol%C3%A1%21%20Vim%20pelo%20site%20da%20SoulCont%20e%20quero%20conversar%20sobre%20minha%20empresa." target="_blank" rel="noopener noreferrer" data-direct-whatsapp="true" data-track-position="footer">WhatsApp São Paulo · (11) 91653-9680</a>
                    <a class="footer-lean__mail" href="mailto:contato@soulcont.com">contato@soulcont.com</a>
                </div>
            </div>
            <nav class="footer-lean__links" aria-label="Links do rodapé">
                <a href="/HTML/servicos.html">Serviços</a>
                <a href="/HTML/abertura-de-empresa.html">Abrir empresa</a>
                <a href="/HTML/troca-de-contador.html">Trocar de contador</a>
                <a href="/HTML/ferramentas.html">Ferramentas</a>
                <a href="/BLOG/index.html">Blog</a>
                <a href="/cidades/">Cidades atendidas</a>
                <a href="/HTML/sobre.html">Sobre</a>
            </nav>
            <div class="footer-meta-v2 footer-lean__legal">
                <p>Vitor Rodrigues de Lima · CRC SP353836 · Leonardo Silva de Sousa · CRCCE 024206/O5</p>
                <p>&copy; <span id="current-year">2026</span> SoulCont · CNPJ 63.937.299/0001-25 · <a href="/HTML/politica-de-privacidade.html">Privacidade</a></p>
            </div>
        </div>
    </footer>
    <script src="/assets/js/menu.js?v=4.1" defer></script><script src="/assets/js/footer.js?v=3.7" defer></script><script src="/assets/js/motion.js?v=1.0" defer></script><script src="/assets/js/main.js?v=1.0" defer></script><script src="/assets/js/soulcont-brand.js?v=1.3" defer></script><script src="/assets/js/cookies.js?v=4.1" defer></script>
</body>
</html>
'''


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for city in CITIES:
        if city["slug"] == "sao-paulo":
            # The São Paulo hub is a bespoke page with neighborhood links and schema.
            # It is maintained alongside the neighborhood generator.
            continue
        target = OUTPUT / city["slug"] / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_city(city), encoding="utf-8", newline="\n")
    (OUTPUT / "index.html").write_text(render_hub(), encoding="utf-8", newline="\n")
    print(f"Generated hub and {len(CITIES) - 1} city pages in {OUTPUT}; preserved the São Paulo hub")


if __name__ == "__main__":
    main()
