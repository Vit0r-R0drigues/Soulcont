/*
 * Rodapé padrão das calculadoras SoulCont.
 *
 * Preenche o elemento #calcRodape com:
 *   1. o carimbo de vigência das tabelas e a base legal da calculadora;
 *   2. o botão que apaga os dados que a calculadora guarda no navegador.
 *
 * O texto de vigência e a base legal vêm de data-attributes no próprio
 * elemento, para que cada página descreva a sua própria fundamentação:
 *
 *   <div id="calcRodape"
 *        data-vigencia="Tabelas vigentes em 2026"
 *        data-base-legal="Lei 15.270/2025; Lei 8.212/1991"></div>
 */
(function () {
    'use strict';

    /* Prefixos usados pelas calculadoras para guardar o preenchimento.
       Favoritos do hub (vl_tools_favorites_v1) são preferência de navegação,
       não dado pessoal, e por isso ficam de fora. */
    var PREFIXOS_DADOS = [
        'vl_ferias_',
        'vl_irrf_',
        'vl_rescisao_',
        'vl_suite_calculadora_'
    ];

    function chavesSalvas() {
        var achadas = [];
        try {
            for (var i = 0; i < localStorage.length; i++) {
                var chave = localStorage.key(i);
                if (!chave) continue;
                for (var p = 0; p < PREFIXOS_DADOS.length; p++) {
                    if (chave.indexOf(PREFIXOS_DADOS[p]) === 0) {
                        achadas.push(chave);
                        break;
                    }
                }
            }
        } catch (erro) {
            /* localStorage bloqueado (modo privado//cookies desativados) */
        }
        return achadas;
    }

    function limpar(feedback, botao) {
        var chaves = chavesSalvas();
        try {
            chaves.forEach(function (chave) {
                localStorage.removeItem(chave);
            });
        } catch (erro) {
            feedback.textContent = 'Não foi possível limpar: o navegador bloqueou o armazenamento local.';
            return;
        }

        feedback.textContent = chaves.length
            ? 'Dados apagados deste navegador. Recarregando...'
            : 'Não havia nada salvo neste navegador.';

        if (!chaves.length) return;

        botao.disabled = true;
        window.setTimeout(function () {
            window.location.reload();
        }, 900);
    }

    function montar() {
        var alvo = document.getElementById('calcRodape');
        if (!alvo || alvo.dataset.montado === 'true') return;
        alvo.dataset.montado = 'true';

        var vigencia = alvo.dataset.vigencia || 'Tabelas vigentes em 2026';
        var baseLegal = alvo.dataset.baseLegal || '';

        alvo.className = 'calc-rodape';

        var info = document.createElement('div');
        info.className = 'calc-rodape__info';

        var selo = document.createElement('p');
        selo.className = 'calc-rodape__vigencia';
        selo.innerHTML = '<span class="calc-rodape__ponto" aria-hidden="true"></span>' + vigencia;
        info.appendChild(selo);

        if (baseLegal) {
            var base = document.createElement('p');
            base.className = 'calc-rodape__base';
            base.innerHTML = '<strong>Base legal:</strong> ' + baseLegal;
            info.appendChild(base);
        }

        var nota = document.createElement('p');
        nota.className = 'calc-rodape__base';
        nota.textContent = 'O preenchimento fica salvo apenas neste navegador e não é enviado à SoulCont.';
        info.appendChild(nota);

        var acoes = document.createElement('div');
        acoes.className = 'calc-rodape__acoes';

        var botao = document.createElement('button');
        botao.type = 'button';
        botao.className = 'calc-rodape__botao';
        botao.textContent = 'Limpar dados salvos';

        var feedback = document.createElement('p');
        feedback.className = 'calc-rodape__feedback';
        feedback.setAttribute('role', 'status');
        feedback.setAttribute('aria-live', 'polite');

        botao.addEventListener('click', function () {
            limpar(feedback, botao);
        });

        acoes.appendChild(botao);
        acoes.appendChild(feedback);

        alvo.appendChild(info);
        alvo.appendChild(acoes);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', montar);
    } else {
        montar();
    }
})();
