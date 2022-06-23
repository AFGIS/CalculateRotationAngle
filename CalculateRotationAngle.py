import arcpy
import os

# Set local variables
in_features = arcpy.GetParameterAsText(0)

if in_features[-3:] == "shp":
    out_feature_class = os.path.dirname(in_features) + "\\intermediateTempFile.shp"
    orientationField = "MBG_Orient"
    objectIDField = "FID"
else:
    out_feature_class = os.path.dirname(in_features) + "\\intermediateTempFile"
    orientationField = "MBG_Orientation"
    objectIDField = "OBJECTID"



if arcpy.Exists(out_feature_class):
    arcpy.management.Delete(out_feature_class)

fields = arcpy.ListFields(in_features, "Angle")

if len(fields) != 1:
    arcpy.management.AddField(in_features, "Angle", "DOUBLE")

# Execute Minimum Bounding Geometry
arcpy.management.MinimumBoundingGeometry(in_features, out_feature_class, "RECTANGLE_BY_AREA", "NONE",
                                          mbg_fields_option=True)

search_feats = {f[0]:f[1] for f in arcpy.da.SearchCursor(out_feature_class,[objectIDField, orientationField])}

with arcpy.da.UpdateCursor(in_features,[objectIDField,"Angle"]) as upd_cur:
    for upd_row in upd_cur:
        upd_row[1] = search_feats[upd_row[0]] + 270
        upd_cur.updateRow(upd_row)

arcpy.management.Delete(out_feature_class)

del search_feats, upd_cur