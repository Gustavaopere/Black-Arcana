#!/usr/bin/env python3
"""Compare finite engine-class fingerprints between build and physical-ledger references.
No semantic equivalence inferred from matching Code hashes or version proximity.
"""
from __future__ import annotations
import argparse, json
from io import BytesIO
from pathlib import Path
from contextlib import ExitStack
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require
from neoforge_211248_gazing_pearl_saveddata_engine_probe import verify_distribution
from alexscaves_1010_destroyed_item_engine_reference import ARTIFACTS as PHYSICAL_ARTIFACTS

MC="net/minecraft/"
NF="net/neoforged/neoforge/"
GROUPS={
    "state_transport": [MC+x for x in (
        "nbt/CompoundTag","world/item/component/CustomData","world/item/ItemStack","world/item/Item",
        "core/component/DataComponentPatch","core/component/DataComponents","core/component/PatchedDataComponentMap",
        "world/inventory/AbstractContainerMenu","network/protocol/game/ClientboundContainerSetSlotPacket",
        "network/protocol/game/ClientboundContainerSetContentPacket","world/item/ItemCooldowns",
        "world/item/enchantment/Enchantment","world/item/enchantment/EnchantmentHelper")]+
        [NF+x for x in ("common/extensions/IItemExtension","common/extensions/IItemStackExtension")],
    "shield_and_combat": [MC+x for x in (
        "world/item/ShieldItem","world/entity/LivingEntity","world/entity/player/Player","world/entity/Entity",
        "server/level/ServerPlayer","world/damagesource/DamageSource","world/damagesource/DamageSources")]+
        [NF+x for x in ("event/EventHooks","common/CommonHooks")],
    "world_mining_and_inventory": [MC+x for x in (
        "server/level/ServerPlayerGameMode","world/entity/projectile/ProjectileUtil","world/item/DiggerItem",
        "world/level/BlockGetter","world/level/Level","world/level/LevelAccessor","world/level/block/Block",
        "world/level/block/ShulkerBoxBlock","world/level/block/state/BlockBehaviour$BlockStateBase","world/phys/AABB",
        "world/entity/player/Inventory","world/entity/item/ItemEntity","server/level/ServerLevel",
        "world/level/entity/PersistentEntitySectionManager","world/level/entity/EntitySection")]+
        [NF+x for x in ("common/extensions/IBlockExtension","common/extensions/IBlockStateExtension")],
    "remote_explosion_and_tickets": [MC+x for x in (
        "world/level/block/TntBlock","world/entity/item/PrimedTnt","world/level/ForcedChunksSavedData",
        "world/level/Explosion","world/level/ExplosionDamageCalculator","world/level/EntityBasedExplosionDamageCalculator",
        "server/network/ServerGamePacketListenerImpl","world/level/block/state/BlockState")]+
        [NF+"common/world/chunk/"+x for x in ("ForcedChunkManager","ForcedChunkManager$TicketTracker",
            "ForcedChunkManager$TicketOwner","TicketController","TicketHelper")]+
        [NF+"common/world/chunk/RegisterTicketControllersEvent",NF+"common/world/chunk/LoadingValidationCallback"],
    "saved_data": [MC+x for x in ("world/level/storage/DimensionDataStorage","world/level/saveddata/SavedData","world/level/saveddata/SavedData$Factory")],
}
PIN_248={
    MC+"world/item/ItemStack":"072cd6887595d3f928a3a1a9605662ff547fe3201d6b6d713a43bfd2719f1a13",
    MC+"world/item/Item":"d4234cf5acb218b2056a38845170ec8266e16dc39ae0ed5fe5328cac153af462",
    MC+"world/entity/Entity":"4f65b7d5d4628e9f10a6a23e5a0f68814520d8019f4bc001924cd752c00eed84",
    MC+"world/entity/projectile/ProjectileUtil":"47c5e685f77f34709e3c8bc883962d326185b6dac67578572a86c268a3801bda",
    MC+"world/level/Explosion":"3b656cd810d9fbbe001b4477ee5dff9f243c75d42458cd54fababed971da3e07",
    MC+"world/level/block/TntBlock":"fb116b17eb40038991e262edd4fcc43592f07db5838699039ef2c50ba4981a26",
    NF+"common/world/chunk/ForcedChunkManager":"5b585bb44efc3822ef4cfb5a09afa44c810e35c38f336a2d03a60f271dcc98f2",
}
def identify(path):
    raw=path.read_bytes()
    return {"bytes":len(raw),"sha256":digest(raw)}
def compare(a,b):
    if not a or not b:return "MISSING_IN_ONE_OR_BOTH"
    if a["sha256"]!=b["sha256"]:return "CLASS_BYTES_DIFFER"
    if a["source"]!=b["source"]:return "IDENTICAL_CLASS_BYTES_SOURCE_CHANGED"
    return "IDENTICAL_CLASS_BYTES"

def inspect(args):
    require(not args.output.exists(),"write-once report")
    verify_distribution(args.root248/"server.jar",args.root248/"srg.jar")
    identity={}
    for label,root in (("21.1.248",args.root248),("21.1.250",args.root250)):
        info={k:identify(root/(k+".jar")) for k in ("installer","server","srg","universal")}
        require(all(1_000_000<v["bytes"]<150_000_000 for v in info.values()),"archive budget")
        require(info["installer"]["sha256"]==(root/"installer.sha256").read_text().split()[0].lower(),
                "installer official checksum mismatch")
        require(info["universal"]["sha256"]==(root/"universal.sha256").read_text().split()[0].lower(),
                "universal official checksum mismatch")
        identity[label]=info
    require(identity["21.1.248"]["installer"]["sha256"]=="68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c","248 installer pin")
    require(identity["21.1.248"]["universal"]["sha256"]=="90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5","248 universal pin")
    require(identity["21.1.250"]["universal"]["sha256"]==PHYSICAL_ARTIFACTS["universal"]["sha256"] and
            identity["21.1.250"]["universal"]["bytes"]==PHYSICAL_ARTIFACTS["universal"]["size_bytes"],"250 universal pin")
    require(identity["21.1.250"]["installer"]=={"bytes":6972109,"sha256":"0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60"},"250 installer pin")
    require(identity["21.1.250"]["server"]==identity["21.1.248"]["server"] and identity["21.1.250"]["srg"]==identity["21.1.248"]["srg"],"distributed archive equality drift")
    owners=sorted(set().union(*GROUPS.values()))
    require(30<len(owners)<=80,"finite owner roster")
    with ExitStack() as stack:
        archives={}
        for label,root in (("21.1.248",args.root248),("21.1.250",args.root250)):
            archives[label]=[]
            for k in ("server","universal","srg"):
                z=stack.enter_context(ZipFile(root/(k+".jar")))
                names=z.namelist()
                require(len(names)==len(set(names)),"duplicate archive entries")
                archives[label].append((k,z,set(names)))
        rows={}
        for owner in owners:
            pair={}
            for label,sources in archives.items():
                found=[(k,z) for k,z,names in sources if owner+".class" in names]
                if not found:
                    pair[label]=None
                    continue
                k,z=found[0]
                raw=z.read(owner+".class")
                rd=ClassReader(raw)
                require(rd.name==owner and rd.major==65,"class identity mismatch")
                pair[label]={"source":k,"available_sources":[name for name,_ in found],
                             "sha256":digest(raw),"bytes":len(raw),
                             "method_count":len(rd.methods),"field_count":len(rd.fields)}
            if owner in PIN_248:require(pair["21.1.248"] and pair["21.1.248"]["sha256"]==PIN_248[owner],"previous evidence mismatch")
            rows[owner]={"groups":[k for k,v in GROUPS.items() if owner in v],
                         "versions":pair,"comparison":compare(pair["21.1.248"],pair["21.1.250"])}
        # The universal archive differs as a ZIP. Compare exact member bytes,
        # independently of ZIP container metadata, without redistributing content.
        u248=archives["21.1.248"][1][1]
        u250=archives["21.1.250"][1][1]
        n248={x.filename for x in u248.infolist() if not x.is_dir()}
        n250={x.filename for x in u250.infolist() if not x.is_dir()}
        require(len(n248|n250)<=10000,"universal member budget")
        changes=[]
        totals={"class":{"same":0,"changed":0,"only248":0,"only250":0},
                "resource":{"same":0,"changed":0,"only248":0,"only250":0}}
        for name in sorted(n248|n250):
            group="class" if name.endswith(".class") else "resource"
            a=digest(u248.read(name)) if name in n248 else None
            b=digest(u250.read(name)) if name in n250 else None
            kind="same" if a==b else "only248" if b is None else "only250" if a is None else "changed"
            totals[group][kind]+=1
            if kind!="same":changes.append({"entry":name,"kind":kind,"sha248":a,"sha250":b})
        universal_delta={"totals":totals,"changed_entries":changes}
        require(len(rows)==59 and all(v["comparison"]=="IDENTICAL_CLASS_BYTES" for v in rows.values()),"finite owner comparison drift")
        require(totals=={"class":{"same":1491,"changed":1,"only248":0,"only250":0},
                         "resource":{"same":788,"changed":3,"only248":1,"only250":1}},"universal census drift")
        nested={}
        for patch,archive,pin in (
            (248,u248,"f3cb872880f7dd7923d50f77bd9cf120291f3370fc89fd6a0f865f1e30d60517"),
            (250,u250,"eee41553202c153f025a2461de319a17641246d037a848f96e50bcaec48021e6")):
            name=f"META-INF/jarjar/net.neoforged.neoforge-coremods-21.1.{patch}.jar"
            raw=archive.read(name)
            require(digest(raw)==pin and len(raw)<10_000_000,"nested CoreMods identity")
            z=stack.enter_context(ZipFile(BytesIO(raw)))
            infos=[x for x in z.infolist() if not x.is_dir()]
            require(len(z.namelist())==len(set(z.namelist())),"duplicate CoreMods paths")
            require(len(infos)<=10000 and sum(x.file_size for x in infos)<50_000_000,"CoreMods budget")
            nested[patch]={x.filename:digest(z.read(x)) for x in infos}
        nested_rows=[]
        nested_totals={"class":{"same":0,"changed":0,"only248":0,"only250":0},
                       "resource":{"same":0,"changed":0,"only248":0,"only250":0}}
        for name in sorted(set(nested[248])|set(nested[250])):
            a,b=nested[248].get(name),nested[250].get(name)
            kind="same" if a==b else "only248" if b is None else "only250" if a is None else "changed"
            nested_totals["class" if name.endswith(".class") else "resource"][kind]+=1
            nested_rows.append({"entry":name,"comparison":kind,"sha248":a,"sha250":b})
        coremods_delta={"totals":nested_totals,"members":nested_rows}
    report={"schema_version":3,"scope":"DISTRIBUTED_ARCHIVE_AND_CLASS_BYTE_COMPARISON_ONLY",
            "build_reference":"21.1.248","physical_ledger_reference":"21.1.250",
            "artifacts":identity,"classes":rows,"universal_member_comparison":universal_delta,"coremods_member_comparison":coremods_delta,
            "limits":{"runtime_loaded_bytes":"NOT_OBSERVED","transitive_equivalence":"NOT_CERTIFIED",
                      "physical_qa":"NOT_TESTED","mutating_hook":"NOT_VERIFIED","mutation":"NO_MUTATION",
                      "provider_universe_closed":False,"semantic_magic_roots_delta":0}}
    raw=canonical(report).encode()
    require(len(raw)<=200000,"report budget")
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("xb") as f:f.write(raw)
    print("REPORT_SHA256",digest(raw),"BYTES",len(raw),"OWNERS",len(rows))
    print("ARTIFACTS",json.dumps(identity,sort_keys=True))
    print("UNIVERSAL_DELTA",json.dumps(universal_delta,sort_keys=True))
    print("COREMODS_DELTA",json.dumps(coremods_delta,sort_keys=True))
    for owner,row in rows.items():print("CLASS",owner,json.dumps(row,sort_keys=True))
    print("NO_MUTATION NO_RUNTIME_EQUIVALENCE")

def self_test():
    a={"sha256":"a","source":"server"}
    require(compare(a,a)=="IDENTICAL_CLASS_BYTES","same")
    require(compare(a,{"sha256":"b","source":"server"})=="CLASS_BYTES_DIFFER","different")
    require(compare(a,{"sha256":"a","source":"srg"})=="IDENTICAL_CLASS_BYTES_SOURCE_CHANGED","source")
    require(compare(a,None)=="MISSING_IN_ONE_OR_BOTH","missing")
    print("PASS: four comparison cases")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root248",type=Path)
    p.add_argument("--root250",type=Path)
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        require(all((a.root248,a.root250,a.output)),"inputs required")
        inspect(a)
