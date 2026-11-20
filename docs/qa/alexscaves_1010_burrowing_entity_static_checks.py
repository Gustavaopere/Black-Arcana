#!/usr/bin/env python3
"""SHA-pinned local semantic assertions over javap; not a runtime/QA certificate."""
import argparse
import hashlib
from pathlib import Path

SHA = {
    "BurrowingArrowEntity.javap.txt": "9512813a4c6a70a65159c87a13f74c902ca39a4c30c22e80a5c4e9e7e77972fa",
    "BurrowingArrowItem.javap.txt": "2a3f0d614d505e3d45742f039bb49313bc4c773e0b6fed98d80281f81f0ca8ba",
    "ACItemRegistry_6.javap.txt": "827d92a19a4bb247a7445b17f43aa1b822104ccc29634912843017665ba3b221",
}

def require(condition, reason):
    if not condition:
        raise AssertionError(reason)

def method(text, declaration):
    key = "  " + declaration + "\n"
    require(text.count(key) == 1, "method absent or ambiguous: " + declaration)
    body = text.split(key, 1)[1].split("      LineNumberTable:", 1)[0]
    require("    Code:" in body, "method Code missing: " + declaration)
    return body

def audit(folder):
    text = {}
    for name, digest in SHA.items():
        raw = (folder / name).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == digest, "javap digest mismatch: " + name)
        text[name] = raw.decode("utf-8")
    entity = text["BurrowingArrowEntity.javap.txt"]
    item = text["BurrowingArrowItem.javap.txt"]
    dispenser = text["ACItemRegistry_6.javap.txt"]
    fq = "public com.github.alexmodguy.alexscaves.server.entity.item.BurrowingArrowEntity("
    a = method(entity, fq+"net.minecraft.world.entity.EntityType, net.minecraft.world.level.Level);")
    b = method(entity, fq+"net.minecraft.world.level.Level, net.minecraft.world.entity.LivingEntity);")
    c = method(entity, fq+"net.minecraft.world.level.Level, double, double, double);")
    for body in (a,b,c):
        require("double 3.5d" in body and "setBaseDamage:(D)V" in body, "base damage")
    require("ac$setPierceLevel:(B)V" in a and "ac$setPierceLevel:(B)V" in b, "owner constructors pierce")
    require("ac$setPierceLevel:(B)V" not in c, "position constructor differs")
    for body in (b,c):
        require("ACItemRegistry.BURROWING_ARROW" in body, "native stack")
    factory = method(item,"public net.minecraft.world.entity.projectile.AbstractArrow createArrow(net.minecraft.world.level.Level, net.minecraft.world.item.ItemStack, net.minecraft.world.entity.LivingEntity, net.minecraft.world.item.ItemStack);")
    require('BurrowingArrowEntity."<init>":(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)V' in factory, "item constructor route")
    require("aload_2" not in factory and "aload         4" not in factory, "item does not locally use ammo or weapon stacks")
    dispens = method(dispenser,"protected net.minecraft.world.entity.projectile.Projectile getProjectile(net.minecraft.world.level.Level, net.minecraft.core.Position, net.minecraft.world.item.ItemStack);")
    require('BurrowingArrowEntity."<init>":(Lnet/minecraft/world/level/Level;DDD)V' in dispens, "dispenser route")
    require("AbstractArrow$Pickup.ALLOWED" in dispens and "AbstractArrow.pickup" in dispens, "dispenser pickup")
    mine = method(entity,"private boolean canMine(net.minecraft.core.BlockPos);")
    for s in ("getOwner:()Lnet/minecraft/world/entity/Entity;", "6: ifnull        18",
              "instanceof", "net/minecraft/world/entity/player/Player", "16: iconst_0",
              "ACTagRegistry.UNMOVEABLE", "FluidState.isEmpty:()Z",
              "float -1.0f", "getDugBlockCount:()I", "iconst_5", "if_icmpge"):
        require(s in mine, "canMine gate: "+s)
    tick = method(entity,"public void tick();")
    for s in ("AbstractArrow.tick:()V", "float 0.2f", "float 15.0f",
              "float 10.0f", "Math.max:(FF)F", "f2i",
              "destroyBlockProgress", "Level.destroyBlock:", "getDugBlockCount:()I",
              "setDugBlockCount:(I)V", "Vec3.normalize", "double 0.30000001192092896d",
              "double 0.20000000298023224d", "bipush        8", "bipush        38"):
        require(s in tick, "tick contract: "+s)
    require(tick.index("232: invokevirtual") < tick.index("235: pop") < tick.index("243: invokevirtual"),
            "destroyBlock Boolean ignored, count incremented unconditionally")
    require("isClientSide" not in tick and "getGameRules" not in tick, "no local side or gamerule check")
    for declaration in ("protected void onHitBlock(net.minecraft.world.phys.BlockHitResult);",
        "protected void tickDespawn();", "public void startFalling();",
        "public void remove(net.minecraft.world.entity.Entity$RemovalReason);",
        "protected net.minecraft.world.item.ItemStack getDefaultPickupItem();",
        "public float getDiggingAmount(float);"):
        require("Code:" in method(entity,declaration), "lifecycle method: "+declaration)
    require("addAdditionalSaveData" not in entity and "readAdditionalSaveData" not in entity,
            "no locally declared extra NBT handlers")
    print("PASS: SHA-exact class-local Burrowing Arrow branches; NO_MUTATION / NOT_VERIFIED / NOT_TESTED")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcript-dir", required=True, type=Path)
    args = parser.parse_args()
    audit(args.transcript_dir)
