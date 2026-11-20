#!/usr/bin/env python3
"""Verify selected CaveBook SHA-exact bytecode facts; never a gameplay certificate."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

CHECKS = {
    'CaveBookItem': '722c46d0e9f6baee5d0997ff8c556db0269c035f1d678314c6b42caf71a1c238',
    'CommonProxy': '6552d7a5966f1a0539eda4b90588680b5da02bf28fcfb9a6d6aede5ca0804cb4',
    'ClientProxy': '4a18115257725c14c0c6b8285932bd5834e9be3e2778a154d3d925dc5e732b9d',
    'CaveBookScreen': '3b99cb08ecd96fe55c589e5d393aafa3f934dbf96bc64f50d29856251a5cdffc',
    'BookEntry': '6e17abf16abb22926b79d6d2b945ccb67ea144cfeccd4c1b65331402a41da49b',
    'CaveBookProgress': 'c32103b460a49f0c01bf4d90bce2fe1647a94150076aa1309b4b6b897dab832e',
    'CaveInfoItem': '2150b671133f3420cda0a5368cbee214811bb94105e0024ae1d0e6a471fc9176',
    'LecternBooks': 'b06b9cd436459727979ee4e74eccea44a27b8ee193fd1579694098294c5e5997',
}

def require(ok, message):
    if not ok: raise AssertionError(message)

def method(source, signature):
    key='  '+signature+'\n'
    require(source.count(key)==1,'method absent or ambiguous: '+signature)
    tail=source.split(key,1)[1]
    require('    Code:' in tail,'no body: '+signature)
    return tail.split('      LineNumberTable:',1)[0]

def has_all(source, fragments, location):
    for token in fragments:
        require(token in source, location+' missing '+token)

def audit(folder):
    report=json.loads((folder/'report.json').read_text(encoding='utf-8'))
    require(report['scope']=='DISCOVERY_NOT_CERTIFIED' and report['mutation']=='NO_MUTATION' and not report['provider_universe_closed'] and report['physical_qa']=='NOT_TESTED','invalid promotion')
    transcripts={}
    for short, digest in CHECKS.items():
        matches=[(k,v) for k,v in report['captures'].items() if k.endswith('/'+short)]
        require(len(matches)==1,'capture not unique: '+short)
        path=folder/matches[0][1]['transcript']
        raw=path.read_bytes()
        require(hashlib.sha256(raw).hexdigest()==digest,'SHA changed: '+short)
        require(matches[0][1]['javap_sha256']==digest,'manifest inconsistent: '+short)
        transcripts[short]=raw.decode('utf-8')
    item=transcripts['CaveBookItem']
    use=method(item,'public net.minecraft.world.InteractionResultHolder<net.minecraft.world.item.ItemStack> use(net.minecraft.world.level.Level, net.minecraft.world.entity.player.Player, net.minecraft.world.InteractionHand);')
    has_all(use,['ServerPlayer','CriteriaTriggers.CONSUME_ITEM','ConsumeItemTrigger.trigger:',
                 'Stats.ITEM_USED','ServerPlayer.awardStat:','Player.swing:',
                 'Level.isClientSide:','CommonProxy.openBookGUI:','ACCompat.usePass:'], 'item use')
    require('ItemStack.shrink:' not in use and 'ItemStack.hurtAndBreak:' not in use,'item unexpectedly consumes stack')
    ctor=method(item,'public com.github.alexmodguy.alexscaves.server.item.CaveBookItem();')
    has_all(ctor,['Item$Properties.stacksTo:','Rarity.UNCOMMON'],'item constructor')
    tip=method(item,'public void appendHoverText(net.minecraft.world.item.ItemStack, net.minecraft.world.item.Item$TooltipContext, java.util.List<net.minecraft.network.chat.Component>, net.minecraft.world.item.TooltipFlag);')
    has_all(tip,['item.alexscaves.cave_book.desc','ChatFormatting.GRAY'],'tooltip')
    client=method(transcripts['ClientProxy'],'public void openBookGUI(net.minecraft.world.item.ItemStack);')
    has_all(client,['CaveBookScreen','Minecraft.setScreen:'],'client GUI')
    common=method(transcripts['CommonProxy'],'public void openBookGUI(net.minecraft.world.item.ItemStack);')
    require('0: return' in common and 'setScreen:' not in common,'server proxy must remain inert')
    gui=transcripts['CaveBookScreen']
    has_all(method(gui,'public com.github.alexmodguy.alexscaves.client.gui.book.CaveBookScreen();'),['books/root.json'],'default page')
    has_all(method(gui,'public com.github.alexmodguy.alexscaves.client.gui.book.CaveBookScreen(java.lang.String);'),['CaveBookProgress.getCaveBookProgress:','Minecraft.player'],'local-player progress')
    has_all(method(gui,'protected com.github.alexmodguy.alexscaves.client.gui.book.BookEntry readBookEntry(net.minecraft.resources.ResourceLocation);'),['ResourceManager.getResource:','BookEntry.deserialize:'],'resource loader')
    has_all(method(gui,'public static java.lang.String getBookFileDirectory();'),['alexscaves:books/'],'book path')
    has_all(method(transcripts['BookEntry'],'public int getVisibility(com.github.alexmodguy.alexscaves.client.gui.book.CaveBookScreen);'),['CaveBookProgress.isUnlockedFor:','CaveBookProgress$Subcategory.SECRETS'],'visibility gate')
    progress=transcripts['CaveBookProgress']
    has_all(method(progress,'public static com.github.alexmodguy.alexscaves.server.misc.CaveBookProgress getCaveBookProgress(net.minecraft.world.entity.player.Player);'),['CitadelEntityData.getOrCreateCitadelTag:','AlexsCavesBookProgress'],'progress read')
    has_all(method(progress,'public static void saveCaveBookProgress(com.github.alexmodguy.alexscaves.server.misc.CaveBookProgress, net.minecraft.world.entity.player.Player);'),['CitadelEntityData.setCitadelTag:','Citadel.sendMSGToAll:','Citadel.sendMSGToServer:'],'progress sync')
    has_all(method(progress,'public boolean unlockNextFor(java.lang.String);'),['ACServerConfig.onlyOneResearchNeeded','CaveBookProgress$Subcategory.canUnlockNext:'],'unlock gate')
    codex=method(transcripts['CaveInfoItem'],'public net.minecraft.world.InteractionResultHolder<net.minecraft.world.item.ItemStack> use(net.minecraft.world.level.Level, net.minecraft.world.entity.player.Player, net.minecraft.world.InteractionHand);')
    has_all(codex,['ACItemRegistry.CAVE_CODEX','CaveBookProgress.unlockNextFor:','CaveBookProgress.saveCaveBookProgress:','ItemStack.shrink:','ACCompat.useConsume:'],'codex consumer')
    bypath={r['path']:r for r in report['resources']}
    recipe=bypath['data/alexscaves/recipe/cave_book.json']
    require(recipe['resource_type']=='minecraft:crafting_shapeless','recipe type')
    req={(r['kind'],r['id']) for r in recipe['ingredient_ids']}
    require(req=={('item','minecraft:book'),('item','alexscaves:cave_tablet'),('tag','alexscaves:nuggets/gold')},'ingredients')
    adv=bypath['data/alexscaves/advancement/alexscaves/cave_book.json']
    require(adv['parent']=='alexscaves:alexscaves/cave_tablet' and adv['criterion_triggers']['cave_book']=='minecraft:inventory_changed','advancement trigger')
    print('PASS: SHA-exact CaveBook item GUI / Codex / advancement boundaries; NO_MUTATION; NOT_TESTED')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--transcript-dir',required=True,type=Path)
    args=parser.parse_args();audit(args.transcript_dir)
