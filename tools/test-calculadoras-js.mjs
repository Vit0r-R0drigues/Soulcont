/*
 * Testes de regressão que executam o JAVASCRIPT REALMENTE SERVIDO pelo site.
 *
 * Motivo de existir: tools/test_calculadoras_formulas.py reimplementa as
 * fórmulas em Python. Isso valida o modelo, mas não o código que vai ao ar —
 * foi assim que a calculadora de rescisão passou a divergir da calculadora de
 * IRRF sem que nenhum teste acusasse. Aqui os arquivos .js são carregados e
 * executados; se as implementações divergirem, o teste quebra.
 *
 * Uso:  node tools/test-calculadoras-js.mjs
 */

import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

/* --- DOM mínimo para os arquivos carregarem sem navegador ------------- */
function criarContexto() {
  const noop = () => {};
  const elemento = new Proxy(
    {
      style: {}, dataset: {}, options: [], value: '', textContent: '',
      classList: { add: noop, remove: noop, toggle: noop, contains: () => false },
      addEventListener: noop, appendChild: noop, removeChild: noop,
      querySelector: () => null, querySelectorAll: () => [],
    },
    { get: (alvo, chave) => (chave in alvo ? alvo[chave] : undefined), set: () => true },
  );

  const ctx = {
    console, Math, Date, Number, String, Array, Object, JSON, Intl, RegExp,
    isNaN, parseFloat, parseInt, Infinity, NaN, Promise, Error,
    localStorage: { getItem: () => null, setItem: noop, removeItem: noop, key: () => null, length: 0 },
    document: {
      addEventListener: noop, readyState: 'complete', hidden: false,
      getElementById: () => elemento, querySelector: () => elemento,
      querySelectorAll: () => [], createElement: () => elemento,
      body: elemento, head: elemento, title: '',
    },
    window: { addEventListener: noop, matchMedia: () => ({ matches: false }), location: { search: '' } },
    setTimeout: noop, clearTimeout: noop, requestAnimationFrame: noop,
    performance: { now: () => 0 },
  };
  ctx.globalThis = ctx;
  ctx.window.document = ctx.document;
  return vm.createContext(ctx);
}

function carregar(ctx, ...arquivos) {
  for (const arquivo of arquivos) {
    vm.runInContext(fs.readFileSync(path.join(RAIZ, arquivo), 'utf8'), ctx, { filename: arquivo });
  }
  return ctx;
}

/* --- mini framework -------------------------------------------------- */
let passou = 0;
const falhas = [];

function teste(nome, fn) {
  try {
    fn();
    passou += 1;
  } catch (erro) {
    falhas.push({ nome, mensagem: erro.message });
  }
}

function quase(obtido, esperado, nome, tolerancia = 0.02) {
  if (Math.abs(obtido - esperado) > tolerancia) {
    throw new Error(`${nome}: esperado ${esperado.toFixed(2)}, obtido ${obtido.toFixed(2)}`);
  }
}

/* --- carga ----------------------------------------------------------- */
const ctxRescisao = carregar(criarContexto(),
  'assets/js/tabelas-fiscais-2026.js',
  'assets/js/calculadora-rescisao-v2.js');
vm.runInContext('globalThis.__api = { calcIRRFmensal, calcINSS, INSS_2026, IRRF_2026 };', ctxRescisao);
const rescisao = ctxRescisao.__api;

const ctxIrrf = carregar(criarContexto(),
  'assets/js/tabelas-fiscais-2026.js',
  'assets/js/calculadora-irrf.js');
vm.runInContext(
  'globalThis.__api = { calcularINSSProgressivo, calcularIRRFBruto, calcularReducaoLei15270, IRRF_CONFIG_2026 };',
  ctxIrrf);
const irrf = ctxIrrf.__api;

const fiscal = carregar(criarContexto(), 'assets/js/tabelas-fiscais-2026.js').SoulcontFiscal;

/* --- 1. tabelas vigentes --------------------------------------------- */
teste('salário mínimo e teto do INSS de 2026', () => {
  quase(fiscal.SALARIO_MINIMO, 1621.00, 'salário mínimo');
  quase(fiscal.TETO_INSS, 8475.55, 'teto do INSS');
  quase(fiscal.INSS[fiscal.INSS.length - 1].limite, 8475.55, 'última faixa');
});

teste('parâmetros do IRRF e da Lei 15.270/2025', () => {
  quase(fiscal.DEDUCAO_DEPENDENTE, 189.59, 'dedução por dependente');
  quase(fiscal.DESCONTO_SIMPLIFICADO, 607.20, 'desconto simplificado');
  quase(fiscal.REDUCAO_MAXIMA, 312.89, 'redutor máximo');
  quase(fiscal.REDUCAO_COEF_A, 978.62, 'coeficiente A');
  quase(fiscal.REDUCAO_COEF_B, 0.133145, 'coeficiente B', 1e-9);
});

teste('limite do MEI segue R$ 81.000 em 2026', () => {
  quase(fiscal.MEI.limiteAnual, 81000, 'limite MEI');
});

teste('INSS progressivo bate nos pontos conhecidos', () => {
  quase(fiscal.calcularINSS(1621.00), 121.58, 'INSS no mínimo');
  quase(fiscal.calcularINSS(20000), 988.09, 'INSS no teto');
});

/* --- 2. o bug que motivou estes testes ------------------------------- */
teste('redutor da Lei 15.270 usa o rendimento BRUTO, não a base', () => {
  // Bruto de R$ 5.500 fica na faixa de transição: 978,62 - 0,133145 x 5.500.
  quase(fiscal.calcularReducao(5500, Infinity), 246.32, 'redutor em 5.500');
  // Acima de R$ 7.350 não há redutor algum.
  quase(fiscal.calcularReducao(7800, Infinity), 0, 'redutor acima do teto');
  // Até R$ 5.000 o redutor é fixo e zera o imposto devido.
  quase(fiscal.calcularReducao(5000, Infinity), 312.89, 'redutor até 5.000');
  quase(fiscal.calcularIRRFMensal({ rendimentoBruto: 5000 }).imposto, 0, 'IRRF zerado em 5.000');
});

teste('desconto simplificado substitui as deduções legais (não soma)', () => {
  const r = fiscal.calcularIRRFMensal({ rendimentoBruto: 3000 });
  const inss = fiscal.calcularINSS(3000);
  const esperada = 3000 - Math.max(inss, 607.20);
  quase(r.baseCalculo, esperada, 'base de cálculo');
});

teste('as duas calculadoras de IRRF concordam em toda a faixa crítica', () => {
  for (const bruto of [3000, 4500, 5000, 5500, 6000, 6500, 7000, 7350, 7800, 7950, 8500, 12000, 25000]) {
    const inss = irrf.calcularINSSProgressivo(bruto);
    const deducao = Math.max(inss, irrf.IRRF_CONFIG_2026.descontoSimplificado);
    const bruta = irrf.calcularIRRFBruto(Math.max(0, bruto - deducao)).imposto;
    const referencia = Math.max(0, bruta - irrf.calcularReducaoLei15270(bruto, bruta));
    const daRescisao = rescisao.calcIRRFmensal(bruto, inss, 0, true).imposto;
    quase(daRescisao, referencia, `divergência em R$ ${bruto}`);
  }
});

/* --- 3. fonte única -------------------------------------------------- */
teste('calculadoras compartilham a MESMA tabela (sem cópias)', () => {
  if (rescisao.INSS_2026 !== ctxRescisao.SoulcontFiscal.INSS) {
    throw new Error('rescisão declara a própria tabela de INSS');
  }
  if (irrf.IRRF_CONFIG_2026.faixasIRRF !== ctxIrrf.SoulcontFiscal.IRRF_TABELA) {
    throw new Error('calculadora de IRRF declara a própria tabela');
  }
});

/* --- 4. Simples Nacional --------------------------------------------- */
teste('alíquota efetiva do Simples (Anexo III, RBT12 600k)', () => {
  const faixa = fiscal.SIMPLES.III.find((f) => 600000 <= f.limite);
  const efetiva = (600000 * faixa.aliquota - faixa.deducao) / 600000;
  quase(efetiva * 100, 10.56, 'alíquota efetiva', 0.01);
  quase(50000 * efetiva, 5280, 'DAS do mês');
});

teste('corte do Fator R em 28%', () => {
  quase(fiscal.FATOR_R_CORTE, 0.28, 'corte do Fator R', 1e-9);
});

/* --- 5. guarda contra o retorno da duplicação ------------------------ */
teste('nenhum valor fiscal escrito à mão fora da fonte única', () => {
  // Números que só podem existir em tabelas-fiscais-2026.js. Se aparecerem
  // em outro arquivo, a duplicação voltou — e com ela o risco de divergência.
  const proibidos = [
    '607.2', '189.59', '312.89', '978.62', '0.133145',
    '8475.55', '1621.00', '2428.80', '2826.65', '3751.05',
    '4664.68', '908.73', '675.49', '394.16', '182.16', '81000',
  ];
  const dir = path.join(RAIZ, 'assets', 'js');
  const reincidentes = [];

  for (const arquivo of fs.readdirSync(dir)) {
    if (!arquivo.endsWith('.js') || arquivo === 'tabelas-fiscais-2026.js') continue;
    const conteudo = fs.readFileSync(path.join(dir, arquivo), 'utf8');
    for (const valor of proibidos) {
      if (conteudo.includes(valor)) reincidentes.push(`${arquivo} contém ${valor}`);
    }
  }

  if (reincidentes.length) {
    throw new Error(`valores fiscais duplicados:\n      ${reincidentes.join('\n      ')}`);
  }
});

/* --- 6. calculadoras novas ------------------------------------------- */
teste('Fator R e Simples híbrido estão registrados no hub', () => {
  const defs = fs.readFileSync(
    path.join(RAIZ, 'assets/js/calculadora-suite-defs-tributarias.js'), 'utf8');
  const hub = fs.readFileSync(path.join(RAIZ, 'HTML/ferramentas.html'), 'utf8');

  for (const id of ['fator-r', 'simples-hibrido-ibs-cbs']) {
    if (!defs.includes(`registerDefinition('${id}'`)) {
      throw new Error(`definição ausente: ${id}`);
    }
    if (!hub.includes(`calc=${id}`)) {
      throw new Error(`card ausente no hub: ${id}`);
    }
  }
});

/* --- resultado ------------------------------------------------------- */
console.log(`\n${passou} teste(s) passaram.`);
if (falhas.length) {
  console.error(`${falhas.length} falha(s):\n`);
  for (const f of falhas) console.error(`  ✗ ${f.nome}\n    ${f.mensagem}`);
  process.exit(1);
}
console.log('Todos os testes passaram.\n');
