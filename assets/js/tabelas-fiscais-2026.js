/*
 * FONTE ÚNICA das tabelas fiscais usadas por todas as calculadoras SoulCont.
 *
 * Antes deste arquivo, INSS e IRRF estavam copiados em cinco lugares
 * diferentes. Foi essa duplicação que permitiu que a calculadora de rescisão
 * divergisse da calculadora de IRRF. Ao virar o ano, altere SOMENTE aqui.
 *
 * Este script precisa ser carregado ANTES das calculadoras. Todos usam `defer`,
 * que preserva a ordem de execução declarada no HTML.
 *
 * Última conferência: 15/08/2026
 */
(function (global) {
    'use strict';

    /* INSS — contribuição progressiva do segurado empregado.
       Salário mínimo de R$ 1.621,00 e teto de R$ 8.475,55 vigentes em 2026.
       Base: Lei 8.212/1991 com os reajustes anuais. */
    var INSS = [
        { limite: 1621.00, aliquota: 0.075 },
        { limite: 2902.84, aliquota: 0.09 },
        { limite: 4354.27, aliquota: 0.12 },
        { limite: 8475.55, aliquota: 0.14 }
    ];

    /* IRRF — tabela progressiva mensal. */
    var IRRF_TABELA = [
        { limite: 2428.80, aliquota: 0, deducao: 0 },
        { limite: 2826.65, aliquota: 0.075, deducao: 182.16 },
        { limite: 3751.05, aliquota: 0.15, deducao: 394.16 },
        { limite: 4664.68, aliquota: 0.225, deducao: 675.49 },
        { limite: Infinity, aliquota: 0.275, deducao: 908.73 }
    ];

    var DEDUCAO_DEPENDENTE = 189.59;

    /* Desconto simplificado mensal: SUBSTITUI as deduções legais (INSS,
       dependentes, pensão) quando for mais vantajoso — nunca se soma a elas. */
    var DESCONTO_SIMPLIFICADO = 607.20;

    /* Redutor do IRRF criado pela Lei 15.270/2025, vigente desde 01/2026.
       As faixas de R$ 5.000 e R$ 7.350 incidem sobre o RENDIMENTO BRUTO
       tributável do pagamento, não sobre a base de cálculo já reduzida.
       R$ 312,89 é exatamente o IRRF devido sobre R$ 5.000 com desconto
       simplificado, o que zera o imposto no limite da isenção. */
    var REDUCAO_MAXIMA = 312.89;
    var REDUCAO_FAIXA_ATE = 5000;
    var REDUCAO_FAIXA_FIM = 7350;
    var REDUCAO_COEF_A = 978.62;
    var REDUCAO_COEF_B = 0.133145;

    function arredondar(valor) {
        return Math.round((Number(valor) + Number.EPSILON) * 100) / 100;
    }

    /* INSS progressivo por faixas, respeitando o teto. */
    function calcularINSS(salario) {
        var base = Math.max(0, Number(salario) || 0);
        var total = 0;
        var anterior = 0;
        for (var i = 0; i < INSS.length; i++) {
            var faixa = INSS[i];
            var trecho = Math.min(base, faixa.limite) - anterior;
            if (trecho > 0) total += trecho * faixa.aliquota;
            anterior = faixa.limite;
            if (base <= faixa.limite) break;
        }
        return arredondar(total);
    }

    /* IRRF pela tabela progressiva, ANTES do redutor da Lei 15.270/2025. */
    function calcularIRRFBruto(baseCalculo) {
        var base = Math.max(0, Number(baseCalculo) || 0);
        var faixa = null;
        for (var i = 0; i < IRRF_TABELA.length; i++) {
            if (base <= IRRF_TABELA[i].limite) { faixa = IRRF_TABELA[i]; break; }
        }
        if (!faixa) faixa = IRRF_TABELA[IRRF_TABELA.length - 1];
        return arredondar(Math.max(0, base * faixa.aliquota - faixa.deducao));
    }

    /* Redutor da Lei 15.270/2025.
       @param rendimentoBruto rendimento BRUTO tributável do pagamento
       @param impostoBruto    IRRF apurado pela tabela (limita o redutor) */
    function calcularReducao(rendimentoBruto, impostoBruto) {
        var rendimento = Math.max(0, Number(rendimentoBruto) || 0);
        var imposto = Math.max(0, Number(impostoBruto) || 0);
        var teorica = 0;

        if (rendimento <= REDUCAO_FAIXA_ATE) {
            teorica = REDUCAO_MAXIMA;
        } else if (rendimento <= REDUCAO_FAIXA_FIM) {
            teorica = REDUCAO_COEF_A - (REDUCAO_COEF_B * rendimento);
        }

        return arredondar(Math.min(imposto, Math.max(0, teorica)));
    }

    /* IRRF mensal completo: escolhe entre deduções legais e desconto
       simplificado (o que resultar em menos imposto) e aplica o redutor. */
    function calcularIRRFMensal(opcoes) {
        var bruto = Math.max(0, Number(opcoes.rendimentoBruto) || 0);
        var inss = opcoes.inss === undefined ? calcularINSS(bruto) : Math.max(0, Number(opcoes.inss) || 0);
        var dependentes = Math.max(0, Number(opcoes.dependentes) || 0);
        var pensao = Math.max(0, Number(opcoes.pensao) || 0);
        var outras = Math.max(0, Number(opcoes.outrasDeducoes) || 0);

        var deducoesLegais = inss + dependentes * DEDUCAO_DEPENDENTE + pensao + outras;
        var usaSimplificado = DESCONTO_SIMPLIFICADO > deducoesLegais;
        var deducao = usaSimplificado ? DESCONTO_SIMPLIFICADO : deducoesLegais;

        var base = Math.max(0, bruto - deducao);
        var impostoBruto = calcularIRRFBruto(base);
        var reducao = calcularReducao(bruto, impostoBruto);

        return {
            inss: inss,
            deducaoAplicada: arredondar(deducao),
            modo: usaSimplificado ? 'Desconto simplificado mensal' : 'Deduções legais',
            baseCalculo: arredondar(base),
            impostoBruto: impostoBruto,
            reducao: reducao,
            imposto: arredondar(Math.max(0, impostoBruto - reducao))
        };
    }

    /* Simples Nacional — Anexos I a V (LC 123/2006). */
    var SIMPLES = {
        I: [
            { limite: 180000, aliquota: 0.04, deducao: 0 },
            { limite: 360000, aliquota: 0.073, deducao: 5940 },
            { limite: 720000, aliquota: 0.095, deducao: 13860 },
            { limite: 1800000, aliquota: 0.107, deducao: 22500 },
            { limite: 3600000, aliquota: 0.143, deducao: 87300 },
            { limite: 4800000, aliquota: 0.19, deducao: 378000 }
        ],
        II: [
            { limite: 180000, aliquota: 0.045, deducao: 0 },
            { limite: 360000, aliquota: 0.078, deducao: 5940 },
            { limite: 720000, aliquota: 0.1, deducao: 13860 },
            { limite: 1800000, aliquota: 0.112, deducao: 22500 },
            { limite: 3600000, aliquota: 0.147, deducao: 85500 },
            { limite: 4800000, aliquota: 0.3, deducao: 720000 }
        ],
        III: [
            { limite: 180000, aliquota: 0.06, deducao: 0 },
            { limite: 360000, aliquota: 0.112, deducao: 9360 },
            { limite: 720000, aliquota: 0.135, deducao: 17640 },
            { limite: 1800000, aliquota: 0.16, deducao: 35640 },
            { limite: 3600000, aliquota: 0.21, deducao: 125640 },
            { limite: 4800000, aliquota: 0.33, deducao: 648000 }
        ],
        IV: [
            { limite: 180000, aliquota: 0.045, deducao: 0 },
            { limite: 360000, aliquota: 0.09, deducao: 8100 },
            { limite: 720000, aliquota: 0.102, deducao: 12420 },
            { limite: 1800000, aliquota: 0.14, deducao: 39780 },
            { limite: 3600000, aliquota: 0.22, deducao: 183780 },
            { limite: 4800000, aliquota: 0.33, deducao: 828000 }
        ],
        V: [
            { limite: 180000, aliquota: 0.155, deducao: 0 },
            { limite: 360000, aliquota: 0.18, deducao: 4500 },
            { limite: 720000, aliquota: 0.195, deducao: 9900 },
            { limite: 1800000, aliquota: 0.205, deducao: 17100 },
            { limite: 3600000, aliquota: 0.23, deducao: 62100 },
            { limite: 4800000, aliquota: 0.305, deducao: 540000 }
        ]
    };

    /* MEI: limite anual de R$ 81.000 mantido em 2026.
       O PLP 186/26 propõe R$ 110.000 a partir de 2027, ainda sem aprovação. */
    var MEI = {
        limiteAnual: 81000,
        toleranciaAnual: 97200,
        limiteMensalMedio: 6750
    };

    /* Fator R: folha dos últimos 12 meses ÷ receita bruta dos últimos 12 meses.
       A partir de 28% as atividades sujeitas migram do Anexo V para o III. */
    var FATOR_R_CORTE = 0.28;

    global.SoulcontFiscal = {
        ano: 2026,
        atualizadoEm: '2026-08-15',
        INSS: INSS,
        IRRF_TABELA: IRRF_TABELA,
        DEDUCAO_DEPENDENTE: DEDUCAO_DEPENDENTE,
        DESCONTO_SIMPLIFICADO: DESCONTO_SIMPLIFICADO,
        REDUCAO_MAXIMA: REDUCAO_MAXIMA,
        REDUCAO_FAIXA_ATE: REDUCAO_FAIXA_ATE,
        REDUCAO_FAIXA_FIM: REDUCAO_FAIXA_FIM,
        REDUCAO_COEF_A: REDUCAO_COEF_A,
        REDUCAO_COEF_B: REDUCAO_COEF_B,
        SIMPLES: SIMPLES,
        MEI: MEI,
        FATOR_R_CORTE: FATOR_R_CORTE,
        SALARIO_MINIMO: 1621.00,
        TETO_INSS: 8475.55,
        arredondar: arredondar,
        calcularINSS: calcularINSS,
        calcularIRRFBruto: calcularIRRFBruto,
        calcularReducao: calcularReducao,
        calcularIRRFMensal: calcularIRRFMensal
    };

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = global.SoulcontFiscal;
    }
})(typeof globalThis !== 'undefined' ? globalThis : this);
