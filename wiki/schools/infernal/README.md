# Magia Infernal

## Estado

`CONCEITO / PESQUISA — NÃO IMPLEMENTADO COMO ESCOLA BLACK ARCANA`

## Identidade

Magia Infernal representa poder do Nether obtido por pactos, combustão sobrenatural, pressão térmica, ruína e uma fonte física exclusiva chamada **Lava Infernal**. Deve ser devastadora e cara, mas não simplesmente Fire Magic com números maiores.

## Deduplicação obrigatória

O pack já possui spells Ignis via Cataclysm: Spellbooks, incluindo historicamente `Infernal Strike`, `Incineration`, `Ashen Breath`, `Bone Storm`, `Piercing Bone`, `Hellish Blade` e `Unfolding Coruscation`. Essas entradas devem ser catalogadas primeiro e usadas como provider-native quando cobrirem o efeito pretendido.

Também existem Cataclysm: Ignis Soulfires e Ignis Soulfires: Spellbooks, ligados a Souled Ignitium/soulfire. A nova escola não deve clonar esse conteúdo.

## Host

Preferência: **Iron's Spells 'n Spellbooks** como superfície de escola/spell, com Black Arcana como integração de fonte, authority, world safety, bindings e efeitos que o provider não possui nativamente.

## Fonte — Lava Infernal

Spells comuns podem continuar seguindo a economia do provider quando forem spells nativos existentes. A identidade Black Arcana de alto nível usa uma fonte adicional/alternativa de Lava Infernal armazenada em `mB` no Nether.

Regras:

- Lava Infernal é recurso distinto de lava vanilla, Soul Energy, mana e Black Flame;
- só pode ser criada/coletada/armazenada de forma válida no Nether;
- não pode ser transportada para fora do Nether por bucket, tank móvel, portal, contraption ou serialização indireta;
- storage fora do Nether rejeita inserção/uso e nunca converte silenciosamente o fluido;
- vínculo cross-dimension com fonte infernal é proibido por padrão;
- dimensão inválida = fail-closed, sem cobrança parcial e sem cast.

## Fantasia mecânica

A escola deve cobrir nichos como:

- jatos/ondas de hellfire;
- fissuras e erupções;
- impacto térmico + mágico;
- armas infernais temporárias quando não redundantes;
- marcas que tornam o alvo suscetível a efeitos infernais;
- zonas de combustão sobrenatural;
- correntes/pactos e invocação temática se não duplicarem Goety;
- spells Miracle-tier equivalentes em destruição, com custos enormes de fonte.

## Dano

`HELLFIRE` deve possuir identidade própria e não ser tratado como simples `minecraft:on_fire`.

Uma implementação futura pode decompor o resultado em componentes físicos/térmicos/mágicos, mas:

- fire immunity não deve ser ignorada silenciosamente;
- se houver componente mágico que permaneça após resistência a fogo, isso precisa estar explícito na página do spell e em tags/resistências do RPG;
- não criar dano absoluto que burle todas as defenses;
- boss/PvP multipliers e caps permanecem obrigatórios.

## Relação com Black Flame

Black Flame e Magia Infernal são diferentes:

- **Black Flame** = fogo proibido/soul-fire do Black Arcana com frontier/mutation/lifecycle próprios;
- **Infernal** = poder ligado ao Nether e Lava Infernal, com estética térmica/vermelha e economia de fonte física.

Um spell não pode ser renomeado entre as duas famílias sem semântica explícita.

## Obtenção e progressão — direção

A progressão deve exigir presença real no Nether e infraestrutura. Possíveis etapas a validar:

1. descobrir conhecimento infernal/ritual;
2. obter catalisador ligado a Ignis/Soulfire/provider existente quando apropriado;
3. construir reservatório/fornalha infernal no Nether;
4. converter/coletar Lava Infernal de forma bounded;
5. criar vínculo do caster com a estrutura;
6. desbloquear tiers superiores conforme capacidade, risco e progressão do RPG Skill Tree.

Nenhuma etapa está aprovada como receita final até a auditoria dos providers existentes terminar.

## VFX

Lava vermelho-escura mais saturada que vanilla, emissivo forte, veios negros, brasas densas, miragem térmica, jatos volumétricos e impactos com geometria infernal. Visual deve diferenciar claramente lava vanilla, Soul Fire e Black Flame.

## Próximos gates

- catálogo completo de spells Ignis/Cataclysm atuais;
- auditar Soul Fire'd e demais providers de hellfire/soulfire da modlist;
- verificar APIs de fluid/storage/dimension;
- fechar multiblock/reservatório;
- definir spells de delta real após deduplicação;
- Stage 08 para números finais.
