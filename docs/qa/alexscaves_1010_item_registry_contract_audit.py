#!/usr/bin/env python3
"""Read-only SHA-exact, bounded ACItemRegistry/ACDeferredRegister contract.

No provider class is loaded. A fail-closed JVM stack evaluator proves initializer
argument flow; lexical write windows and inferred lowercase field IDs are not used.
The contract covers registration plumbing and local helper/callback bodies, not
all item/entity implementations, installed dispatch, a player hook, or gameplay QA.
"""
from __future__ import annotations

import argparse
import copy
from collections import Counter
import json
from pathlib import Path
import re
import struct
import zipfile

from alexscaves_1010_armor_material_audit import (
    AuditError, ClassReader, canonical, digest, load_seal, require, rows,
    verify_artifact, SHA1, SHA256, SIZE,
)
from alexscaves_1010_item_registry_probe import (
    TARGET, BRIDGE, EXPECTED_FIELDS, SUPPLIER, PREFIX, cp_index, inspect_methods,
)
from alexscaves_1010_food_builder_probe import refs_for

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / "wiki/modpack-catalog/providers/✅-alexs-caves-continued"
SEAL = PROVIDER / "EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.json"
IDS = PREFIX + "server/misc/ACRegistryIds"
ID_FACTORY = PREFIX + "server/misc/ACIdFactories"
ENTRY = PREFIX + "AlexsCaves"
REGISTER_DESC = "(Ljava/lang/String;Ljava/util/function/Supplier;)Ljava/util/function/Supplier;"
SPAWN_DESC = "(Ljava/lang/String;Ljava/util/function/Supplier;IILnet/minecraft/resources/ResourceKey;)V"
ITEM_DESC = "()Lnet/minecraft/world/item/Item;"
PLAYER_DESC = "(Lnet/minecraft/world/entity/player/Player;)Lnet/minecraft/world/entity/projectile/ThrowableItemProjectile;"
CLAIMS = {
    "claim_scope": "STATIC_TECHNICAL_CATALOG_ONLY",
    "evidence_grade": "SHA_EXACT_BINARY_BEHAVIOR",
    "static_technical_contract": "CERTIFIED_STATIC_7_AXES",
    "runtime_dispatch": "NOT_VERIFIED", "mutating_hook": "NOT_VERIFIED",
    "physical_qa": "NOT_TESTED", "perk_certification": "NOT_CERTIFIED",
    "mutation": "NO_MUTATION", "provider_universe_closed": False,
    "semantic_magic_roots_delta": 0,
}
AXES = {
    "identity": "Publisher 1.0.10 SHA-1/SHA-256/size; all 200 registry fields, 208 coded declarations, five bridge methods, seven nested classes and focused native lifecycle/ID bridges.",
    "behavior": "Causal stack provenance for 188 field registrations and 43 additional spawn-egg declarations; full common helpers, six player projectile factories and fourteen nested callback/constructor bodies. The other item factories retain identity and whole-body hashes only.",
    "parameters": "Literal namespace alexscaves, registry key Registries.ITEM, 188 individual paths/factory handles, 43 spawn-egg names/colors/tab/entity suppliers, six material declarations, four rarity aliases, setup operands and exact local callback guards/coordinates/costs.",
    "targeting": "Registration plumbing has no gameplay target selection. getSpawnEggFor resolves map suppliers, checks SpawnEggItem and compares EntityType identity; local projectile callbacks construct at supplied coordinates or with player.level/player. This does not certify downstream projectile targeting or hit acceptance.",
    "costs": "No mana/cooldown settlement in the registration pipeline. The local nuclear dispenser callback unconditionally requests shrink(1) after addFreshEntity, sound and game-event calls; external acceptance is ignored. Factory durability or other downstream costs are outside the behavior claim.",
    "integration": "DEF_REG to raw DeferredRegister to native constructor event-bus registration; commonSetup enqueueWork to setup; deferred construction via ACRegistryIds ThreadLocal restoration. Calls and return handling are certified locally; external Minecraft/NeoForge implementations and installed dispatch remain unverified.",
    "validation": "Typed 1,555-class census, declaration/body reconciliation, CP/BootstrapMethods-resolved stack flow, exact body/branch/operand pins, semantic negative controls and twice-run binary CLI reproduction with unchanged inputs. No gameplay execution.",
}
BOUNDARIES = {
    "certified": "Registration argument flow, literal declarations, local common helper/callback code and direct native lifecycle handoffs only.",
    "factory_item_behavior": "IDENTITY_AND_WHOLE_BODY_HASHES_ONLY",
    "projectile_entity_lifecycle": "NOT_CERTIFIED",
    "external_engine_behavior": "NOT_CERTIFIED",
    "installed_registry_execution": "NOT_VERIFIED",
    "safe_per_player_hook": "NOT_VERIFIED",
    "threadlocal_key_consumption": "NO_NATIVE_PENDING_CALLER_OBSERVED",
    "semantic_roots": "HELPER_ONLY_ZERO_NEW_MAGIC_ROOTS",
}
# Pins are intentionally source constants, not values trusted from the seal.
CLASS_PINS = {
    'com/github/alexmodguy/alexscaves/AlexsCaves': '4f4dce8345d5161b2aa9f22aa5b859bcfc4611219a82480bd2856558442e0abe',
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry': '114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1',
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$1': '8fcf765148b848978f8d4fae8d1fd8a1c44ecf96f787d80c202ded3c09383b29',
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$2': 'adc65f3faa898a0fd5098903781de3d979bbc7b3f385d0bc31a94ec1946843c2',
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$3': '7cad662acb78e26cbf4dd7766e06aa07c9a70d9de40c83e79af8e2e1863f3cca',
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$4': 'cfa9851960ce71cdff5a7808c68fb0c6e6dba90edd9df4c97951ab70dad0234d',
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$5': '52e59afa55413b17530f60de11bebd7700fad23b72b8b219657ba792ae2ebf47',
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$6': '721d302ffe9969fd15510f63035c2d338be5a962a91f88519c0b527efe8b53a6',
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$7': '28e78bc3d6c52bdca735bb1e8663b834f4a82d2879ad8a70b63f5c889e7b78f9',
    'com/github/alexmodguy/alexscaves/server/misc/ACDeferredRegister': '08743e318b3bac302e7602373ff6ca96903f3694ec9fb75457e7cc15ed4305e9',
    'com/github/alexmodguy/alexscaves/server/misc/ACIdFactories': '53dd4fc45d0bc2ed33cea2341b2b4efa5b9f04eab9417e1f9be0b1cf86607716',
    'com/github/alexmodguy/alexscaves/server/misc/ACRegistryIds': '7eded908c4e715b18ed1403eaf662a21427e1bb3362e8f60775578e884368be1',
}
BODY_PINS = {
    'com/github/alexmodguy/alexscaves/AlexsCaves.<clinit>()V': ['583e4c040f1b43467f50b54c1c54123e9df7b074c9413d6792f733b02f86f646', '2b084947bff689c282ca78bcc127f839d19e22aacc56e4452f28b2ce3132825f', 46, False],
    'com/github/alexmodguy/alexscaves/AlexsCaves.<init>()V': ['7a42f665873a7e05d8d1005355b47afe8267f8276627663a985e910909192a20', 'e9a0da3992d31091a2134c63958bdfde7be3a6b8f8609ceb1ce3f6c4bcf6561f', 162, True],
    'com/github/alexmodguy/alexscaves/AlexsCaves.clientSetup(Lnet/neoforged/fml/event/lifecycle/FMLClientSetupEvent;)V': ['59695adbd604ffa5b2f9ec040c424c74e86f8ccde91a07c08eb0e2c745aaa93f', '216bf84e97126f845f0b1988af5889b8923bbe04a36610c29c97c82e8e6c4d73', 5, False],
    'com/github/alexmodguy/alexscaves/AlexsCaves.commonSetup(Lnet/neoforged/fml/event/lifecycle/FMLCommonSetupEvent;)V': ['cf3b71ab5b54c5e266e2604685dd31bf2882a2760646b18edcf606dfedcb84dc', '44ccd054647de47668f0be5c3cb8b2af4662f1cb40db5c47097625cb54cf62a6', 10, True],
    'com/github/alexmodguy/alexscaves/AlexsCaves.lambda$clientSetup$3()V': ['2b938965c11f67befdfedbf8de4cb028f54c84026762eea4f055e72541f77d04', 'ba126e0aefb1f4c0933eb4664c1b6a2373406bef9b0bc3184cbac1a0a305a16d', 3, False],
    'com/github/alexmodguy/alexscaves/AlexsCaves.lambda$commonSetup$0()V': ['bbab6be3021746446d21ad505ad5baac4e0b34d3883da60d23b51f6de0fe5826', '2bda22d62aeb10dfd9745d6ede69cf2902714c1945fad5ef5b5a2686cf7314bb', 10, True],
    'com/github/alexmodguy/alexscaves/AlexsCaves.lambda$registerCapabilities$1(Lcom/github/alexmodguy/alexscaves/server/block/blockentity/AbyssalAltarBlockEntity;Lnet/minecraft/core/Direction;)Lnet/neoforged/neoforge/items/IItemHandler;': ['8421f98b9a462155eef24a752500651e595954c7acd631d75f4d67b578921db4', '4ea83c51fd7323f9cb488bb4af3b18eaaa9b8d3a1af469ae2722187a526710a7', 10, False],
    'com/github/alexmodguy/alexscaves/AlexsCaves.lambda$registerCapabilities$2(Lcom/github/alexmodguy/alexscaves/server/block/blockentity/NuclearFurnaceBlockEntity;Lnet/minecraft/core/Direction;)Lnet/neoforged/neoforge/items/IItemHandler;': ['8421f98b9a462155eef24a752500651e595954c7acd631d75f4d67b578921db4', '4ea83c51fd7323f9cb488bb4af3b18eaaa9b8d3a1af469ae2722187a526710a7', 10, False],
    'com/github/alexmodguy/alexscaves/AlexsCaves.loadComplete(Lnet/neoforged/fml/event/lifecycle/FMLLoadCompleteEvent;)V': ['f4e8088cd2f18a4b0449e9c328ad1ffc4599ee9654b351e407fd48b7d6688253', '100c00f3a5bc1c6a595834f00ad5f08813a8a2ff8f4404358c7440713406c9c1', 11, False],
    'com/github/alexmodguy/alexscaves/AlexsCaves.loadConfig(Lnet/neoforged/fml/event/config/ModConfigEvent$Loading;)V': ['94c207afc5bd058644c5ff0cae34ed7a12fa36251e73f49f8753398b8f527c11', 'ce587a1e9e324f9668a0865a3f89d24415508722e2d3bd3df769be7db10b924e', 2, False],
    'com/github/alexmodguy/alexscaves/AlexsCaves.modInfo()Lcodx/codxlib/api/ModInfo;': ['05d1e6f0501d04bc9ede83047e0b9cb9d9a5456ab42c5874ba60a594d3e6e034', '0addbf3480828dd17ae6571b8b0515858235e86ff5eb6959ff3f47776c51119f', 9, False],
    'com/github/alexmodguy/alexscaves/AlexsCaves.readModIncompatibilities()V': ['9d5f717e7f621c8c63a51b4a7099dcd0e90a0ef1c3e3d2b98a430f15b8d1ba18', 'a586596ee07112666f64570ec52a40feb928cbf9e4946ee841c5fa0ec6209fb2', 26, False],
    'com/github/alexmodguy/alexscaves/AlexsCaves.registerBrewingRecipes(Lnet/neoforged/neoforge/event/brewing/RegisterBrewingRecipesEvent;)V': ['d8ebce1d1a630e56bb95b07fc7f4a825410c037f7c826840cd1077cc3fe5e354', '27e99b438638ec7683693363246566e371db997b8418b971c301c205b6d0edce', 8, False],
    'com/github/alexmodguy/alexscaves/AlexsCaves.registerCapabilities(Lnet/neoforged/neoforge/capabilities/RegisterCapabilitiesEvent;)V': ['de09fbd940fd1f9c160206bd66d9f8490c66a5f6179e7c25524261ae97b642ae', 'd9a9f3dcd5ad5ea6ea024932eae84737394fb2a6f43594ecd3e35ea022351ede', 15, False],
    'com/github/alexmodguy/alexscaves/AlexsCaves.registerLayerDefinitions(Lnet/neoforged/neoforge/client/event/EntityRenderersEvent$RegisterLayerDefinitions;)V': ['a2f50707505efd2b73fab440366cec84b85c28d51269bc09015f4dcb5067b947', 'eac598116b9b7aa61612560e1b05e2f231044ffc9e99e45c5131dbf053d182b0', 3, False],
    'com/github/alexmodguy/alexscaves/AlexsCaves.registerTicketControllers(Lnet/neoforged/neoforge/common/world/chunk/RegisterTicketControllersEvent;)V': ['ef7e29243d96169b0b61edf2e078f9e17d90b23ece93a081b38cb37a5b542396', '1c449070ae09ab126e894bd482901b91cb0f27cc47dab0302f9cc8fade44849a', 14, False],
    'com/github/alexmodguy/alexscaves/AlexsCaves.reloadConfig(Lnet/neoforged/fml/event/config/ModConfigEvent$Reloading;)V': ['94c207afc5bd058644c5ff0cae34ed7a12fa36251e73f49f8753398b8f527c11', 'ce587a1e9e324f9668a0865a3f89d24415508722e2d3bd3df769be7db10b924e', 2, False],
    'com/github/alexmodguy/alexscaves/AlexsCaves.sendMSGToAll(Ljava/lang/Object;)V': ['c47adc2f381f82e58a417b74f3595d1a3e5ef6e659ede5e5dcd97e1c7c6a7d03', '94e433d143d3f0af1403d596e2c0b0b487acf6fc750cf7c92fcfd1889a04783d', 17, False],
    'com/github/alexmodguy/alexscaves/AlexsCaves.sendMSGToServer(Ljava/lang/Object;)V': ['9d7885a55465022e8558f11654e3e81af46c8248cb4b209aade727b8a9dd12e1', 'da5a7a7e64af101c0d6c4a548aa1a921a099c946ee18b14efb67de225495f5a7', 3, False],
    'com/github/alexmodguy/alexscaves/AlexsCaves.sendNonLocal(Ljava/lang/Object;Lnet/minecraft/server/level/ServerPlayer;)V': ['3d9af2e100f8296cd4e84c04d366f83a9ba47b1ebde8ffa32c72f147ff3a93d4', 'a085afeb8513ac96a596afd722875d9418dc099436efdaf5f9967fa041af58ec', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$1.<init>()V': ['d6f7264189858f154b120ac2e9b76f4b4dae9ddb629e4ec627af7810207e1a24', 'c859c99dd80823674bb91171f88bf9ddaefab94c2f14c0ec9ceafcc73b3b75f8', 3, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$1.getProjectile(Lnet/minecraft/world/level/Level;Lnet/minecraft/core/Position;Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/entity/projectile/Projectile;': ['929fd3ea8f7b0b9e936869c91306049e55d1175795adeb48a9ee8be2f14eed4f', '487a4d37a651473fcef83089c59ad1f9aeb079457a23b4bec9c0f402e81a35c0', 16, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$2.<init>()V': ['d6f7264189858f154b120ac2e9b76f4b4dae9ddb629e4ec627af7810207e1a24', 'c859c99dd80823674bb91171f88bf9ddaefab94c2f14c0ec9ceafcc73b3b75f8', 3, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$2.getProjectile(Lnet/minecraft/world/level/Level;Lnet/minecraft/core/Position;Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/entity/projectile/Projectile;': ['0f3b71de1590c889091220b858d78203871f24bcc5ca1fc2d9fc24dc0db8efd3', '51a051f3e5f393ac7685ae4b92540cd1e5521e21b6742ae44dc09cb20ad76dec', 11, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$3.<init>()V': ['d6f7264189858f154b120ac2e9b76f4b4dae9ddb629e4ec627af7810207e1a24', 'c859c99dd80823674bb91171f88bf9ddaefab94c2f14c0ec9ceafcc73b3b75f8', 3, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$3.getProjectile(Lnet/minecraft/world/level/Level;Lnet/minecraft/core/Position;Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/entity/projectile/Projectile;': ['0f3b71de1590c889091220b858d78203871f24bcc5ca1fc2d9fc24dc0db8efd3', '790649cdd3d05a176b879cd632049e80f55a3e6b399ebbe001e7b0a1b7f50878', 11, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$4.<init>()V': ['d6f7264189858f154b120ac2e9b76f4b4dae9ddb629e4ec627af7810207e1a24', 'c859c99dd80823674bb91171f88bf9ddaefab94c2f14c0ec9ceafcc73b3b75f8', 3, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$4.getProjectile(Lnet/minecraft/world/level/Level;Lnet/minecraft/core/Position;Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/entity/projectile/Projectile;': ['aea4d478384a77efa0b7256df2d0d529e3e6ac967d0895e5c14ba8199312377a', '73c49332c7902b6ccb50647cd193064dc2ccf9beed11cac4430cfea7c624bd5a', 19, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$5.<init>()V': ['d6f7264189858f154b120ac2e9b76f4b4dae9ddb629e4ec627af7810207e1a24', 'c859c99dd80823674bb91171f88bf9ddaefab94c2f14c0ec9ceafcc73b3b75f8', 3, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$5.getProjectile(Lnet/minecraft/world/level/Level;Lnet/minecraft/core/Position;Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/entity/projectile/Projectile;': ['0f3b71de1590c889091220b858d78203871f24bcc5ca1fc2d9fc24dc0db8efd3', '1c6faad16d4ec4ce974e3db353978d9812801d64f7833821d778f718f9d2b4a2', 11, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$6.<init>()V': ['d6f7264189858f154b120ac2e9b76f4b4dae9ddb629e4ec627af7810207e1a24', 'c859c99dd80823674bb91171f88bf9ddaefab94c2f14c0ec9ceafcc73b3b75f8', 3, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$6.getProjectile(Lnet/minecraft/world/level/Level;Lnet/minecraft/core/Position;Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/entity/projectile/Projectile;': ['929fd3ea8f7b0b9e936869c91306049e55d1175795adeb48a9ee8be2f14eed4f', '817c58046c0ae136f15437b05c28362374058636a8ffc726404cc45f4192dcd3', 16, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$7.<init>()V': ['d6f7264189858f154b120ac2e9b76f4b4dae9ddb629e4ec627af7810207e1a24', '2f632ac03e94dfd47549e3cb3f271662fa19c1f88aa80747069394a7c0ef859f', 3, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry$7.execute(Lnet/minecraft/core/dispenser/BlockSource;Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/item/ItemStack;': ['266e38ac5adde1395dd320958ac1b483ae6d48df7f8e2a4fae2ef9bc544bf4e9', '541cae9dbfd43b5e22f61e88492450611c0255d603463e3a2a7bb5753cd94789', 59, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.<clinit>()V': ['bb73db4c0f1d1c84abdf5ab1c07defd24db79e5e8c754b8c9f9ec8481a84a84a', '37c76b83778533021b7931e770a55b4e4ac4be25d1ff3bb10881ebb258647756', 1382, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.<init>()V': ['d6f7264189858f154b120ac2e9b76f4b4dae9ddb629e4ec627af7810207e1a24', 'a4e909f6fbb3424695cfd8081458c1db352953a8b4021610a41ca8bcbc874b14', 3, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.blockItemProperties()Lnet/minecraft/world/item/Item$Properties;': ['73e40e814ff7272e1b735faea0e40f8009d2c8a4abd92a228bdb0575518d8e75', 'd7252cb22ebfc15f85638523cb90ffcc649233a4a33425b7c947232a6bc91b81', 4, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.getSpawnEggFor(Lnet/minecraft/world/entity/EntityType;)Lnet/minecraft/world/item/Item;': ['6e2a13839dfd3b5e68f259b23fe8afc1c46d0b6b795eb9bd517c9fbff023ee7a', 'f7b916b8223cd6907abf82ce877ba0546efe593f9925fc593d86b40a24a2d368', 31, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.getSpawnEggsForTab(Lnet/minecraft/resources/ResourceKey;)Ljava/util/List;': ['ac0eb4a71de94c9c76110314bfeb130732fbb80bdf038462761d4e13fb84bfa0', 'd45de2469888c5182bb45bffcb655866007d0f425189a6dd2dc2243a440a2324', 30, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$spawnEgg$199(Ljava/util/function/Supplier;II)Lnet/minecraft/world/item/Item;': ['e0e5feab1526ea9ceacc12568f5e1997e90611dcc35430ba2f0098910a4980e9', '11b7e5a41ad8cc9e3a58e8decbe0a1732821fa35ba79244164b56d7879fdf6ab', 10, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$0()Lnet/minecraft/world/item/Item;': ['f92e731930bb5e5ac0ef34ba531672a7e39dd36b3460aadd05ef8393306cb8e6', '99d6569430dd30f9cb0a7dd4e4d7f39dca65364d0d1ffa789d6564c3160e5f63', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$1()Lnet/minecraft/world/item/Item;': ['7a060c80d6f76e2ba1ce4c0d43eb0de44b7e4a182c0dff083a3a67c325a52327', '797e4dc9f5ff93027caa8ec8e5db3182a33b2c3ede5182dfd267750cdffa53de', 10, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$10()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$100()Lnet/minecraft/world/item/Item;': ['bb759be18025281f8a946a5f6fd1fe312accf4cf80ecc8b2595dcf7c8f113ff8', '5fa01429a74291b5a74c7af6532af8c85b0fc21daa89815e227e2bee72a3eacb', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$101()Lnet/minecraft/world/item/Item;': ['eebdd0659953be4bb91c294e3f4a682c85a6f2621e1dd175eb714304ae565b07', '2988bd04e2e58480242aefe4f6731e61bf324cf8d8cc6cd2d54794abd25bf1e0', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$102()Lnet/minecraft/world/item/Item;': ['1c5056eeb3274285c2026d3af92ee741e8706da73774c758904117ccba0c5e31', '14370beed2ec9353a5250cde1f97d8c5d5dd92b4b8540a4111411067996487d6', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$103()Lnet/minecraft/world/item/Item;': ['a9bfbdf9d227839dbb872f120c68e9df77c8723eed98d8e146c790aa3f395613', 'c177d8ad8f6084b86e6f6d0dbd5ac65b138574f6ee12f31c393f1cb1c12df6a9', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$104()Lnet/minecraft/world/item/Item;': ['9868e34dbf3a04069b519c24047b9a3f461dc7ad514f62323ac120ff232a3dfa', '70ebd3ce11f335078507bcdbb0ae3aaa78e1e68e821852af72c68345ef11b116', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$105()Lnet/minecraft/world/item/Item;': ['c69181618911cbcd762e36a54c5de44dae0a49af9b0841994acddb24b4630096', 'a2deae9b738adb77a7eb0171d92f905cc948b079fc01b966b34923b7a9fc2e4d', 8, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$106()Lnet/minecraft/world/item/Item;': ['78b65499de90c40a538c2b78c0b5d60b12730fc55811b77593c435e0f8d97993', 'fab3379b52d191b5381c1c4748fdc1bd3f596ad8ed2236f13d4e24abeffc5c2b', 8, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$107()Lnet/minecraft/world/item/Item;': ['60b0fb2e31c9004a8ef5f1ef43f7302bbf922132b4ea8f9c1e9e6fd3da7cd0f0', '237d618e107e50d44651966e81819da3bd3d8828cfdcb6d1b2391c4c888676f3', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$108()Lnet/minecraft/world/item/Item;': ['4438cdab039371f4694b57692b605d35685312dff79f1b4c98930fd423aed0ad', '97608bafd76651f213904775fde9b7fb104324bf4f7250e311876109d4c43bb1', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$109()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$11()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$110()Lnet/minecraft/world/item/Item;': ['8b877c684803c7473ec03238d4f62a31f2125d8b896b31340e2bd3894d3db0da', '413ddf15da6c0a206f58abd4ff458af35feab89841af1100f821bc4bb8333d8a', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$111()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$112(Lnet/minecraft/world/entity/player/Player;)Lnet/minecraft/world/entity/projectile/ThrowableItemProjectile;': ['620d93b80cee080c5a16582cdc36b279266c396c9c32312ab22b450cb5394f5c', '7ceec9db4d3ce241ff69d91a57b195be89cfdd7de26b3264e1e169b3b2eb34d7', 7, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$113()Lnet/minecraft/world/item/Item;': ['5b5396ac73dc271445003cefeda4e6066978b2df1997228de0b035949d3a39f8', 'b2a4414fbbd63e40af31cb69ba1dd1af3d44c9741ed8b0d184e3792b18307185', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$114()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$115()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$116()Lnet/minecraft/world/item/Item;': ['0079638de9ee5ad6d6196c2458e431429611703447f431c4381b482ec4ba026d', 'db9d30c2cd452caf3dfbb7eb9cec8ef1c1baddf4615ce3d18cca2e1ac4bd5a21', 12, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$117()Lnet/minecraft/world/item/Item;': ['ce365cbfa29f68a65b0cd3c469c62818dc127ee1c0a7280472ba9cf64b4611cb', 'defa5dea828272bf5edca7bd4c794b9f8e71b5f15934cf810f6401652c4220fd', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$118()Lnet/minecraft/world/item/Item;': ['dc6779b993945dbea8f6f00354e2f87488e8710808291fd586e8be35b4bbc746', 'cc259c5a3543daebb0b31a46659f5341f797c008538fcde70eaa2c2a8a236aba', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$119()Lnet/minecraft/world/item/Item;': ['057db943ce22f427be5b7cf5b0450f65f1a1b92f4b42a6691e703d3bc4d5b7f6', 'a1b645ddccc5e044f1ff2df176cc6cc5b15d312cfda94edcee7795420ebec9a5', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$12()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$120(Lnet/minecraft/world/entity/player/Player;)Lnet/minecraft/world/entity/projectile/ThrowableItemProjectile;': ['34ecf715b0867f36fc58398b0de7571f4d01dbf5d44995fd6b7e3396729576d1', '1077b9eeb205fce66b9a07c074db0e10b8b2efd652cf26fd3661688c58cb2ac9', 7, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$121()Lnet/minecraft/world/item/Item;': ['279cb235c5eba0d207bae281636c396354915b06416eb9bec09335bdb108cd6d', '9605a22619238be67fc74493fd5ca35a1cf7a9ad874171fbaa027d9d1977ca22', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$122()Lnet/minecraft/world/item/Item;': ['20fac1a05d60f7390148c4a90e14a151511ba918fb57388a09b978b7dbcd4948', 'a4959ec8c3cfae3cb3f7bcae1384a6f4c40ca68ca833d81eb865977b1263674c', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$123()Lnet/minecraft/world/item/Item;': ['f471c4a9996a2f28e510801f65c1ac5561deb610ed9859620ea3f4e05d4c75d6', 'abd35bf05a318c7a321dccb5a8898e1ba23c77dbaca32068d5f48ffe45085e8f', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$124()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$125()Lnet/minecraft/world/item/Item;': ['822434c14e8326e5ab8ac425279bf944b013d5a1086969d54845a05592dc65f6', '517c1deb74abae0dfc7c4e6a70b9da66825e75fa1903c794be0f990761858544', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$126()Lnet/minecraft/world/item/Item;': ['d0d2a63312000db2260bc3604e40342a9749e580340ffabe9c285988d75925f1', 'cc87e9d878d5cd757b5efc0344dde40b1ce826ece1a964a4ca1f9f037e4a2c57', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$127()Lnet/minecraft/world/item/Item;': ['4ac1962b5748b72b3e62f5e6a2bc5fbb76086e8bc5c706f70ad8f32bbbe558aa', '341dd0b5e6408fe2b9b8dd1a4ac85840ae56edc03fe6e106ec8d9378779ad609', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$128()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$129()Lnet/minecraft/world/item/Item;': ['6ba1983282a777582b1768407e8d5fa5ccc3afc88285edbf63935d9ec62a3859', '03e336fdd611329019dd12eaeb69a2ee7dc0b83761f3ce1c689d34923f2a3051', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$13()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$130()Lnet/minecraft/world/item/Item;': ['54b73bd23a130ea59f2c5c9f48fc554d0f2468ca800b52ebfee05ab66a49bb2c', '5427fbddcb336f06c0f101655ce0efcb04b569bd3abf5d9c6d6b100fa439c06b', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$131()Lnet/minecraft/world/item/Item;': ['c7e3a5e1d12501813858bf1f4397213e04844f8079e4a4077d3f3809a5660b64', '88ae591302ffec8e6ca2721a562754fa5d2df6d19b792105be4510545d68275d', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$132()Lnet/minecraft/world/item/Item;': ['288afe754080d8f8762710181f9791891cff1e5e2748a7d6d4542a321cfe254c', '24f7127409514d878487cb009a3aff247c8e5cee2e925597a0abde40db79eb88', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$133()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$134()Lnet/minecraft/world/item/Item;': ['050f52ecb79c931c3a455149c9f7537653be12d3fc22fe11bf940b207da78dea', 'dda5cd0097ef451e47a32876dcf0a0a69a24fd78afe0260d3124f63c5ffd76a4', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$135()Lnet/minecraft/world/item/Item;': ['4ab51a5f80296bb82149e023b386ab8fd56f442c07762060aac3ed6ae44f911f', 'a77382a0a5971b85c55902bbf49e4bdc0af13a90ff585ce4602ce5c0c2192c00', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$136()Lnet/minecraft/world/item/Item;': ['4804ddcbcc419efb87881c1f26eab54e769a43cb3ca100a843c21b0cbbc8893e', '1da9c22a744990ae12535d251c29f66a4c76f3a56ab4ab5631820c3dc6020a65', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$137()Lnet/minecraft/world/item/Item;': ['a3543185d285f315e5549ac45441884c63f5637ef43ad4cbe5eaa5765bfb7011', '79496433e08c077ad645204b08d8541772df99f850058f5d970cd13fea40cb5f', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$138()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$139()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$14()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$140()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$141()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$142()Lnet/minecraft/world/item/Item;': ['112fc48bf1da395ba13daa8917c029717d9ae0f69e0b1b55543578b8c26de48d', '1dff52a96df9f4b20eb789e8948616f1a29906cf46985e9f19db25e573b3e9e4', 8, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$143()Lnet/minecraft/world/item/Item;': ['4a93d89d9850d92d449ca0f2464ab19694a6e4a0013528f28c647082c6757670', '887ea72e0215d516a78398d8a29426720db5cbdb09b8b0dc8bddeec5e9c09d9b', 13, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$144()Lnet/minecraft/world/item/Item;': ['5621aa0d7d742c33a7621df1a3c2ccbc13cd4c7b10cf299ce0d6027a13aa49e3', '541d90f9af3ef6affcb12ae7eb7ef6813212799aff1f0ae6a45a0d1cd59d8885', 13, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$145()Lnet/minecraft/world/item/Item;': ['59c8cc9dd12de9c7fba6cf3ac214421be8f2822511f0ac9e62fbb87eccd17317', '893974818209ab2cb9c9c917fe492d6ee4188e37104e8c1ddcea8d40d3bf5743', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$146()Lnet/minecraft/world/item/Item;': ['aa6d34966ba31d55c535bd67e05f6c97a40b5e984bacc3e088bdf663676ec32b', 'a85d00ffc46b14ee3d5ef45b516488336f808537746c72324c47fcf49567c9ec', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$147()Lnet/minecraft/world/item/Item;': ['605ef3ed81b37cce5c193b2c7edee63ab262172120834f5bc32a0e624a31393e', 'c9e87e9856dfecac9e48b39187013c21a281064abe3e7e6c62e77f6fd9d3c18f', 10, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$148()Lnet/minecraft/world/item/Item;': ['4bd1e5aff54435022bd750a735cb42593c7603f10626025fdd553c897acc7573', '39a48e45b65e66d9fd06da224d5a0e34ef33bdd3a1ea621cab9459ede94f2a2f', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$149()Lnet/minecraft/world/item/Item;': ['ef1b8448d9d33e5c71ab2d445960e3321419a7113df99662978c5bb17b49dfe2', '9395a19f5b68764edf5d49ec865171a33227ffcb3556e470118244ca3868bb8a', 5, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$15()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$150()Lnet/minecraft/world/item/Item;': ['a90039a60a0bc10b2d11d2ccc0faa534b6c9e1bc6dc48daf9f42f409fae8a3d1', '149088a82a3848674dbd94dac3ed6f49e7e9cc4c1a45d0f6d1d696a5dcb8371b', 5, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$151()Lnet/minecraft/world/item/Item;': ['2cf146833c4613f3c6038bd925527e834d419dad1399b796fa484062d7341773', '696917be149bc4729ec29ee9afbda62a84bf6da821a31fdaa83fe4fea6e5f1d6', 5, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$152()Lnet/minecraft/world/item/Item;': ['55645415c36c0551bd0e31b7bafcc45d52cdd5d7ecd1107c5ed0e48e936b6d79', '51d3313b1c6d67adeaaa8f4e223cd9814c55b62666c2f4e16464cbbd3458eeea', 5, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$153()Lnet/minecraft/world/item/Item;': ['b679636ea7c47b3b75cebed47103963c4c5088e28c3e89d1d572e5bbea20c813', '93db51d766b892bd1c4f543c5740d64be53acfbcadbbf1ccc0228c3700b1914d', 5, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$154()Lnet/minecraft/world/item/Item;': ['930487822b3cda2c3cdcb6c2ff2b48afe81fe3e22c0bf71e70ced53f582df3dc', '4acf84aca69c01ae41569a6ced1ab1a156a36ad97ef27000939913d885ef94e1', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$155()Lnet/minecraft/world/item/Item;': ['930487822b3cda2c3cdcb6c2ff2b48afe81fe3e22c0bf71e70ced53f582df3dc', '4acf84aca69c01ae41569a6ced1ab1a156a36ad97ef27000939913d885ef94e1', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$156()Lnet/minecraft/world/item/Item;': ['930487822b3cda2c3cdcb6c2ff2b48afe81fe3e22c0bf71e70ced53f582df3dc', '4acf84aca69c01ae41569a6ced1ab1a156a36ad97ef27000939913d885ef94e1', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$157()Lnet/minecraft/world/item/Item;': ['930487822b3cda2c3cdcb6c2ff2b48afe81fe3e22c0bf71e70ced53f582df3dc', '4acf84aca69c01ae41569a6ced1ab1a156a36ad97ef27000939913d885ef94e1', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$158()Lnet/minecraft/world/item/Item;': ['930487822b3cda2c3cdcb6c2ff2b48afe81fe3e22c0bf71e70ced53f582df3dc', '4acf84aca69c01ae41569a6ced1ab1a156a36ad97ef27000939913d885ef94e1', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$159()Lnet/minecraft/world/item/Item;': ['0542af313c6f9d1baebf9f2d8319d6c787f6b8e4a1a2627a61957b257698aeae', '6da23032a844cf9bf560e1c459f10cf654666a7d11ce93cd3763953851385521', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$16()Lnet/minecraft/world/item/Item;': ['8eedb42718de2b1062ad616449d83c8b6577741845712c901bd1fbb73a7c70f6', 'b7594b00d026b1b00f92b735a361bcf2a2074043550ba283092f2a77047d4c78', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$160()Lnet/minecraft/world/item/Item;': ['0542af313c6f9d1baebf9f2d8319d6c787f6b8e4a1a2627a61957b257698aeae', '6da23032a844cf9bf560e1c459f10cf654666a7d11ce93cd3763953851385521', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$161()Lnet/minecraft/world/item/Item;': ['0542af313c6f9d1baebf9f2d8319d6c787f6b8e4a1a2627a61957b257698aeae', '6da23032a844cf9bf560e1c459f10cf654666a7d11ce93cd3763953851385521', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$162()Lnet/minecraft/world/item/Item;': ['0542af313c6f9d1baebf9f2d8319d6c787f6b8e4a1a2627a61957b257698aeae', '6da23032a844cf9bf560e1c459f10cf654666a7d11ce93cd3763953851385521', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$163()Lnet/minecraft/world/item/Item;': ['0542af313c6f9d1baebf9f2d8319d6c787f6b8e4a1a2627a61957b257698aeae', '6da23032a844cf9bf560e1c459f10cf654666a7d11ce93cd3763953851385521', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$164()Lnet/minecraft/world/item/Item;': ['f18af631ec58d5bf8d6b350215a8fab261c218eac2b135b5d8c4fced5e106d53', 'b23e2df912b7b9373374339c43ef53bb34773984d0e9ef39700171861f437b5e', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$165(Lnet/minecraft/world/entity/player/Player;)Lnet/minecraft/world/entity/projectile/ThrowableItemProjectile;': ['512e6c38b9e98613519743dc5bbc34cff32de2d237b4486a74b02dbf5c2867a4', '8fc87b9784eb6318771c1d69e27d94f96cae34b78f1d8e8be2b30d17a041289e', 7, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$166()Lnet/minecraft/world/item/Item;': ['b1207d3c3493cba9f22a6a9f795d105ae5176c5ba075726e0b9f4280c72d1609', 'bd87b883f7bc8a44a3d74f90f1dfdf3f7a614b4cd9d1a4efb796bdf4196adb68', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$167(Lnet/minecraft/world/entity/player/Player;)Lnet/minecraft/world/entity/projectile/ThrowableItemProjectile;': ['512e6c38b9e98613519743dc5bbc34cff32de2d237b4486a74b02dbf5c2867a4', '8fc87b9784eb6318771c1d69e27d94f96cae34b78f1d8e8be2b30d17a041289e', 7, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$168()Lnet/minecraft/world/item/Item;': ['4c62609bf9f25265d90a3f88bffd4493e6362f978abda2161d7f97ea9ec9ac28', '6bf5c9f89bf983d52fbb59254c3181d9c5f40f6e927f182e10b6782582e567ad', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$169(Lnet/minecraft/world/entity/player/Player;)Lnet/minecraft/world/entity/projectile/ThrowableItemProjectile;': ['512e6c38b9e98613519743dc5bbc34cff32de2d237b4486a74b02dbf5c2867a4', '8fc87b9784eb6318771c1d69e27d94f96cae34b78f1d8e8be2b30d17a041289e', 7, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$17()Lnet/minecraft/world/item/Item;': ['064d0390cae5a841928f65e348b74c7cc83ba03a9af28b79178af14867c78535', '97dc688a88ce6d5bb7977bdd0b54a82f274c7c247f03e2e4c9a2e17863d92141', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$170()Lnet/minecraft/world/item/Item;': ['b8243502eff7adfa97638db4839e654631ff1cf86a89b85cbba221b3a5be8052', 'd65a887d128f309ec502620e3223cb72a94c6a1ab4888a6314714d55b423b12e', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$171()Lnet/minecraft/world/item/Item;': ['47edde1f791b575cba9f2b4651cddb32b46cfa0bfaf4fcb8d9bc55916ce2043f', '7b7802b4ed7c099bd88139541ebf8130d1c92d15ecc286d305374a4d46611807', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$172()Lnet/minecraft/world/item/Item;': ['8566af6220458047a5bcd4b371172601c61fac9f8574338bf463d0220a9469f1', '1d8aa7800d716f0041c0d2d09976c5b15ec30d36875682a185217ad7be414883', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$173()Lnet/minecraft/world/item/Item;': ['faf19d4e9d8ddf3d2a5f18b1fe3caf4c9be31148180a94aaf401a3819ab1d665', '01afb92a7551f50bb16d2775f9ae02b23976f6b7879996b012a834bc07b982c9', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$174()Lnet/minecraft/world/item/Item;': ['743c600464c92408a92f17805c11a665d11f2607953e01424b60713a2866be2c', '5a4f14aa8c35ae1004697b38488cad8c1e3d329bb4485af63bd452fec2b6f55a', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$175()Lnet/minecraft/world/item/Item;': ['184d720dca50e5151703f10878a2b0ba1b47fe85ab2d710f2e66958e4e0765b6', 'c3e7237285233cb3c622897e2e79aed625b1c1ba65fb0a68738211d74b79ae16', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$176()Lnet/minecraft/world/item/Item;': ['d17f73f69d5a0c34c99b325d57b69889975d4a8902c0092851933dd5bc969ccd', '75ca98c27bedc2eaddee54914d32f038e28c1c72fee716bc49548692a2ff4e2f', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$177()Lnet/minecraft/world/item/Item;': ['5826654e7b9dc14aa0d8bb343d65c00fd0406c2020b5b7ad7b49af08682d687b', '150d55bb7134c44364b910d2c0170c549aa7168b7893af0c94e3897953e8a7a7', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$178()Lnet/minecraft/world/item/Item;': ['cc77d69c52740570c5260020558b7ffdb8fbac6be1a53ee17b628fc29e30a653', 'f7a034d37e66e17dfd09825bb421afd4a7344b18d9311cfd5c327f1a7c083b2e', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$179()Lnet/minecraft/world/item/Item;': ['68a34a12937f8826274b4cf37e3b949499d5b0d64a4f3b4f2a293c3f0b800b76', '601d7fa7bb318dc081635b6d95adecf30af170265b0b52796295fc3c2a3f0f08', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$18()Lnet/minecraft/world/item/Item;': ['f8ce2e07f40753612f56ebe56edb49e12174a8c1042dbf16864db018597cf438', '59c6b313c56777dda4bc024485decc709fbf010c7d510c7b347f58ae15137f28', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$180()Lnet/minecraft/world/item/Item;': ['3bdd3bf723aedf7c2791fa768f1be944a0115617edd1ac186f5be92e5bf3cfeb', '770ad8b548cf64e7fa976b03bb265b9df8c6bdb5dfae2c61b9f6b0fc7242fcef', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$181()Lnet/minecraft/world/item/Item;': ['4695bc463cfdbffb43121cd3c2adb63f7dedb49c54784503528a9123ef96a062', '922ffcba817593dc57a71f9101c26d886c2c8821645ad839b6087019ad61c56e', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$182()Lnet/minecraft/world/item/Item;': ['4695bc463cfdbffb43121cd3c2adb63f7dedb49c54784503528a9123ef96a062', '922ffcba817593dc57a71f9101c26d886c2c8821645ad839b6087019ad61c56e', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$183()Lnet/minecraft/world/item/Item;': ['9dcd9c444f05df03a91cce7f516726bc079f55db87d018ef5a704b5d83365d9b', 'ef4a0bb05c62057d3724c567ab91437ba9309a1f5bdf1bdd2366195941efd4d6', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$184()Lnet/minecraft/world/item/Item;': ['c8fa191e78906e808af28455deb7158eed8d35b0d51c8dd3c65965de1a09cb48', '2523e9b707d68510e5b8e1ee7e54e36e2fa22e66da7f2f9e7cb916af40d881ba', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$185()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$186()Lnet/minecraft/world/item/Item;': ['b6c0bed743b3bc0e46a6ea997fbe39b128b1fa0f1b0a18ed98ec5d873020ec39', 'a00afc5052f65440903e62ed306395f6c1542937688ea87401b9a9557d7f285c', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$187()Lnet/minecraft/world/item/Item;': ['79d0884fc7c242b39f1d5bce534ca142ae256e74a6c6d238bc13c300317a8efa', '69ef66532b0ef5efedcac00f6fb56b144832be19449d5564e32054c8efcb53b9', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$188()Lnet/minecraft/world/item/Item;': ['0e77e72163171f231f71b095e94e0e3899dfb6c9a4cb6474a0e2c12e72f120f2', '9d29742fe0fa1d1540c5b1a05acbdffe974846f0c0d021d2009623ad0f68757e', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$189()Lnet/minecraft/world/item/Item;': ['257187a78894696f95fba75968464ff074ddbea5e0acc9587017dc4980444fdb', '18620f2aec39a63be419ba110ff513806ea252b6ab63b9ee589c6fa621b9e26c', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$19()Lnet/minecraft/world/item/Item;': ['267a9752d0d4f5251379ba0d64a0d7e93d21d6289a0615734ce7b6f3ffc0d823', '6d3b71a07e382b801303eec720bb347786064a4a9e884f5084747076e7e3c5a1', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$190()Lnet/minecraft/world/item/Item;': ['f337d5c701cb2492f908ce230a7a5f2526e78c6140e3c62fda7b45e531963d6f', '89a2f9ecfd43ea36dbee22a0b19497a85439adf24c766ecd6ab7b50756e746dc', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$191()Lnet/minecraft/world/item/Item;': ['4dc589cd486b67dc65677e0388911cb53182ffdfb49ca2459bf226a07bb96d72', '5a9ad64dbb780cca8e29e410eb1974578fb130c5a0fc348c10e626626b1a710d', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$192()Lnet/minecraft/world/item/Item;': ['77af284e6a1cafcde0382f7c188510bf17598d6f0b5c16f8a0627d812539fa77', '42a0727c81677c0e226a7868689c969958a6115bf6296825e8ae517edc2b62a2', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$193()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$194()Lnet/minecraft/world/item/Item;': ['79991495f89f8b2a26c31b11fd5c8a53dd7de0615da9ceaa5e5050d8882f4692', 'a0a35d9a026b53888a019be0b08547b4f894f4df3e60a3fed5bc1a88cf804f21', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$195()Lnet/minecraft/world/item/Item;': ['ae1b7fa1dd80b3bcc9503ebc8167774ba1fb044bf485bd9c5fc7b95a452e86ba', 'ad2eeff7f18b4f3f3e53eb51ac5f294b53f981f80a168447869f25bab14a9cad', 17, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$196()Lnet/minecraft/world/item/Item;': ['e559a38fd03a5f06618574de17f28978ef49c402eaa1abe4c78b8f5ae583a84f', '98508081dc449b2e294b7296ab7bec626d218e44dd846ade00002bd3835ade4e', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$197()Lnet/minecraft/world/item/Item;': ['cf75f86145e14cda77689d73e549a72b510ca42c306256c39c309349422f32fe', '5759f9a734c1cd4070f2d57e0e0d3e97bdd07fb671008f4465fd69f440a3f80d', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$198()Lnet/minecraft/world/item/Item;': ['546da6af37d6cc4834693c322a2cd13c1852123744a3bd55006b0bee3fd5ed63', 'c413047f0275e4de3f45d6fa8d12eb52d15c04c5095340b17651874450e5583a', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$2()Lnet/minecraft/world/item/Item;': ['a11ef33511a53e1b6126b92fb466b7eca18c83b69639d811f08c33dd4a30c846', '916262296bbae1fb784ac4aa89d2d95d2f301f6a0830684eca8facd3261ffd99', 10, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$20()Lnet/minecraft/world/item/Item;': ['6be6cb4de8570768436590ecdd12cfd11e44f1c9b8e76b7eb58a324d6b4d63ce', 'd5746049d40ac0bafdb3b78aac9a4134cba1f81838a06bb5866b30c3143402bc', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$21()Lnet/minecraft/world/item/Item;': ['457db85180802ebe916e565ef89c4725c86f13661b4a7e4ff39f5d12bc23d8fa', 'f37b8bd92c86d894fe6e11a47125e19a840b45a9782987c2faf8450f3b457b63', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$22()Lnet/minecraft/world/item/Item;': ['bb739a62ac8939c3317c1e83c081dca139df6af9ef12d4a7daadff1546b6df7d', 'b4770d9442363e231b20ea21cb93e64e408c161c60b6faf1fdc025394f884f75', 8, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$23()Lnet/minecraft/world/item/Item;': ['677ca6f95fa1dd4d45052acb461a8cd4e8e003c8626f2254acfe161eb6dab010', '548c2b660456dd186b7854eff6ca6119217aa6af8a30c07f2c9524534694aabe', 13, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$24()Lnet/minecraft/world/item/Item;': ['a3d300010965f464125054df502fe1fc9588b306fd1a5fcded520367f9440e88', 'c2466a2e1a2cdcb796a1a256729db25fcdec16acc94e2d5187a8f86711487350', 13, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$25()Lnet/minecraft/world/item/Item;': ['bdcdd27b8688b4c77b965a94ae39cde059587468e45dcc27f4329ee79552537c', '0d55eca0893acc7181b4d9ebb09a9fd2eaa6d6ee8a26271199bbffa07a9bf4d4', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$26()Lnet/minecraft/world/item/Item;': ['96488931db6e9772a9b9df8b053959e67628f244e3e33bc64e36c2d61b60f22f', '994cf68add910a60bc2bf1a6b83a19def83f16dff0d6823cb4d0594b348ac4b9', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$27()Lnet/minecraft/world/level/material/Fluid;': ['17ddd17374a6af404edd3800059ef59916e856e35318f410ae35626c71e4da88', 'b9158080d45f100c7a25afd3d013a9065f4a88780d0410b14b85b1d7b1c6daa2', 2, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$28()Lnet/minecraft/world/item/Item;': ['453b73b31f0029d7869d40793ba0788953f6c7cfe17fef1b1958c8c9bf282087', 'd5d42f1d2e972f17f9763a9c32c76216687a63a56c902e953f8dfce584b21e94', 13, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$29()Lnet/minecraft/world/item/Item;': ['524ed65e3057f687119fed0161a940288848b18a7a7f687ebc7b10cbb7d4b977', '66b3c4ecead45775722a59ff6949678c03f22ce86b5be7ddf555d96c6d343faa', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$3()Lnet/minecraft/world/item/Item;': ['be573644231006f03d2c5b21d6f8184ad86d1b1686ac563df66c68cf3c130113', 'c9d51f96f5fd6de55791ec041a984bfe34dc6a937dfa270f4d23ef80d7e05e4a', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$30()Lnet/minecraft/world/item/Item;': ['c72e66c2f6cfad6794592a75218598a4d16581c355446ccc8b47548f1053e03a', '41645db9d71db887d001428e2ba7977012efadeebefa30c8ef9b87e030400db7', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$31()Lnet/minecraft/world/item/Item;': ['d1470ce3ce5bd3973e689d9564f311c4ba223a65d6020b2d01daf76a578ed6f9', '9f14c3604f2a8c5ddad098e7d383f00fd4cadd16d65229056c8df107c425f1e4', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$32()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$33()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$34()Lnet/minecraft/world/item/Item;': ['a5aec9a3988897712319c8b970fee704fbec87303173c64b39b5363bfcfa54f9', '30618e031600679730e93f91f0def4fc326784769b2737235c6bf7228f51aa28', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$35()Lnet/minecraft/world/item/Item;': ['06fad7a5b6e47e921cd25b041a9caad976b82bd0671c9f2c5021e8b4076e7c0e', 'c826b91e642dc6be1509cd91791bc5dcc92a52fcac86a9f3434f73df0f2d6cdb', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$36()Lnet/minecraft/world/item/Item;': ['0422c42f5408367b8987440476afca13be6ae1bd001f429a8789cf3ba7d57b60', '757e6a6d8820044de39b4861dee528786350aa463e4034ec3ab8aeaf1fb39df1', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$37()Lnet/minecraft/world/item/Item;': ['5814d536831c0df71d18745af3571e2420a7881043c4011999201da8e21dc26e', '9059432bf03ed9a74e204ee4cd62113017738eeec8e4c47c97a764b7e5277bd6', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$38()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$39()Lnet/minecraft/world/item/Item;': ['ee3e2938dc2505334e6ffd9a426211567d9f88dfe25de95b09778f5747711122', '65202a54d8575ab44192b74edf4b0cc0d72ae3e6073fdcfaea6862b4365bf531', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$4()Lnet/minecraft/world/item/Item;': ['fd14cec01c6613bb605bd92463c6724aa1cfda01168104b8bd95a515bc832841', '15815cfe16002239b7c3b5cc0ee58a45b5948e72f5607df5321c49838919b43b', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$40()Lnet/minecraft/world/item/Item;': ['f88517fec12d13fcfc61890e09e7310f0a000ab35eea36adc82ddd7af3bab032', '1716d3d5d194f07bde2a2f9e02cee2e173e94de5f22e3d17abb601b2c94940fd', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$41()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$42()Lnet/minecraft/world/item/Item;': ['cc034be26bcab1d267ef64005d24c47e2c15d001aa3f316f876edcfd5185f25c', 'a081b4b006913e5debfe0a59bee0ce182c8bf9646cfbec03b5e7def9b08e9e52', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$43()Lnet/minecraft/world/item/Item;': ['f355991cfaa016f715e8dee7d1afda2fd1dbb72d1ccda502ebed923d21c46167', 'ea5e98aa42d728edfad89f30a2c3ef1b128eb2201de256e7c2d03a3826c0933d', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$44()Lnet/minecraft/world/item/Item;': ['c0bd3bf9fd92112f5a4ceab6a56f9418b2e14f63ba06275708254e711eba1045', '9de2dc138983464c4e2ec94fcc01eecdc395519070e38407cba553608a54fda9', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$45()Lnet/minecraft/world/item/Item;': ['33b072bd23f120bb5040ee52db21241e05a6589692f0a9d9c95565bf8a70ccef', '9238559a2cbd817b5b345d286c08c59443d259501ecbae4736c75f0d63e14383', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$46()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$47()Lnet/minecraft/world/item/Item;': ['0497f58be62ddb1acf377596e3340cb8a1598d4a267ae99c1cdd1fefd0872699', 'c551eea011075caec6b307618bda57a3e40940db4b2ea09479e49a612979e674', 10, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$48()Lnet/minecraft/world/item/Item;': ['440b1f66a218b862b6cd168ad2f4708a9994736cb60b995875fed413e53fb88d', '49ca852fac8e636468144bb0208afca2e04cdcc4426a463d4e230817c5e046ca', 10, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$49()Lnet/minecraft/world/item/Item;': ['b05a5a0d5218ba481b9ca05220fb579000fa64c3e2af6ac8878b39e1ea0105e8', '524a137e1b2472ea048d9ad1431e4cb8ca5ee7d0539051f0df596bf083ffc05f', 12, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$5()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$50()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$51()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$52()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$53()Lnet/minecraft/world/item/Item;': ['f92e731930bb5e5ac0ef34ba531672a7e39dd36b3460aadd05ef8393306cb8e6', '99d6569430dd30f9cb0a7dd4e4d7f39dca65364d0d1ffa789d6564c3160e5f63', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$54()Lnet/minecraft/world/item/Item;': ['7714ba8e18f0db6bab2bd0b341653f96a9a5f981ad808b1dabf72c54365bea0b', '98160517268a91f108a836e3f5854843e96772fdf820806959b3794b72d03ddc', 10, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$55()Lnet/minecraft/world/item/Item;': ['d7729687750c047d200bb210236a4297426cad16d43e8e27a3403f58ca9bfc4b', 'beeaf131783e3a213daa67ba40a15993ed6295a254b81c43eb992880fc25c251', 13, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$56()Lnet/minecraft/world/item/Item;': ['c0191793b07b408c17c0d50d73b00e6b9c15d729c3a87634f5ba3d8e82341334', 'a7e0efa70fc4792d849f3b8dc2c9a0d6feabb2ce38ce7888514867526eac2502', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$57()Lnet/minecraft/world/item/Item;': ['5086655ba3e3905fb21dcd00d6e96e803457987f773a20e77a05dda8ed8baf0c', '511077d1f36ac2a7714c635250ef85c5a237e6205f1cce1c385c1b18032207a2', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$58()Lnet/minecraft/world/item/Item;': ['1e1c9e0dfea75205c2e2c0d0be0a2bf12982fc02d8ad825bb6b1dfd62e883a0f', 'd049af527de5959f4f67c253cea598babc298e8b4e1294664765b0b6dc082328', 8, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$59()Lnet/minecraft/world/item/Item;': ['1e1c9e0dfea75205c2e2c0d0be0a2bf12982fc02d8ad825bb6b1dfd62e883a0f', 'd049af527de5959f4f67c253cea598babc298e8b4e1294664765b0b6dc082328', 8, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$6()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$60()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$61()Lnet/minecraft/world/item/Item;': ['f7886c69cc8624eef1d837a7fbb2d8d6f8aabc615da8cb336ab491ade6ce6235', 'f78662318b95bcf601e52e806b6415b00d9ea80d818ce88c9285b26baa736a50', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$62(Lnet/minecraft/world/entity/player/Player;)Lnet/minecraft/world/entity/projectile/ThrowableItemProjectile;': ['bac38bfbe1e84aa5e44899e89c1c1f99fb192995ee71d1ea50d65e1c155b1c6b', '03621fd531e73eb5db27b257c5189e0a258223e4e51bc3ee011a42e6fdee22d7', 7, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$63()Lnet/minecraft/world/item/Item;': ['6170bbfd08b2836ed9e776a6faf4682e4f9708646716c0160e13bcc32986c125', '4c0cc5a93e11e9f3ee8f64ba35af135aa2f52fc9041346d62a0c9f9815be5fcf', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$64()Lnet/minecraft/world/item/Item;': ['1ee7980eccd745100779b6563c43ddf9cb8c0f8184a61b2d52b8c7bee1f6a338', '13f205a3b5205928b7aa3a1541dd5406628ef890bc2f083001e3861c27ce32c0', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$65()Lnet/minecraft/world/item/Item;': ['a2ed034a1d56a99a005cfae5480389ac42ac12aaff2b62885fa0f41b1217211e', '6fe7fab24f2b69a675aa9091bbf97b66786ce9228f7e6b347a33ee553520af5a', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$66()Lnet/minecraft/world/item/Item;': ['aaf8577259d92e748676d4b3a21900a43c36ee085c844bc9c7f8ddf9185d7ef2', '834da1433debce5f74f37278053f9accebfeaf7bf8db7e381dd76b28386dbb82', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$67()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$68()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$69()Lnet/minecraft/world/item/Item;': ['f897098418696851186b969485d9ba015be4f88764f03cae42ee0e5fce5f0ec5', '8b2496fa8059bd6ed4971392cd637fd39e45eba140e0b55dc211e6462ab740c5', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$7()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$70()Lnet/minecraft/world/item/Item;': ['80ea46f68e34fe17dd07490c99129cfbc1dee6067ffd6fc353b72d9e684022bb', '73fd8eba0162e856b3f5a7cafe5740a6a056f4ca2043913f0cc16d019ff18c79', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$71()Lnet/minecraft/world/item/Item;': ['678903cbf3732ae64e0aa1fc33148fa398a2c73f64ca5b1ff5fc718e5f6b41e5', 'd6256c917856f0d5e3bd19d46a242d3c34f3e7f7b51663e5bc62d68232c989d1', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$72()Lnet/minecraft/world/item/Item;': ['323374ac5fc296f76167c1aa99e5cd21a15eba184c6235b3f20366a571f4b258', '98b47d50d57b5b2b450ebc9122290d7c64e83e4a10c1ed68d697aa385bc2afe5', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$73()Lnet/minecraft/world/item/Item;': ['97c2de487a982e04941e1183de8616b31f8ca5d1b29a6fd9a009ac03cbe85d20', 'd085fcc8ff76bfe2597c7887c7b50a14a1fd4d36f612a27d9fc06a22298c6341', 10, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$74()Lnet/minecraft/world/item/Item;': ['a8f68e374288c6495c5ab854c9c17cd777cc30b4be5e4e71a31e41531873d736', '52e31a0b8d94742d21c802bfb746871bcd2254221b94c92a20a0dab7995a7e05', 8, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$75()Lnet/minecraft/world/item/Item;': ['fedee03199354e73780730b633430c0760f223c2f41e75e32493e01baa810a8a', 'a36b3946fd4e79da019dca167b2859e05f58fbf5cf234bd013933b3a0355772f', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$76()Lnet/minecraft/world/item/Item;': ['c7d03efa3231a277b801b47f279daf31b7ecb661758d807dd6188498a88ac2f0', 'b43d0d7ab5bcc101515b507fd03e2e42b86c8133dbb14cd53c76e5097b5eda18', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$77()Lnet/minecraft/world/item/Item;': ['79991495f89f8b2a26c31b11fd5c8a53dd7de0615da9ceaa5e5050d8882f4692', 'a0a35d9a026b53888a019be0b08547b4f894f4df3e60a3fed5bc1a88cf804f21', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$78()Lnet/minecraft/world/item/Item;': ['88c61256d64e06e710e192c1ef6ae4bf68a9fd533398441ee251d3657ac387f5', '0fccdd7ae951cf289da0c7a2a7a49093407ed374452f109a0d58941fa46983b4', 17, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$79()Lnet/minecraft/world/level/material/Fluid;': ['17ddd17374a6af404edd3800059ef59916e856e35318f410ae35626c71e4da88', 'b9158080d45f100c7a25afd3d013a9065f4a88780d0410b14b85b1d7b1c6daa2', 2, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$8()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$80()Lnet/minecraft/world/item/Item;': ['890937e2190ba7e244b6f1dc3c35740b4af2802b9096780d845497837ba47581', '2727e115dce63cbe14f4cae6499205cac3d129c6dd03f31b725b377cbce78af2', 13, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$81()Lnet/minecraft/world/item/Item;': ['5f9a28c1c02355af250f93146866e90c7f407f9517033183fad2123dd3399197', 'a02d24f16bb89efd793c69f59a697e0a7b4aa851d97ba0761c9890c12362c810', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$82()Lnet/minecraft/world/item/Item;': ['94dcf7ed122a232c1b9e0aef7a3a5af3f24778a986ac0fb52f861b934091e0d1', '8466629a2acfb8b3e6c265e28b410908730eda24c004c17a02a53d3bac4defbc', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$83()Lnet/minecraft/world/level/material/Fluid;': ['17ddd17374a6af404edd3800059ef59916e856e35318f410ae35626c71e4da88', 'b9158080d45f100c7a25afd3d013a9065f4a88780d0410b14b85b1d7b1c6daa2', 2, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$84()Lnet/minecraft/world/item/Item;': ['2afb9a0374d54244d796e67cdb0c0e9dd5393eab63049456bf109f686dadeb0b', '44b1b80df6ad39942896b7992bac679ecd1f886456b3292d84118c68244ebdad', 13, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$85()Lnet/minecraft/world/item/Item;': ['b57e3d9fc62af8cc35f4a2048b358309913eead7e195c0ebe35bd5747faede1e', 'dcfe7d7a8c309c8b2a50c84db8189a672247e2cd7b91d03842524a20ec9ee248', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$86()Lnet/minecraft/world/item/Item;': ['12be78e1f3afe2d45829e798ca98e9858bc681e70eb9f6519794257f8dd58a3d', '5f1078d4c1d731bc6be5907a9977268310566921fcc539b44236bde11e5898d9', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$87()Lnet/minecraft/world/level/material/Fluid;': ['17ddd17374a6af404edd3800059ef59916e856e35318f410ae35626c71e4da88', 'b9158080d45f100c7a25afd3d013a9065f4a88780d0410b14b85b1d7b1c6daa2', 2, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$88()Lnet/minecraft/world/item/Item;': ['fc3ae35eecabc8a02f3f04ab286e47880a5b1f2742409b6101bd83a9ebca3072', 'fa77238f89aa696520c04539c00e55d653ca634342faa3cbb0dc4f0aad64a5ec', 13, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$89()Lnet/minecraft/world/item/Item;': ['07c4bb65197cc74dfa2422ec189549e0b198c212299762fca0a2f856afc353b6', 'c128d7f7c1ff193511c9923ceba526e11df94edf2b8284b92527f58a9728bbbd', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$9()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$90()Lnet/minecraft/world/item/Item;': ['d385d5b08e71c8ae683c30c5f0402acecbcb5ec0b6f13d0e33c25bbf57cdf7ba', '23d8d82861469e5f7ef90ec3eaf6addcdbfd78802b969e2307f887c20302976f', 4, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$91()Lnet/minecraft/world/level/material/Fluid;': ['17ddd17374a6af404edd3800059ef59916e856e35318f410ae35626c71e4da88', 'b9158080d45f100c7a25afd3d013a9065f4a88780d0410b14b85b1d7b1c6daa2', 2, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$92()Lnet/minecraft/world/item/Item;': ['6ee50396f6047acee481212ad62d3c4cbd750e9f550376efcf754d6068cb5eae', 'eba8ae14507ad16638b937620f68b6219c3b678b9db0d1fd9ed9ec9dd3297d89', 13, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$93()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$94()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$95()Lnet/minecraft/world/item/Item;': ['77d3588c5936f38daac0f0fd99705911cbc0eeb21799bef1e28f2620dac4b7cf', 'e7ad6add600cfa64d27a50c1073aa16550cc31fc3a1b9e46dc2bc72f6b1cc417', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$96()Lnet/minecraft/world/item/Item;': ['4ae0e2e5f3fda87fd14fe38619600121aab9aa0c06e9ed219b973b31104f1122', '18e2049a466745fd9951bae728237e1c33907941d204acde9d4ae43ff471273c', 9, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$97()Lnet/minecraft/world/item/Item;': ['aed11af8b9d9ef38c84d5022f206e308f85dda0e997415e05b0c2bc3ad61eee3', '323485eca98eac0559bb9abf5cca51473ef49eb4d6b4303cd41f33cb31c7a633', 7, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$98()Lnet/minecraft/world/item/Item;': ['230455d831544af1585d3aa7b09b67eae3496a0ea6e124691121a4427c13f618', 'fe2d2e4f5b6c1c198edbcd3c3b26415dfd461ad1d7b023b0709403102cb89f51', 11, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$99()Lnet/minecraft/world/item/Item;': ['0ac37708db5c575df3a9f25e24dfcfd3c6af655f1dd353cadd67884cc74b7f5f', 'f0f045a203176c0cfc095f952222b91847726883117e08050327fa69b620bd4c', 6, False],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.setup()V': ['4824f7bd08b59f416a503e5b0d349acfc2a442fbb9f9c73df045533465762c84', '3d17a9dceed7db61842f3056f6fb83d209b0fc91cf6027f219d259784bb1c073', 346, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.spawnEgg(Ljava/lang/String;Ljava/util/function/Supplier;IILnet/minecraft/resources/ResourceKey;)V': ['991a1bf5fcd88f6154a180798a9e5dab810d9aca7d6c194a635ae87fcd7336c3', '9b6c48b4b44d7e19ce8f0b074ee6172a82f641dbacc73a62e90bf0482aa4a374', 15, True],
    'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.spawnEggType(Lnet/minecraft/world/item/SpawnEggItem;)Lnet/minecraft/world/entity/EntityType;': ['6199eb64aec510f176fb56b21b057049e27e42f66f93e83b6352006bfee2eb9b', 'c1ef449d796565fff7c3922ce1b0459d0cd93d5bf438e271ee900422977ef442', 4, True],
    'com/github/alexmodguy/alexscaves/server/misc/ACDeferredRegister.<init>(Lnet/minecraft/resources/ResourceKey;Ljava/lang/String;)V': ['e13db20acd0c2b1f05f49da92f28b30323231be0f94375155859583c57d03ef1', 'cea5b2676460d398ea70e6a15017851dec3e85173e1df54f7b23f23fad030be3', 14, True],
    'com/github/alexmodguy/alexscaves/server/misc/ACDeferredRegister.create(Lnet/minecraft/resources/ResourceKey;Ljava/lang/String;)Lcom/github/alexmodguy/alexscaves/server/misc/ACDeferredRegister;': ['c3077de1d4f41f81e3144cc60372d618da2b51e53ba4b15f1e6f532a921b33b6', '25177cbaa5693b99d1e6d33c33c7b50418d701ebf3fb3bf57535696dd867cd6d', 6, True],
    'com/github/alexmodguy/alexscaves/server/misc/ACDeferredRegister.lambda$register$0(Lnet/minecraft/resources/ResourceKey;Ljava/util/function/Supplier;)Ljava/lang/Object;': ['d307bb2625a536b2f88867ab735e6caed4cf56ceb4e07b210907fd34a75a9ea8', '8798e1c55ba28e5a355fb9e784d23e3995ad0dd10f168fae77f2ea4431d124a3', 4, True],
    'com/github/alexmodguy/alexscaves/server/misc/ACDeferredRegister.raw()Lnet/neoforged/neoforge/registries/DeferredRegister;': ['d0cf9f922ab010f8c80625ee6685ff3cb0a085a2217bde1a5d580997c5014bcb', '5e1b89b94fe221eab8cf064bc637dd106f81e4a440a2d059fff9723c6fde816b', 3, True],
    'com/github/alexmodguy/alexscaves/server/misc/ACDeferredRegister.register(Ljava/lang/String;Ljava/util/function/Supplier;)Ljava/util/function/Supplier;': ['e0a5346c986f4d08bd681e3f49fb1c9efd926d25adeab8f8c8c37295fcbe4d95', 'c467a7baa1004631a619dd9fd73d06f944bc91b3f45d98b1810144ab22758c8b', 16, True],
    'com/github/alexmodguy/alexscaves/server/misc/ACIdFactories.<init>()V': ['d6f7264189858f154b120ac2e9b76f4b4dae9ddb629e4ec627af7810207e1a24', 'a4e909f6fbb3424695cfd8081458c1db352953a8b4021610a41ca8bcbc874b14', 3, True],
    'com/github/alexmodguy/alexscaves/server/misc/ACIdFactories.of(Ljava/lang/String;Ljava/lang/String;)Lnet/minecraft/resources/ResourceLocation;': ['b73796a756bab71d795da49934925732b2f951ceb4b6d7173d54e2804b20f01b', '4680f4f4e2be86ac6ac2b325639f6b941343e42fbd95bcb28fad4eacb29a5f92', 4, True],
    'com/github/alexmodguy/alexscaves/server/misc/ACIdFactories.parse(Ljava/lang/String;)Lnet/minecraft/resources/ResourceLocation;': ['dcfad17ffecca370f37d96501be731d7796fc33815576b9bd79436cf2d0c59dc', 'ec1b11a5edbb87c65174c9b6f36cb8a0ca9a804b8a2f6d9257fc553a04fb6816', 3, True],
    'com/github/alexmodguy/alexscaves/server/misc/ACIdFactories.vanilla(Ljava/lang/String;)Lnet/minecraft/resources/ResourceLocation;': ['9b344ef2ef9d6a46808c617610b0f99fd6b40968895bc7f805e0815e903bd57b', '6585baa3eabebc5c552a3513850072e24f6abfb4965c8779399d50dc007e6865', 3, True],
    'com/github/alexmodguy/alexscaves/server/misc/ACRegistryIds.<clinit>()V': ['f7d71159e113cf82e6104844e132da2b8215b93f6642748c81420e1025d7b931', '17c4f532b622afb8e0a32dcda2fdc5f831b52184df9d1700ab0226d60e3beca1', 5, True],
    'com/github/alexmodguy/alexscaves/server/misc/ACRegistryIds.<init>()V': ['d6f7264189858f154b120ac2e9b76f4b4dae9ddb629e4ec627af7810207e1a24', 'a4e909f6fbb3424695cfd8081458c1db352953a8b4021610a41ca8bcbc874b14', 3, True],
    'com/github/alexmodguy/alexscaves/server/misc/ACRegistryIds.constructing(Lnet/minecraft/resources/ResourceKey;Ljava/util/function/Supplier;)Ljava/lang/Object;': ['3e8109215accd9f2c64c4c1d101f363a0b55316a209a34260d75b4bc79d08e66', 'b9b0fa29f7987cc57952e1c7fd6534e3013f5fdaf8167b8e656a09b4db9e7fdd', 31, True],
    'com/github/alexmodguy/alexscaves/server/misc/ACRegistryIds.pending()Lnet/minecraft/resources/ResourceKey;': ['674533d73daece2bd3ec5f8427ae4f02b290ac2b8309731140be005e7a793473', '17c19b99fd47a6a5c5e5d5e41473344b113469a8017fdf622228a822fa441841', 4, True],
}
NATIVE_PIN = '38998688306d74c46a0a59d72e7d8b59b7fc486f6d61700a7d445b90c1f6d7df'


def method_key(method):
    declaration = method["declaration"]
    return declaration["name"], declaration["descriptor"]


def method_at(data, name, descriptor=None):
    found = [m for m in data["methods"] if m["declaration"]["name"] == name
             and (descriptor is None or m["declaration"]["descriptor"] == descriptor)]
    require(len(found) == 1, "method not unique: " + name)
    return found[0]


def descriptor_parts(descriptor):
    require(descriptor.startswith("("), "bad method descriptor")
    cursor, arguments = 1, []
    while descriptor[cursor] != ")":
        start = cursor
        while descriptor[cursor] == "[":
            cursor += 1
        if descriptor[cursor] == "L":
            cursor = descriptor.index(";", cursor) + 1
        else:
            require(descriptor[cursor] in "BCDFIJSZ", "bad argument descriptor")
            cursor += 1
        arguments.append(descriptor[start:cursor])
    return arguments, descriptor[cursor + 1:]


def member(constant):
    value = constant["value"]
    require(constant["tag"] in (9, 10, 11) and len(value) == 3 and value[2][0] == 12,
            "typed member constant required")
    return {"owner": value[1], "name": value[2][1], "descriptor": value[2][2]}


def cp(data, row):
    index = cp_index(row["operand"])
    require(index is not None and str(index) in data["constants"], "missing typed operand")
    return data["constants"][str(index)]


def factory_site(data, row):
    constant = cp(data, row)
    require(constant["tag"] == 18, "invokedynamic constant type drift")
    _, index, signature = constant["value"]
    require(0 <= index < len(data["bootstrap_methods"]), "bootstrap index drift")
    bootstrap = data["bootstrap_methods"][index]
    return index, signature[1], signature[2], bootstrap


def supplier_handle(data, row):
    index, name, descriptor, bootstrap = factory_site(data, row)
    require((name, descriptor) == ("get", "()Ljava/util/function/Supplier;"),
            "supplier factory descriptor drift")
    require(bootstrap["handle"]["reference_kind"] == 6 and
            bootstrap["handle"]["reference"][1:2] == ["java/lang/invoke/LambdaMetafactory"] and
            bootstrap["handle"]["reference"][2][1] == "metafactory", "not LambdaMetafactory")
    args = bootstrap["arguments"]
    require(len(args) == 3 and args[0] == "()Ljava/lang/Object;" and args[2] == ITEM_DESC,
            "supplier erased/instantiated type drift")
    handle = args[1]
    require(handle["reference_kind"] == 6 and handle["reference"][0] == 10,
            "factory must use REF_invokeStatic Methodref")
    _, owner, (_, method, desc) = handle["reference"]
    require(owner == TARGET and method.startswith("lambda$static$") and desc == ITEM_DESC,
            "supplier factory owner/name/descriptor drift")
    target = method_at(data, method, desc)
    return index, {"reference_kind": 6, "owner": owner, "name": method, "descriptor": desc,
                   "code_sha256": target["declaration"]["code_sha256"],
                   "instruction_sha256": target["instruction_sha256"]}


def evaluate_initializer(data):
    """Symbolically consume the entire straight-line clinit, fail on unknown opcodes.

    Values carry causal producers, not adjacent lexical slices. Constructor dup
    aliases and literal integer arrays are retained to prove non-supplier writes.
    All calls consume descriptor-sized arguments; unknown call results remain
    opaque and can never be accepted as a supplier binding.
    """
    body = method_at(data, "<clinit>", "()V")
    require(not body["declaration"]["exception_handlers"], "initializer exception flow")
    stack, writes, calls = [], {}, []

    def pop():
        require(bool(stack), "initializer operand stack underflow")
        return stack.pop()

    def arguments(desc):
        types, result = descriptor_parts(desc)
        values = [pop() for _ in types][::-1]
        return values, result

    for row in body["instructions"]:
        opcode, offset = row["opcode"], row["offset"]
        if opcode in ("ldc", "ldc_w", "ldc2_w"):
            constant = cp(data, row)
            tag, value = constant["tag"], constant["value"]
            if tag == 8:
                stack.append({"kind": "string", "value": value, "offset": offset})
            elif tag in (3, 4, 5, 6):
                raw = bytes.fromhex(value["hex"])
                number = struct.unpack({3:">i",4:">f",5:">q",6:">d"}[tag], raw)[0]
                stack.append({"kind": "number", "value": number, "offset": offset})
            else:
                raise AuditError("unsupported initializer literal type")
        elif opcode.startswith("iconst_"):
            value = -1 if opcode == "iconst_m1" else int(opcode[7:])
            stack.append({"kind": "number", "value": value, "offset": offset})
        elif opcode.startswith("fconst_"):
            stack.append({"kind": "number", "value": float(opcode[7:]), "offset": offset})
        elif opcode in ("bipush", "sipush"):
            stack.append({"kind": "number", "value": int(row["operand"]), "offset": offset})
        elif opcode == "new":
            constant = cp(data, row)
            require(constant["tag"] == 7, "new must refer to class")
            stack.append({"kind": "object", "owner": constant["value"], "offset": offset})
        elif opcode == "dup":
            require(bool(stack), "dup without value")
            stack.append(stack[-1])
        elif opcode == "newarray":
            size = pop()
            require(row["operand"] == "int" and size["kind"] == "number" and
                    isinstance(size["value"], int) and 0 <= size["value"] <= 64,
                    "unsupported initializer array")
            stack.append({"kind": "array", "values": [None] * size["value"], "offset": offset})
        elif opcode == "iastore":
            value, index, array = pop(), pop(), pop()
            require(array["kind"] == "array" and index["kind"] == "number" and
                    value["kind"] == "number" and 0 <= index["value"] < len(array["values"]),
                    "initializer array write drift")
            require(array["values"][index["value"]] is None, "duplicate literal array write")
            array["values"][index["value"]] = value["value"]
        elif opcode == "getstatic":
            ref = member(cp(data, row))
            if ref["owner"] == TARGET:
                require(ref["name"] in writes, "registry field read before declaration")
            stack.append({"kind": "field", **ref, "offset": offset})
        elif opcode == "putstatic":
            ref, value = member(cp(data, row)), pop()
            require(ref["owner"] == TARGET and ref["name"] not in writes,
                    "unknown or duplicate initializer field write")
            writes[ref["name"]] = {"descriptor": ref["descriptor"], "write_offset": offset,
                                    "value": copy.deepcopy(value)}
        elif opcode == "invokedynamic":
            index, name, desc, bootstrap = factory_site(data, row)
            args, result = arguments(desc)
            require(result != "V", "void dynamic initializer")
            stack.append({"kind": "dynamic", "index": index, "name": name,
                          "descriptor": desc, "arguments": args, "offset": offset})
        elif opcode in ("invokestatic", "invokevirtual", "invokespecial", "invokeinterface"):
            ref = member(cp(data, row))
            args, result = arguments(ref["descriptor"])
            receiver = None if opcode == "invokestatic" else pop()
            call = {"kind": "call", **ref, "arguments": args, "receiver": receiver, "offset": offset}
            if ref["name"] == "<init>":
                require(opcode == "invokespecial" and result == "V" and
                        receiver["kind"] == "object" and receiver["owner"] == ref["owner"] and
                        "constructor" not in receiver, "constructor alias/owner drift")
                receiver["constructor"] = {"descriptor": ref["descriptor"], "arguments": args,
                                           "offset": offset}
            else:
                calls.append(copy.deepcopy(call))
                if result != "V":
                    stack.append(call)
        elif opcode == "pop":
            pop()
        elif opcode == "return":
            require(not stack, "initializer stack not empty at return")
        else:
            raise AuditError("unsupported initializer opcode: " + opcode)
    require(not stack and body["instructions"][-1]["opcode"] == "return", "initializer termination")
    return writes, calls


def resolve_bindings(data):
    writes, calls = evaluate_initializer(data)
    fields = {field["name"]: field for field in data["fields"]}
    require(len(fields) == 200 and dict(Counter(f["descriptor"] for f in fields.values())) == EXPECTED_FIELDS,
            "200-field declaration roster drift")
    require(set(writes) == set(fields) and all(writes[n]["descriptor"] == f["descriptor"]
            for n, f in fields.items()), "initializer/declaration write coverage drift")
    declaration = writes["DEF_REG"]["value"]
    require(declaration["kind"] == "call" and declaration["owner"] == BRIDGE and
            declaration["name"] == "create" and declaration["receiver"] is None,
            "DEF_REG create flow drift")
    key, namespace = declaration["arguments"]
    require(key == {"kind": "field", "owner": "net/minecraft/core/registries/Registries",
                    "name": "ITEM", "descriptor": "Lnet/minecraft/resources/ResourceKey;", "offset": 292},
            "item registry key drift")
    require(namespace["kind"] == "string" and namespace["value"] == "alexscaves",
            "literal namespace drift")
    bindings = []
    instructions = {row["offset"]: row for row in method_at(data, "<clinit>")["instructions"]}
    for name in sorted(fields):
        if fields[name]["descriptor"] != SUPPLIER:
            continue
        write = writes[name]
        value = write["value"]
        require(value["kind"] == "call" and value["owner"] == BRIDGE and
                value["name"] == "register" and value["descriptor"] == REGISTER_DESC,
                "supplier field is not result of bridge register")
        receiver = value["receiver"]
        require(receiver["kind"] == "field" and receiver["owner"] == TARGET and
                receiver["name"] == "DEF_REG", "supplier register receiver drift")
        literal, supplier = value["arguments"]
        require(literal["kind"] == "string" and re.fullmatch(r"[a-z0-9_./-]+", literal["value"]),
                "supplier resource path is not literal")
        require(supplier["kind"] == "dynamic" and not supplier["arguments"],
                "supplier causal factory flow drift")
        index, factory = supplier_handle(data, instructions[supplier["offset"]])
        require(receiver["offset"] < literal["offset"] < supplier["offset"] < value["offset"] < write["write_offset"],
                "supplier evaluation order drift")
        bindings.append({"field": name, "namespace": namespace["value"], "path": literal["value"],
                         "resource_location": namespace["value"] + ":" + literal["value"],
                         "receiver_read_offset": receiver["offset"], "literal_offset": literal["offset"],
                         "factory_site_offset": supplier["offset"], "register_offset": value["offset"],
                         "write_offset": write["write_offset"], "bootstrap_index": index, "factory": factory})
    require(len(bindings) == 188 and len({b["path"] for b in bindings}) == 188 and
            len({b["factory"]["name"] for b in bindings}) == 188, "supplier bijection drift")
    egg_method = method_at(data, "spawnEgg", SPAWN_DESC)
    concat_site = next(row for row in egg_method["instructions"] if row["offset"] == 4)
    _, concat_name, concat_desc, concat = factory_site(data, concat_site)
    require(concat_name == "makeConcatWithConstants" and concat_desc ==
            "(Ljava/lang/String;)Ljava/lang/String;" and
            concat["handle"]["reference_kind"] == 6 and
            concat["handle"]["reference"][1] == "java/lang/invoke/StringConcatFactory" and
            concat["arguments"] == ["spawn_egg_\u0001"], "spawn egg path recipe drift")
    recipe = concat["arguments"][0]
    eggs = []
    for call in calls:
        if (call["owner"], call["name"], call["descriptor"]) != (TARGET, "spawnEgg", SPAWN_DESC):
            continue
        name, entity, primary, secondary, tab = call["arguments"]
        require(name["kind"] == "string" and entity["kind"] == "field" and
                primary["kind"] == secondary["kind"] == "number" and tab["kind"] == "field",
                "spawn egg argument provenance drift")
        eggs.append({"base_name": name["value"], "path": recipe.replace("\u0001", name["value"]),
                     "resource_location": "alexscaves:" + recipe.replace("\u0001", name["value"]),
                     "entity_supplier": {k: entity[k] for k in ("owner", "name", "descriptor")},
                     "primary_color": primary["value"], "secondary_color": secondary["value"],
                     "creative_tab": {k: tab[k] for k in ("owner", "name", "descriptor")},
                     "call_offset": call["offset"]})
    require(len(eggs) == 43 and len({e["path"] for e in eggs}) == 43 and
            not ({e["path"] for e in eggs} & {b["path"] for b in bindings}), "spawn egg roster drift")
    support = {name: write for name, write in writes.items() if fields[name]["descriptor"] != SUPPLIER}
    return bindings, eggs, support



def local_callback_contracts(classes):
    """Describe the finite local code boundary without claiming entity execution."""
    output = {}
    projectiles = {1: "SeekingArrowEntity", 2: "CinderBrickEntity", 3: "InkBombEntity",
                   4: "InkBombEntity", 5: "GuanoEntity", 6: "BurrowingArrowEntity"}
    for number, entity in projectiles.items():
        owner = TARGET + "$" + str(number)
        data = classes[owner]
        method = method_at(data, "getProjectile")
        instructions = method["instructions"]
        require(not any(row["opcode"].startswith(("if", "goto")) or "switch" in row["opcode"]
                        for row in instructions), "projectile callback guard drift")
        calls = [member(cp(data, row)) for row in instructions if row["opcode"].startswith("invoke")]
        ctor = next(ref for ref in calls if ref["name"] == "<init>")
        require(ctor["owner"] == PREFIX + "server/entity/item/" + entity and
                ctor["descriptor"] == "(Lnet/minecraft/world/level/Level;DDD)V",
                "projectile callback constructor drift")
        require(not any(ref["name"] in ("addFreshEntity", "shrink") for ref in calls),
                "projectile factory cannot claim local spawn/cost")
        output[owner] = {"method": "getProjectile", "entity": ctor["owner"],
                         "constructor_descriptor": ctor["descriptor"],
                         "constructor_arguments": ["level", "position.x", "position.y", "position.z"],
                         "owner_argument": None, "pickup_allowed_write": number in (1, 6),
                         "set_glowing_bomb": True if number == 4 else None,
                         "set_item_argument": "input_stack" if number == 4 else None,
                         "local_guards": [], "spawn_request": False, "stack_cost_request": None,
                         "instruction_sha256": method["instruction_sha256"]}
    target = classes[TARGET]
    entities = {"lambda$static$62": "CinderBrickEntity", "lambda$static$112": "DepthChargeEntity",
                "lambda$static$120": "GuanoEntity", "lambda$static$165": "ThrownIceCreamScoopEntity",
                "lambda$static$167": "ThrownIceCreamScoopEntity", "lambda$static$169": "ThrownIceCreamScoopEntity"}
    for name, entity in entities.items():
        method = method_at(target, name, PLAYER_DESC)
        require([row["opcode"] for row in method["instructions"]] ==
                ["new", "dup", "aload_0", "invokevirtual", "aload_0", "invokespecial", "areturn"],
                "player projectile factory local flow drift")
        output[TARGET + "." + name] = {"method": name, "entity": PREFIX + "server/entity/item/" + entity,
            "constructor_arguments": ["player.level()", "player"], "set_item_argument": None,
            "local_guards": [], "spawn_request": False, "stack_cost_request": None,
            "instruction_sha256": method["instruction_sha256"]}
    data = classes[TARGET + "$7"]
    method = method_at(data, "execute")
    instructions = {row["offset"]: row for row in method["instructions"]}
    require(not any(row["opcode"].startswith(("if", "goto")) or "switch" in row["opcode"]
                    for row in instructions.values()), "nuclear dispenser local guard drift")
    require([member(cp(data, instructions[offset]))["name"] for offset in (66, 98, 111, 116)] ==
            ["addFreshEntity", "playSound", "gameEvent", "shrink"] and
            instructions[69]["opcode"] == "pop" and instructions[115]["opcode"] == "iconst_1" and
            instructions[120]["opcode"] == "areturn", "nuclear dispenser cost/order/acceptance drift")
    output[TARGET + "$7"] = {"method": "execute", "entity": PREFIX + "server/entity/item/NuclearBombEntity",
        "position": ["dispenserPos.relative(FACING).x + 0.5d", "dispenserPos.relative(FACING).y",
                     "dispenserPos.relative(FACING).z + 0.5d"],
        "ordered_requests": ["addFreshEntity", "playSound", "gameEvent", "shrink"],
        "add_fresh_entity_result": "DISCARDED_BOOLEAN", "owner_argument": None,
        "sound": {"event": "TNT_PRIMED", "source": "BLOCKS", "volume": 1.0, "pitch": 1.0,
                  "player": None, "position": "bomb.x/y/z"},
        "game_event": {"event": "ENTITY_PLACE", "entity": None, "position": "front_block"},
        "stack_cost_request": 1, "cost_guard": "NONE_IF_PRIOR_CALLS_RETURN_NORMALLY",
        "local_guards": [], "return": "SAME_INPUT_STACK", "fuse_setter_call": False,
        "instruction_sha256": method["instruction_sha256"]}
    return output


def compact_class(reader, data, full):
    selected = {method_key(m) for m in data["methods"] if full(method_key(m))}
    result = {key: data[key] for key in ("class_sha256", "parent", "interfaces", "fields", "bootstrap_methods")}
    result["methods"] = [{key: value for key, value in m.items()
                          if key != "instructions" or method_key(m) in selected}
                         for m in data["methods"]]
    used = set()
    for method in result["methods"]:
        for row in method.get("instructions", []):
            index = cp_index(row["operand"])
            if index is not None:
                used.add(index)
    result["constants"] = {str(index): {"tag": reader.pool[index][0], "value": reader.resolve(index)}
                           for index in sorted(used)}
    result["declared_method_count"] = len(reader.methods)
    result["coded_method_count"] = len(data["methods"])
    return result


def native(jar, javap):
    verify_artifact(jar)
    with zipfile.ZipFile(jar) as archive:
        entries = archive.namelist()
        require(len(entries) == len(set(entries)), "duplicate ZIP members")
        paths = sorted(path for path in entries if path.endswith(".class"))
        require(len(paths) == 1555, "class roster drift")
        owners = [TARGET, BRIDGE, IDS, ID_FACTORY, ENTRY,
                  *sorted(path[:-6] for path in paths if path.startswith(TARGET + "$"))]
        classes = {}
        for owner in owners:
            reader, parsed, data = inspect_methods(jar, javap, archive, owner)
            if owner == TARGET:
                full = lambda key: not key[0].startswith("lambda$static$") or key[1] == PLAYER_DESC
            elif owner == ENTRY:
                full = lambda key: key[0] in ("<init>", "commonSetup", "lambda$commonSetup$0")
            else:
                full = lambda key: True
            classes[owner] = compact_class(reader, data, full)
        census, direct_calls = {}, []
        tracked = {TARGET, BRIDGE, IDS, ID_FACTORY}
        for path in paths:
            reader = ClassReader(archive.read(path))
            require(reader.name + ".class" == path and reader.major == 65, "class identity drift")
            typed = {owner: reader.typed_refs(owner) for owner in sorted(tracked)}
            typed = {owner: values for owner, values in typed.items() if values}
            refs = refs_for(reader, tracked)
            if typed or refs:
                census[reader.name] = {"typed_counts": {owner: len(values) for owner, values in typed.items()},
                                      "typed_references_sha256": digest(canonical(typed).encode()),
                                      "member_reference_count": len(refs),
                                      "member_references_sha256": digest(canonical(refs).encode())}
            for ref in refs:
                if ref["kind"] in (10, 11) and (ref["owner"] != TARGET or ref["name"] in
                    ("setup", "getSpawnEggFor", "getSpawnEggsForTab", "spawnEgg", "spawnEggType")):
                    direct_calls.append({"caller": reader.name, **ref})
        bindings, eggs, support = resolve_bindings(classes[TARGET])
        pending = [ref for ref in direct_calls if ref["owner"] == IDS and ref["name"] == "pending"]
        require(not pending, "ACRegistryIds.pending caller boundary drift")
        return {"class_entries_scanned": len(paths),
                "class_roster_sha256": digest(("\n".join(paths) + "\n").encode()),
                "typed_census": census,
                "typed_census_method": "Typed CLASS/member/NameAndType/MethodType and declaration descriptors; plain strings are excluded. Owner records retain counts and complete-reference digests.",
                "direct_helper_method_references": direct_calls,
                "classes": classes, "bindings": bindings, "spawn_egg_registrations": eggs,
                "local_callback_contracts": local_callback_contracts(classes),
                "support_field_initializers": support,
                "counts": {"registry_fields": 200, "supplier_field_bindings": 188,
                           "extra_spawn_egg_declarations": 43, "literal_registration_requests": 231,
                           "target_declared_and_coded_methods": 208, "bridge_declared_and_coded_methods": 5,
                           "nested_classes": 7, "nested_coded_methods": 14,
                           "player_projectile_factories": 6, "pending_method_references": 0}}



def validate_bridge_pipeline(classes):
    """Check the concrete deferred/native handoffs and return/exception handling."""
    bridge = classes[BRIDGE]
    require(bridge["declared_method_count"] == bridge["coded_method_count"] == 5,
            "bridge method coverage drift")
    register = method_at(bridge, "register", REGISTER_DESC)
    instructions = register["instructions"]
    require([row["opcode"] for row in instructions] ==
            ["aload_0", "getfield", "aload_0", "getfield", "aload_1", "invokestatic",
             "invokestatic", "astore_3", "aload_0", "getfield", "aload_1", "aload_3",
             "aload_2", "invokedynamic", "invokevirtual", "areturn"],
            "deferred register evaluation order drift")
    refs = {row["offset"]: member(cp(bridge, row)) for row in instructions
            if row["opcode"] in ("getfield", "invokestatic", "invokevirtual")}
    require([(refs[offset]["owner"], refs[offset]["name"]) for offset in (1, 5, 9, 12, 17, 28)] ==
            [(BRIDGE, "registryKey"), (BRIDGE, "namespace"), (ID_FACTORY, "of"),
             ("net/minecraft/resources/ResourceKey", "create"), (BRIDGE, "delegate"),
             ("net/neoforged/neoforge/registries/DeferredRegister", "register")],
            "deferred register typed handoff drift")
    dynamic = next(row for row in instructions if row["opcode"] == "invokedynamic")
    _, name, descriptor, bootstrap = factory_site(bridge, dynamic)
    require(name == "get" and descriptor ==
            "(Lnet/minecraft/resources/ResourceKey;Ljava/util/function/Supplier;)Ljava/util/function/Supplier;" and
            bootstrap["arguments"][1] == {"reference_kind": 6, "reference": [10, BRIDGE,
                [12, "lambda$register$0", "(Lnet/minecraft/resources/ResourceKey;Ljava/util/function/Supplier;)Ljava/lang/Object;"]]},
            "deferred wrapper dispatch drift")
    wrapped = method_at(bridge, "lambda$register$0")["instructions"]
    require(member(cp(bridge, wrapped[2]))["owner"] == IDS and
            member(cp(bridge, wrapped[2]))["name"] == "constructing",
            "wrapped supplier native construction drift")
    ids = classes[IDS]
    constructing = method_at(ids, "constructing")
    require(constructing["declaration"]["exception_handlers"] ==
            [{"start": 17, "end": 24, "target": 46, "catch": None},
             {"start": 46, "end": 48, "target": 46, "catch": None}],
            "construction cleanup exception boundary drift")
    id_rows = {row["offset"]: row for row in constructing["instructions"]}
    require((id_rows[25]["opcode"], id_rows[25]["operand"], id_rows[49]["opcode"], id_rows[49]["operand"]) ==
            ("ifnonnull", "37", "ifnonnull", "61") and
            [member(cp(ids, id_rows[offset]))["name"] for offset in (3, 14, 18, 31, 41, 55, 65)] ==
            ["get", "set", "get", "remove", "set", "remove", "set"] and
            id_rows[70]["opcode"] == "athrow", "construction restore/rethrow drift")
    entry = classes[ENTRY]
    ctor = {row["offset"]: row for row in method_at(entry, "<init>")["instructions"]}
    require(member(cp(entry, ctor[261])) == {"owner": TARGET, "name": "DEF_REG",
            "descriptor": "L" + BRIDGE + ";"} and
            member(cp(entry, ctor[264]))["owner"] == BRIDGE and
            member(cp(entry, ctor[264]))["name"] == "raw" and
            ctor[267]["opcode"] == "aload_1" and
            member(cp(entry, ctor[268])) == {"owner": "net/neoforged/neoforge/registries/DeferredRegister",
                "name": "register", "descriptor": "(Lnet/neoforged/bus/api/IEventBus;)V"},
            "native event-bus registration boundary drift")
    require([member(cp(entry, ctor[offset]))["name"] for offset in (38, 41, 44)] ==
            ["get", "getActiveContainer", "getEventBus"] and ctor[47]["opcode"] == "astore_1",
            "native mod event-bus origin drift")
    setup = {row["offset"]: row for row in method_at(entry, "commonSetup")["instructions"]}
    _, name, descriptor, bootstrap = factory_site(entry, setup[10])
    require(name == "run" and descriptor == "()Ljava/lang/Runnable;" and
            bootstrap["arguments"][1]["reference"][1:] == [ENTRY, [12, "lambda$commonSetup$0", "()V"]] and
            member(cp(entry, setup[15]))["name"] == "enqueueWork",
            "common setup deferred dispatch drift")
    queued = {row["offset"]: row for row in method_at(entry, "lambda$commonSetup$0")["instructions"]}
    require(member(cp(entry, queued[12])) == {"owner": TARGET, "name": "setup", "descriptor": "()V"},
            "queued item setup handoff drift")


def validate_methods(classes):
    require(set(classes) == set(CLASS_PINS), "contract class roster drift")
    for owner, data in classes.items():
        require(data["class_sha256"] == CLASS_PINS[owner], "pinned class identity drift: " + owner)
        keys = [method_key(m) for m in data["methods"]]
        require(len(keys) == len(set(keys)) == data["coded_method_count"], "method coverage/duplicates")
        for method in data["methods"]:
            pin_key = owner + "." + method["declaration"]["name"] + method["declaration"]["descriptor"]
            require(pin_key in BODY_PINS and
                    [method["declaration"]["code_sha256"], method["instruction_sha256"], method["instruction_count"]]
                    == BODY_PINS[pin_key][:3], "method body pin drift: " + pin_key)
            require(("instructions" in method) == BODY_PINS[pin_key][3], "full-body scope drift: " + pin_key)
            if "instructions" in method:
                instructions = method["instructions"]
                require(len(instructions) == method["instruction_count"] and
                        len({row["offset"] for row in instructions}) == len(instructions) and
                        instructions == sorted(instructions, key=lambda row: row["offset"]) and
                        digest(canonical(instructions).encode()) == method["instruction_sha256"],
                        "whole method instructions drift: " + pin_key)


def validate_contract(report):
    require(report["schema"] == "AC_ITEM_REGISTRY_CONTRACT_V1", "schema drift")
    require(report["artifact"] == {"version": "1.0.10", "sha1": SHA1, "sha256": SHA256,
                                   "size_bytes": SIZE}, "artifact claim drift")
    require(report["claims"] == CLAIMS and report["axes"] == AXES and
            report["boundaries"] == BOUNDARIES, "contract claim/scope drift")
    require(report["discovery_prerequisite"] == {"schema": "AC_ITEM_REGISTRY_DISCOVERY_V1",
            "report_sha256": "ac1f8d785501c5c1d2dbe1e22ee9248682af9662c6f6c4dbb972c536f33561e8",
            "disposition": "Immutable original discovery; not promoted to a contract."},
            "discovery prerequisite drift")
    evidence = report["native"]
    validate_methods(evidence["classes"])
    validate_bridge_pipeline(evidence["classes"])
    require(evidence["local_callback_contracts"] == local_callback_contracts(evidence["classes"]),
            "local callback semantic profile drift")
    bindings, eggs, support = resolve_bindings(evidence["classes"][TARGET])
    require(evidence["bindings"] == bindings, "causal binding table drift")
    require(evidence["spawn_egg_registrations"] == eggs, "spawn egg declaration table drift")
    require(evidence["support_field_initializers"] == support, "support field causal initializers drift")
    require(evidence["class_entries_scanned"] == 1555, "typed class census drift")
    require(digest(canonical(evidence).encode()) == NATIVE_PIN, "pinned complete bounded evidence drift")


def build_report(jar, javap):
    report = {"schema": "AC_ITEM_REGISTRY_CONTRACT_V1",
              "artifact": {"version": "1.0.10", "sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
              "claims": CLAIMS, "axes": AXES, "boundaries": BOUNDARIES,
              "discovery_prerequisite": {"schema": "AC_ITEM_REGISTRY_DISCOVERY_V1",
                  "report_sha256": "ac1f8d785501c5c1d2dbe1e22ee9248682af9662c6f6c4dbb972c536f33561e8",
                  "disposition": "Immutable original discovery; not promoted to a contract."},
              "native": native(jar, javap)}
    validate_contract(report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("jar", "javap", "seal", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    require(args.output.suffix == ".json" and not args.output.exists(), "new JSON output required")
    require(args.output.resolve() not in {args.jar.resolve(), args.javap.resolve(), args.seal.resolve()},
            "output must not replace input")
    expected = load_seal(args.seal)
    validate_contract(expected)
    report = build_report(args.jar, args.javap)
    require(report == expected, "exact native contract differs from checked seal")
    encoded = canonical(report)
    require(len(encoded.encode()) < 2_000_000, "bounded seal exceeds loader budget")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(encoded, encoding="utf8")
    print("REPORT_SHA256", digest(args.output.read_bytes()))
    print("COUNTS", json.dumps(report["native"]["counts"], sort_keys=True))
    print("END_ITEM_REGISTRY_CONTRACT NO_MUTATION STATIC_7_AXES RUNTIME_NOT_VERIFIED QA_NOT_TESTED")


if __name__ == "__main__":
    main()
