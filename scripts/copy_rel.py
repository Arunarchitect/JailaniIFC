# Your script is working like this:
# File A	Current IFC opened in Bonsai/Blender
# File B	External IFC (Sreekesh_new.ifc)
# Goal	Copy TEXT_LEADER → Product relations from B into A

# This line in your output means you found a GUID with no target relationship in File B:
# WARNING: No target product relation found in File B for: GUID



import bonsai.tool as tool
import ifcopenshell
import ifcopenshell.guid
import bpy
import os

# ---------------- SETTINGS ----------------
DRY_RUN = True  # First run True. After checking log, change to False.
FILE_B_NAME = "Jailani_draft.ifc"
OUTPUT_SUFFIX = "New"

GUID_STRING = """
2aoiAZmMTEsO42I3Sp16Xq,3oG4nCoz56jRXDofkW3Npz,1oYDh1Suv95gB5S0DXz9vv,1P0WpONsL2_fIgdDm4$tJi,1OnefPYsjDgAzknMxfkDAv,2xHvwjNvD49wH2Eb$itxU2,2mkgtyuR13ugGYX$5ld0jx,1K41Hk5Vn8jOcLb_phdXpm,3ZWA5acMT3iRb$zzawHHeL,0wqLQLyFr3J9HMtPmbEIh9,2wq0RaKEjAq8euRAk15fbe,3u1ye5Obj4CAmPf$C9OYi_,3cB9c2Zan92uJ8xofJqBEn,1kZ6arMArE$9y9yZJ4GHr0,20AGRrGGj80gr6A0T4jVcD,3Plz$VqHz1TwmYGwoMmAAs,12swJzLLH4_ANk1ONmui5M,3H1HuE4IvB1h_3F4F7Lm0e,2F7pFQM9fETARVOBt1J95Q,0VkbIo1A12aBmKXQxbogGf,2kYcCA5uf3DQIxlH4mQAXs,0zWZptiqz7X8rMh5CZiVrx,1kbHomPrX9jemvndvLu4R1,2mDlwRAUL1Sfu1jTYYReCt,1DowydeJ1ELgXVJ172Vzbz,1XN4oGVQvEKvbsHcSlGtkB,2umq$cZgz3oxMnjGyK3iq1,3xq3kOo9TAOedjyUbcPm5o,0FeV5qzKT4TRdT7u9pBOJb,0ktzV6uQbEwgZxEIvBrjVK,3PEiNYjcPDbwTu1P1y5Kkx,0mELnxbUzAs9pBe_PR9izm,2b$yie90vAr8Iz73ZSv3$K,0LuzcCMm53v9fCKeBSKf9R,1YnGETroHElA8rmJ_077a1,2Pi$KcTUvC395wxTc_Rxtb,0vFIv3B$zFGwHRdFBpZ46i,2mbtAgrUH3q8t5Pm33jGPL,1GoDiVvC9BnhyltlAMvle7,2YnYomgLbBlOedDehn9IMs,2KkI7mlRn3kP5qwusELqFR,2AlMp_rrTB4Aq3N8A4pJBq,1EilNGP7b8Ngyg6LE5DvpN,2H3Rs3pMr739S5B2P66fWI,3zPVcC10T06ON_t9KcqqYi,3XajPGjrf0IPjkWnWqr9FQ,3701REA4XFGgNOKkUu9Z1R,0IlH5KzEj2oQKoZcfl92kM,34wrX0d5v3jPGWb1TdBPmD,16i55JdbjBDgzx2H01IEE1,1mQ90d1S9859tX1zdYXOc0,10jGdX9h9DjxAQK$b9BELk,1BJuE8zF52IReVmUWByoKv,3lu5CWP1HFEAGLKDOUPP5B,0iveiZoNz048_yqdK95blk,1PFbuGSNr05RacGmJuZ7cP,188SetLv132xnFR8PDRqRY,3QLvYWFDP1NuiiQeFJZvFX,0eoXyhI6HCmAm5mYsvFKRX,24UfnUgcDDaepgAJ6MerLe,3IrQkOgFnD9uMa1BD5TJdv,33CmBKeCnALvE0u4yGk4l8,2azprbCMvD4BzlXYJmQi8T,2ySxDAwfr6rBZiyJMnyvI2,01sQChoL18w86THdB66riM,3Q_0Mm9r93mPvOdIA7Gu8C,0kQcsmw6DAew6jTLWvFLHo,05C9CJcbv8yhpwDmPkRDjA,340BjcpT9F4AO9F5p9txJ8,1sQc$BbMf2Hhtu$Nsco270,1scujomCHCGg5R0HDLd1Mj,2_8uoZdgP7QP92oUNvETbk,2uTq5V3tjDchBF10ZCzDs0,01eSte5q55q9LfIjViXjQJ,1RNj8vc3r1Xx$jyfNpG1wh,0Aplg5a857putqNCno9poP,1k$cgL6cX3QxxDF_xttM7N,01vc774Bj9AOETurqIabVL,3ZRAr0s7X55xNLmxckXWnS,1hANyzXYX6ohXsyIeaQnek,3HXFjhp195pvCzQNLf61n$,1GAiwNAQXC$BQFk_vGg5FN,1_l653Gkb6Ye$g_5c8RbIX,3_7$fC6WD01Qf6Ckzdlg$K,1FoQjWDsbC3A_EM7ibfFGg
"""


TARGET_ANNOTATION_GUIDS = [
    x.strip() for x in GUID_STRING.split(",") if x.strip()
]

TARGET_CLASSES = [
    "IfcSwitchingDevice",
    "IfcOutlet",
    "IfcLightFixture",
    "IfcElectricAppliance"
]

SOURCE_MODE = "LAST_ONLY"
# "LAST_ONLY" = copy only last product relation from File B
# "ALL"       = copy all target product relations from File B
# ------------------------------------------

model_a = tool.Ifc.get()

file_a_path = tool.Ifc.get_path()
folder = os.path.dirname(file_a_path)

file_b_path = os.path.normpath(os.path.join(folder, FILE_B_NAME))
model_b = ifcopenshell.open(file_b_path)

name, ext = os.path.splitext(os.path.basename(file_a_path))
output_path = os.path.normpath(os.path.join(folder, name + OUTPUT_SUFFIX + ext))

log = bpy.data.texts.get("IFC Output") or bpy.data.texts.new("IFC Output")
log.clear()

def write(msg=""):
    log.write(str(msg) + "\n")

def is_target_product(product):
    return product and any(product.is_a(cls) for cls in TARGET_CLASSES)

def get_target_relations(model, annotation):
    rels = []
    for inv in model.get_inverse(annotation):
        if inv.is_a("IfcRelAssignsToProduct"):
            product = inv.RelatingProduct
            if is_target_product(product):
                rels.append(inv)
    return rels

def remove_annotation_from_old_relations(model, annotation):
    for rel in list(get_target_relations(model, annotation)):
        old_related = list(rel.RelatedObjects)
        new_related = [x for x in old_related if x != annotation]

        write("Removing old A relation: #" + str(rel.id()))
        write("Old product: " + str(rel.RelatingProduct))
        write("RelatedObjects before: " + str([x.id() for x in old_related]))
        write("RelatedObjects after : " + str([x.id() for x in new_related]))

        if not DRY_RUN:
            if len(new_related) == 0:
                model.remove(rel)
                write("Action: deleted empty relation")
            else:
                rel.RelatedObjects = tuple(new_related)
                write("Action: removed annotation from relation")
        else:
            write("Action: DRY RUN only. No change made.")

        write("-" * 60)

def assign_annotation_to_product(model, annotation, product):
    existing_rel = None

    for inv in model.get_inverse(product):
        if inv.is_a("IfcRelAssignsToProduct") and inv.RelatingProduct == product:
            existing_rel = inv
            break

    if existing_rel:
        related = list(existing_rel.RelatedObjects)

        if annotation not in related:
            related.append(annotation)

            if not DRY_RUN:
                existing_rel.RelatedObjects = tuple(related)

            write("Added annotation to existing relation #" + str(existing_rel.id()))
        else:
            write("Annotation already exists in relation #" + str(existing_rel.id()))

    else:
        owner_history_list = model.by_type("IfcOwnerHistory")
        owner_history = owner_history_list[0] if owner_history_list else None

        if not DRY_RUN:
            new_rel = model.create_entity(
                "IfcRelAssignsToProduct",
                ifcopenshell.guid.new(),
                owner_history,
                None,
                None,
                (annotation,),
                None,
                product
            )
            write("Created new relation #" + str(new_rel.id()))
        else:
            write("Would create new IfcRelAssignsToProduct relation")

write("COPY TEXT_LEADER PRODUCT RELATIONS FROM FILE B TO FILE A")
write("=" * 100)
write("Mode: " + ("DRY RUN - no changes saved" if DRY_RUN else "LIVE - File A will be modified and saved"))
write("File A/current: " + file_a_path)
write("File B/source : " + file_b_path)
write("Output file   : " + output_path)
write("Source mode   : " + SOURCE_MODE)
write("Target classes: " + ", ".join(TARGET_CLASSES))
write("Target GUIDs  : " + ", ".join(TARGET_ANNOTATION_GUIDS))
write("=" * 100)

processed = 0
matched = 0
skipped_not_in_guid_list = 0
skipped_no_a_annotation = 0
skipped_no_b_annotation = 0
skipped_no_b_relation = 0
skipped_missing_product_in_a = 0

# Process only GUIDs given in GUID_STRING
for gid in TARGET_ANNOTATION_GUIDS:

    annotation_a = model_a.by_guid(gid)

    if not annotation_a:
        skipped_no_a_annotation += 1
        write("")
        write("WARNING: Annotation GUID not found in File A: " + gid)
        continue

    if not annotation_a.is_a("IfcAnnotation") or annotation_a.Name != "TEXT_LEADER":
        skipped_not_in_guid_list += 1
        write("")
        write("WARNING: GUID exists in File A, but is not TEXT_LEADER annotation: " + gid)
        write(str(annotation_a))
        continue

    processed += 1

    annotation_b = model_b.by_guid(gid)

    if not annotation_b:
        skipped_no_b_annotation += 1
        write("")
        write("WARNING: Same annotation GUID not found in File B: " + gid)
        continue

    rels_b = get_target_relations(model_b, annotation_b)

    if not rels_b:
        skipped_no_b_relation += 1
        write("")
        write("WARNING: No target product relation found in File B for: " + gid)
        continue

    if SOURCE_MODE == "LAST_ONLY":
        rels_b = [rels_b[-1]]

    write("")
    write("=" * 100)
    write("MATCHED TEXT_LEADER")
    write("Annotation GUID: " + gid)
    write("File A annotation: " + str(annotation_a))
    write("File B annotation: " + str(annotation_b))
    write("Relations copied from B: " + str(len(rels_b)))

    target_products_a = []

    for rel_b in rels_b:
        product_b = rel_b.RelatingProduct
        product_gid = product_b.GlobalId
        product_a = model_a.by_guid(product_gid)

        write("")
        write("Source B relation: #" + str(rel_b.id()))
        write("Source B product : " + str(product_b))
        write("Product GUID     : " + product_gid)

        if not product_a:
            skipped_missing_product_in_a += 1
            write("WARNING: Matching product not found in File A. Skipped.")
            continue

        write("Target A product : " + str(product_a))

        blender_obj = tool.Ifc.get_object(product_a)
        write("A Blender object : " + (blender_obj.name if blender_obj else "None"))

        target_products_a.append(product_a)

    if not target_products_a:
        continue

    write("")
    write("Cleaning old File A product relations for this annotation...")
    remove_annotation_from_old_relations(model_a, annotation_a)

    write("")
    write("Creating/copying File B relations into File A...")
    for product_a in target_products_a:
        assign_annotation_to_product(model_a, annotation_a, product_a)

    matched += 1

write("")
write("=" * 100)
write("SUMMARY")
write("Target GUIDs given             : " + str(len(TARGET_ANNOTATION_GUIDS)))
write("TEXT_LEADER annotations checked: " + str(processed))
write("Annotations updated/matched    : " + str(matched))
write("GUID not found in File A       : " + str(skipped_no_a_annotation))
write("Not TEXT_LEADER in File A      : " + str(skipped_not_in_guid_list))
write("No same annotation in File B   : " + str(skipped_no_b_annotation))
write("No product relation in File B  : " + str(skipped_no_b_relation))
write("Missing product in File A      : " + str(skipped_missing_product_in_a))

if not DRY_RUN:
    model_a.write(output_path)
    write("Saved fixed File A to:")
    write(output_path)
else:
    write("DRY RUN complete. No file saved.")

write("=" * 100)