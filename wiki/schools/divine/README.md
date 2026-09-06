# Magia Divina / Celestial

## Estado

`CONCEITO / PESQUISA — NÃO IMPLEMENTADO COMO NOVA ESCOLA BLACK ARCANA`

## Premissa

A fantasia é magia dos céus, consagração, julgamento, proteção e milagres **sem depender do Aether**. O Overworld já oferece céu, ciclo solar/lunar, estrelas, altitude, clima e locais consagrados suficientes para sustentar essa identidade.

## Providers existentes que devem vir primeiro

### Paladin Spells

O addon instalado já fornece Holy gameplay no Iron's e deve continuar como provider-native para seus spells atuais:

- Bulwark;
- Taunt;
- Sworn Protector;
- Bedrock Skin;
- Ram.

A nova disciplina não deve recriar escudo de armadura, taunt, redirecionamento de dano, imobilização defensiva ou dash de armadura com outro nome.

### Asterism Arcanum

Já existe escola Astral no Iron's baseada em estrelas e energia celeste. O catálogo deve separar `ASTRAL` de `DIVINE/HOLY`: compartilhar céu/estrelas não torna as duas escolas equivalentes.

### Eidolon: Repraised

A teurgia já cobre ritos, altares, orações/oferendas e caminhos luminosos/sombrios. Quando a fantasia exigir liturgia/rito, preferir integração com essa autoridade em vez de duplicar um segundo sistema de altar genérico.

## Host

Preferência para spells ativos: **Iron's Spells / Holy ecosystem**. Black Arcana entra como compositor de regras, sanctums, miracles, safety, domains e bridges quando houver delta real.

## Identidade mecânica

Divina deve ir além de 'heal + dano amarelo'. Nichos candidatos após deduplicação:

- feixes verticais de julgamento;
- banimento/repulsão de entidades explicitamente elegíveis;
- sanctification de área;
- proteção por juramento/consagração;
- revelação/visão celeste;
- intervenção contra maldições/efeitos profanos;
- marcas de graça e condenação;
- criação de zonas onde regras Holy específicas são impostas;
- milagres de tier extremo com preparação e recurso especial.

## Recurso

Spells normais da escola podem usar a mana do Iron's para permanecer integrados ao ecossistema. Para evitar que os maiores milagres virem apenas 'spell com custo 900 de mana', propõe-se uma camada adicional para ultimates:

**Ressonância Celestial** — carga armazenada em um `Sanctum Core`/observatório consagrado.

Ela não é uma segunda mana para todos os spells. Serve somente como requisito/custo de `MIRACLE_TIER`.

## Como obter Ressonância Celestial sem Aether

Direção preferencial:

- estrutura precisa de visão real do céu/condições válidas;
- alinhamento solar, lunar ou astral funciona como gate;
- ritual/consagração explícita gera a carga;
- itens/ações Holy provider-native podem participar quando houver hook causal;
- eventos celestes podem aumentar eficiência, nunca criar recurso infinito sem ação;
- Asterism pode fornecer contexto astral, mas não deve ter seus recursos convertidos genericamente sem API/contrato.

`Sky exposure` é condição, não gerador passivo infinito.

## Sanctum Core

Conceito de infraestrutura:

`CASTER ⇄ CONSECRATED LINK ⇄ SANCTUM CORE ⇄ CELESTIAL RESONANCE`

O Sanctum possui owner, capacidade, carga real, condições de céu e política de vínculo. Diferente do sangue e da Lava Infernal, a unidade final ainda está `TBD` e não deve ser chamada de mB se não for fluido.

## Ordem x Divina

- **Ordem**: lei, geometria, estabilidade, selos e estrutura arcana.
- **Divina**: graça, julgamento, consagração, céu e milagres.

Um círculo perfeito não é automaticamente Holy; um raio celestial não é automaticamente Order.

## Holy x Astral

- **Holy/Divine** responde a consagração, juramentos, graça/profanidade e efeitos sagrados.
- **Astral** responde a estrelas/cosmos e identidade própria do Asterism.

Poderes híbridos podem existir apenas quando a página declarar os dois providers/tags e a causalidade for verificável.

## VFX

Feixes do céu, halos, constelações, prismas, círculos luminosos, partículas de poeira estelar, sigilos Holy, raios volumétricos e impactos que iluminem a cena sem depender de uma dimensão celestial externa.

## Próximos gates

- catalogar todos os Holy spells existentes no Iron's/addons;
- catalogar Asterism e separar sobreposição Astral;
- auditar Eidolon theurgy;
- verificar todos os addons que já adicionem cura, purificação, smite/holy beam ou banishment;
- selecionar somente spells com delta mecânico real;
- fechar a economia de Miracle-tier e progressão no Stage 08.
