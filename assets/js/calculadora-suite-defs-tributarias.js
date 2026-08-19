(function () {
    const suite = window.CalculadoraSuite || {};
    const H = suite.helpers;
    if (!suite.registerDefinition || !H) return;

    suite.registerDefinition('simples-nacional', {
        pageTitle: 'Simulador de Simples Nacional por Faturamento',
        pageDescription: 'Estime aliquota efetiva e DAS mensal com base no faturamento e anexo do Simples Nacional.',
        badges: ['Tributario', 'DAS mensal', 'Comparativo rapido'],
        calculateLabel: 'Calcular Simples Nacional',
        fields: [
            {
                id: 'rbt12',
                type: 'number',
                label: 'Faturamento acumulado em 12 meses (RBT12)',
                placeholder: 'R$ 0,00',
                min: 0,
                step: '0.01',
                help: 'Use o acumulado real dos ultimos 12 meses.'
            },
            {
                id: 'receitaMes',
                type: 'number',
                label: 'Faturamento do mes atual',
                placeholder: 'R$ 0,00',
                min: 0,
                step: '0.01'
            },
            {
                id: 'anexo',
                type: 'select',
                label: 'Anexo principal',
                options: [
                    { value: 'I', label: 'Anexo I - Comercio' },
                    { value: 'II', label: 'Anexo II - Industria' },
                    { value: 'III', label: 'Anexo III - Servicos' },
                    { value: 'IV', label: 'Anexo IV - Servicos especificos' },
                    { value: 'V', label: 'Anexo V - Servicos intelectuais' }
                ]
            },
            {
                id: 'folha12',
                type: 'number',
                label: 'Folha dos ultimos 12 meses (opcional)',
                placeholder: 'R$ 0,00',
                min: 0,
                step: '0.01',
                help: 'Ajuda na leitura do Fator R para anexos III e V.'
            }
        ],
        example: {
            rbt12: 960000,
            receitaMes: 78000,
            anexo: 'III',
            folha12: 310000
        },
        validate(values) {
            if (values.rbt12 <= 0) return 'Informe o faturamento acumulado de 12 meses.';
            if (values.receitaMes <= 0) return 'Informe o faturamento do mes para estimar o DAS.';
            return '';
        },
        compute(values) {
            const simples = H.calcularAliquotaEfetivaSimples(values.anexo, values.rbt12);
            const dasMes = values.receitaMes * simples.aliquotaEfetiva;
            const cargaAnual = dasMes * 12;
            const receitaPosDAS = Math.max(0, values.receitaMes - dasMes);
            const fatorR = values.folha12 > 0 ? (values.folha12 / values.rbt12) : 0;
            const leituraFatorR = values.folha12 > 0
                ? (fatorR >= 0.28 ? 'Fator R acima de 28%: tende a favorecer anexo III.' : 'Fator R abaixo de 28%: revisar enquadramento de servicos.')
                : 'Informe a folha anual para analisar Fator R.';
            const anexoSugerido = values.folha12 > 0 && (values.anexo === 'III' || values.anexo === 'V')
                ? (fatorR >= 0.28 ? 'III' : 'V')
                : values.anexo;
            const simulacaoSugerida = H.calcularAliquotaEfetivaSimples(anexoSugerido, values.rbt12);
            const diferencaPotencialMes = values.receitaMes * (simples.aliquotaEfetiva - simulacaoSugerida.aliquotaEfetiva);

            return {
                highlight: H.metricCurrency('DAS estimado no mes', dasMes),
                secondaryA: H.metricPercent('Aliquota efetiva', simples.aliquotaEfetiva * 100),
                secondaryB: H.metricCurrency('Carga anual estimada', cargaAnual),
                notes: [
                    { label: 'Faixa aplicada', metric: H.metricText('Faixa', `Ate ${H.formatCurrency(simples.faixa.limite)} | nominal ${H.formatPercent(simples.faixa.aliquota * 100)}`) },
                    { label: 'Parcela a deduzir', metric: H.metricCurrency('Parcela', simples.faixa.deducao) },
                    { label: 'Fator R', metric: H.metricText('Leitura', leituraFatorR) },
                    { label: 'Potencial mensal com anexo sugerido', metric: H.metricCurrency('Diferenca', diferencaPotencialMes) }
                ],
                steps: [
                    `Classificacao por faixa do anexo ${values.anexo}.`,
                    'Calculo da aliquota efetiva com parcela a deduzir.',
                    'Estimativa do DAS mensal e impacto anual.'
                ],
                details: [
                    { label: 'Receita do mes', value: H.formatCurrency(values.receitaMes) },
                    { label: 'Receita liquida apos DAS', value: H.formatCurrency(receitaPosDAS) },
                    { label: 'Aliquota nominal da faixa', value: H.formatPercent(simples.faixa.aliquota * 100) },
                    { label: 'Aliquota efetiva usada', value: H.formatPercent(simples.aliquotaEfetiva * 100) },
                    { label: 'Anexo sugerido pelo Fator R', value: anexoSugerido }
                ],
                chart: {
                    labels: ['DAS estimado', 'Receita apos DAS'],
                    values: [H.round2(dasMes), H.round2(receitaPosDAS)],
                    colors: ['#d46d13', '#0f766e']
                }
            };
        }
    });

    suite.registerDefinition('inss-irrf-estimado', {
        pageTitle: 'Simulador de INSS e IRRF Estimado',
        pageDescription: 'Calcule descontos previdenciarios e imposto de renda retido na fonte com parametros mensais.',
        badges: ['Folha', 'INSS', 'IRRF'],
        calculateLabel: 'Calcular INSS e IRRF',
        fields: [
            { id: 'rendimentoBruto', type: 'number', label: 'Rendimento bruto mensal', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'dependentes', type: 'number', label: 'Dependentes para IRRF', min: 0, step: '1' },
            { id: 'pensao', type: 'number', label: 'Pensao alimenticia dedutivel', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'outrasDeducoes', type: 'number', label: 'Outras deducoes legais', placeholder: 'R$ 0,00', min: 0, step: '0.01' }
        ],
        example: {
            rendimentoBruto: 6200,
            dependentes: 1,
            pensao: 0,
            outrasDeducoes: 200
        },
        validate(values) {
            if (values.rendimentoBruto <= 0) return 'Informe o rendimento bruto para calcular os descontos.';
            return '';
        },
        compute(values) {
            const mensal = H.calcularIRRFMensal(values.rendimentoBruto, {
                dependentes: values.dependentes,
                pensao: values.pensao,
                outrasDeducoes: values.outrasDeducoes
            });

            return {
                highlight: H.metricCurrency('Liquido estimado', mensal.liquido),
                secondaryA: H.metricCurrency('INSS estimado', mensal.inss),
                secondaryB: H.metricCurrency('IRRF estimado', mensal.irrf.impostoFinal),
                notes: [
                    { label: 'Base de calculo IRRF', metric: H.metricCurrency('Base', mensal.baseIRRF) },
                    { label: 'Reducao legal aplicada', metric: H.metricCurrency('Reducao', mensal.irrf.reducao) },
                    { label: 'Deducao considerada', metric: H.metricCurrency('Deducao', mensal.deducaoAplicada) }
                ],
                steps: [
                    'Calculo do INSS progressivo por faixas.',
                    'Comparacao entre deducoes legais e desconto simplificado.',
                    'Aplicacao da tabela de IRRF e exibicao do liquido.'
                ],
                details: [
                    { label: 'Rendimento bruto', value: H.formatCurrency(values.rendimentoBruto) },
                    { label: 'Dependentes', value: `${values.dependentes} dependente(s)` },
                    { label: 'Pensao dedutivel', value: H.formatCurrency(values.pensao) },
                    { label: 'Outras deducoes', value: H.formatCurrency(values.outrasDeducoes) }
                ],
                chart: {
                    labels: ['Liquido', 'INSS', 'IRRF', 'Outras deducoes'],
                    values: [
                        H.round2(Math.max(0, mensal.liquido)),
                        H.round2(mensal.inss),
                        H.round2(mensal.irrf.impostoFinal),
                        H.round2(values.pensao + values.outrasDeducoes)
                    ],
                    colors: ['#0f766e', '#0a7dd1', '#d46d13', '#64748b']
                }
            };
        }
    });

    suite.registerDefinition('limite-mei', {
        pageTitle: 'Calculadora de Limite MEI e Projecao',
        pageDescription: 'Projete o faturamento anual do MEI e identifique risco de desenquadramento com antecedencia.',
        badges: ['MEI', 'Limite anual', 'Projecao'],
        calculateLabel: 'Calcular limite MEI',
        fields: [
            { id: 'faturamentoAcumulado', type: 'number', label: 'Faturamento acumulado no ano', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            {
                id: 'mesesDecorridos',
                type: 'select',
                label: 'Meses ja encerrados no ano',
                options: [
                    { value: '1', label: '1 mes' }, { value: '2', label: '2 meses' }, { value: '3', label: '3 meses' },
                    { value: '4', label: '4 meses' }, { value: '5', label: '5 meses' }, { value: '6', label: '6 meses' },
                    { value: '7', label: '7 meses' }, { value: '8', label: '8 meses' }, { value: '9', label: '9 meses' },
                    { value: '10', label: '10 meses' }, { value: '11', label: '11 meses' }, { value: '12', label: '12 meses' }
                ]
            },
            { id: 'mediaMensal', type: 'number', label: 'Projecao de faturamento mensal para os proximos meses', placeholder: 'R$ 0,00', min: 0, step: '0.01' }
        ],
        example: {
            faturamentoAcumulado: 56000,
            mesesDecorridos: '8',
            mediaMensal: 7600
        },
        validate() {
            return '';
        },
        compute(values) {
            const limiteAnual = globalThis.SoulcontFiscal.MEI.limiteAnual;
            const mesesDecorridos = H.clamp(values.mesesDecorridos, 1, 12);
            const limiteProporcional = (limiteAnual / 12) * mesesDecorridos;
            const mesesRestantes = 12 - mesesDecorridos;
            const projecaoAnual = values.faturamentoAcumulado + (values.mediaMensal * mesesRestantes);
            const excessoProjetado = Math.max(0, projecaoAnual - limiteAnual);
            const excessoPercentual = limiteAnual > 0 ? (projecaoAnual / limiteAnual - 1) * 100 : 0;

            let status = 'Dentro do limite do MEI.';
            if (projecaoAnual > 97200) {
                status = 'Acima de 20% do limite. Risco alto de desenquadramento retroativo.';
            } else if (projecaoAnual > limiteAnual) {
                status = 'Excesso de ate 20% do limite. Planeje migracao para evitar surpresa.';
            }

            return {
                highlight: H.metricCurrency('Projecao anual', projecaoAnual),
                secondaryA: H.metricCurrency('Limite anual MEI', limiteAnual),
                secondaryB: H.metricCurrency('Excesso projetado', excessoProjetado),
                notes: [
                    { label: 'Status', metric: H.metricText('Status', status) },
                    { label: 'Limite proporcional no ano', metric: H.metricCurrency('Proporcional', limiteProporcional) },
                    { label: 'Excesso percentual', metric: H.metricPercent('Excesso', Math.max(0, excessoPercentual)) }
                ],
                steps: [
                    'Calculo do limite proporcional conforme meses decorridos.',
                    'Projecao do faturamento restante ate dezembro.',
                    'Classificacao de risco de desenquadramento.'
                ],
                details: [
                    { label: 'Faturamento acumulado', value: H.formatCurrency(values.faturamentoAcumulado) },
                    { label: 'Meses restantes', value: `${mesesRestantes} mes(es)` },
                    { label: 'Media mensal projetada', value: H.formatCurrency(values.mediaMensal) },
                    { label: 'Faixa de alerta 20%', value: H.formatCurrency(97200) }
                ],
                chart: {
                    labels: ['Projecao anual', 'Limite MEI'],
                    values: [H.round2(projecaoAnual), limiteAnual],
                    colors: ['#0a7dd1', '#d46d13']
                }
            };
        }
    });

    suite.registerDefinition('mei-vs-simples', {
        pageTitle: 'Comparador MEI x Simples Nacional',
        pageDescription: 'Compare custo tributario estimado entre MEI e Simples Nacional para apoiar seu enquadramento.',
        badges: ['Comparativo', 'MEI', 'Simples'],
        calculateLabel: 'Comparar regimes',
        fields: [
            { id: 'faturamentoMensal', type: 'number', label: 'Faturamento medio mensal', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            {
                id: 'atividade',
                type: 'select',
                label: 'Tipo principal de atividade',
                options: [
                    { value: 'comercio', label: 'Comercio' },
                    { value: 'servico', label: 'Servico' },
                    { value: 'misto', label: 'Comercio + Servico' }
                ]
            },
            {
                id: 'anexoSimples',
                type: 'select',
                label: 'Anexo estimado no Simples',
                options: [
                    { value: 'I', label: 'Anexo I' },
                    { value: 'III', label: 'Anexo III' },
                    { value: 'V', label: 'Anexo V' }
                ]
            }
        ],
        example: {
            faturamentoMensal: 9800,
            atividade: 'servico',
            anexoSimples: 'III'
        },
        validate(values) {
            if (values.faturamentoMensal <= 0) return 'Informe o faturamento mensal para comparar os regimes.';
            return '';
        },
        compute(values) {
            const inssMEI = 81.05;
            const adicionalMEI = values.atividade === 'servico' ? 5 : (values.atividade === 'misto' ? 6 : 1);
            const meiMensal = inssMEI + adicionalMEI;

            const rbt12 = values.faturamentoMensal * 12;
            const simples = H.calcularAliquotaEfetivaSimples(values.anexoSimples, rbt12);
            const simplesMensal = values.faturamentoMensal * simples.aliquotaEfetiva;

            const diferencaMensal = simplesMensal - meiMensal;
            const diferencaAnual = diferencaMensal * 12;
            const economiaAnual = Math.abs(diferencaAnual);
            const ultrapassaMEI = rbt12 > globalThis.SoulcontFiscal.MEI.limiteAnual;
            const regimeMaisEconomico = diferencaMensal > 0 ? 'MEI' : 'Simples';
            const mensagem = ultrapassaMEI
                ? 'Com este faturamento anual projetado, o limite do MEI pode ser ultrapassado.'
                : `No comparativo de tributos, ${regimeMaisEconomico} tende a ser mais economico.`;

            return {
                highlight: H.metricCurrency(
                    regimeMaisEconomico === 'MEI' ? 'Economia anual no MEI' : 'Economia anual no Simples',
                    economiaAnual
                ),
                secondaryA: H.metricCurrency('Tributo mensal MEI', meiMensal),
                secondaryB: H.metricCurrency('Tributo mensal Simples', simplesMensal),
                notes: [
                    { label: 'Leitura do enquadramento', metric: H.metricText('Status', mensagem) },
                    { label: 'Aliquota efetiva do Simples', metric: H.metricPercent('Aliquota', simples.aliquotaEfetiva * 100) },
                    { label: 'Faturamento anual projetado', metric: H.metricCurrency('RBT12', rbt12) },
                    { label: 'Parcela INSS do MEI', metric: H.metricCurrency('5% do salario minimo 2026', inssMEI) }
                ],
                steps: [
                    'Estimativa do tributo fixo mensal do MEI.',
                    'Calculo da aliquota efetiva no Simples pelo RBT12.',
                    'Comparacao mensal e anual de custo tributario.'
                ],
                details: [
                    { label: 'Anexo usado no Simples', value: values.anexoSimples },
                    { label: 'Faixa do anexo', value: `Ate ${H.formatCurrency(simples.faixa.limite)}` },
                    { label: 'Diferenca mensal', value: H.formatCurrency(diferencaMensal) },
                    { label: 'Diferenca anual', value: H.formatCurrency(diferencaAnual) }
                ],
                chart: {
                    labels: ['MEI mensal', 'Simples mensal'],
                    values: [H.round2(meiMensal), H.round2(simplesMensal)],
                    colors: ['#0f766e', '#0a7dd1']
                }
            };
        }
    });

    suite.registerDefinition('simples-vs-lucro-presumido', {
        pageTitle: 'Comparador Simples Nacional x Lucro Presumido',
        pageDescription: 'Compare os principais tributos mensais entre Simples e Lucro Presumido para apoiar o enquadramento.',
        badges: ['Comparativo', 'Tributario', 'Planejamento'],
        calculateLabel: 'Comparar regimes',
        fields: [
            { id: 'faturamentoMensal', type: 'number', label: 'Faturamento medio mensal', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'rbt12', type: 'number', label: 'Faturamento acumulado de 12 meses', placeholder: 'R$ 0,00', min: 0, step: '0.01', help: 'Se nao tiver, use 12x o faturamento medio.' },
            { id: 'atividade', type: 'select', label: 'Atividade predominante', options: H.atividadePresumidoOptions() },
            {
                id: 'anexoSimples',
                type: 'select',
                label: 'Anexo estimado no Simples',
                options: [
                    { value: 'I', label: 'Anexo I - Comercio' },
                    { value: 'II', label: 'Anexo II - Industria' },
                    { value: 'III', label: 'Anexo III - Servicos' },
                    { value: 'IV', label: 'Anexo IV - Servicos especificos' },
                    { value: 'V', label: 'Anexo V - Servicos intelectuais' }
                ]
            },
            { id: 'folhaMensal', type: 'number', label: 'Folha mensal estimada', placeholder: 'R$ 0,00', min: 0, step: '0.01', help: 'Usada para estimar CPP fora do DAS no Anexo IV e no Presumido.' },
            { id: 'aliquotaLocal', type: 'number', label: 'ISS ou ICMS adicional no Presumido (%)', min: 0, max: 10, step: '0.1', help: 'Opcional. Use apenas se quiser incluir tributo local na simulacao do Presumido.' }
        ],
        example: {
            faturamentoMensal: 85000,
            rbt12: 1020000,
            atividade: 'servicos',
            anexoSimples: 'III',
            folhaMensal: 18000,
            aliquotaLocal: 2
        },
        validate(values) {
            if (values.faturamentoMensal <= 0) return 'Informe o faturamento medio mensal.';
            if (values.rbt12 <= 0) return 'Informe o faturamento acumulado de 12 meses.';
            return '';
        },
        compute(values) {
            const simples = H.calcularAliquotaEfetivaSimples(values.anexoSimples, values.rbt12);
            const dasMensal = values.faturamentoMensal * simples.aliquotaEfetiva;
            const cppSimples = values.anexoSimples === 'IV' ? (values.folhaMensal * 0.20) : 0;
            const totalSimples = dasMensal + cppSimples;

            const presumido = H.calcularLucroPresumidoMensal(values.faturamentoMensal, values.atividade, values.aliquotaLocal);
            const cppPresumido = values.folhaMensal * 0.20;
            const totalPresumido = presumido.total + cppPresumido;

            const economiaMensal = Math.abs(totalSimples - totalPresumido);
            const economiaAnual = economiaMensal * 12;
            const regimeMaisLeve = totalSimples <= totalPresumido ? 'Simples Nacional' : 'Lucro Presumido';
            const diferencaPontos = values.faturamentoMensal > 0
                ? ((totalPresumido - totalSimples) / values.faturamentoMensal) * 100
                : 0;

            return {
                highlight: H.metricCurrency(`Economia anual estimada no ${regimeMaisLeve}`, economiaAnual),
                secondaryA: H.metricCurrency('Custo mensal no Simples', totalSimples),
                secondaryB: H.metricCurrency('Custo mensal no Presumido', totalPresumido),
                notes: [
                    { label: 'Aliquota efetiva do Simples', metric: H.metricPercent('Aliquota', simples.aliquotaEfetiva * 100) },
                    { label: 'Diferenca em pontos sobre a receita', metric: H.metricPercent('Diferenca', diferencaPontos) },
                    { label: 'Leitura', metric: H.metricText('Regime mais leve', `${regimeMaisLeve} tende a gerar menor carga principal nesta simulacao.`) }
                ],
                steps: [
                    'Estimativa do DAS pelo RBT12 e anexo informado.',
                    'Apuracao do Lucro Presumido com IRPJ, CSLL, PIS/Cofins e tributo local.',
                    'Comparacao mensal e anual entre os dois regimes.'
                ],
                details: [
                    { label: 'DAS mensal no Simples', value: H.formatCurrency(dasMensal) },
                    { label: 'CPP fora do DAS (Simples)', value: H.formatCurrency(cppSimples) },
                    { label: 'Tributos principais no Presumido', value: H.formatCurrency(presumido.total) },
                    { label: 'CPP sobre folha no Presumido', value: H.formatCurrency(cppPresumido) },
                    { label: 'PIS/Cofins no Presumido', value: H.formatCurrency(presumido.pisCofins) },
                    { label: 'IRPJ + adicional no Presumido', value: H.formatCurrency(presumido.irpj) }
                ],
                chart: {
                    labels: ['Simples', 'Lucro Presumido'],
                    values: [H.round2(totalSimples), H.round2(totalPresumido)],
                    colors: ['#0f766e', '#d46d13']
                }
            };
        }
    });

    suite.registerDefinition('pro-labore-liquido', {
        pageTitle: 'Calculadora de Pro-labore Liquido',
        pageDescription: 'Estime o liquido do pro-labore do socio, o INSS retido, o IRRF e o custo total para a empresa.',
        badges: ['Socios', 'Pro-labore', 'Retirada'],
        calculateLabel: 'Calcular pro-labore',
        fields: [
            { id: 'proLaboreBruto', type: 'number', label: 'Pro-labore bruto mensal', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'regimeEmpresa', type: 'select', label: 'Regime da empresa para CPP patronal', options: H.regimeProLaboreOptions() },
            { id: 'dependentes', type: 'number', label: 'Dependentes para IRRF', min: 0, step: '1' },
            { id: 'pensao', type: 'number', label: 'Pensao alimenticia dedutivel', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'outrasDeducoes', type: 'number', label: 'Outras deducoes mensais', placeholder: 'R$ 0,00', min: 0, step: '0.01' }
        ],
        example: {
            proLaboreBruto: 8000,
            regimeEmpresa: 'presumido_real',
            dependentes: 1,
            pensao: 0,
            outrasDeducoes: 0
        },
        validate(values) {
            if (values.proLaboreBruto <= 0) return 'Informe o pro-labore bruto mensal.';
            return '';
        },
        compute(values) {
            const proLabore = H.calcularProLaboreLiquido(values.proLaboreBruto, {
                dependentes: values.dependentes,
                pensao: values.pensao,
                outrasDeducoes: values.outrasDeducoes
            });
            const cppPatronal = H.calcularCPPPatronalProLabore(values.regimeEmpresa, values.proLaboreBruto);
            const custoEmpresa = values.proLaboreBruto + cppPatronal;
            const cargaTotal = proLabore.inssSocio + proLabore.irrf.impostoFinal + cppPatronal;

            return {
                highlight: H.metricCurrency('Pro-labore liquido mensal', proLabore.liquido),
                secondaryA: H.metricCurrency('Custo total da empresa', custoEmpresa),
                secondaryB: H.metricCurrency('Retirada liquida anual', proLabore.liquido * 12),
                notes: [
                    { label: 'INSS do socio', metric: H.metricCurrency('11% sobre o pro-labore ate o teto', proLabore.inssSocio) },
                    { label: 'IRRF estimado', metric: H.metricCurrency('IRRF', proLabore.irrf.impostoFinal) },
                    { label: 'Carga total mensal', metric: H.metricCurrency('Carga total', cargaTotal) }
                ],
                steps: [
                    'Retencao previdenciaria do socio sobre o pro-labore.',
                    'Calculo da base mensal de IRRF com dependentes e deducoes.',
                    'Soma do custo patronal quando o regime exige CPP fora do DAS.'
                ],
                details: [
                    { label: 'Base mensal de IRRF', value: H.formatCurrency(proLabore.baseIRRF) },
                    { label: 'CPP patronal estimada', value: H.formatCurrency(cppPatronal) },
                    { label: 'Deducao aplicada no IRRF', value: H.formatCurrency(proLabore.deducaoAplicada) },
                    { label: 'Liquido anual estimado', value: H.formatCurrency(proLabore.liquido * 12) }
                ],
                chart: {
                    labels: ['Liquido do socio', 'INSS socio', 'IRRF', 'CPP patronal'],
                    values: [
                        H.round2(proLabore.liquido),
                        H.round2(proLabore.inssSocio),
                        H.round2(proLabore.irrf.impostoFinal),
                        H.round2(cppPatronal)
                    ],
                    colors: ['#0f766e', '#0a7dd1', '#d46d13', '#64748b']
                }
            };
        }
    });

    suite.registerDefinition('distribuicao-lucros', {
        pageTitle: 'Calculadora de Distribuicao de Lucros Disponivel',
        pageDescription: 'Projete o lucro distribuivel do mes e a parcela estimada do socio conforme a participacao informada.',
        badges: ['Socios', 'Lucros', 'Caixa'],
        calculateLabel: 'Calcular distribuicao',
        fields: [
            { id: 'faturamentoMensal', type: 'number', label: 'Faturamento do mes', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'custosMensais', type: 'number', label: 'Custos operacionais + pro-labore', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'tributosMensais', type: 'number', label: 'Tributos do mes', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'reservaPercentual', type: 'range', label: 'Percentual para reserva de caixa', min: 0, max: 40, step: 1, value: 15, outputSuffix: '%' },
            { id: 'participacaoSocio', type: 'range', label: 'Participacao do socio nos lucros', min: 1, max: 100, step: 1, value: 100, outputSuffix: '%' }
        ],
        example: {
            faturamentoMensal: 120000,
            custosMensais: 63000,
            tributosMensais: 9800,
            reservaPercentual: 15,
            participacaoSocio: 50
        },
        validate(values) {
            if (values.faturamentoMensal <= 0) return 'Informe o faturamento do mes.';
            return '';
        },
        compute(values) {
            const lucroAntesReserva = values.faturamentoMensal - values.custosMensais - values.tributosMensais;
            const reserva = lucroAntesReserva > 0 ? (lucroAntesReserva * (H.clamp(values.reservaPercentual, 0, 40) / 100)) : 0;
            const lucroDistribuivel = Math.max(0, lucroAntesReserva - reserva);
            const parcelaSocio = lucroDistribuivel * (H.clamp(values.participacaoSocio, 1, 100) / 100);
            const margemLiquida = values.faturamentoMensal > 0 ? (lucroAntesReserva / values.faturamentoMensal) * 100 : 0;

            return {
                highlight: H.metricCurrency('Parcela mensal estimada do socio', parcelaSocio),
                secondaryA: H.metricCurrency('Lucro distribuivel total', lucroDistribuivel),
                secondaryB: H.metricCurrency('Reserva mensal sugerida', reserva),
                notes: [
                    { label: 'Lucro antes da reserva', metric: H.metricCurrency('Lucro', lucroAntesReserva) },
                    { label: 'Margem liquida apos tributos', metric: H.metricPercent('Margem', margemLiquida) },
                    { label: 'Leitura', metric: H.metricText('Leitura', lucroAntesReserva > 0 ? 'Ha espaco para distribuir lucros sem consumir toda a folga do caixa.' : 'Nao ha lucro mensal para distribuicao neste cenario.') }
                ],
                steps: [
                    'Subtracao de custos e tributos sobre a receita do mes.',
                    'Separacao de uma reserva minima para capital de giro.',
                    'Rateio da parcela distribuivel conforme a participacao do socio.'
                ],
                details: [
                    { label: 'Receita anualizada', value: H.formatCurrency(values.faturamentoMensal * 12) },
                    { label: 'Lucro distribuivel anual', value: H.formatCurrency(lucroDistribuivel * 12) },
                    { label: 'Participacao do socio', value: H.formatPercent(values.participacaoSocio) },
                    { label: 'Parcela anual do socio', value: H.formatCurrency(parcelaSocio * 12) }
                ],
                chart: {
                    labels: ['Custos + pro-labore', 'Tributos', 'Reserva', 'Lucro distribuivel'],
                    values: [
                        H.round2(values.custosMensais),
                        H.round2(values.tributosMensais),
                        H.round2(reserva),
                        H.round2(lucroDistribuivel)
                    ],
                    colors: ['#64748b', '#d46d13', '#0a7dd1', '#0f766e']
                }
            };
        }
    });

    /* ----------------------------------------------------------------
       Fator R — a conta que decide entre o Anexo III e o Anexo V para
       atividades de serviço. Além do percentual, mostra o impacto em
       reais e quanto de folha falta para alcançar o corte de 28%.
       Base: LC 123/2006, art. 18, §§ 5º-J e 5º-M.
       ---------------------------------------------------------------- */
    suite.registerDefinition('fator-r', {
        pageTitle: 'Calculadora de Fator R',
        pageDescription: 'Descubra se sua empresa de serviços se enquadra no Anexo III ou no Anexo V do Simples Nacional e quanto isso representa por mês.',
        badges: ['Simples Nacional', 'Anexo III x V', 'Prestador de serviço'],
        calculateLabel: 'Calcular Fator R',
        fields: [
            {
                id: 'folha12',
                type: 'number',
                label: 'Folha de pagamento dos últimos 12 meses',
                placeholder: 'R$ 0,00',
                min: 0,
                step: '0.01',
                help: 'Inclui salários, pró-labore, encargos e FGTS dos últimos 12 meses.'
            },
            {
                id: 'rbt12',
                type: 'number',
                label: 'Receita bruta dos últimos 12 meses (RBT12)',
                placeholder: 'R$ 0,00',
                min: 0,
                step: '0.01'
            },
            {
                id: 'receitaMes',
                type: 'number',
                label: 'Faturamento do mês atual',
                placeholder: 'R$ 0,00',
                min: 0,
                step: '0.01',
                help: 'Usado para estimar quanto o anexo muda no DAS deste mês.'
            }
        ],
        example: {
            folha12: 180000,
            rbt12: 600000,
            receitaMes: 50000
        },
        validate(values) {
            if (values.rbt12 <= 0) return 'Informe a receita bruta dos últimos 12 meses.';
            if (values.folha12 < 0) return 'A folha não pode ser negativa.';
            return '';
        },
        compute(values) {
            const CORTE = 0.28;
            const fatorR = values.rbt12 > 0 ? values.folha12 / values.rbt12 : 0;
            const atingiu = fatorR >= CORTE;
            const anexo = atingiu ? 'III' : 'V';

            const simIII = H.calcularAliquotaEfetivaSimples('III', values.rbt12);
            const simV = H.calcularAliquotaEfetivaSimples('V', values.rbt12);

            const dasIII = values.receitaMes * simIII.aliquotaEfetiva;
            const dasV = values.receitaMes * simV.aliquotaEfetiva;
            const dasAtual = atingiu ? dasIII : dasV;
            const diferencaMes = Math.max(0, dasV - dasIII);

            /* Folha necessária para alcançar os 28% mantendo a mesma receita. */
            const folhaAlvo = values.rbt12 * CORTE;
            const folhaFaltante = Math.max(0, folhaAlvo - values.folha12);

            const leitura = atingiu
                ? 'Fator R de ' + H.formatPercent(fatorR * 100) + ': a empresa alcança o corte de 28% e tende ao Anexo III, de carga menor.'
                : 'Fator R de ' + H.formatPercent(fatorR * 100) + ': abaixo do corte de 28%, a tributação tende ao Anexo V.';

            const caminho = atingiu
                ? 'Mantenha o acompanhamento mensal: uma queda na folha ou um salto na receita pode derrubar o Fator R e mudar o anexo.'
                : 'Faltam ' + H.formatCurrency(folhaFaltante) + ' de folha nos 12 meses para alcançar o corte. Avaliar pró-labore e contratações pode mudar o enquadramento — mas a decisão precisa considerar o custo dos encargos.';

            return {
                highlight: H.metricPercent('Fator R', fatorR * 100),
                secondaryA: H.metricText('Anexo indicado', 'Anexo ' + anexo),
                secondaryB: H.metricCurrency('DAS estimado no mês', dasAtual),
                notes: [
                    { label: 'Situação', metric: H.metricText('Leitura', leitura) },
                    { label: 'Diferença entre Anexo V e III no mês', metric: H.metricCurrency('Diferença', diferencaMes) },
                    { label: 'Diferença projetada em 12 meses', metric: H.metricCurrency('Diferença', diferencaMes * 12) },
                    { label: 'Próximo passo', metric: H.metricText('Caminho', caminho) }
                ],
                steps: [
                    'Divisão da folha de 12 meses pela receita bruta de 12 meses.',
                    'Comparação do resultado com o corte de 28% da LC 123/2006.',
                    'Estimativa do DAS nos Anexos III e V para medir o impacto.'
                ],
                details: [
                    { label: 'Folha de 12 meses', value: H.formatCurrency(values.folha12) },
                    { label: 'Receita bruta de 12 meses', value: H.formatCurrency(values.rbt12) },
                    { label: 'Folha necessária para 28%', value: H.formatCurrency(folhaAlvo) },
                    { label: 'Alíquota efetiva no Anexo III', value: H.formatPercent(simIII.aliquotaEfetiva * 100) },
                    { label: 'Alíquota efetiva no Anexo V', value: H.formatPercent(simV.aliquotaEfetiva * 100) },
                    { label: 'DAS no Anexo III', value: H.formatCurrency(dasIII) },
                    { label: 'DAS no Anexo V', value: H.formatCurrency(dasV) }
                ],
                chart: {
                    labels: ['DAS no Anexo III', 'DAS no Anexo V'],
                    values: [H.round2(dasIII), H.round2(dasV)],
                    colors: ['#0f766e', '#d46d13']
                }
            };
        }
    });

    /* ----------------------------------------------------------------
       Simples híbrido — IBS/CBS por fora do DAS.

       A LC 214/2025 permite que a empresa continue no Simples para os
       demais tributos e apure IBS/CBS pelo regime regular. A opção é
       feita entre 1º e 30 de setembro de 2026, com efeito em 2027.

       Por que a conta importa: quem permanece 100% no DAS transfere ao
       cliente um crédito de IBS/CBS limitado à parcela desses tributos
       embutida no próprio DAS. No regime regular, o cliente credita a
       alíquota cheia. Para quem vende B2B, essa diferença vira desconto
       exigido pelo comprador — ou perda do contrato.

       Os percentuais de repartição e a alíquota de referência são
       ESTIMATIVAS e ficam ajustáveis: a regulamentação ainda está em
       construção e as alíquotas definitivas só valem a partir de 2033.
       ---------------------------------------------------------------- */

    /* Parcela aproximada do DAS que corresponde aos tributos substituídos
       por IBS/CBS (ISS/ICMS + PIS/Cofins), conforme a repartição dos
       anexos da LC 123/2006. Varia por faixa; aqui é uma média do anexo. */
    const PARCELA_IBSCBS_NO_DAS = { I: 0.46, II: 0.44, III: 0.47, IV: 0.62, V: 0.30 };

    suite.registerDefinition('simples-hibrido-ibs-cbs', {
        pageTitle: 'Simples híbrido: vale apurar IBS e CBS por fora?',
        pageDescription: 'Compare permanecer 100% no DAS com apurar IBS/CBS pelo regime regular. A opção vai de 1º a 30 de setembro de 2026 e vale a partir de 2027.',
        badges: ['Reforma tributária', 'Prazo: setembro/2026', 'Estimativa'],
        calculateLabel: 'Comparar os dois regimes',
        fields: [
            {
                id: 'receitaMes',
                type: 'number',
                label: 'Faturamento mensal',
                placeholder: 'R$ 0,00',
                min: 0,
                step: '0.01'
            },
            {
                id: 'rbt12',
                type: 'number',
                label: 'Receita bruta dos últimos 12 meses (RBT12)',
                placeholder: 'R$ 0,00',
                min: 0,
                step: '0.01'
            },
            {
                id: 'anexo',
                type: 'select',
                label: 'Anexo do Simples',
                options: [
                    { value: 'I', label: 'Anexo I - Comércio' },
                    { value: 'II', label: 'Anexo II - Indústria' },
                    { value: 'III', label: 'Anexo III - Serviços' },
                    { value: 'IV', label: 'Anexo IV - Serviços específicos' },
                    { value: 'V', label: 'Anexo V - Serviços intelectuais' }
                ]
            },
            {
                id: 'percentualB2B',
                type: 'number',
                label: 'Quanto do faturamento vem de clientes empresa (%)',
                placeholder: '0 a 100',
                min: 0,
                max: 100,
                step: '1',
                help: 'Considere só clientes do regime regular, que aproveitam crédito. Venda para consumidor final não entra.'
            },
            {
                id: 'comprasCreditaveis',
                type: 'number',
                label: 'Compras mensais de fornecedores do regime regular',
                placeholder: 'R$ 0,00',
                min: 0,
                step: '0.01',
                help: 'Insumos, mercadorias e serviços que gerariam crédito de IBS/CBS.'
            },
            {
                id: 'aliquotaReferencia',
                type: 'number',
                label: 'Alíquota de referência IBS + CBS (%)',
                placeholder: '26,5',
                min: 0,
                max: 40,
                step: '0.1',
                help: 'Estimativa oficial para o regime pleno. Ajuste conforme sua atividade e a regulamentação vigente.'
            }
        ],
        example: {
            receitaMes: 50000,
            rbt12: 600000,
            anexo: 'III',
            percentualB2B: 80,
            comprasCreditaveis: 6000,
            aliquotaReferencia: 26.5
        },
        validate(values) {
            if (values.receitaMes <= 0) return 'Informe o faturamento mensal.';
            if (values.rbt12 <= 0) return 'Informe a receita bruta dos últimos 12 meses.';
            if (values.percentualB2B < 0 || values.percentualB2B > 100) return 'O percentual de clientes empresa deve ficar entre 0 e 100.';
            return '';
        },
        compute(values) {
            const aliq = (values.aliquotaReferencia > 0 ? values.aliquotaReferencia : 26.5) / 100;
            const fatiaB2B = H.clamp(values.percentualB2B, 0, 100) / 100;
            const receitaB2B = values.receitaMes * fatiaB2B;
            const parcelaNoDAS = PARCELA_IBSCBS_NO_DAS[values.anexo] || 0.45;

            /* Cenário A — permanecer 100% no DAS */
            const simples = H.calcularAliquotaEfetivaSimples(values.anexo, values.rbt12);
            const dasAtual = values.receitaMes * simples.aliquotaEfetiva;
            const ibsCbsNoDAS = dasAtual * parcelaNoDAS;
            /* Crédito repassado ao cliente é limitado ao que foi pago no DAS,
               proporcional à fatia B2B do faturamento. */
            const creditoClienteHoje = ibsCbsNoDAS * fatiaB2B;

            /* Cenário B — regime híbrido */
            const dasReduzido = dasAtual - ibsCbsNoDAS;
            const debitoIBSCBS = values.receitaMes * aliq;
            const creditoCompras = values.comprasCreditaveis * aliq;
            const ibsCbsLiquido = Math.max(0, debitoIBSCBS - creditoCompras);
            const custoHibrido = dasReduzido + ibsCbsLiquido;
            const creditoClienteHibrido = receitaB2B * aliq;

            /* A diferença de crédito é o que o cliente empresa deixa de
               aproveitar hoje — na prática, poder de barganha contra você. */
            const lacunaCredito = Math.max(0, creditoClienteHibrido - creditoClienteHoje);
            const custoAdicional = custoHibrido - dasAtual;
            const saldo = lacunaCredito - custoAdicional;

            let veredito;
            if (fatiaB2B === 0) {
                veredito = 'Seu faturamento é de consumidor final, que não aproveita crédito. Nesse perfil, permanecer 100% no DAS costuma ser o caminho mais simples e mais barato.';
            } else if (saldo > 0) {
                veredito = 'O crédito que seus clientes empresa deixam de aproveitar hoje (' + H.formatCurrency(lacunaCredito) + '/mês) supera o custo estimado de migrar (' + H.formatCurrency(Math.max(0, custoAdicional)) + '/mês). O regime híbrido tende a valer a pena — leve a simulação para análise antes de setembro.';
            } else {
                veredito = 'O custo estimado de migrar (' + H.formatCurrency(Math.max(0, custoAdicional)) + '/mês) supera o crédito adicional gerado ao cliente (' + H.formatCurrency(lacunaCredito) + '/mês). Permanecer no DAS unificado tende a ser melhor, salvo exigência contratual de crédito cheio.';
            }

            return {
                highlight: H.metricCurrency('Diferença mensal a favor do híbrido', saldo),
                secondaryA: H.metricCurrency('Custo hoje (DAS unificado)', dasAtual),
                secondaryB: H.metricCurrency('Custo estimado no híbrido', custoHibrido),
                notes: [
                    { label: 'Leitura', metric: H.metricText('Veredito', veredito) },
                    { label: 'Crédito que o cliente aproveita hoje', metric: H.metricCurrency('Crédito', creditoClienteHoje) },
                    { label: 'Crédito que o cliente aproveitaria no híbrido', metric: H.metricCurrency('Crédito', creditoClienteHibrido) },
                    { label: 'Prazo da opção', metric: H.metricText('Prazo', 'De 1º a 30 de setembro de 2026, com efeito a partir de janeiro de 2027.') }
                ],
                steps: [
                    'Apuração do DAS atual e da parcela de IBS/CBS embutida nele.',
                    'Simulação do regime híbrido: DAS reduzido + IBS/CBS por débito e crédito.',
                    'Comparação entre o custo adicional e o crédito gerado ao cliente empresa.'
                ],
                details: [
                    { label: 'Faturamento para clientes empresa', value: H.formatCurrency(receitaB2B) },
                    { label: 'Alíquota efetiva do Simples', value: H.formatPercent(simples.aliquotaEfetiva * 100) },
                    { label: 'Parcela de IBS/CBS dentro do DAS (estimada)', value: H.formatPercent(parcelaNoDAS * 100) },
                    { label: 'DAS reduzido no híbrido', value: H.formatCurrency(dasReduzido) },
                    { label: 'Débito de IBS/CBS', value: H.formatCurrency(debitoIBSCBS) },
                    { label: 'Crédito sobre compras', value: H.formatCurrency(creditoCompras) },
                    { label: 'IBS/CBS líquido a recolher', value: H.formatCurrency(ibsCbsLiquido) },
                    { label: 'Custo adicional mensal do híbrido', value: H.formatCurrency(custoAdicional) }
                ],
                chart: {
                    labels: ['DAS unificado', 'Regime híbrido'],
                    values: [H.round2(dasAtual), H.round2(custoHibrido)],
                    colors: ['#0f766e', '#d46d13']
                }
            };
        }
    });
})();
