# Pausa Espiritual — feed para Alexa

Esse projetinho é irmão do `conhecimento-geral-feed`, mas separado: publica,
todo dia, uma pausa guiada de ~5 minutos (respiração + mantra/reflexão,
estilo genérico e universal, sem ligação com nenhuma tradição religiosa
específica) num link público que a Alexa lê em voz alta. Você mesmo decide
depois em que ordem ela entra na sua Rotina da manhã (antes ou depois da
cápsula de Conhecimento Geral, por exemplo).

Não gera conteúdo com IA sozinho — só roda uma vez por dia e avança pra
próxima pausa de um banco fixo de 5 roteiros (`content.json`), que rotaciona
em ciclo (dia 6 repete o roteiro do dia 1, e assim por diante).

## Como os arquivos se encaixam

- `content.json` — o banco de pausas (categoria + texto). 5 roteiros:
  respiração e intenção do dia, respiração 4-7-8 e gratidão, escaneamento
  corporal e presença, respiração quadrada e clareza, respiração profunda e
  gentileza consigo mesmo.
- `state.json` — só guarda qual é o índice da próxima pausa a publicar.
- `build_feed.py` — lê os dois de cima e escreve `docs/feed.json` no
  formato exigido pela Amazon (Flash Briefing Skill API).
- `docs/feed.json` — o arquivo que a Alexa realmente consome. Fica
  publicado via GitHub Pages.
- `.github/workflows/daily-feed.yml` — roda `build_feed.py` automaticamente
  todo dia às 05:00 (horário de Brasília), sem precisar mexer em nada.

## Passo 1 — Criar o repositório no GitHub

1. Crie um repositório novo (separado do `conhecimento-geral-feed` — pode
   ser público ou privado, mas privado exige plano pago pra Pages; se for
   usar o plano gratuito, deixe público, o conteúdo não tem nada sensível).
2. Suba todos os arquivos desta pasta pra esse repositório, mantendo a
   estrutura de pastas.

**Atenção com a pasta `.github/workflows`**: da última vez, o arraste de
pastas pelo gerenciador de arquivos não subiu essa pasta porque ela começa
com ponto (fica "escondida" no seu sistema). Se isso acontecer de novo, é só
criar o arquivo manualmente pela própria interface do GitHub: **Add file →
Create new file**, e no campo do nome digite o caminho completo
`.github/workflows/daily-feed.yml` (o GitHub cria as pastas sozinho a
partir das barras) e cole o conteúdo desse arquivo.

## Passo 2 — Ativar o GitHub Pages

No repositório: **Settings → Pages → Source** → selecione a branch `main`
e a pasta `/docs`. Depois de salvar, o GitHub te dá uma URL parecida com:

```
https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/
```

O feed em si fica em `.../feed.json` (ex:
`https://SEU-USUARIO.github.io/pausa-espiritual-feed/feed.json`).

Depois de saber a URL de verdade, atualize a constante `REDIRECTION_URL`
no topo do `build_feed.py` com ela (é só o link de "saiba mais" que
aparece no app Alexa, não afeta o áudio).

## Passo 3 — Conferir se a automação diária está ativa

A Action em `.github/workflows/daily-feed.yml` já vem configurada pra
rodar sozinha todo dia. Pra confirmar: aba **Actions** do repositório →
deve aparecer "Atualizar pausa diária (Pausa Espiritual)" listado. Dá pra
rodar manualmente uma vez ali (botão "Run workflow") só pra testar antes de
configurar a Alexa.

## Passo 4 — Criar uma segunda Flash Briefing Skill

Essa pausa usa uma skill separada da de Conhecimento Geral (assim você
controla a ordem das duas de forma independente na sua Rotina).

1. Acesse o [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask)
   com sua conta Amazon.
2. Crie uma **nova** skill do tipo **Flash Briefing** (não reaproveite a
   que já existe — precisa ser outra, senão uma sobrescreve a outra na
   Rotina).
3. Adicione um "feed" apontando pra URL do `feed.json` desse repositório
   (a do Passo 2).
4. Configure o feed como **Text** (não Audio) — a Alexa usa text-to-speech
   pra ler o `mainText`.
5. Publique a skill em modo de desenvolvimento/privado (não precisa
   certificação pública, é só pra uso pessoal).

## Passo 5 — Colocar na Rotina da manhã

No app Alexa: **Mais → Rotinas** → sua rotina da manhã → adicione uma nova
ação **Flash Briefing** e selecione essa nova skill. Você escolhe a ordem
entre ela e a do Conhecimento Geral arrastando as ações dentro da Rotina.

## Manutenção

O banco tem só 5 roteiros fixos (não muda a cada 12 dias como o de
Conhecimento Geral, já que são práticas atemporais de respiração — não
"conteúdo" que precisa de novidade). Se um dia você quiser trocar ou
adicionar roteiros novos, é só:

1. Editar/adicionar itens em `content.json` (mesmo formato: `categoria` e
   `texto`, até ~4500 caracteres cada).
2. Dar commit/push — a Action já continua rotacionando normalmente a
   partir daí.
