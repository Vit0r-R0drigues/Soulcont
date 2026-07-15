document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('whatsappForm');
    const submitButton = form ? form.querySelector('.whatsapp-submit') : null;
    const formStatus = document.getElementById('form-status');
    const destinationField = document.getElementById('destinoWhatsApp');

    if (!form || !destinationField) {
        return;
    }

    form.addEventListener('submit', (event) => {
        event.preventDefault();

        if (!form.checkValidity()) {
            if (formStatus) {
                formStatus.textContent = 'Revise os campos obrigatórios antes de continuar.';
            }
            form.reportValidity();
            return;
        }

        const telefoneDestino = destinationField.value.replace(/\D/g, '');
        const destinoSelecionado = destinationField.options[destinationField.selectedIndex]?.text.trim() || '';

        if (!telefoneDestino) {
            if (formStatus) {
                formStatus.textContent = 'Escolha o WhatsApp de São Paulo ou do Ceará para continuar.';
            }
            destinationField.focus();
            return;
        }

        if (submitButton) {
            submitButton.classList.add('is-submitting');
            submitButton.setAttribute('aria-busy', 'true');
        }

        if (formStatus) {
            formStatus.textContent = 'Abrindo o WhatsApp escolhido com a sua mensagem. Você poderá revisar tudo antes de enviar.';
        }

        const campos = {
            nome: document.getElementById('nome')?.value.trim() || '',
            telefone: document.getElementById('telefone')?.value.trim() || '',
            email: document.getElementById('email')?.value.trim() || '',
            empresa: document.getElementById('empresa')?.value.trim() || '',
            objetivo: document.getElementById('objetivo')?.value.trim() || '',
            momento: document.getElementById('momento')?.value.trim() || '',
            mensagem: document.getElementById('mensagem')?.value.trim() || ''
        };

        const linhas = [
            'Olá! Quero falar com a SoulCont.',
            `Canal escolhido: ${destinoSelecionado}`,
            'Origem: Site SoulCont (soulcontt.com.br)',
            `Página: ${document.title}`,
            campos.nome ? `Nome: ${campos.nome}` : '',
            campos.telefone ? `Telefone: ${campos.telefone}` : '',
            campos.email ? `E-mail: ${campos.email}` : '',
            campos.empresa ? `Empresa ou atividade: ${campos.empresa}` : '',
            campos.objetivo ? `Objetivo principal: ${campos.objetivo}` : '',
            campos.momento ? `Momento atual: ${campos.momento}` : '',
            campos.mensagem ? `Contexto: ${campos.mensagem}` : '',
            '',
            'Gostaria de entender o melhor próximo passo com a SoulCont.'
        ].filter(Boolean);

        const url = `https://wa.me/${telefoneDestino}?text=${encodeURIComponent(linhas.join('\n'))}`;
        window.setTimeout(() => {
            window.location.href = url;
        }, 120);
    });
});
