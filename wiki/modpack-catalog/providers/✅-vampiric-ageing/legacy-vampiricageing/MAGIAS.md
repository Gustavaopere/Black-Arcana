# Vampiric Ageing 1.21-1.4.21 — magias e poderes

Source authority: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`.

## Classificação correta

Vampiric Ageing **não registra spells próprios em um spell registry**. Sua superfície sobrenatural é composta por Age Ranks, passivos e **9 Actions** provider-native (com Werewolves instalado), expostas por **10 Skills** controladas pelo sistema de ageing.

Este arquivo cumpre o índice `MAGIAS.md` da Wiki sem chamar Actions de spells. Valores abaixo são defaults source-level e podem ser alterados por configuração.

## Vampire

### Celerity

- Action: `vampiricageing:celerity_action`
- Skill: `vampiricageing:celerity_skill`
- default Age: **1**
- cooldown: **60 s**
- duração: **8 s**
- efeito: Movement Speed por modifier provider-owned.
- observação: o config default 1.025 é usado diretamente como `ADD_MULTIPLIED_TOTAL`; percentual efetivo requer runtime QA.

### Step Assist

- Action: `vampiricageing:step_assist_action`
- Skill: `vampiricageing:step_assist_skill`
- default Age: **2**
- efeito: **+0.5 Step Height**
- default cooldown: 0
- duração default: efetivamente muito longa via configuração clamped.
- cooldown não-zero possui mismatch de unidades source-level.

### Blood Tap / Drain Blood

- Action: `vampiricageing:drain_blood_action`
- Skill: `vampiricageing:blood_drain_skill`
- default Age: **3**
- cooldown: **150 s**
- duração: **45 s**
- efeito: ataques durante a janela usam o pipeline de bite do Vampirism para drenar sangue do alvo e liquidar o ganho via `VampirePlayer.drinkBlood(...)`.
- não possui dano extra próprio na classe da Action; o dano causador é o ataque que dispara o hook.

### Water Walking

- Action: `vampiricageing:water_walking_action`
- Skill: `vampiricageing:water_walking_skill`
- default Age: **4**
- cooldown default: **0**
- duração default: configuração `Integer.MAX_VALUE` clamped
- efeito: ativa o estado provider-owned que permite a mecânica de andar sobre água.

## Hunter

### Tainted Blood

- Skill: `vampiricageing:tainted_blood_skill`
- não é uma Action
- default base Age para acesso: **2**
- introduz o estado Tainted Blood usado para cumulative Tainted Age e para progressão de habilidades Hunter avançadas.

### Step Assist Hunter

- Action: `vampiricageing:step_assist_hunter_action`
- Skill: `vampiricageing:step_assist_hunter_skill`
- default base Age: **4**
- efeito: **+0.5 Step Height**
- default cooldown: 0
- duração default: efetivamente muito longa via config clamped
- cooldown não-zero possui mismatch de unidades source-level.

### Wise Eye

- Action: `vampiricageing:hunter_wise_eye_action`
- Skill: `vampiricageing:wise_eye_skill`
- default base Age: **5**
- config de cooldown: **10**
- config de duração: **120**, mas **não é usada por `getDuration()` na build auditada**
- efeito: bypass de invisibilidade; slowdown default de **-0.95 `ADD_MULTIPLIED_TOTAL`** enquanto ativo.
- timing exato: runtime QA obrigatório.

### Hunter Teleport

- Action: `vampiricageing:hunter_teleport_action`
- Skill: `vampiricageing:hunter_teleport_skill`
- default cumulative Tainted Age: **8**
- cooldown: **20 s**
- range: **35 blocos**
- bloqueado durante ageing Bat Mode
- valida destino contra miss, colisão e líquido antes do teleport provider-owned.

### Limited Bat Mode

- Action: `vampiricageing:limited_hunter_batmode_action`
- Skill: `vampiricageing:limited_bat_mode_skill`
- default cumulative Tainted Age: **10**
- cooldown: **120 s**
- duração: **240 s**
- flight speed: **0.02**
- exhaustion adicional: **0.008** por update provider
- efeitos: voo, dimensões/pose de bat, Armor e Armor Toughness `-1 ADD_MULTIPLIED_TOTAL` durante a forma.
- bloqueios incluem água, End, dimensão da blacklist do Vampirism e veículo.
- transformação permanente usa duração configurada extremamente longa/clamped.

## Werewolf

### Improved Senses

- Action: `vampiricageing:improved_senses_action`
- Skill: `vampiricageing:improved_senses_skill`
- presente porque Werewolves está instalado
- default Age: **5**
- gate adicional default: Werewolves `SENSE` skill
- config cooldown: **10** retornado diretamente pela Action
- duração: **120** convertido para ticks
- efeito: bypass de invisibilidade e slowdown **-0.95 `ADD_MULTIPLIED_TOTAL`** enquanto ativo.
- cooldown em unidades efetivas: runtime QA necessário.

## Poderes passivos por Age

Vampiric Ageing também modifica passivamente, conforme facção/rank/config:

- Max Health;
- Attack Damage;
- Vampire Blood Exhaustion;
- sun/fire/holy-water weakness handling;
- DBNO / Neonatal timing;
- Hunter movement, XP/food exhaustion, mining/trades and Tainted Blood behavior;
- Werewolf bite damage, leap, form duration, heal-on-bite, raw-meat nutrition/saturation and silver vulnerability;
- optional Vampire healing/immortality mechanics.

Esses passivos não devem ser duplicados como spells. Os defaults e o pipeline estão documentados em `PROGRESSION-AND-AGE-METHODS.md` e `TECHNICAL-AUDIT.md`.

## Dano

Não existe uma tabela única de "dano das magias" porque a maior parte desta superfície não é spell-damage:

- Celerity/Step Assist/Water Walking/Wise Eye/Improved Senses são estados/atributos/utilidade;
- Teleport e Bat Mode são mobilidade;
- Blood Tap acopla-se ao ataque e ao settlement de blood do Vampirism;
- Age Ranks podem adicionar Attack Damage passivamente;
- Werewolf Age pode modificar Bite Damage;
- configs opcionais alteram como determinados DamageSources afetam Vampires/Hunters/Werewolves.

Qualquer dano final deve ser atribuído ao pipeline real do provider, não a uma aproximação genérica de "spell damage".
