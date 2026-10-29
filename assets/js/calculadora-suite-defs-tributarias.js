(function () {
    const suite = window.CalculadoraSuite || {};
    const H = suite.helpers;
    if (!suite.registerDefinition || !H) return;

    suite.registerDefinition('simples-nacional', {
        pageTitle: 'Simulador de Simples Nacional por Faturamento',
        pageDescription: 'Estime alíquota efetiva e DAS mensal com base no faturamento e anexo do Simples Nacional.',
        badges: ['Tributário', 'DAS mensal', 'Comparativo rápido'],
        calculateLabel: 'Calcular Simples Nacional',
        fields: [
            {
                id: 'rbt12',
                type: 'number',
                label: 'Faturamento acumulado em 12 meses (RBT12)',
                placeholder: 'R$ 0,00',
                min: 0,
                step: '0.01',
                help: 'Use o acumulado real dos últimos 12 meses.'
            },
            {
                id: 'receitaMes',
                type: 'number',
                label: 'Faturamento do mês atual',
                placeholder: 'R$ 0,00',
                min: 0,
                step: '0.01'
            },
            {
                id: 'anexo',
                type: 'select',
                label: 'Anexo principal',
                options: [
                    { value: 'I', label: 'Anexo I - Comércio' },
                    { value: 'II', label: 'Anexo II - Indústria' },
                    { value: 'III', label: 'Anexo III - Serviços' },
                    { value: 'IV', label: 'Anexo IV - Serviços específicos' },
                    { value: 'V', label: 'Anexo V - Serviços intelectuais' }
                ]
            },
            {
                id: 'folha12',
                type: 'number',
                label: 'Folha dos últimos 12 meses (opcional)',
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
            if (values.receitaMes <= 0) return 'Informe o faturamento do mês para estimar o DAS.';
            return '';
        },
        compute(values) {
            const simples = H.calcularAliquotaEfetivaSimples(values.anexo, values.rbt12);
            const dasMes = values.receitaMes * simples.aliquotaEfetiva;
            const cargaAnual = dasMes * 12;
            const receitaPosDAS = Math.max(0, values.receitaMes - dasMes);
            const fatorR = values.folha12 > 0 ? (values.folha12 / values.rbt12) : 0;
            const leituraFatorR = values.folha12 > 0
                ? (fatorR >= 0.28 ? 'Fator R acima de 28%: tende a favorecer anexo III.' : 'Fator R abaixo de 28%: revisar enquadramento de serviços.')
                : 'Informe a folha anual para analisar Fator R.';
            const anexoSugerido = values.folha12 > 0 && (values.anexo === 'III' || values.anexo === 'V')
                ? (fatorR >= 0.28 ? 'III' : 'V')
                : values.anexo;
            const simulacaoSugerida = H.calcularAliquotaEfetivaSimples(anexoSugerido, values.rbt12);
            const diferencaPotencialMes = values.receitaMes * (simples.aliquotaEfetiva - simulacaoSugerida.aliquotaEfetiva);

            return {
                highlight: H.metricCurrency('DAS estimado no mês', dasMes),
                secondaryA: H.metricPercent('Alíquota efetiva', simples.aliquotaEfetiva * 100),
                secondaryB: H.metricCurrency('Carga anual estimada', cargaAnual),
                notes: [
                    { label: 'Faixa aplicada', metric: H.metricText('Faixa', `Até ${H.formatCurrency(simples.faixa.limite)} | nominal ${H.formatPercent(simples.faixa.aliquota * 100)}`) },
                    { label: 'Parcela a deduzir', metric: H.metricCurrency('Parcela', simples.faixa.deducao) },
                    { label: 'Fator R', metric: H.metricText('Leitura', leituraFatorR) },
                    { label: 'Potencial mensal com anexo sugerido', metric: H.metricCurrency('Diferenca', diferencaPotencialMes) }
                ],
                steps: [
                    `Classificação por faixa do anexo ${values.anexo}.`,
                    'Cálculo da alíquota efetiva com parcela a deduzir.',
                    'Estimativa do DAS mensal e impacto anual.'
                ],
                details: [
                    { label: 'Receita do mês', value: H.formatCurrency(values.receitaMes) },
                    { label: 'Receita líquida após DAS', value: H.formatCurrency(receitaPosDAS) },
                    { label: 'Alíquota nominal da faixa', value: H.formatPercent(simples.faixa.aliquota * 100) },
                    { label: 'Alíquota efetiva usada', value: H.formatPercent(simples.aliquotaEfetiva * 100) },
                    { label: 'Anexo sugerido pelo Fator R', value: anexoSugerido }
                ],
                chart: {
                    labels: ['DAS estimado', 'Receita após DAS'],
                    values: [H.round2(dasMes), H.round2(receitaPosDAS)],
                    colors: ['#d98c5f', '#4f8f7a']
                }
            };
        }
    });

    suite.registerDefinition('inss-irrf-estimado', {
        pageTitle: 'Simulador de INSS e IRRF Estimado',
        pageDescription: 'Calcule descontos previdenciários e imposto de renda retido na fonte com parâmetros mensais.',
        badges: ['Folha', 'INSS', 'IRRF'],
        calculateLabel: 'Calcular INSS e IRRF',
        fields: [
            { id: 'rendimentoBruto', type: 'number', label: 'Rendimento bruto mensal', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'dependentes', type: 'number', label: 'Dependentes para IRRF', min: 0, step: '1' },
            { id: 'pensao', type: 'number', label: 'Pensão alimentícia dedutível', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'outrasDeducoes', type: 'number', label: 'Outras deduções legais', placeholder: 'R$ 0,00', min: 0, step: '0.01' }
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
                highlight: H.metricCurrency('Líquido estimado', mensal.liquido),
                secondaryA: H.metricCurrency('INSS estimado', mensal.inss),
                secondaryB: H.metricCurrency('IRRF estimado', mensal.irrf.impostoFinal),
                notes: [
                    { label: 'Base de cálculo IRRF', metric: H.metricCurrency('Base', mensal.baseIRRF) },
                    { label: 'Redução legal aplicada', metric: H.metricCurrency('Redução', mensal.irrf.reducao) },
                    { label: 'Dedução considerada', metric: H.metricCurrency('Dedução', mensal.deducaoAplicada) }
                ],
                steps: [
                    'Cálculo do INSS progressivo por faixas.',
                    'Comparação entre deduções legais e desconto simplificado.',
                    'Aplicação da tabela de IRRF e exibição do líquido.'
                ],
                details: [
                    { label: 'Rendimento bruto', value: H.formatCurrency(values.rendimentoBruto) },
                    { label: 'Dependentes', value: `${values.dependentes} dependente(s)` },
                    { label: 'Pensão dedutível', value: H.formatCurrency(values.pensao) },
                    { label: 'Outras deduções', value: H.formatCurrency(values.outrasDeducoes) }
                ],
                chart: {
                    labels: ['Liquido', 'INSS', 'IRRF', 'Outras deduções'],
                    values: [
                        H.round2(Math.max(0, mensal.liquido)),
                        H.round2(mensal.inss),
                        H.round2(mensal.irrf.impostoFinal),
                        H.round2(values.pensao + values.outrasDeducoes)
                    ],
                    colors: ['#4f8f7a', '#c8a86b', '#d98c5f', '#7d93a8']
                }
            };
        }
    });

    suite.registerDefinition('limite-mei', {
        pageTitle: 'Calculadora de Limite MEI e Projeção',
        pageDescription: 'Projete o faturamento anual do MEI e identifique risco de desenquadramento com antecedência.',
        badges: ['MEI', 'Limite anual', 'Projeção'],
        calculateLabel: 'Calcular limite MEI',
        fields: [
            { id: 'faturamentoAcumulado', type: 'number', label: 'Faturamento acumulado no ano', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            {
                id: 'mesesDecorridos',
                type: 'select',
                label: 'Meses já encerrados no ano',
                options: [
                    { value: '1', label: '1 mês' }, { value: '2', label: '2 meses' }, { value: '3', label: '3 meses' },
                    { value: '4', label: '4 meses' }, { value: '5', label: '5 meses' }, { value: '6', label: '6 meses' },
                    { value: '7', label: '7 meses' }, { value: '8', label: '8 meses' }, { value: '9', label: '9 meses' },
                    { value: '10', label: '10 meses' }, { value: '11', label: '11 meses' }, { value: '12', label: '12 meses' }
                ]
            },
            { id: 'mediaMensal', type: 'number', label: 'Projeção de faturamento mensal para os próximos meses', placeholder: 'R$ 0,00', min: 0, step: '0.01' }
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
            const limiteAnual = 81000;
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
                status = 'Excesso de até 20% do limite. Planeje migração para evitar surpresa.';
            }

            return {
                highlight: H.metricCurrency('Projeção anual', projecaoAnual),
                secondaryA: H.metricCurrency('Limite anual MEI', limiteAnual),
                secondaryB: H.metricCurrency('Excesso projetado', excessoProjetado),
                notes: [
                    { label: 'Status', metric: H.metricText('Status', status) },
                    { label: 'Limite proporcional no ano', metric: H.metricCurrency('Proporcional', limiteProporcional) },
                    { label: 'Excesso percentual', metric: H.metricPercent('Excesso', Math.max(0, excessoPercentual)) }
                ],
                steps: [
                    'Cálculo do limite proporcional conforme meses decorridos.',
                    'Projeção do faturamento restante até dezembro.',
                    'Classificação de risco de desenquadramento.'
                ],
                details: [
                    { label: 'Faturamento acumulado', value: H.formatCurrency(values.faturamentoAcumulado) },
                    { label: 'Meses restantes', value: `${mesesRestantes} mês(es)` },
                    { label: 'Média mensal projetada', value: H.formatCurrency(values.mediaMensal) },
                    { label: 'Faixa de alerta 20%', value: H.formatCurrency(97200) }
                ],
                chart: {
                    labels: ['Projeção anual', 'Limite MEI'],
                    values: [H.round2(projecaoAnual), limiteAnual],
                    colors: ['#c8a86b', '#d98c5f']
                }
            };
        }
    });

    suite.registerDefinition('mei-vs-simples', {
        pageTitle: 'Comparador MEI x Simples Nacional',
        pageDescription: 'Compare custo tributário estimado entre MEI e Simples Nacional para apoiar seu enquadramento.',
        badges: ['Comparativo', 'MEI', 'Simples'],
        calculateLabel: 'Comparar regimes',
        fields: [
            { id: 'faturamentoMensal', type: 'number', label: 'Faturamento médio mensal', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            {
                id: 'atividade',
                type: 'select',
                label: 'Tipo principal de atividade',
                options: [
                    { value: 'comercio', label: 'Comércio' },
                    { value: 'servico', label: 'Serviço' },
                    { value: 'misto', label: 'Comércio + Serviço' }
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
            const ultrapassaMEI = rbt12 > 81000;
            const regimeMaisEconomico = diferencaMensal > 0 ? 'MEI' : 'Simples';
            const mensagem = ultrapassaMEI
                ? 'Com este faturamento anual projetado, o limite do MEI pode ser ultrapassado.'
                : `No comparativo de tributos, ${regimeMaisEconomico} tende a ser mais econômico.`;

            return {
                highlight: H.metricCurrency(
                    regimeMaisEconomico === 'MEI' ? 'Economia anual no MEI' : 'Economia anual no Simples',
                    economiaAnual
                ),
                secondaryA: H.metricCurrency('Tributo mensal MEI', meiMensal),
                secondaryB: H.metricCurrency('Tributo mensal Simples', simplesMensal),
                notes: [
                    { label: 'Leitura do enquadramento', metric: H.metricText('Status', mensagem) },
                    { label: 'Alíquota efetiva do Simples', metric: H.metricPercent('Aliquota', simples.aliquotaEfetiva * 100) },
                    { label: 'Faturamento anual projetado', metric: H.metricCurrency('RBT12', rbt12) },
                    { label: 'Parcela INSS do MEI', metric: H.metricCurrency('5% do salário mínimo 2026', inssMEI) }
                ],
                steps: [
                    'Estimativa do tributo fixo mensal do MEI.',
                    'Cálculo da alíquota efetiva no Simples pelo RBT12.',
                    'Comparação mensal e anual de custo tributário.'
                ],
                details: [
                    { label: 'Anexo usado no Simples', value: values.anexoSimples },
                    { label: 'Faixa do anexo', value: `Até ${H.formatCurrency(simples.faixa.limite)}` },
                    { label: 'Diferença mensal', value: H.formatCurrency(diferencaMensal) },
                    { label: 'Diferença anual', value: H.formatCurrency(diferencaAnual) }
                ],
                chart: {
                    labels: ['MEI mensal', 'Simples mensal'],
                    values: [H.round2(meiMensal), H.round2(simplesMensal)],
                    colors: ['#4f8f7a', '#c8a86b']
                }
            };
        }
    });

    suite.registerDefinition('simples-vs-lucro-presumido', {
        pageTitle: 'Comparador Simples Nacional x Lucro Presumido',
        pageDescription: 'Compare os principais tributos mensais entre Simples e Lucro Presumido para apoiar o enquadramento.',
        badges: ['Comparativo', 'Tributário', 'Planejamento'],
        calculateLabel: 'Comparar regimes',
        fields: [
            { id: 'faturamentoMensal', type: 'number', label: 'Faturamento médio mensal', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'rbt12', type: 'number', label: 'Faturamento acumulado de 12 meses', placeholder: 'R$ 0,00', min: 0, step: '0.01', help: 'Se não tiver, use 12x o faturamento médio.' },
            { id: 'atividade', type: 'select', label: 'Atividade predominante', options: H.atividadePresumidoOptions() },
            {
                id: 'anexoSimples',
                type: 'select',
                label: 'Anexo estimado no Simples',
                options: [
                    { value: 'I', label: 'Anexo I - Comércio' },
                    { value: 'II', label: 'Anexo II - Indústria' },
                    { value: 'III', label: 'Anexo III - Serviços' },
                    { value: 'IV', label: 'Anexo IV - Serviços específicos' },
                    { value: 'V', label: 'Anexo V - Serviços intelectuais' }
                ]
            },
            { id: 'folhaMensal', type: 'number', label: 'Folha mensal estimada', placeholder: 'R$ 0,00', min: 0, step: '0.01', help: 'Usada para estimar CPP fora do DAS no Anexo IV e no Presumido.' },
            { id: 'aliquotaLocal', type: 'number', label: 'ISS ou ICMS adicional no Presumido (%)', min: 0, max: 10, step: '0.1', help: 'Opcional. Use apenas se quiser incluir tributo local na simulação do Presumido.' }
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
            if (values.faturamentoMensal <= 0) return 'Informe o faturamento médio mensal.';
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
                    { label: 'Alíquota efetiva do Simples', metric: H.metricPercent('Aliquota', simples.aliquotaEfetiva * 100) },
                    { label: 'Diferença em pontos sobre a receita', metric: H.metricPercent('Diferenca', diferencaPontos) },
                    { label: 'Leitura', metric: H.metricText('Regime mais leve', `${regimeMaisLeve} tende a gerar menor carga principal nesta simulação.`) }
                ],
                steps: [
                    'Estimativa do DAS pelo RBT12 e anexo informado.',
                    'Apuração do Lucro Presumido com IRPJ, CSLL, PIS/Cofins e tributo local.',
                    'Comparação mensal e anual entre os dois regimes.'
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
                    colors: ['#4f8f7a', '#d98c5f']
                }
            };
        }
    });

    suite.registerDefinition('pro-labore-liquido', {
        pageTitle: 'Calculadora de Pró-labore Líquido',
        pageDescription: 'Estime o líquido do pró-labore do sócio, o INSS retido, o IRRF e o custo total para a empresa.',
        badges: ['Sócios', 'Pró-labore', 'Retirada'],
        calculateLabel: 'Calcular pró-labore',
        fields: [
            { id: 'proLaboreBruto', type: 'number', label: 'Pró-labore bruto mensal', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'regimeEmpresa', type: 'select', label: 'Regime da empresa para CPP patronal', options: H.regimeProLaboreOptions() },
            { id: 'dependentes', type: 'number', label: 'Dependentes para IRRF', min: 0, step: '1' },
            { id: 'pensao', type: 'number', label: 'Pensão alimentícia dedutível', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'outrasDeducoes', type: 'number', label: 'Outras deduções mensais', placeholder: 'R$ 0,00', min: 0, step: '0.01' }
        ],
        example: {
            proLaboreBruto: 8000,
            regimeEmpresa: 'presumido_real',
            dependentes: 1,
            pensao: 0,
            outrasDeducoes: 0
        },
        validate(values) {
            if (values.proLaboreBruto <= 0) return 'Informe o pró-labore bruto mensal.';
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
                highlight: H.metricCurrency('Pró-labore líquido mensal', proLabore.liquido),
                secondaryA: H.metricCurrency('Custo total da empresa', custoEmpresa),
                secondaryB: H.metricCurrency('Retirada líquida anual', proLabore.liquido * 12),
                notes: [
                    { label: 'INSS do sócio', metric: H.metricCurrency('11% sobre o pró-labore até o teto', proLabore.inssSocio) },
                    { label: 'IRRF estimado', metric: H.metricCurrency('IRRF', proLabore.irrf.impostoFinal) },
                    { label: 'Carga total mensal', metric: H.metricCurrency('Carga total', cargaTotal) }
                ],
                steps: [
                    'Retenção previdenciária do sócio sobre o pró-labore.',
                    'Cálculo da base mensal de IRRF com dependentes e deduções.',
                    'Soma do custo patronal quando o regime exige CPP fora do DAS.'
                ],
                details: [
                    { label: 'Base mensal de IRRF', value: H.formatCurrency(proLabore.baseIRRF) },
                    { label: 'CPP patronal estimada', value: H.formatCurrency(cppPatronal) },
                    { label: 'Dedução aplicada no IRRF', value: H.formatCurrency(proLabore.deducaoAplicada) },
                    { label: 'Líquido anual estimado', value: H.formatCurrency(proLabore.liquido * 12) }
                ],
                chart: {
                    labels: ['Líquido do sócio', 'INSS sócio', 'IRRF', 'CPP patronal'],
                    values: [
                        H.round2(proLabore.liquido),
                        H.round2(proLabore.inssSocio),
                        H.round2(proLabore.irrf.impostoFinal),
                        H.round2(cppPatronal)
                    ],
                    colors: ['#4f8f7a', '#c8a86b', '#d98c5f', '#7d93a8']
                }
            };
        }
    });

    suite.registerDefinition('distribuicao-lucros', {
        pageTitle: 'Calculadora de Distribuição de Lucros Disponível',
        pageDescription: 'Projete o lucro distribuível do mês, a parcela do sócio e a retenção de 10% de IR sobre dividendos acima de R$ 50 mil por mês (Lei 15.270/2025).',
        badges: ['Sócios', 'Lucros', 'IR sobre dividendos'],
        calculateLabel: 'Calcular distribuição',
        fields: [
            { id: 'faturamentoMensal', type: 'number', label: 'Faturamento do mês', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'custosMensais', type: 'number', label: 'Custos operacionais + pró-labore', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'tributosMensais', type: 'number', label: 'Tributos do mês', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'reservaPercentual', type: 'range', label: 'Percentual para reserva de caixa', min: 0, max: 40, step: 1, value: 15, outputSuffix: '%' },
            { id: 'participacaoSocio', type: 'range', label: 'Participação do sócio nos lucros', min: 1, max: 100, step: 1, value: 100, outputSuffix: '%' },
            {
                id: 'origemLucro',
                type: 'select',
                label: 'De quando são esses lucros?',
                options: [
                    { value: 'novo', label: 'Resultado de 2026 em diante' },
                    { value: 'transicao', label: 'Lucros até 2025, com distribuição aprovada até 31/12/2025' }
                ],
                help: 'Lucros apurados até 2025 e aprovados até 31/12/2025 seguem a regra de transição, sem a retenção.'
            },
            {
                id: 'outrosLucrosMes',
                type: 'number',
                label: 'Outros lucros pagos a esse sócio pela empresa no mesmo mês (opcional)',
                placeholder: 'R$ 0,00',
                min: 0,
                step: '0.01',
                help: 'O limite de R$ 50 mil considera tudo o que a empresa paga ao sócio no mês.'
            }
        ],
        example: {
            faturamentoMensal: 120000,
            custosMensais: 63000,
            tributosMensais: 9800,
            reservaPercentual: 15,
            participacaoSocio: 50,
            origemLucro: 'novo',
            outrosLucrosMes: 0
        },
        validate(values) {
            if (values.faturamentoMensal <= 0) return 'Informe o faturamento do mês.';
            return '';
        },
        compute(values) {
            const lucroAntesReserva = values.faturamentoMensal - values.custosMensais - values.tributosMensais;
            const reserva = lucroAntesReserva > 0 ? (lucroAntesReserva * (H.clamp(values.reservaPercentual, 0, 40) / 100)) : 0;
            const lucroDistribuivel = Math.max(0, lucroAntesReserva - reserva);
            const parcelaSocio = lucroDistribuivel * (H.clamp(values.participacaoSocio, 1, 100) / 100);
            const margemLiquida = values.faturamentoMensal > 0 ? (lucroAntesReserva / values.faturamentoMensal) * 100 : 0;
            const outrosLucros = Math.max(0, values.outrosLucrosMes || 0);
            const totalPagoMes = parcelaSocio + outrosLucros;
            const retencao = H.calcularRetencaoDividendos(totalPagoMes, values.origemLucro);
            const limite = H.config.dividendos.limiteMensal;
            const percentual = `${Math.round(H.config.dividendos.aliquotaRetencao * 100)}%`;

            let leituraRetencao;
            if (values.origemLucro === 'transicao') {
                leituraRetencao = 'Regra de transição: lucros até 2025 aprovados até 31/12/2025 não têm a retenção de 10%. Guarde a ata ou o documento de aprovação.';
            } else if (retencao.sujeito) {
                leituraRetencao = `O total do mês passa de ${H.formatCurrency(limite)}: a empresa retém ${percentual} sobre o valor total pago. O valor retido pode ser compensado na declaração anual do sócio.`;
            } else {
                leituraRetencao = `Até ${H.formatCurrency(limite)} por mês da mesma empresa não há retenção na fonte. Rendas altas no ano ainda podem entrar no imposto mínimo da declaração anual.`;
            }

            return {
                highlight: H.metricCurrency('Valor líquido estimado para o sócio no mês', retencao.liquido),
                secondaryA: H.metricCurrency(`IR retido na fonte (${percentual})`, retencao.retencao),
                secondaryB: H.metricCurrency('Lucro distribuível total', lucroDistribuivel),
                notes: [
                    { label: 'Parcela do sócio (antes do IR)', metric: H.metricCurrency('Parcela', parcelaSocio) },
                    { label: 'Total pago ao sócio no mês', metric: H.metricCurrency('Total', totalPagoMes) },
                    { label: 'Reserva mensal sugerida', metric: H.metricCurrency('Reserva', reserva) },
                    { label: 'Margem líquida após tributos', metric: H.metricPercent('Margem', margemLiquida) },
                    { label: 'IR sobre dividendos', metric: H.metricText('Leitura', leituraRetencao) }
                ],
                steps: [
                    'Subtração de custos e tributos sobre a receita do mês.',
                    'Separação de uma reserva mínima para capital de giro.',
                    'Rateio da parcela distribuível conforme a participação do sócio.',
                    `Retenção de ${percentual} quando o total pago ao sócio no mês passa de ${H.formatCurrency(limite)}.`
                ],
                details: [
                    { label: 'Receita anualizada', value: H.formatCurrency(values.faturamentoMensal * 12) },
                    { label: 'Lucro distribuível anual', value: H.formatCurrency(lucroDistribuivel * 12) },
                    { label: 'Participação do sócio', value: H.formatPercent(values.participacaoSocio) },
                    { label: 'Retenção anual estimada', value: H.formatCurrency(retencao.retencao * 12) },
                    { label: 'Valor líquido anual do sócio', value: H.formatCurrency(retencao.liquido * 12) }
                ],
                chart: {
                    labels: ['Custos + pró-labore', 'Tributos', 'Reserva', 'Lucro distribuível'],
                    values: [
                        H.round2(values.custosMensais),
                        H.round2(values.tributosMensais),
                        H.round2(reserva),
                        H.round2(lucroDistribuivel)
                    ],
                    colors: ['#7d93a8', '#d98c5f', '#c8a86b', '#4f8f7a']
                }
            };
        }
    });
    suite.registerDefinition('fator-r', {
        pageTitle: 'Calculadora de Fator R: Anexo III ou Anexo V',
        pageDescription: 'Veja se sua empresa de serviços fica no Anexo III ou no V do Simples Nacional e quanto de pró-labore faltaria para chegar aos 28%.',
        badges: ['Simples Nacional', 'Fator R', 'Pró-labore'],
        calculateLabel: 'Calcular Fator R',
        fields: [
            {
                id: 'rbt12',
                type: 'number',
                label: 'Faturamento dos últimos 12 meses (RBT12)',
                placeholder: 'R$ 0,00',
                min: 0,
                step: '0.01'
            },
            {
                id: 'receitaMes',
                type: 'number',
                label: 'Faturamento do mês',
                placeholder: 'R$ 0,00',
                min: 0,
                step: '0.01'
            },
            {
                id: 'folha12',
                type: 'number',
                label: 'Folha dos últimos 12 meses',
                placeholder: 'R$ 0,00',
                min: 0,
                step: '0.01',
                help: 'Some salários, pró-labore, 13º, férias, FGTS e INSS patronal pagos nos últimos 12 meses.'
            },
            {
                id: 'proLaboreAtual',
                type: 'number',
                label: 'Pró-labore mensal atual do sócio',
                placeholder: 'R$ 0,00',
                min: 0,
                step: '0.01',
                help: 'Usado para estimar o INSS e o IRRF de um pró-labore maior.'
            }
        ],
        example: {
            rbt12: 600000,
            receitaMes: 50000,
            folha12: 96000,
            proLaboreAtual: 3000
        },
        validate(values) {
            if (values.rbt12 <= 0) return 'Informe o faturamento dos últimos 12 meses.';
            if (values.receitaMes <= 0) return 'Informe o faturamento do mês.';
            return '';
        },
        compute(values) {
            const minimo = H.config.fatorRMinimo;
            const fatorR = values.rbt12 > 0 ? values.folha12 / values.rbt12 : 0;
            const noAnexoIII = fatorR >= minimo;
            const aliquotaIII = H.calcularAliquotaEfetivaSimples('III', values.rbt12).aliquotaEfetiva;
            const aliquotaV = H.calcularAliquotaEfetivaSimples('V', values.rbt12).aliquotaEfetiva;
            const dasIII = values.receitaMes * aliquotaIII;
            const dasV = values.receitaMes * aliquotaV;

            // Pró-labore extra por mês, mantido por 12 meses, para a folha chegar a 28% do RBT12.
            const folhaNecessaria = values.rbt12 * minimo;
            const faltaAnual = Math.max(0, folhaNecessaria - values.folha12);
            const proLaboreExtra = faltaAnual / 12;

            // No Anexo III a CPP já está no DAS: o custo extra é o INSS e o IRRF do sócio sobre o aumento.
            const atual = H.calcularProLaboreLiquido(values.proLaboreAtual);
            const novo = H.calcularProLaboreLiquido(values.proLaboreAtual + proLaboreExtra);
            const custoExtra = (novo.inssSocio - atual.inssSocio) + (novo.irrf.impostoFinal - atual.irrf.impostoFinal);
            const reducaoDAS = dasV - dasIII;
            const economiaLiquida = reducaoDAS - custoExtra;

            const fatorRPercent = fatorR * 100;
            const minimoPercent = minimo * 100;

            let leitura;
            if (noAnexoIII) {
                const folga = values.folha12 - folhaNecessaria;
                leitura = `Fator R de ${H.formatPercent(fatorRPercent)}: a empresa já fica no Anexo III. A folha está ${H.formatCurrency(folga)} acima do mínimo nos 12 meses; acompanhe mês a mês para não cair abaixo de ${H.formatPercent(minimoPercent)}.`;
            } else if (economiaLiquida > 0) {
                leitura = `Subir o pró-labore em ${H.formatCurrency(proLaboreExtra)} por mês tende a compensar: o DAS cai ${H.formatCurrency(reducaoDAS)} e o INSS e o IRRF extras do sócio somam ${H.formatCurrency(custoExtra)}.`;
            } else {
                leitura = `Neste cenário, o INSS e o IRRF de um pró-labore maior (${H.formatCurrency(custoExtra)}) superam a redução do DAS (${H.formatCurrency(reducaoDAS)}). Vale revisar com o contador.`;
            }

            return {
                highlight: noAnexoIII
                    ? H.metricText('Anexo do Simples', 'Anexo III (Fator R acima de 28%)')
                    : H.metricCurrency('Economia mensal estimada no Anexo III', Math.max(0, economiaLiquida)),
                secondaryA: H.metricPercent('Fator R atual', fatorRPercent),
                secondaryB: H.metricCurrency('Pró-labore extra por mês para chegar a 28%', proLaboreExtra),
                notes: [
                    { label: 'DAS do mês no Anexo III', metric: H.metricCurrency('DAS', dasIII) },
                    { label: 'DAS do mês no Anexo V', metric: H.metricCurrency('DAS', dasV) },
                    { label: 'INSS + IRRF extras do sócio', metric: H.metricCurrency('Custo', noAnexoIII ? 0 : custoExtra) },
                    { label: 'Leitura', metric: H.metricText('Leitura', leitura) }
                ],
                steps: [
                    'Fator R = folha dos últimos 12 meses dividida pelo faturamento dos últimos 12 meses.',
                    `A partir de ${H.formatPercent(minimoPercent)}, a atividade sujeita ao Fator R é tributada no Anexo III; abaixo disso, no Anexo V.`,
                    'Pró-labore extra = (28% do RBT12 menos a folha atual) dividido por 12 meses.',
                    'Custo do aumento = INSS de 11% e IRRF do sócio sobre o pró-labore maior.'
                ],
                details: [
                    { label: 'Alíquota efetiva no Anexo III', value: H.formatPercent(aliquotaIII * 100) },
                    { label: 'Alíquota efetiva no Anexo V', value: H.formatPercent(aliquotaV * 100) },
                    { label: 'Folha mínima em 12 meses (28%)', value: H.formatCurrency(folhaNecessaria) },
                    { label: 'Pró-labore mensal sugerido', value: H.formatCurrency(values.proLaboreAtual + proLaboreExtra) },
                    { label: 'Aviso', value: 'Vale só para atividades do Simples sujeitas ao Fator R. A folha considerada é a dos 12 meses anteriores, então o efeito do aumento é gradual.' }
                ],
                chart: {
                    labels: ['DAS no Anexo III', 'DAS no Anexo V'],
                    values: [H.round2(dasIII), H.round2(dasV)],
                    colors: ['#4f8f7a', '#d98c5f']
                }
            };
        }
    });

    suite.registerDefinition('imposto-minimo-altas-rendas', {
        pageTitle: 'Calculadora do Imposto Mínimo para Altas Rendas (IRPFM)',
        pageDescription: 'Estime se a renda do ano passa de R$ 600 mil e quanto de imposto mínimo pode faltar na declaração, conforme a Lei 15.270/2025.',
        badges: ['IRPF', 'Altas rendas', 'Dividendos'],
        calculateLabel: 'Calcular imposto mínimo',
        fields: [
            { id: 'rendTributaveis', type: 'number', label: 'Rendimentos tributáveis no ano (salário, pró-labore, aluguéis...)', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'dividendos', type: 'number', label: 'Lucros e dividendos recebidos no ano', placeholder: 'R$ 0,00', min: 0, step: '0.01', help: 'Não inclua lucros até 2025 que seguem a regra de transição.' },
            { id: 'outrosRendimentos', type: 'number', label: 'Outros rendimentos isentos ou de tributação exclusiva', placeholder: 'R$ 0,00', min: 0, step: '0.01', help: 'Ex.: aplicações financeiras. Não inclua poupança, ganho de capital, herança/doação, LCI, LCA, CRI, CRA e indenizações, que ficam fora da base.' },
            { id: 'irDevido', type: 'number', label: 'IR devido na declaração pela tabela progressiva', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'irRetidoDividendos', type: 'number', label: 'IR retido de 10% sobre dividendos no ano', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'outroIRPago', type: 'number', label: 'Outro IR já pago sobre os rendimentos da base (fonte ou exclusivo)', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'cargaEmpresa', type: 'number', label: 'Carga efetiva de IRPJ + CSLL da empresa que pagou os dividendos (%) · opcional', min: 0, max: 45, step: '0.1', help: 'IRPJ + CSLL do ano divididos pelo lucro contábil. Usada para o redutor; deixe 0 se não souber.' }
        ],
        example: {
            rendTributaveis: 60000,
            dividendos: 600000,
            outrosRendimentos: 140000,
            irDevido: 6000,
            irRetidoDividendos: 0,
            outroIRPago: 0,
            cargaEmpresa: 0
        },
        validate(values) {
            if ((values.rendTributaveis + values.dividendos + values.outrosRendimentos) <= 0) return 'Informe os rendimentos do ano.';
            return '';
        },
        compute(values) {
            const limiteInicial = 600000;
            const limiteTeto = 1200000;
            const aliquotaPara = (renda) => {
                if (renda <= limiteInicial) return 0;
                if (renda >= limiteTeto) return 0.10;
                return ((renda / 60000) - 10) / 100;
            };

            const renda = values.rendTributaveis + values.dividendos + values.outrosRendimentos;
            const aliquota = aliquotaPara(renda);
            const impostoMinimoBruto = renda * aliquota;

            // Redutor (art. 16-B): quando carga da empresa + alíquota efetiva do mínimo sobre os dividendos passa de 34%.
            const rendaSemDividendos = renda - values.dividendos;
            const acrescimoPorDividendos = impostoMinimoBruto - (rendaSemDividendos * aliquotaPara(rendaSemDividendos));
            const aliquotaEfetivaDividendos = values.dividendos > 0 ? acrescimoPorDividendos / values.dividendos : 0;
            const cargaEmpresa = H.clamp(values.cargaEmpresa, 0, 45) / 100;
            const redutor = cargaEmpresa > 0 && values.dividendos > 0
                ? Math.min(acrescimoPorDividendos, values.dividendos * Math.max(0, (cargaEmpresa + aliquotaEfetivaDividendos) - 0.34))
                : 0;

            const deducoes = values.irDevido + values.irRetidoDividendos + values.outroIRPago + redutor;
            const complemento = Math.max(0, impostoMinimoBruto - deducoes);
            const cargaFinal = renda > 0 ? ((values.irDevido + values.irRetidoDividendos + values.outroIRPago + complemento) / renda) * 100 : 0;

            let leitura;
            if (aliquota === 0) {
                leitura = 'A renda do ano não passa de R$ 600 mil: não há imposto mínimo.';
            } else if (complemento > 0) {
                leitura = `O IR já pago não alcança o mínimo de ${H.formatPercent(aliquota * 100)} da renda. A diferença entra no saldo da declaração anual.`;
            } else {
                leitura = 'O IR já pago e retido cobre o imposto mínimo: não há valor a complementar.';
            }

            return {
                highlight: H.metricCurrency('Imposto mínimo a complementar na declaração', complemento),
                secondaryA: H.metricPercent('Alíquota mínima', aliquota * 100),
                secondaryB: H.metricCurrency('Renda considerada no ano', renda),
                notes: [
                    { label: 'Imposto mínimo antes das deduções', metric: H.metricCurrency('Mínimo', impostoMinimoBruto) },
                    { label: 'IR já pago e retido', metric: H.metricCurrency('Pago', values.irDevido + values.irRetidoDividendos + values.outroIRPago) },
                    { label: 'Redutor sobre dividendos', metric: H.metricCurrency('Redutor', redutor) },
                    { label: 'Carga total de IR sobre a renda', metric: H.metricPercent('Carga', cargaFinal) },
                    { label: 'Leitura', metric: H.metricText('Leitura', leitura) }
                ],
                steps: [
                    'Soma da renda do ano, incluindo dividendos e rendimentos isentos ou exclusivos que entram na base.',
                    'Alíquota de 0% em R$ 600 mil subindo até 10% em R$ 1,2 milhão: (renda / 60.000) - 10.',
                    'Do imposto mínimo saem o IR da tabela, o IR retido sobre dividendos, outros IR já pagos e o redutor.',
                    'Redutor: dividendos x (carga efetiva da empresa + alíquota efetiva do mínimo sobre os dividendos - 34%).'
                ],
                details: [
                    { label: 'Alíquota efetiva do mínimo sobre os dividendos', value: H.formatPercent(aliquotaEfetivaDividendos * 100) },
                    { label: 'Carga efetiva informada da empresa', value: H.formatPercent(cargaEmpresa * 100) },
                    { label: 'Primeira apuração', value: 'Declaração de 2027, sobre a renda de 2026.' },
                    { label: 'Aviso', value: 'Simulação simplificada. O redutor usa 34% (bancos e seguradoras têm percentuais maiores) e depende das demonstrações da empresa. Confirme com o contador.' }
                ],
                chart: {
                    labels: ['IR da tabela', 'IR retido em dividendos', 'Outro IR pago', 'Complemento'],
                    values: [H.round2(values.irDevido), H.round2(values.irRetidoDividendos), H.round2(values.outroIRPago), H.round2(complemento)],
                    colors: ['#7d93a8', '#c8a86b', '#4f8f7a', '#d98c5f']
                }
            };
        }
    });

    suite.registerDefinition('simples-ibs-cbs', {
        pageTitle: 'Simples Nacional 2027: IBS/CBS por dentro ou por fora do DAS',
        pageDescription: 'Compare o imposto da empresa e o crédito que seus clientes aproveitam ao recolher IBS e CBS dentro do DAS ou pelo regime regular, a partir de 2027.',
        badges: ['Reforma tributária', 'Simples Nacional', 'CBS 2027'],
        calculateLabel: 'Comparar opções',
        fields: [
            { id: 'receitaMes', type: 'number', label: 'Faturamento do mês', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'rbt12', type: 'number', label: 'Faturamento dos últimos 12 meses (RBT12)', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            {
                id: 'anexo',
                type: 'select',
                label: 'Anexo do Simples',
                options: [
                    { value: 'III', label: 'Anexo III - Serviços' },
                    { value: 'V', label: 'Anexo V - Serviços intelectuais' },
                    { value: 'IV', label: 'Anexo IV - Serviços específicos' },
                    { value: 'I', label: 'Anexo I - Comércio' },
                    { value: 'II', label: 'Anexo II - Indústria' }
                ]
            },
            { id: 'parteCBSnoDAS', type: 'number', label: 'Parte do DAS que hoje é PIS + Cofins (%)', min: 0, max: 40, step: '0.01', value: 15.6, help: 'Veja a tabela de repartição do seu anexo e faixa. Em 2027 essa parte vira CBS dentro do DAS.' },
            { id: 'vendasEmpresas', type: 'range', label: 'Vendas para empresas que aproveitam crédito', min: 0, max: 100, step: 5, value: 70, outputSuffix: '%' },
            { id: 'comprasComCredito', type: 'number', label: 'Compras e despesas do mês com IBS/CBS a creditar', placeholder: 'R$ 0,00', min: 0, step: '0.01', help: 'Só conta no regime regular (por fora).' },
            { id: 'aliquotaCBS', type: 'number', label: 'Alíquota da CBS (%)', min: 0, max: 20, step: '0.01', value: 11.3, help: 'Referência calculada pelo TCU para 2027. O Senado pode alterar até 15/12/2026.' },
            { id: 'aliquotaIBS', type: 'number', label: 'Alíquota do IBS (%)', min: 0, max: 20, step: '0.01', value: 0.1, help: 'Em 2027 o IBS ainda está na fase de teste (0,1%).' }
        ],
        example: {
            receitaMes: 60000,
            rbt12: 600000,
            anexo: 'III',
            parteCBSnoDAS: 15.6,
            vendasEmpresas: 70,
            comprasComCredito: 8000,
            aliquotaCBS: 11.3,
            aliquotaIBS: 0.1
        },
        validate(values) {
            if (values.receitaMes <= 0) return 'Informe o faturamento do mês.';
            if (values.rbt12 <= 0) return 'Informe o faturamento dos últimos 12 meses.';
            return '';
        },
        compute(values) {
            const aliquotaSimples = H.calcularAliquotaEfetivaSimples(values.anexo, values.rbt12).aliquotaEfetiva;
            const das = values.receitaMes * aliquotaSimples;
            const parteCBS = H.clamp(values.parteCBSnoDAS, 0, 40) / 100;
            const cbsDentroDAS = das * parteCBS;
            const partB2B = H.clamp(values.vendasEmpresas, 0, 100) / 100;
            const aliquotaIVA = (H.clamp(values.aliquotaCBS, 0, 20) + H.clamp(values.aliquotaIBS, 0, 20)) / 100;

            // Por dentro: tudo no DAS; o cliente só credita a parcela de CBS/IBS embutida no DAS.
            const impostoDentro = das;
            const creditoClienteDentro = cbsDentroDAS * partB2B;

            // Por fora (regime regular): DAS sem a parcela de CBS/IBS, mais débito sobre as vendas menos crédito nas compras.
            const dasSemCBS = das - cbsDentroDAS;
            const debito = values.receitaMes * aliquotaIVA;
            const credito = values.comprasComCredito * aliquotaIVA;
            const saldoIVA = Math.max(0, debito - credito);
            const saldoCredor = Math.max(0, credito - debito);
            const impostoFora = dasSemCBS + saldoIVA;
            const creditoClienteFora = debito * partB2B;

            const impostoAMais = impostoFora - impostoDentro;
            const creditoAMais = creditoClienteFora - creditoClienteDentro;
            const balanco = creditoAMais - impostoAMais;

            let leitura;
            if (partB2B === 0) {
                leitura = 'Sem vendas para empresas, o crédito não tem valor para os clientes: recolher por dentro do DAS tende a ser melhor.';
            } else if (balanco > 0) {
                leitura = `Por fora, seus clientes empresas aproveitam ${H.formatCurrency(creditoAMais)} a mais de crédito por mês, mais do que o imposto extra da empresa (${H.formatCurrency(Math.max(0, impostoAMais))}). Isso pode tornar seu preço mais competitivo para empresas.`;
            } else {
                leitura = `Por fora, o imposto extra (${H.formatCurrency(impostoAMais)}) supera o crédito a mais dos clientes (${H.formatCurrency(creditoAMais)}). Recolher por dentro do DAS tende a ser melhor.`;
            }

            return {
                highlight: H.metricCurrency(impostoAMais >= 0 ? 'Imposto a mais por mês ao recolher por fora' : 'Imposto a menos por mês ao recolher por fora', Math.abs(impostoAMais)),
                secondaryA: H.metricCurrency('Crédito a mais para clientes empresas', creditoAMais),
                secondaryB: H.metricCurrency('Saldo para a cadeia (crédito - imposto extra)', balanco),
                notes: [
                    { label: 'Por dentro: DAS do mês', metric: H.metricCurrency('DAS', impostoDentro) },
                    { label: 'Por fora: DAS sem CBS/IBS + IBS/CBS a pagar', metric: H.metricCurrency('Total', impostoFora) },
                    { label: 'Crédito do cliente por dentro / por fora', metric: H.metricText('Crédito', `${H.formatCurrency(creditoClienteDentro)} / ${H.formatCurrency(creditoClienteFora)}`) },
                    { label: 'Leitura', metric: H.metricText('Leitura', leitura) }
                ],
                steps: [
                    'DAS pelo anexo e faixa; a parte de PIS/Cofins vira CBS dentro do DAS em 2027.',
                    'Por dentro: o cliente credita só a CBS/IBS embutida no DAS.',
                    'Por fora: DAS sem essa parte, mais CBS/IBS sobre as vendas, menos crédito nas compras.',
                    'Por fora: o cliente credita toda a CBS/IBS destacada na nota.'
                ],
                details: [
                    { label: 'Alíquota efetiva do Simples', value: H.formatPercent(aliquotaSimples * 100) },
                    { label: 'CBS/IBS dentro do DAS', value: H.formatCurrency(cbsDentroDAS) },
                    { label: 'Débito de CBS/IBS por fora', value: H.formatCurrency(debito) },
                    { label: 'Crédito nas compras', value: H.formatCurrency(credito) },
                    { label: 'Saldo credor a levar para o mês seguinte', value: H.formatCurrency(saldoCredor) },
                    { label: 'Prazos', value: 'A opção é semestral (setembro e março). A primeira janela para 2027 terminou em 30/10/2026; a próxima, em março de 2027, vale para o 2º semestre.' },
                    { label: 'Aviso', value: 'Simulação gerencial com preço de venda igual nos dois cenários. Não inclui split payment, regimes diferenciados nem alíquotas reduzidas.' }
                ],
                chart: {
                    labels: ['Imposto por dentro', 'Imposto por fora', 'Crédito do cliente por dentro', 'Crédito do cliente por fora'],
                    values: [H.round2(impostoDentro), H.round2(impostoFora), H.round2(creditoClienteDentro), H.round2(creditoClienteFora)],
                    colors: ['#7d93a8', '#d98c5f', '#4f8f7a', '#c8a86b']
                }
            };
        }
    });
})();
