# Migração VL Contabilidade para SoulCont

O arquivo `cloudflare-vl-to-soulcont.csv` contém os redirecionamentos permanentes
do domínio antigo para os destinos equivalentes na SoulCont.

## Antes de ativar

1. Copie para a Cloudflare todos os registros DNS existentes no provedor atual,
   principalmente MX, SPF, DKIM, DMARC e verificações do Zoho, OpenAI e Facebook.
2. Confirme que o e-mail do domínio antigo continua recebendo e enviando mensagens.
3. Importe o CSV em **Rules → Redirects → Bulk Redirects**.
4. Crie e habilite a regra que utiliza a lista importada.
5. Somente depois altere os nameservers no Registro.br.

O CSV não possui cabeçalho, segue a ordem exigida pela Cloudflare e configura:

- código HTTP 301;
- preservação da query string;
- correspondências explícitas para o domínio raiz e `www`;
- sem redirecionamento genérico de URLs desconhecidas.

## Verificação

Após a propagação:

- teste HTTP e HTTPS nos dois hosts;
- confirme um único salto 301;
- confirme HTTP 200 em cada destino;
- verifique os dois domínios no Search Console;
- solicite a alteração de endereço apenas depois que todos os 301 estiverem ativos;
- mantenha domínio e redirecionamentos por pelo menos 12 meses.

Documentação: <https://developers.cloudflare.com/rules/url-forwarding/bulk-redirects/reference/csv-file-format/>
