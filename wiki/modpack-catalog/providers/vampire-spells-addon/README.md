# Vampire Spells Addon 0.0.9 — bridge Vampirism ↔ Iron's Spells

Status: `EXACT-RELEASE SOURCE-PINNED / BRIDGE SEMANTICS CATALOGED / IRON'S 3.16.3 RUNTIME QA PENDING`

## Estado canônico

- mod id: `vampire_spells_addon`
- JAR instalado: `vampire_spells_addon-neoforge-1.21.1-0.0.9.jar`
- versão instalada: `1.21.1-0.0.9`
- Minecraft: `1.21.1`
- loader: NeoForge
- Java: 21
- source oficial: `xsharov/VampireSpellsAddon`
- release/tag auditada: `1.21.1-0.0.9`
- source pin exato da release: `2d36e94e67611a316b7311b11e4574b499025580`
- SHA-256 do asset NeoForge publicado: `8997f71035f29e4d2fe9e37dd76ca5f4b574906d1aed0914df6c119111570fed`

A release oficial `1.21.1-0.0.9` aponta para o commit acima e publica exatamente o asset NeoForge de Minecraft 1.21.1. Esta auditoria usa esse commit como autoridade de comportamento do addon.

## Classificação correta

Vampire Spells Addon **não registra uma nova escola nem um conjunto próprio de spells**. Ele é uma bridge/overlay entre:

- Iron's Spells 'n Spellbooks, que continua autoridade do spell registry, escola, cast source, mana, cooldown e resolução do spell;
- Vampirism, que continua autoridade da identidade Vampire, `BloodStats`, consumo/restauração de blood e demais estados de facção;
- o próprio addon, que possui somente a política cross-provider de resource substitution e as alterações Blood/Holy descritas abaixo.

Portanto o catálogo do addon não deve duplicar os 110 spells base do Iron's nem tratá-los como conteúdo originado aqui. O escopo correto é documentar **quais capacidades host são alteradas e como o pipeline muda**.

## Compatibilidade declarada × pack instalado

A release declara suporte a:

| Componente | Faixa declarada pelo addon | Pack atual | Estado |
|---|---|---|---|
| NeoForge | `>=21.1.200` e `<21.2` | `21.1.248` | dentro da faixa |
| Vampirism | `>=1.10.7` e `<1.11` | `1.10.13` | dentro da faixa |
| Iron's Spells | `>=1.21.1-3.14.3` e `<1.21.1-4` | `1.21.1-3.16.3` | dentro da faixa; QA específica pendente |

O source audit do próprio addon foi feito explicitamente contra Iron's `3.16.2` e Vampirism source `1.10.13`. Como o pack usa Iron's `3.16.3`, a faixa de metadata permite a combinação, mas os mixins/reflection contracts usados pelo addon ainda precisam ser revalidados em runtime contra o JAR instalado. Até lá, qualquer integração Black Arcana que dependa dos internals específicos do addon permanece **fail-closed**.

## Blood School — escopo host atual

O Iron's base instalado possui 10 spells Blood ativos. O addon classifica dinamicamente por `SchoolType` e aplica a política de cooldown a qualquer spell Blood de Vampire.

### Substituição de mana por blood

Por default:

1. um Vampire tenta pagar normalmente a mana de um spell Blood que consome mana;
2. se a mana atual não cobre o preço integral, o addon permite fallback para blood;
3. o custo de mana é substituído por `0` somente na transação elegível;
4. o custo de blood é debitado atomicamente do recurso real do Vampirism;
5. se o pagamento integral de blood falha, o cast é impedido sem débito parcial;
6. a mesma ação não pode pagar mana e blood simultaneamente pelo bridge.

Exceções provider-native do addon:

- `irons_spellbooks:ray_of_siphoning` nunca usa resource replacement; mantém o custo normal de mana e pode restaurar blood;
- creative players são excluídos;
- cast sources que não consomem mana são excluídos;
- recasts são excluídos;
- `alwaysUseBloodForVampireBloodSpells=true` força blood-only para os casts elegíveis mesmo quando mana é suficiente.

Com os defaults da configuração, `bloodCostRatioMin` e `bloodCostRatioMax` são ambos `0.05`, então o custo efetivo padrão é `ceil(manaCost × 0.05)` blood para casts elegíveis. Esse número é configurável e não deve ser hardcoded por Black Arcana.

### Cooldown

Todo spell da Blood School castado por Vampire recebe o multiplicador configurável `vampireBloodSpellCooldownMultiplier`, default `2/3`. Isso representa cooldown final aproximadamente 1,5× mais curto.

Black Arcana não deve aplicar um segundo modificador equivalente sobre o mesmo cast sem contrato explícito de composição.

## Ray of Siphoning e Devour

### Ray of Siphoning

- ID: `irons_spellbooks:ray_of_siphoning`;
- continua pagando mana normalmente;
- restaura Vampirism blood com base em **dano de vida efetivamente entregue**, depois de absorção/processamento;
- default de restauração: `round(actualHealthDamage × 1.0)`;
- saturation default: `0.5`;
- a solicitação é limitada pela capacidade livre do blood bar;
- a animação do ray é invertida para apontar em direção ao Vampire caster.

### Devour

- ID: `irons_spellbooks:devour`;
- para Vampire, o mana price recebe multiplicador default `2.0`;
- o preço final ajustado é também a base para o eventual fallback atômico para blood;
- restaura Vampirism blood com base em dano de vida efetivamente entregue;
- default de restauração: `round(actualHealthDamage × 2.0)`;
- saturation default: `0.6`.

Nenhuma restauração deve ser calculada novamente por Black Arcana observando apenas `LivingDamageEvent` ou aumento final da barra: isso duplicaria o settlement do addon.

## Holy School — overlay confirmado

O addon também altera a relação de Vampires com spells Holy do Iron's.

### Dano Holy

- dano Holy contra NPC Vampire reconhecido pelo Vampirism é dobrado pelo addon;
- se um Vampire player for o caster de dano Holy, o dano de vida efetivamente entregue é refletido de volta ao caster;
- a reflexão usa o dano pós-processamento correlacionado, não o valor precoce do spell event.

### Cura Holy

- cura Holy em Vampire player é convertida em dano correspondente e o heal correlacionado é suprimido;
- se caster e target forem entidades distintas e o Vampire for o caster, ele também recebe a penalidade correspondente;
- o addon usa estado de correlação bounded/expirável para não suprimir uma cura futura não relacionada.

### Holy utility allowlist

Se um Vampire player tenta usar qualquer uma destas seis spells Holy, o addon cancela o pre-cast, limpa `additionalCastData` e aplica `5` de magic self-damage:

- `irons_spellbooks:angel_wing`
- `irons_spellbooks:fortify`
- `irons_spellbooks:wisp`
- `irons_spellbooks:haste`
- `irons_spellbooks:cleanse`
- `irons_spellbooks:sunbeam`

A allowlist é explícita no source 0.0.9; não deve ser estendida por nome/escola sem nova evidência.

## Authority e deduplicação

### Iron's Spells continua authority

O addon não cria segundo spell registry, segunda school Blood/Holy, segunda mana bar ou segundo cooldown engine. Eventos e mixins interceptam o pipeline do Iron's.

### Vampirism continua authority

O addon usa a API real do Vampirism para:

- identificar Vampire;
- ler blood atual/máximo;
- consumir blood;
- restaurar blood.

Não há segunda barra de blood do addon.

### Uma ação, um pipeline

A identidade causal é o cast do Iron's e seu settlement correspondente. Black Arcana não deve processar separadamente como novas ações:

- pre-cast do Iron's;
- fallback mana→blood;
- debit do Vampirism;
- cooldown event;
- Ray/Devour damage pulse;
- blood restoration result.

Esses passos pertencem ao mesmo cast/efeito causal quando correlacionados pelo addon.

## Relação com native Vampirism Actions

Native Vampire/Hunter/Lord Actions do Vampirism **não se tornam spells do Iron's** por causa deste addon. Bat, Teleport, Freeze, Rage, Half Invulnerable e demais actions continuam sob `IActionHandler`, skill gates e economia provider-native próprios.

Não aplicar automaticamente:

- mana a native actions;
- Blood School cooldown a native actions;
- fallback mana→blood a native actions;
- Holy semantics do Iron's a ações que não passam pelo spell pipeline auditado.

## Regra de integração Black Arcana

Black Arcana pode observar ou compor sobre o resultado deste bridge somente preservando:

- um cast causal;
- um resource settlement;
- Iron's como authority do spell;
- Vampirism como authority do blood;
- addon como authority desta política cross-provider específica.

É proibido criar um segundo conversor genérico mana↔blood para o mesmo cast, reembolsar blood depois do addon, cobrar blood antes do addon ou classificar a bridge como unificação global de recursos mágicos.

## QA ainda pendente

Antes de declarar runtime confirmado no pack atual, validar ao menos:

- load dedicado com NeoForge `21.1.248`, Vampirism `1.10.13` e Iron's `3.16.3`;
- resolução reflection dos contratos dos dois providers;
- mixin de affordability/cast do Iron's 3.16.3;
- mixin client do Ray 3.16.3;
- 10 Blood spells em mana suficiente/insuficiente e blood suficiente/insuficiente;
- Ray e Devour com armor, absorption, overkill e blood bar cheia;
- cooldown Blood;
- Holy damage em NPC Vampire;
- Holy reflection em Vampire caster;
- Holy healing/self-healing;
- seis Holy utility spells;
- interrupção, recast, logout, death e dimension transition com correlation state pendente.

Até essa matriz passar, o estado correto é **source-pinned / semantic contract confirmed / runtime QA pending**, não `RUNTIME CONFIRMADO`.
