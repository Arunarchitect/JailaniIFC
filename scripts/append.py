"""
Append IFC elements from a library file (A.ifc) into the IFC project
currently open in Bonsai (B.ifc), skipping any element that triggers
the known ifcopenshell SafeRemovalContext AssertionError instead of
crashing the whole batch.

USAGE
1. Paste this into Blender's Text Editor (Scripting workspace) while
   B.ifc is the active Bonsai project.
2. Set LIBRARY_PATH below to A.ifc.
3. Paste GlobalIds into GLOBAL_IDS_RAW as a plain comma-separated
   string -- no quotes needed, just paste them as-is.
   Leave GLOBAL_IDS_RAW empty and set ELEMENT_CLASSES instead to
   append by class, or leave both empty to attempt every IfcProduct.
4. Run (Alt+P). A log opens automatically in a NEW window as a
   Text Editor showing what was appended / skipped / failed.
"""

import bpy
import ifcopenshell
import ifcopenshell.api
import bonsai.tool as tool

# ---------------- CONFIG ----------------
LIBRARY_PATH = r"D:\BIM\IFCdraft\JailaniIFC\Jailani.ifc"  # file A (source)

# Paste GlobalIds here as plain comma-separated text -- no quotes needed.
GLOBAL_IDS_RAW = """
2aoiAZmMTEsO42I3Sp16Xq,3oG4nCoz56jRXDofkW3Npz,1oYDh1Suv95gB5S0DXz9vv,1P0WpONsL2_fIgdDm4$tJi,1OnefPYsjDgAzknMxfkDAv,2xHvwjNvD49wH2Eb$itxU2,2mkgtyuR13ugGYX$5ld0jx,1K41Hk5Vn8jOcLb_phdXpm,3ZWA5acMT3iRb$zzawHHeL,0wqLQLyFr3J9HMtPmbEIh9,2wq0RaKEjAq8euRAk15fbe,3u1ye5Obj4CAmPf$C9OYi_,3cB9c2Zan92uJ8xofJqBEn,1kZ6arMArE$9y9yZJ4GHr0,20AGRrGGj80gr6A0T4jVcD,3Plz$VqHz1TwmYGwoMmAAs,12swJzLLH4_ANk1ONmui5M,3H1HuE4IvB1h_3F4F7Lm0e,2F7pFQM9fETARVOBt1J95Q,0VkbIo1A12aBmKXQxbogGf,2kYcCA5uf3DQIxlH4mQAXs,0zWZptiqz7X8rMh5CZiVrx,1kbHomPrX9jemvndvLu4R1,2mDlwRAUL1Sfu1jTYYReCt,1DowydeJ1ELgXVJ172Vzbz,1XN4oGVQvEKvbsHcSlGtkB,2umq$cZgz3oxMnjGyK3iq1,3xq3kOo9TAOedjyUbcPm5o,0FeV5qzKT4TRdT7u9pBOJb,0ktzV6uQbEwgZxEIvBrjVK,3PEiNYjcPDbwTu1P1y5Kkx,0mELnxbUzAs9pBe_PR9izm,2b$yie90vAr8Iz73ZSv3$K,0LuzcCMm53v9fCKeBSKf9R,1YnGETroHElA8rmJ_077a1,2Pi$KcTUvC395wxTc_Rxtb,0vFIv3B$zFGwHRdFBpZ46i,2mbtAgrUH3q8t5Pm33jGPL,1GoDiVvC9BnhyltlAMvle7,2YnYomgLbBlOedDehn9IMs,2KkI7mlRn3kP5qwusELqFR,2AlMp_rrTB4Aq3N8A4pJBq,1EilNGP7b8Ngyg6LE5DvpN,2H3Rs3pMr739S5B2P66fWI,3zPVcC10T06ON_t9KcqqYi,3XajPGjrf0IPjkWnWqr9FQ,3701REA4XFGgNOKkUu9Z1R,0IlH5KzEj2oQKoZcfl92kM,34wrX0d5v3jPGWb1TdBPmD,16i55JdbjBDgzx2H01IEE1,1mQ90d1S9859tX1zdYXOc0,10jGdX9h9DjxAQK$b9BELk,1BJuE8zF52IReVmUWByoKv,3lu5CWP1HFEAGLKDOUPP5B,0iveiZoNz048_yqdK95blk,1PFbuGSNr05RacGmJuZ7cP,188SetLv132xnFR8PDRqRY,3QLvYWFDP1NuiiQeFJZvFX,0eoXyhI6HCmAm5mYsvFKRX,24UfnUgcDDaepgAJ6MerLe,3IrQkOgFnD9uMa1BD5TJdv,33CmBKeCnALvE0u4yGk4l8,2azprbCMvD4BzlXYJmQi8T,2ySxDAwfr6rBZiyJMnyvI2,01sQChoL18w86THdB66riM,3Q_0Mm9r93mPvOdIA7Gu8C,0kQcsmw6DAew6jTLWvFLHo,05C9CJcbv8yhpwDmPkRDjA,340BjcpT9F4AO9F5p9txJ8,1sQc$BbMf2Hhtu$Nsco270,1scujomCHCGg5R0HDLd1Mj,2_8uoZdgP7QP92oUNvETbk,2uTq5V3tjDchBF10ZCzDs0,01eSte5q55q9LfIjViXjQJ,1RNj8vc3r1Xx$jyfNpG1wh,0Aplg5a857putqNCno9poP,1k$cgL6cX3QxxDF_xttM7N,01vc774Bj9AOETurqIabVL,3ZRAr0s7X55xNLmxckXWnS,1hANyzXYX6ohXsyIeaQnek,3HXFjhp195pvCzQNLf61n$,1GAiwNAQXC$BQFk_vGg5FN,1_l653Gkb6Ye$g_5c8RbIX,3_7$fC6WD01Qf6Ckzdlg$K,1FoQjWDsbC3A_EM7ibfFGg
"""

ELEMENT_CLASSES = []   # e.g. ["IfcFurniture", "IfcDoorType"] - by class
# If GLOBAL_IDS_RAW and ELEMENT_CLASSES are both empty, every
# IfcProduct in the library is attempted.
# -----------------------------------------


def parse_global_ids(raw):
    # Splits on commas/whitespace/newlines, drops empties, dedupes while
    # preserving order.
    parts = [p.strip() for p in raw.replace("\n", ",").split(",")]
    seen = set()
    out = []
    for p in parts:
        if p and p not in seen:
            seen.add(p)
            out.append(p)
    return out


def get_target_elements(library_file):
    guids = parse_global_ids(GLOBAL_IDS_RAW)
    if guids:
        out = []
        for g in guids:
            try:
                out.append(library_file.by_guid(g))
            except RuntimeError:
                print(f"GlobalId not found in library: {g}")
        return out
    if ELEMENT_CLASSES:
        out = []
        for cls in ELEMENT_CLASSES:
            out.extend(library_file.by_type(cls))
        return out
    return library_file.by_type("IfcProduct")


def open_log_in_new_text_editor(text_block):
    bpy.ops.wm.window_new()
    new_window = bpy.context.window_manager.windows[-1]
    area = new_window.screen.areas[0]
    area.type = 'TEXT_EDITOR'
    area.spaces[0].text = text_block


def main():
    file_b = tool.Ifc.get()
    if file_b is None:
        raise Exception("No IFC project is currently loaded in Bonsai (file B).")

    library_file = ifcopenshell.open(LIBRARY_PATH)
    elements = get_target_elements(library_file)

    log = []
    log.append(f"Append run: {len(elements)} candidate elements from {LIBRARY_PATH}")
    log.append(f"Target project: {tool.Ifc.get_path() or '(unsaved)'}")
    log.append("-" * 70)

    appended, skipped = 0, 0

    for el in elements:
        name = getattr(el, "Name", None) or "Unnamed"
        guid = getattr(el, "GlobalId", "no-guid")
        label = f"{el.is_a():20s} {name:30s} {guid}"
        try:
            ifcopenshell.api.run(
                "project.append_asset",
                file_b,
                library=library_file,
                element=el,
                assume_asset_uniqueness_by_name=False,
            )
            appended += 1
            log.append(f"OK    {label}")
        except AssertionError:
            skipped += 1
            log.append(f"SKIP  {label}  -- SafeRemovalContext assertion failed")
        except Exception as e:
            skipped += 1
            log.append(f"FAIL  {label}  -- {type(e).__name__}: {e}")

    log.append("-" * 70)
    log.append(f"Appended: {appended}   Skipped/Failed: {skipped}")
    log.append("")
    log.append("NOTE: newly appended elements exist in the IFC model now.")
    log.append("If they don't show in the viewport, save the project and")
    log.append("reopen it in Bonsai (File > Open) to force a full resync,")
    log.append("or use Bonsai's own 'Reload' if your version has it.")

    text_name = "append_log.txt"
    if text_name in bpy.data.texts:
        bpy.data.texts.remove(bpy.data.texts[text_name])
    text_block = bpy.data.texts.new(text_name)
    text_block.write("\n".join(log))

    open_log_in_new_text_editor(text_block)
    print("\n".join(log))


main()