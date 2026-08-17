#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text, old, new, label):
    if old not in text:
        raise SystemExit(f"{label}: expected text not found: {old!r}")
    return text.replace(old, new, 1)


def species_block(text, species, next_marker):
    start_token = f"[SPECIES_{species}]"
    start = text.find(start_token)
    if start < 0:
        raise SystemExit(f"Could not find {start_token}")
    end = text.find(next_marker, start + len(start_token))
    if end < 0:
        raise SystemExit(f"Could not find end marker {next_marker!r} after {start_token}")
    return start, end, text[start:end]


def replace_field(block, field, value):
    pattern = rf"(\.{re.escape(field)}\s*=\s*)([^,\n]+)(,)"
    new_block, count = re.subn(pattern, rf"\g<1>{value}\3", block, count=1)
    if count != 1:
        raise SystemExit(f"Could not replace .{field} in species block")
    return new_block


# -----------------------------------------------------------------------------
# 1) Turn Lucario / Mega Lucario into the first PokeMan Journey original line.
#    The Lucario IDs are deliberately used as hidden prototype plumbing because
#    they already have a stable temporary battle-form pair in the engine.
# -----------------------------------------------------------------------------
species_path = ROOT / "src/data/pokemon/species_info/gen_4_families.h"
text = species_path.read_text()

start, end, base = species_block(text, "LUCARIO", "[SPECIES_LUCARIO_MEGA]")
base = replace_field(base, "baseHP", "100")
base = replace_field(base, "baseAttack", "72")
base = replace_field(base, "baseDefense", "78")
base = replace_field(base, "baseSpeed", "68")
base = replace_field(base, "baseSpAttack", "88")
base = replace_field(base, "baseSpDefense", "78")
base = re.sub(r"\.types\s*=\s*MON_TYPES\([^\n]+", ".types = MON_TYPES(TYPE_FIRE),", base, count=1)
base = re.sub(r"\.abilities\s*=\s*\{[^\n]+", ".abilities = { ABILITY_BLAZE, ABILITY_FLAME_BODY, ABILITY_FLASH_FIRE },", base, count=1)
base = re.sub(r'\.speciesName\s*=\s*_\("[^"]+"\),', '.speciesName = _("Embercub"),', base, count=1)
base = re.sub(r'\.categoryName\s*=\s*_\("[^"]+"\),', '.categoryName = _("Flame Cub"),', base, count=1)
base = re.sub(
    r"\.description\s*=\s*COMPOUND_STRING\(.*?\),\n",
    '.description = COMPOUND_STRING(\n'
    '            "Warm embers glow beneath the fur\\n"\n'
    '            "around its eyes and paws. When its\\n"\n'
    '            "trainer is threatened, those embers\\n"\n'
    '            "flare into a protective blaze."),\n',
    base,
    count=1,
    flags=re.S,
)
# Bear-cub stand-in pixel art for the first technical ROM. The original concept
# art can replace these pointers later without changing the battle mechanic.
base = re.sub(r"\.frontPic\s*=\s*[^,]+,", ".frontPic = gMonFrontPic_Teddiursa,", base, count=1)
base = re.sub(r"\.frontPicSize\s*=\s*[^\n]+", ".frontPicSize = MON_COORDS_SIZE(40, 40),", base, count=1)
base = re.sub(r"\.frontPicYOffset\s*=\s*[^,\n]+,", ".frontPicYOffset = 12,", base, count=1)
base = re.sub(r"\.backPic\s*=\s*[^,]+,", ".backPic = gMonBackPic_Teddiursa,", base, count=1)
base = re.sub(r"\.backPicSize\s*=\s*[^\n]+", ".backPicSize = MON_COORDS_SIZE(48, 48),", base, count=1)
base = re.sub(r"\.backPicYOffset\s*=\s*[^,\n]+,", ".backPicYOffset = 10,", base, count=1)
base = re.sub(r"\.palette\s*=\s*[^,]+,", ".palette = gMonPalette_Teddiursa,", base, count=1)
base = re.sub(r"\.shinyPalette\s*=\s*[^,]+,", ".shinyPalette = gMonShinyPalette_Teddiursa,", base, count=1)
base = re.sub(r"\.iconSprite\s*=\s*[^,]+,", ".iconSprite = gMonIcon_Teddiursa,", base, count=1)
base = re.sub(r"\.iconPalIndex\s*=\s*[^,]+,", ".iconPalIndex = 0,", base, count=1)
base = re.sub(r"\.levelUpLearnset\s*=\s*sLucarioLevelUpLearnset,", ".levelUpLearnset = sCyndaquilLevelUpLearnset,", base, count=1)
base = re.sub(r"\.teachableLearnset\s*=\s*sLucarioTeachableLearnset,", ".teachableLearnset = sCyndaquilTeachableLearnset,", base, count=1)
text = text[:start] + base + text[end:]

# Re-find after base length changed.
start, end, mega = species_block(text, "LUCARIO_MEGA", "#endif //P_MEGA_EVOLUTIONS")
mega = replace_field(mega, "baseHP", "100")
mega = replace_field(mega, "baseAttack", "128")
mega = replace_field(mega, "baseDefense", "108")
mega = replace_field(mega, "baseSpeed", "92")
mega = replace_field(mega, "baseSpAttack", "132")
mega = replace_field(mega, "baseSpDefense", "108")
mega = re.sub(r"\.types\s*=\s*MON_TYPES\([^\n]+", ".types = MON_TYPES(TYPE_FIRE, TYPE_FIGHTING),", mega, count=1)
mega = re.sub(r"\.abilities\s*=\s*\{[^\n]+", ".abilities = { ABILITY_FLAME_BODY, ABILITY_FLAME_BODY, ABILITY_FLAME_BODY },", mega, count=1)
mega = re.sub(r'\.speciesName\s*=\s*_\("[^"]+"\),', '.speciesName = _("Blazebear"),', mega, count=1)
mega = re.sub(r'\.categoryName\s*=\s*_\("[^"]+"\),', '.categoryName = _("Blaze Bear"),', mega, count=1)
mega = re.sub(
    r"\.description\s*=\s*COMPOUND_STRING\(.*?\),\n",
    '.description = COMPOUND_STRING(\n'
    '            "Battle energy engulfs its coat in\\n"\n'
    '            "living flame. Its larger body burns\\n"\n'
    '            "hotter until the fight ends, then it\\n"\n'
    '            "returns to its cub form."),\n',
    mega,
    count=1,
    flags=re.S,
)
mega = re.sub(r"\.frontPic\s*=\s*[^,]+,", ".frontPic = gMonFrontPic_Ursaring,", mega, count=1)
mega = re.sub(r"\.frontPicSize\s*=\s*[^\n]+", ".frontPicSize = MON_COORDS_SIZE(64, 64),", mega, count=1)
mega = re.sub(r"\.frontPicYOffset\s*=\s*[^,\n]+,", ".frontPicYOffset = 0,", mega, count=1)
mega = re.sub(r"\.backPic\s*=\s*[^,]+,", ".backPic = gMonBackPic_Ursaring,", mega, count=1)
mega = re.sub(r"\.backPicSize\s*=\s*[^\n]+", ".backPicSize = MON_COORDS_SIZE(64, 64),", mega, count=1)
mega = re.sub(r"\.backPicYOffset\s*=\s*[^,\n]+,", ".backPicYOffset = 2,", mega, count=1)
mega = re.sub(r"\.palette\s*=\s*[^,]+,", ".palette = gMonPalette_Ursaring,", mega, count=1)
mega = re.sub(r"\.shinyPalette\s*=\s*[^,]+,", ".shinyPalette = gMonShinyPalette_Ursaring,", mega, count=1)
mega = re.sub(r"\.iconSprite\s*=\s*[^,]+,", ".iconSprite = gMonIcon_Ursaring,", mega, count=1)
mega = re.sub(r"\.iconPalIndex\s*=\s*[^,]+,", ".iconPalIndex = 2,", mega, count=1)
mega = re.sub(r"\.levelUpLearnset\s*=\s*sLucarioLevelUpLearnset,", ".levelUpLearnset = sCyndaquilLevelUpLearnset,", mega, count=1)
mega = re.sub(r"\.teachableLearnset\s*=\s*sLucarioTeachableLearnset,", ".teachableLearnset = sCyndaquilTeachableLearnset,", mega, count=1)
text = text[:start] + mega + text[end:]
species_path.write_text(text)

# -----------------------------------------------------------------------------
# 2) Let Embercub trigger the existing temporary battle-form system without a
#    Mega Ring or held stone. This is prototype-only plumbing: the normal item
#    is restored immediately after the engine resolves the form change.
# -----------------------------------------------------------------------------
battle_path = ROOT / "src/battle_util.c"
battle = battle_path.read_text()
needle = "bool32 CanMegaEvolve(enum BattlerId battler)\n{\n"
injection = (
    needle
    + "    // PokeMan Journey prototype: Embercub can battle-evolve on command.\n"
      "    if (gBattleMons[battler].species == SPECIES_LUCARIO && IsOnPlayerSide(battler))\n"
      "        return TRUE;\n\n"
)
battle = replace_once(battle, needle, injection, "CanMegaEvolve injection")

needle = "void ActivateMegaEvolution(enum BattlerId battler)\n{\n    enum Ability ability = GetBattlerAbility(battler);\n"
injection = (
    needle
    + "\n    // PokeMan Journey prototype: use Lucarionite only as hidden form-change plumbing.\n"
      "    if (gBattleMons[battler].species == SPECIES_LUCARIO)\n"
      "    {\n"
      "        u16 originalItem = gBattleMons[battler].item;\n"
      "        gBattleMons[battler].item = ITEM_LUCARIONITE;\n"
      "        gLastUsedItem = ITEM_LUCARIONITE;\n"
      "        SetActiveGimmick(battler, GIMMICK_MEGA);\n"
      "        SetGimmickAsActivated(battler, GIMMICK_MEGA);\n"
      "        TryBattleFormChange(battler, FORM_CHANGE_BATTLE_MEGA_EVOLUTION_ITEM, ability);\n"
      "        gBattleMons[battler].item = originalItem;\n"
      "        BattleScriptPushCursorAndCallback(BattleScript_MegaEvolution);\n"
      "        return;\n"
      "    }\n"
)
battle = replace_once(battle, needle, injection, "ActivateMegaEvolution injection")
battle_path.write_text(battle)

# -----------------------------------------------------------------------------
# 3) Put Embercub directly in the opening Kanto starter selection for easy test.
# -----------------------------------------------------------------------------
starter_path = ROOT / "src/starter_choose.c"
starter = starter_path.read_text()
starter = replace_once(
    starter,
    "[REGION_KANTO] = { SPECIES_BULBASAUR,  SPECIES_MUDKIP,    SPECIES_CYNDAQUIL}",
    "[REGION_KANTO] = { SPECIES_BULBASAUR,  SPECIES_MUDKIP,    SPECIES_LUCARIO}",
    "Kanto starter replacement",
)
starter_path.write_text(starter)

# Make the test build unmistakable on the title menu after the normal v0.5 stamp.
menu_path = ROOT / "src/main_menu.c"
menu = menu_path.read_text()
menu = replace_once(menu, "NEW GAME  V0.5.0", "NEW GAME  EVO TEST", "menu test stamp")
menu_path.write_text(menu)

print("Applied PokeMan Journey battle-evolution prototype: Embercub -> Blazebear")
