(function () {
    const suite = window.CalculadoraSuite || {};
    const H = suite.helpers;
    if (!suite.registerDefinition || !H) return;

    suite.registerDefinition('decimo-terceiro', {
        pageTitle: 'Calculadora de 13º Salário',
        pageDescription: 'Simule 13º salário com meses trabalhados, adiantamento e descontos estimados.',
        badges: ['Trabalhista', '13º', 'Folha'],
        calculateLabel: 'Calcular 13º salário',
        fields: [
            { id: 'salarioBruto', type: 'number', label: 'Salário base mensal', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            {
                id: 'mesesTrabalhados',
                type: 'select',
                label: 'Meses trabalhados no ano',
                options: [
                    { value: '1', label: '1 mês' }, { value: '2', label: '2 meses' }, { value: '3', label: '3 meses' },
                    { value: '4', label: '4 meses' }, { value: '5', label: '5 meses' }, { value: '6', label: '6 meses' },
                    { value: '7', label: '7 meses' }, { value: '8', label: '8 meses' }, { value: '9', label: '9 meses' },
                    { value: '10', label: '10 meses' }, { value: '11', label: '11 meses' }, { value: '12', label: '12 meses' }
                ]
            },
            {
                id: 'percentualAdiantamento',
                type: 'range',
                label: 'Percentual da 1a parcela',
                min: 30,
                max: 50,
                step: 1,
                value: 50,
                outputSuffix: '%'
            },
            { id: 'dependentes', type: 'number', label: 'Dependentes para IRRF', min: 0, step: '1' }
        ],
        example: {
            salarioBruto: 4500,
            mesesTrabalhados: '12',
            percentualAdiantamento: 50,
            dependentes: 1
        },
        validate(values) {
            if (values.salarioBruto <= 0) return 'Informe o salário base para a simulação do 13º.';
            return '';
        },
        compute(values) {
            const decimo = H.calcularDecimoTerceiroLiquido({
                salarioBase: values.salarioBruto,
                mesesTrabalhados: values.mesesTrabalhados,
                percentualAdiantamento: values.percentualAdiantamento,
                dependentes: values.dependentes
            });

            return {
                highlight: H.metricCurrency('2a parcela líquida estimada', decimo.segundaParcelaLiquida),
                secondaryA: H.metricCurrency('1a parcela', decimo.primeiraParcela),
                secondaryB: H.metricCurrency('13º líquido total', decimo.liquidoTotal),
                notes: [
                    { label: 'INSS no 13º', metric: H.metricCurrency('INSS', decimo.inss) },
                    { label: 'IRRF no 13º', metric: H.metricCurrency('IRRF', decimo.irrf.impostoFinal) },
                    { label: 'Valor bruto do 13º', metric: H.metricCurrency('Bruto', decimo.bruto13) }
                ],
                steps: [
                    'Apuração do 13º proporcional por avos.',
                    'Cálculo da primeira parcela conforme percentual escolhido.',
                    'Descontos na segunda parcela e exibição do líquido.'
                ],
                details: [
                    { label: 'Avos considerados', value: `${decimo.avos}/12` },
                    { label: 'Valor bruto do 13º', value: H.formatCurrency(decimo.bruto13) },
                    { label: 'Dependentes', value: `${values.dependentes} dependente(s)` },
                    { label: 'Percentual da 1a parcela', value: H.formatPercent(values.percentualAdiantamento) }
                ],
                chart: {
                    labels: ['1a parcela', '2a parcela líquida', 'Descontos'],
                    values: [
                        H.round2(decimo.primeiraParcela),
                        H.round2(decimo.segundaParcelaLiquida),
                        H.round2(decimo.inss + decimo.irrf.impostoFinal)
                    ],
                    colors: ['#c8a86b', '#4f8f7a', '#d98c5f']
                }
            };
        }
    });

    suite.registerDefinition('custo-funcionario', {
        pageTitle: 'Calculadora de Custo Real do Funcionário',
        pageDescription: 'Calcule o custo mensal e por hora de um funcionário CLT, com encargos do regime da empresa, provisões e o impacto do fim da escala 6x1 (EC 141/2026).',
        badges: ['DP', 'Encargos', 'Escala 6x1 e 5x2'],
        calculateLabel: 'Calcular custo real',
        fields: [
            { id: 'salarioBase', type: 'number', label: 'Salário base mensal', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            {
                id: 'regimeEmpresa',
                type: 'select',
                label: 'Regime tributário da empresa',
                options: [
                    { value: 'simples', label: 'Simples Nacional (Anexos I, II, III ou V)' },
                    { value: 'simples_iv', label: 'Simples Nacional (Anexo IV)' },
                    { value: 'presumido_real', label: 'Lucro Presumido ou Lucro Real' }
                ],
                help: 'No Simples (exceto Anexo IV) o INSS patronal já está no DAS.'
            },
            { id: 'ratFap', type: 'number', label: 'RAT ajustado pelo FAP (%)', min: 0.5, max: 6, step: '0.01', value: 2, help: 'Em geral entre 1% e 3% antes do FAP. Só entra no Anexo IV e no Presumido/Real.' },
            { id: 'terceiros', type: 'number', label: 'Terceiros: Sistema S, salário-educação, Incra (%)', min: 0, max: 6, step: '0.01', value: 5.8, help: 'Em geral 5,8%. Só entra no Presumido/Real.' },
            {
                id: 'escala',
                type: 'select',
                label: 'Escala e jornada semanal',
                options: [
                    { value: '6x1-44', label: '6x1 · 44 horas (regra antiga)' },
                    { value: '5x2-44', label: '5x2 · 44 horas' },
                    { value: '5x2-42', label: '5x2 · 42 horas (EC 141, 1ª etapa)' },
                    { value: '5x2-40', label: '5x2 · 40 horas (EC 141, regra final)' },
                    { value: '12x36', label: '12x36 (média de 42 horas)' }
                ]
            },
            { id: 'valeTransporte', type: 'number', label: 'Valor mensal das passagens (vale-transporte)', placeholder: 'R$ 0,00', min: 0, step: '0.01', help: 'A empresa desconta até 6% do salário; a calculadora considera só a parte que fica com a empresa.' },
            { id: 'beneficios', type: 'number', label: 'Vale-refeição/alimentação e auxílios', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'planoSaude', type: 'number', label: 'Plano de saúde (parte da empresa)', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'outrosBeneficios', type: 'number', label: 'Outros benefícios', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            { id: 'incluirProvisoes', type: 'checkbox', label: 'Incluir provisões de 13º, férias + 1/3 e seus encargos', checked: true },
            { id: 'incluirMultaFgts', type: 'checkbox', label: 'Incluir provisão da multa de 40% do FGTS', checked: false }
        ],
        example: {
            salarioBase: 3800,
            regimeEmpresa: 'presumido_real',
            ratFap: 2,
            terceiros: 5.8,
            escala: '6x1-44',
            valeTransporte: 264,
            beneficios: 680,
            planoSaude: 320,
            outrosBeneficios: 120,
            incluirProvisoes: true,
            incluirMultaFgts: false
        },
        validate(values) {
            if (values.salarioBase <= 0) return 'Informe o salário base do funcionário.';
            return '';
        },
        compute(values) {
            const salario = values.salarioBase;
            const regime = values.regimeEmpresa || 'presumido_real';

            // Encargos sobre a remuneração, conforme o regime da empresa.
            const fgtsPct = 0.08;
            const inssPatronalPct = regime === 'simples' ? 0 : 0.20;
            const ratPct = regime === 'simples' ? 0 : H.clamp(values.ratFap, 0, 6) / 100;
            const terceirosPct = regime === 'presumido_real' ? H.clamp(values.terceiros, 0, 6) / 100 : 0;
            const encargosPct = fgtsPct + inssPatronalPct + ratPct + terceirosPct;

            // Provisões mensais: 13º (1/12), férias (1/12) e 1/3 de férias (1/36); os encargos também incidem sobre elas.
            const provisoesBase = values.incluirProvisoes ? (salario / 12) + (salario / 12) + (salario / 36) : 0;
            const remuneracaoComProvisoes = salario + provisoesBase;
            const fgts = remuneracaoComProvisoes * fgtsPct;
            const inssPatronal = remuneracaoComProvisoes * inssPatronalPct;
            const ratTerceiros = remuneracaoComProvisoes * (ratPct + terceirosPct);
            const multaFgts = values.incluirMultaFgts ? fgts * 0.40 : 0;
            const encargos = fgts + inssPatronal + ratTerceiros + multaFgts;

            // Vale-transporte: a empresa arca com o que passa de 6% do salário.
            const descontoVT = Math.min(values.valeTransporte, salario * 0.06);
            const custoVT = Math.max(0, values.valeTransporte - descontoVT);
            const beneficiosTotal = custoVT + values.beneficios + values.planoSaude + values.outrosBeneficios;

            const custoTotal = salario + provisoesBase + encargos + beneficiosTotal;
            const custoAnual = custoTotal * 12;
            const indiceCusto = salario > 0 ? (custoTotal / salario) * 100 : 0;

            // Horas pagas por mês: jornada semanal x 5 (divisor usual: 44h = 220, 42h = 210, 40h = 200).
            const jornadas = { '6x1-44': 44, '5x2-44': 44, '5x2-42': 42, '5x2-40': 40, '12x36': 42 };
            const horasSemana = jornadas[values.escala] || 44;
            const horasMes = horasSemana * 5;
            const custoHora = custoTotal / horasMes;

            // EC 141/2026: jornada cai para 42h e depois 40h, sem redução de salário.
            const custoHora40 = custoTotal / 200;
            const aumentoHora = horasSemana > 40 ? ((custoHora40 / custoHora) - 1) * 100 : 0;
            const horasFaltantes = Math.max(0, horasSemana - 40) * 5;
            const valorHoraNormal40 = salario / 200;
            const custoCobertura = horasFaltantes * valorHoraNormal40 * 1.5 * (1 + encargosPct);

            const leituraEscala = horasSemana > 40
                ? `Com a EC 141/2026 a jornada cai para 42h e depois para 40h por semana, em 5x2 e sem reduzir o salário. O custo por hora sobe cerca de ${H.formatPercent(aumentoHora)}. Para manter as mesmas ${horasSemana}h com hora extra de 50%, seriam ${H.formatNumber(horasFaltantes, 0)} horas por mês, cerca de ${H.formatCurrency(custoCobertura)} a mais.`
                : 'Esta jornada já está dentro do limite de 40 horas da EC 141/2026.';

            const regimeLabel = {
                simples: 'Simples (I, II, III ou V): sem INSS patronal na folha',
                simples_iv: 'Simples Anexo IV: INSS patronal de 20% + RAT',
                presumido_real: 'Presumido/Real: INSS 20% + RAT + terceiros'
            }[regime];

            return {
                highlight: H.metricCurrency('Custo total mensal', custoTotal),
                secondaryA: H.metricCurrency(`Custo por hora (${horasSemana}h semanais)`, custoHora),
                secondaryB: H.metricCurrency('Custo anual estimado', custoAnual),
                notes: [
                    { label: 'Encargos (FGTS, INSS, RAT e terceiros)', metric: H.metricCurrency('Encargos', encargos) },
                    { label: 'Provisões de 13º e férias', metric: H.metricCurrency('Provisões', provisoesBase) },
                    { label: 'Benefícios (VT líquido do desconto)', metric: H.metricCurrency('Benefícios', beneficiosTotal) },
                    { label: 'Custo sobre o salário', metric: H.metricPercent('Índice', indiceCusto) },
                    { label: 'Fim da escala 6x1', metric: H.metricText('Leitura', leituraEscala) }
                ],
                steps: [
                    'Salário + provisões de 13º, férias e 1/3.',
                    'Encargos sobre salário e provisões conforme o regime da empresa.',
                    'Benefícios, com o vale-transporte já descontado em até 6% do salário.',
                    'Custo por hora = custo total dividido pelas horas da jornada no mês.'
                ],
                details: [
                    { label: 'Regime', value: regimeLabel },
                    { label: 'FGTS (8%)', value: H.formatCurrency(fgts) },
                    { label: 'INSS patronal', value: H.formatCurrency(inssPatronal) },
                    { label: 'RAT + terceiros', value: H.formatCurrency(ratTerceiros) },
                    { label: 'Multa de 40% do FGTS (provisão)', value: H.formatCurrency(multaFgts) },
                    { label: 'Desconto de VT do funcionário', value: H.formatCurrency(descontoVT) },
                    { label: 'Horas pagas no mês', value: `${H.formatNumber(horasMes, 0)} h` },
                    { label: 'Custo por hora com 40h semanais', value: H.formatCurrency(custoHora40) },
                    { label: 'Aviso', value: 'Estimativa gerencial. Não inclui desoneração da folha, adicionais (noturno, insalubridade), horas extras habituais nem regras de convenção coletiva.' }
                ],
                chart: {
                    labels: ['Salário', 'Provisões', 'Encargos', 'Benefícios'],
                    values: [H.round2(salario), H.round2(provisoesBase), H.round2(encargos), H.round2(beneficiosTotal)],
                    colors: ['#c8a86b', '#7d93a8', '#d98c5f', '#4f8f7a']
                }
            };
        }
    });

    suite.registerDefinition('horas-extras', {
        pageTitle: 'Calculadora de Horas Extras e Adicional Noturno',
        pageDescription: 'Calcule horas extras de 50% e 100%, adicional noturno com hora reduzida e o reflexo no descanso semanal remunerado (DSR).',
        badges: ['Trabalhista', 'Horas extras', 'Adicional noturno'],
        calculateLabel: 'Calcular horas extras',
        fields: [
            { id: 'salarioBase', type: 'number', label: 'Salário base mensal', placeholder: 'R$ 0,00', min: 0, step: '0.01' },
            {
                id: 'jornadaSemanal',
                type: 'select',
                label: 'Jornada semanal contratada',
                options: [
                    { value: '44', label: '44 horas (divisor 220)' },
                    { value: '42', label: '42 horas (divisor 210) · EC 141, 1ª etapa' },
                    { value: '40', label: '40 horas (divisor 200) · EC 141, regra final' },
                    { value: '36', label: '36 horas (divisor 180)' },
                    { value: '30', label: '30 horas (divisor 150)' }
                ]
            },
            { id: 'horas50', type: 'number', label: 'Horas extras em dias úteis no mês (50%)', min: 0, step: '0.5' },
            { id: 'horas100', type: 'number', label: 'Horas extras em domingos e feriados no mês (100%)', min: 0, step: '0.5' },
            { id: 'percentual50', type: 'number', label: 'Adicional da hora extra em dia útil (%)', min: 50, max: 150, step: '1', value: 50, help: 'O mínimo legal é 50%; a convenção coletiva pode prever mais.' },
            { id: 'horasNoturnas', type: 'number', label: 'Horas trabalhadas entre 22h e 5h no mês (relógio)', min: 0, step: '0.5', help: 'A calculadora converte para a hora noturna reduzida de 52min30s.' },
            { id: 'percentualNoturno', type: 'number', label: 'Adicional noturno (%)', min: 20, max: 100, step: '1', value: 20, help: 'O mínimo legal urbano é 20%.' },
            { id: 'diasUteis', type: 'number', label: 'Dias úteis no mês', min: 1, max: 31, step: '1', value: 25, help: 'Inclui sábados não trabalhados; exclui domingos e feriados.' },
            { id: 'diasDescanso', type: 'number', label: 'Domingos e feriados no mês', min: 0, max: 15, step: '1', value: 5 }
        ],
        example: {
            salarioBase: 2800,
            jornadaSemanal: '44',
            horas50: 12,
            horas100: 4,
            percentual50: 50,
            horasNoturnas: 20,
            percentualNoturno: 20,
            diasUteis: 25,
            diasDescanso: 5
        },
        validate(values) {
            if (values.salarioBase <= 0) return 'Informe o salário base.';
            if (values.diasUteis <= 0) return 'Informe os dias úteis do mês.';
            return '';
        },
        compute(values) {
            const jornada = Number(values.jornadaSemanal) || 44;
            const divisor = jornada * 5;
            const valorHora = values.salarioBase / divisor;
            const adicional50 = H.clamp(values.percentual50, 50, 150) / 100;
            const adicionalNoturnoPct = H.clamp(values.percentualNoturno, 20, 100) / 100;

            const valorHora50 = valorHora * (1 + adicional50);
            const valorHora100 = valorHora * 2;
            const totalHE50 = values.horas50 * valorHora50;
            const totalHE100 = values.horas100 * valorHora100;

            // Hora noturna reduzida: 52min30s, então cada hora de relógio vale 60/52,5 horas noturnas.
            const horasNoturnasReduzidas = values.horasNoturnas * (60 / 52.5);
            const adicionalNoturno = horasNoturnasReduzidas * valorHora * adicionalNoturnoPct;

            // Reflexo no DSR: média diária das variáveis multiplicada pelos domingos e feriados.
            const variaveis = totalHE50 + totalHE100 + adicionalNoturno;
            const dsr = (variaveis / values.diasUteis) * values.diasDescanso;
            const totalAdicional = variaveis + dsr;
            const fgts = totalAdicional * 0.08;

            return {
                highlight: H.metricCurrency('Total a pagar a mais no mês', totalAdicional),
                secondaryA: H.metricCurrency('Valor da hora normal', valorHora),
                secondaryB: H.metricCurrency('Reflexo no DSR', dsr),
                notes: [
                    { label: `Horas extras ${H.formatPercent(adicional50 * 100)}`, metric: H.metricCurrency('HE', totalHE50) },
                    { label: 'Horas extras 100%', metric: H.metricCurrency('HE', totalHE100) },
                    { label: 'Adicional noturno', metric: H.metricCurrency('Noturno', adicionalNoturno) },
                    { label: 'FGTS sobre os adicionais (8%)', metric: H.metricCurrency('FGTS', fgts) }
                ],
                steps: [
                    `Valor da hora = salário dividido por ${divisor} (jornada de ${jornada}h x 5).`,
                    'Hora extra em dia útil com o adicional informado; domingos e feriados a 100%.',
                    'Horas noturnas convertidas para a hora reduzida de 52min30s, com o adicional informado.',
                    'DSR = soma das variáveis dividida pelos dias úteis, vezes domingos e feriados.'
                ],
                details: [
                    { label: 'Valor da hora extra em dia útil', value: H.formatCurrency(valorHora50) },
                    { label: 'Valor da hora extra a 100%', value: H.formatCurrency(valorHora100) },
                    { label: 'Horas noturnas reduzidas', value: `${H.formatNumber(horasNoturnasReduzidas, 2)} h` },
                    { label: 'Divisor de horas', value: String(divisor) },
                    { label: 'Aviso', value: 'Os valores entram na base de INSS, IRRF e FGTS e refletem em férias, 13º e aviso prévio quando habituais. Confira a convenção coletiva da categoria.' }
                ],
                chart: {
                    labels: ['Horas extras 50%', 'Horas extras 100%', 'Adicional noturno', 'DSR'],
                    values: [H.round2(totalHE50), H.round2(totalHE100), H.round2(adicionalNoturno), H.round2(dsr)],
                    colors: ['#c8a86b', '#d98c5f', '#7d93a8', '#4f8f7a']
                }
            };
        }
    });
})();
