# Iron's Spells 3.16.3 — Auditoria Blood

## Estado

`10/10 SPELLS DO REGISTRY INDIVIDUALIZADOS / SOURCE AUDITADO`

Todos os 10 spells Blood registrados no Iron's 3.16.3 foram conferidos diretamente no source oficial 1.21.

| Spell | ID | Raridade | Max Lv | Mana base | Mana/Lv | CD | Função-chave |
|---|---|---:|---:|---:|---:|---:|---|
| Acupuncture | `acupuncture` | Rare | 10 | 25 | 5 | 20s | needles em torno do alvo |
| Blood Needles | `blood_needles` | Uncommon | 10 | 25 | 5 | 5 needles + 25% lifesteal + i-frames 0 |
| Blood Slash | `blood_slash` | Rare | 5 | 25 | 5 | slash projectile + 15% lifesteal |
| Blood Step | `blood_step` | Uncommon | 5 | 30 | 10 | 12s | teleport + 5s true invisibility |
| Devour | `devour` | Uncommon | 10 | 25 | 4 | 20s | target attack + 15% lifesteal + kill bonus path |
| Heartstop | `heartstop` | Rare | 5 | 100 | 10 | 120s | aplica HEARTSTOP ao próprio caster |
| Raise Dead | `raise_dead` | Uncommon | 6 | 50 | 10 | 150s | summons temporários, SpellSummonEvent |
| Ray of Siphoning | `ray_of_siphoning` | Common | 10 | 8 | 1 | 15s | ray contínuo + 100% lifesteal |
| Wither Skull | `wither_skull` | Uncommon | 10 | 20 | 2 | 1s | wither-skull projectile |
| Sacrifice | `sacrifice` | Rare | 5 | 25 | 5 | 1s | explode summon mágico próprio |

## Descoberta obrigatória para o redesign hemático

**Todos os 10 spells usam a economia de mana normal do Iron's no source 3.16.3.**

Portanto a regra do projeto:

> `Blood magic nunca usa mana normal`

é um **redesign deliberado de custo** que precisa de integração técnica. Não podemos documentá-la como comportamento atual do provider.

## Estratégia correta de integração

Objetivo: preservar o máximo possível do spell provider-native e trocar a camada de combustível.

Pipeline pretendido:

1. jogador solicita um Blood spell Iron's;
2. Black Arcana/Blood adapter calcula o custo hemático equivalente aprovado;
3. normal mana **não é debitada**;
4. resolver fontes hemáticas válidas: corpo, target autorizado, link ou reservatório;
5. reservar sangue mB/health causalmente;
6. deixar o Iron's executar targeting/projectile/effect/summon/lifesteal quando o hook permitir;
7. no cast commit, consumir a reserva hemática;
8. falha anterior ao commit → refund;
9. nenhuma cobrança duplicada de mana + sangue.

Se a API do Iron's não oferecer um boundary seguro para substituir custo sem quebrar casting, o componente fica `BLOQUEADO / FAIL-CLOSED` até existir um adapter verificável. Não criar segundo spell clone apenas para contornar a API.

## Conversão mana atual → sangue

Os números de mana acima são **baseline de peso/custo**, não razão automática para mB.

A conversão `mana → mB` deve ser fechada no balanceamento junto com:
- custo em sangue próprio;
- eficiência do reservatório;
- custo de sangue vinculado;
- sangue alterado/vampírico;
- risco de matar a própria fonte;
- boss/PvP/anti-farm;
- lifesteal loops.

Não adotar `1 mana = 1 mB` ou qualquer razão arbitrária antes dessa etapa.

## Anti-loop importante

Blood Needles/Blood Slash/Devour/Ray of Siphoning já devolvem vida por lifesteal. **Vida recuperada não vira sangue armazenado automaticamente.** Caso contrário o caster poderia pagar sangue → causar dano → recuperar vida → converter vida em mB → sustentar loop quase gratuito.

Toda coleta para reservatório precisa ser uma transação própria, com fonte elegível, teto e causalidade.

## Sangue x vitalidade — casos do provider

- `Sacrifice` sacrifica um `IMagicSummon` próprio. Isso não prova que o summon possui sangue.
- `Raise Dead` invoca skeleton/zombie; undead não devem ser classificados como sangue fisiológico normal por nome de escola.
- `Wither Skull` é Blood-school no registry, mas o efeito não prova fisiologia hemática.
- `Heartstop` aplica um efeito ao próprio caster; o nome não prova ataque cardíaco em target.

Logo a classificação `HEMATIC_BLOOD / ALTERED_BLOOD / NO_BLOOD / UNKNOWN` continua obrigatória e independente da escola do spell.

## Hooks úteis já encontrados

- `SpellSummonEvent` em Raise Dead;
- Iron's damage sources carregam lifesteal explícito para Blood Needles, Blood Slash, Devour e Ray of Siphoning;
- Blood Step reutiliza safety/teleport helpers do próprio Iron's;
- Sacrifice revalida `IMagicSummon` + summoner ownership antes do settlement.

## Deduplicação com Black Arcana já existente

- `Ray of Siphoning` ≠ `Sanguine Harvest`: ray contínuo provider-native vs pulse bounded/anti-farm do Black Arcana.
- `Sacrifice` ocupa servant-to-explosion; não criar outro igual em Infernal/Witchcraft.
- `Raise Dead` ocupa necromancy summon dentro do Iron's; comparar Goety/Eidolon antes de adicionar qualquer raise-dead novo.
- `Blood Step` ocupa blood teleport/evasion; não criar outro blink hemático.

## Próxima etapa Blood

Antes de implementar a economia zero-mana:

1. auditar API/hook real de cost resolution do Iron's 3.16.3;
2. auditar Vampire Spells Addon/Bloodlines/Vampirism para saber quais custos já são traduzidos;
3. fechar `mB` balance;
4. especificar reservoir multiblock e collection routes;
5. testar ausência de mana debit;
6. testar transactional reserve/refund;
7. testar entidades `NO_BLOOD`, incluindo Iron Golem;
8. testar lifesteal sem loop de recurso.
