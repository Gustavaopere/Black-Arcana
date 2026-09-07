# Progressão Empty

## Objetivo do pipeline

As três spells Empty (`drained`, `dullard`, `doorway_effect`) custam 0 mana, mas não podem ser lançadas sem `dreamless_spells:emptied`.

A authority do gate é Dreamless: `checkPreCastConditions` consulta diretamente o MobEffect.

## 1. Empty Gem — focus da escola

`dreamless_spells:empty_gem` pertence a:

- `dreamless_spells:empty_focus`;
- `irons_spellbooks:school_focus`.

Receita 1.1.9 confirmada, shapeless:

- 1× `dreamless_spells:arcane_gem`;
- 1× `dreamless_spells:pavarium_nugget`;
- resultado: 1× `dreamless_spells:empty_gem`.

O Empty Gem é, portanto, a peça provider-native para selecionar a escola Empty em sistemas do Iron's baseados em school focus.

## 2. Empty Rune

`dreamless_spells:empty_rune` é um item registrado e entra em `irons_spellbooks:inscribed_runes`.

Entretanto, no source 1.1.9 auditado não foi localizada uma rota que o produza em survival:

- nenhuma recipe `empty_rune`;
- nenhum loot table contendo `empty_rune`;
- nenhum event/provider específico de obtenção localizado.

O Iron's 3.16.3 cria suas runas escolares com receitas explícitas próprias, normalmente Blank Rune + focus/material escolar. A tag `inscribed_runes` não gera automaticamente uma receita para addon runes.

Estado canônico: **EMPTY RUNE SURVIVAL ACQUISITION NÃO VERIFICADA**.

Não inventar uma receita Black Arcana enquanto essa lacuna não for tratada como decisão de integração/design.

## 3. Empty Priest

As peças Empty Priest são smithing transforms usando `empty_rune` como template e as peças Wizard do Iron's como base.

O full set aplica `Emptied` por 200 ticks, amplifier 3, quando o player ainda não possui o efeito.

## 4. Empty Brawler

As peças Empty Brawler são derivadas das peças Empty Priest, novamente usando `empty_rune`, com Iron Sword como addition no smithing.

O full set também aplica o mesmo `Emptied` 200 ticks/amplifier 3.

## 5. Empty Hunter

As peças Empty Hunter são derivadas das peças Empty Priest, novamente usando `empty_rune`, com Bow como addition no smithing.

O full set também aplica o mesmo `Emptied` 200 ticks/amplifier 3.

## 6. Gate de cast

Com `Emptied` ativo:

- Drained pode iniciar targeting/cast;
- Dullard pode iniciar targeting/cast;
- Doorway Effect pode iniciar targeting/cast.

Sem `Emptied`, o pre-cast falha e o player recebe a mensagem `Your Mana is not truly empty...`.

Durante o `onCast`, o source ainda verifica novamente `Emptied` e usa a mensagem `Your Mana is Truly Empty!` quando o gate continua satisfeito.

## 7. Persistência e anti-abuso

A armadura só **adiciona** Emptied se o efeito estiver ausente. Não foi localizado handler que remova imediatamente Emptied ao quebrar o full set.

Consequência a validar:

1. equipar full set;
2. receber Emptied por até 200 ticks;
3. retirar uma peça ou todo o set;
4. tentar uma spell Empty antes de o efeito expirar.

Se funcionar, existe uma janela provider-native de swap de até ~10 s. Black Arcana não deve mascarar esse comportamento com remoção externa sem decisão explícita.

## 8. Efeito sistêmico do amplifier 3

O effect declara, por unidade de amplifier scaling:

- +25% base Spell Resist;
- +5% base Empty Spell Power;
- -25% base Max Mana.

Aplicado com amplifier 3, o comportamento padrão de MobEffect escala por 4, resultando nominalmente em:

- +100% base Spell Resist;
- +20% base Empty Spell Power;
- -100% base Max Mana.

Isso explica por que as spells Empty custam 0 mana. O valor final de Max Mana no modpack pode continuar diferente de zero por causa de outras operações/modifiers e deve ser medido em runtime.