# Registros DNS pendentes — proteção contra falsificação de e-mail

Estes são os **únicos itens da auditoria que não podem ser resolvidos pelo
código**. Precisam ser criados no painel de DNS de cada domínio.

Situação verificada em **15/08/2026**.

| Domínio | SPF | DMARC | MX | Risco |
|---|---|---|---|---|
| `soulcontt.com.br` (site) | ❌ ausente | ❌ ausente | ❌ ausente | **Alto** — qualquer um pode enviar e-mail em nome do domínio |
| `soulcont.com` (e-mail publicado no site, 155×) | `~all` (softfail) | ❌ ausente | Google | **Alto** — sem política de rejeição |
| `soulcont.com.br` | `-all` ✅ | `p=none` (só monitora) | — | Médio |
| `vlcontabilidadeempresarial.com.br` | `~all` | ❌ ausente | Zoho | Médio |

Por que isso importa mais para um escritório de contabilidade: o golpe mais
comum do setor é o e-mail falsificado em nome do contador pedindo ao cliente
que "atualize os dados bancários do boleto". Sem SPF e DMARC, esse e-mail
chega à caixa de entrada sem nenhum aviso.

---

## 1. `soulcontt.com.br` — bloqueio total (prioridade máxima)

Este domínio **não envia e-mail** (não tem MX). O bloqueio total é seguro e
não quebra nada.

```
Tipo: TXT
Nome: @
Valor: v=spf1 -all
```

```
Tipo: TXT
Nome: _dmarc
Valor: v=DMARC1; p=reject; rua=mailto:contato@soulcont.com; aspf=s; adkim=s
```

```
Tipo: TXT
Nome: *._domainkey
Valor: v=DKIM1; p=
```

O terceiro registro declara que nenhuma chave DKIM é válida para o domínio,
fechando o último caminho de falsificação.

---

## 2. `soulcont.com` — domínio do e-mail real (Google Workspace)

**Não pule as etapas.** Começar direto em `p=reject` pode derrubar e-mail
legítimo. Faça a escalada:

**Etapa 1 — monitorar (agora):**

```
Tipo: TXT
Nome: _dmarc
Valor: v=DMARC1; p=none; rua=mailto:contato@soulcont.com; fo=1
```

**Etapa 2 — endurecer o SPF (agora):** trocar `~all` por `-all`, já que só o
Google envia por este domínio.

```
Tipo: TXT
Nome: @
Valor: v=spf1 include:_spf.google.com -all
```

**Etapa 3 — confirmar o DKIM:** no Admin do Google Workspace, em
*Apps → Google Workspace → Gmail → Autenticar e-mail*, gerar a chave e
publicar o TXT indicado. Sem DKIM, o DMARC fica frágil.

**Etapa 4 — após 2 a 4 semanas** lendo os relatórios e confirmando que só
o Google aparece como remetente:

```
Valor: v=DMARC1; p=quarantine; rua=mailto:contato@soulcont.com; pct=100
```

**Etapa 5 — mais 2 a 4 semanas depois:**

```
Valor: v=DMARC1; p=reject; rua=mailto:contato@soulcont.com
```

---

## 3. `soulcont.com.br` — sair do modo monitoramento

O SPF já está correto (`-all`). Falta endurecer o DMARC pela mesma escalada
do item 2: `p=none` → `p=quarantine` → `p=reject`.

---

## 4. `vlcontabilidadeempresarial.com.br` — criar DMARC (Zoho)

```
Tipo: TXT
Nome: _dmarc
Valor: v=DMARC1; p=none; rua=mailto:contato@soulcont.com; fo=1
```

Confirmar o DKIM no painel do Zoho e depois seguir a mesma escalada até
`p=reject`. O SPF pode ir para `-all` quando confirmado que só o Zoho envia.

---

## Como conferir depois de publicar

```bash
nslookup -type=TXT soulcontt.com.br
nslookup -type=TXT _dmarc.soulcontt.com.br
nslookup -type=TXT _dmarc.soulcont.com
```

A propagação leva de alguns minutos a algumas horas.

---

## O que já foi resolvido no código

Estes itens da auditoria **não dependem de DNS** e já estão aplicados neste
repositório:

- Cabeçalhos de segurança (CSP, HSTS, nosniff, frame-ancestors,
  Referrer-Policy, Permissions-Policy) gerados em `cloudflare/build-static.mjs`
- Recursos de CDN com versão fixada e SRI (`integrity`)
- `/.well-known/security.txt`
- Política de privacidade com base legal, prazo de guarda, encarregado (DPO)
  e a lista de operadores de dados, incluindo o forms.app
- Botão "Limpar dados salvos" nas calculadoras
