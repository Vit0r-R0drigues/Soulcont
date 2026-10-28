(function () {
    const suite = window.CalculadoraSuite || {};
    const H = suite.helpers;
    if (!suite.registerDefinition || !H) return;

    suite.registerDefinition('margem-lucro', {
        pageTitle: 'Calculadora de Margem de Lucro',
        pageDescription: 'Meca margem bruta e líquida da operação para orientar precificação e corte de custos.',
        badges: ['Financeiro', 'Margem', 'Decisão'],
        calculateLabel: 'Calcular margem',
        fields: [
            { id: 'faturamento', type: 'number', label: 'Faturamento mensal', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'custosVariaveis', type: 'number', label: 'Custos variáveis totais', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'custosFixos', type: 'number', label: 'Custos fixos totais', placeholder: 'R$ 0,00', min: 0, step: '0.01' }
        ],
        example: {
            faturamento: 120000,
            custosVariaveis: 68000,
            custosFixos: 29000
        },
        validate(values) {
            if (values.faturamento <= 0) return 'Informe o faturamento para calcular a margem.';
            return '';
        },
        compute(values) {
            const lucroBruto = values.faturamento - values.custosVariaveis;
            const lucroLiquido = lucroBruto - values.custosFixos;
            const margemBruta = values.faturamento > 0 ? (lucroBruto / values.faturamento) * 100 : 0;
            const margemLiquida = values.faturamento > 0 ? (lucroLiquido / values.faturamento) * 100 : 0;

            let leitura = 'Margem saudável para consolidação de caixa.';
            if (margemLiquida < 5) leitura = 'Margem apertada. Revise preço, custos e mix de vendas.';
            if (margemLiquida < 0) leitura = 'Resultado negativo. Ação imediata recomendada.';

            return {
                highlight: H.metricPercent('Margem líquida', margemLiquida),
                secondaryA: H.metricCurrency('Lucro líquido', lucroLiquido),
                secondaryB: H.metricPercent('Margem bruta', margemBruta),
                notes: [
                    { label: 'Leitura estratégica', metric: H.metricText('Diagnóstico', leitura) },
                    { label: 'Custos variáveis', metric: H.metricCurrency('Variaveis', values.custosVariaveis) },
                    { label: 'Custos fixos', metric: H.metricCurrency('Fixos', values.custosFixos) }
                ],
                steps: [
                    'Apuração do lucro bruto pelo faturamento menos custos variáveis.',
                    'Desconto dos custos fixos para obter lucro líquido.',
                    'Transformação do resultado em margem percentual.'
                ],
                details: [
                    { label: 'Faturamento', value: H.formatCurrency(values.faturamento) },
                    { label: 'Lucro bruto', value: H.formatCurrency(lucroBruto) },
                    { label: 'Lucro líquido', value: H.formatCurrency(lucroLiquido) },
                    { label: 'Margem líquida', value: H.formatPercent(margemLiquida) }
                ],
                chart: {
                    labels: ['Custos variáveis', 'Custos fixos', 'Lucro líquido'],
                    values: [H.round2(values.custosVariaveis), H.round2(values.custosFixos), H.round2(Math.max(0, lucroLiquido))],
                    colors: ['#d98c5f', '#7d93a8', '#4f8f7a']
                }
            };
        }
    });

    suite.registerDefinition('ponto-equilibrio', {
        pageTitle: 'Calculadora de Ponto de Equilibrio',
        pageDescription: 'Descubra o faturamento mínimo para cobrir custos fixos com base na margem de contribuição.',
        badges: ['Financeiro', 'Break-even', 'Planejamento'],
        calculateLabel: 'Calcular ponto de equilibrio',
        fields: [
            { id: 'custosFixos', type: 'number', label: 'Custos fixos mensais', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'precoMedio', type: 'number', label: 'Preço médio de venda por unidade', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'custoVariavelUnitario', type: 'number', label: 'Custo variável por unidade', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'faturamentoAtual', type: 'number', label: 'Faturamento atual (opcional)', placeholder: 'R$ 0,00', min: 0, step: '0.01' }
        ],
        example: {
            custosFixos: 45000,
            precoMedio: 280,
            custoVariavelUnitario: 130,
            faturamentoAtual: 98000
        },
        validate(values) {
            if (values.precoMedio <= 0) return 'Informe o preço médio para calcular o ponto de equilibrio.';
            if (values.custoVariavelUnitario >= values.precoMedio) {
                return 'O custo variável unitário deve ser menor que o preço médio.';
            }
            return '';
        },
        compute(values) {
            const margemContribuicao = values.precoMedio - values.custoVariavelUnitario;
            const pontoUnidades = values.custosFixos / margemContribuicao;
            const pontoFaturamento = pontoUnidades * values.precoMedio;
            const margemSeguranca = values.faturamentoAtual > 0
                ? ((values.faturamentoAtual - pontoFaturamento) / values.faturamentoAtual) * 100
                : 0;

            return {
                highlight: H.metricCurrency('Faturamento de equilibrio', pontoFaturamento),
                secondaryA: H.metricNumber('Unidades para equilibrio', pontoUnidades, ' unid'),
                secondaryB: H.metricPercent('Margem de segurança', margemSeguranca),
                notes: [
                    { label: 'Margem de contribuição/unidade', metric: H.metricCurrency('Contribuição', margemContribuicao) },
                    { label: 'Custos fixos', metric: H.metricCurrency('Custos fixos', values.custosFixos) },
                    { label: 'Faturamento atual', metric: H.metricCurrency('Atual', values.faturamentoAtual) }
                ],
                steps: [
                    'Apuração da margem de contribuição por unidade vendida.',
                    'Divisão dos custos fixos pela contribuição para obter unidades mínimas.',
                    'Conversão para faturamento mínimo de equilibrio.'
                ],
                details: [
                    { label: 'Preço médio', value: H.formatCurrency(values.precoMedio) },
                    { label: 'Custo variável unitário', value: H.formatCurrency(values.custoVariavelUnitario) },
                    { label: 'Unidades de equilibrio', value: `${H.formatNumber(pontoUnidades, 2)} unid` },
                    { label: 'Margem de segurança', value: H.formatPercent(margemSeguranca) }
                ],
                chart: {
                    labels: ['Ponto de equilibrio', 'Faturamento atual'],
                    values: [H.round2(pontoFaturamento), H.round2(values.faturamentoAtual)],
                    colors: ['#d98c5f', '#4f8f7a']
                }
            };
        }
    });

    suite.registerDefinition('fluxo-caixa', {
        pageTitle: 'Simulador de Fluxo de Caixa Mensal',
        pageDescription: 'Projete saldo de caixa do mês e identifique necessidade de capital de giro.',
        badges: ['Financeiro', 'Fluxo de caixa', 'Capital de giro'],
        calculateLabel: 'Projetar fluxo de caixa',
        fields: [
            { id: 'saldoInicial', type: 'number', label: 'Saldo inicial de caixa', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'entradas', type: 'number', label: 'Entradas previstas no mês', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'saidasFixas', type: 'number', label: 'Saídas fixas no mês', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'saidasVariaveis', type: 'number', label: 'Saídas variáveis no mês', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'impostos', type: 'number', label: 'Impostos previstos no mês', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'reservaMinima', type: 'number', label: 'Reserva mínima de segurança', placeholder: 'R$ 0,00', min: 0, step: '0.01' }
        ],
        example: {
            saldoInicial: 32000,
            entradas: 95000,
            saidasFixas: 41000,
            saidasVariaveis: 26000,
            impostos: 12000,
            reservaMinima: 15000
        },
        validate(values) {
            if ((values.saldoInicial + values.entradas + values.saidasFixas + values.saidasVariaveis + values.impostos) === 0) {
                return 'Preencha os valores para projetar o fluxo de caixa.';
            }
            return '';
        },
        compute(values) {
            const saidasTotais = values.saidasFixas + values.saidasVariaveis + values.impostos;
            const saldoFinal = values.saldoInicial + values.entradas - saidasTotais;
            const folgaSobreReserva = saldoFinal - values.reservaMinima;
            const necessidadeGiro = Math.max(0, values.reservaMinima - saldoFinal);
            const leitura = folgaSobreReserva >= 0
                ? 'Caixa projetado acima da reserva de segurança.'
                : 'Caixa abaixo da reserva. Planeje capital de giro e corte de saídas.';

            return {
                highlight: H.metricCurrency('Saldo final projetado', saldoFinal),
                secondaryA: H.metricCurrency('Saídas totais', saidasTotais),
                secondaryB: H.metricCurrency('Necessidade de giro', necessidadeGiro),
                notes: [
                    { label: 'Leitura de risco', metric: H.metricText('Leitura', leitura) },
                    { label: 'Reserva mínima', metric: H.metricCurrency('Reserva', values.reservaMinima) },
                    { label: 'Folga sobre reserva', metric: H.metricCurrency('Folga', folgaSobreReserva) }
                ],
                steps: [
                    'Soma das entradas e saldo inicial para caixa disponível.',
                    'Desconto das saídas fixas, variáveis e impostos.',
                    'Comparação do saldo final com reserva mínima de segurança.'
                ],
                details: [
                    { label: 'Saldo inicial', value: H.formatCurrency(values.saldoInicial) },
                    { label: 'Entradas previstas', value: H.formatCurrency(values.entradas) },
                    { label: 'Saídas fixas', value: H.formatCurrency(values.saidasFixas) },
                    { label: 'Saídas variáveis', value: H.formatCurrency(values.saidasVariaveis) }
                ],
                chart: {
                    labels: ['Entradas', 'Saídas totais', 'Saldo final'],
                    values: [H.round2(values.entradas), H.round2(saidasTotais), H.round2(Math.max(0, saldoFinal))],
                    colors: ['#4f8f7a', '#d98c5f', '#c8a86b']
                }
            };
        }
    });

    suite.registerDefinition('saude-financeira', {
        pageTitle: 'Diagnóstico de Saúde Financeira Empresarial',
        pageDescription: 'Receba um score rápido de saúde financeira com indicadores de liquidez, margem e risco.',
        badges: ['Diagnóstico', 'Score', 'Gestão'],
        calculateLabel: 'Gerar diagnóstico',
        fields: [
            { id: 'margemLiquida', type: 'number', label: 'Margem líquida (%)', min: -100, step: '0.01' },
            { id: 'caixaMeses', type: 'number', label: 'Reserva de caixa (em meses)', min: 0, step: '0.1' },
            { id: 'endividamento', type: 'number', label: 'Endividamento sobre receita (%)', min: 0, step: '0.1' },
            { id: 'inadimplencia', type: 'number', label: 'Inadimplência de clientes (%)', min: 0, step: '0.1' },
            { id: 'atrasosFiscais', type: 'select', label: 'Há atrasos fiscais?', options: H.simOuNaoOptions() },
            { id: 'prolaboreSeparado', type: 'select', label: 'Pró-labore separado da conta da empresa?', options: H.simOuNaoOptions() },
            { id: 'dreAtualizada', type: 'select', label: 'DRE atualizada mensalmente?', options: H.simOuNaoOptions() }
        ],
        example: {
            margemLiquida: 9.2,
            caixaMeses: 1.8,
            endividamento: 47,
            inadimplencia: 4.5,
            atrasosFiscais: 'nao',
            prolaboreSeparado: 'sim',
            dreAtualizada: 'sim'
        },
        validate() {
            return '';
        },
        compute(values) {
            let score = 100;

            if (values.margemLiquida < 0) score -= 30;
            else if (values.margemLiquida < 5) score -= 20;
            else if (values.margemLiquida < 10) score -= 10;

            if (values.caixaMeses < 1) score -= 25;
            else if (values.caixaMeses < 3) score -= 12;

            if (values.endividamento > 80) score -= 20;
            else if (values.endividamento > 50) score -= 12;

            if (values.inadimplencia > 10) score -= 15;
            else if (values.inadimplencia > 5) score -= 8;

            if (values.atrasosFiscais === 'sim') score -= 15;
            if (values.prolaboreSeparado === 'nao') score -= 8;
            if (values.dreAtualizada === 'nao') score -= 8;

            score = H.clamp(score, 0, 100);

            let nivel = 'Saudável';
            let acao = 'Mantenha disciplina de caixa e acompanhe indicadores mensalmente.';
            if (score < 60) {
                nivel = 'Crítico';
                acao = 'Priorize caixa, renegociação de dívidas e regularização fiscal imediata.';
            } else if (score < 80) {
                nivel = 'Atenção';
                acao = 'Reforce controles, aumente margem e reduza exposição de risco.';
            }

            return {
                highlight: H.metricNumber('Score de saúde financeira', score, ' / 100'),
                secondaryA: H.metricText('Classificação', nivel),
                secondaryB: H.metricText('Ação prioritária', acao),
                notes: [
                    { label: 'Margem líquida', metric: H.metricPercent('Margem', values.margemLiquida) },
                    { label: 'Reserva de caixa', metric: H.metricNumber('Reserva', values.caixaMeses, ' meses') },
                    { label: 'Endividamento', metric: H.metricPercent('Endividamento', values.endividamento) }
                ],
                steps: [
                    'Leitura dos indicadores de margem, caixa, dívida e inadimplência.',
                    'Aplicação de pesos de risco para compor o score.',
                    'Classificação automática com ação recomendada.'
                ],
                details: [
                    { label: 'Atrasos fiscais', value: values.atrasosFiscais === 'sim' ? 'Sim' : 'Nao' },
                    { label: 'Pró-labore separado', value: values.prolaboreSeparado === 'sim' ? 'Sim' : 'Nao' },
                    { label: 'DRE atualizada', value: values.dreAtualizada === 'sim' ? 'Sim' : 'Nao' },
                    { label: 'Inadimplência', value: H.formatPercent(values.inadimplencia) }
                ],
                chart: {
                    labels: ['Score obtido', 'Faixa de melhoria'],
                    values: [H.round2(score), H.round2(100 - score)],
                    colors: ['#4f8f7a', '#d98c5f']
                }
            };
        }
    });
})();
