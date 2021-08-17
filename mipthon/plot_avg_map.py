import os, numpy
import Ngl, Nio
import sys

#
# Create some dummy data for the contour plot.

filename=sys.argv[1]

f    = Nio.open_file(filename)
psl    = f.variables["psl"][0,:,:]
lat  = f.variables["lat"][:]
lon  = f.variables["lon"][:]
 
wks_type = "png"
wks = Ngl.open_wks(wks_type,filename.split(".nc")[0])

cnres                 = Ngl.Resources()

# Contour resources
cnres.cnFillOn        = True
cnres.cnFillPalette   = "BlueYellowRed"      # New in PyNGL 1.5.0
cnres.cnLinesOn       = False
cnres.cnLineLabelsOn  = False

# Labelbar resource
cnres.lbOrientation   = "horizontal"

# Scalar field resources
cnres.sfXArray        = lon
cnres.sfYArray        = lat

# Map resources
cnres.mpCenterLatF=0.0
cnres.mpCenterLonF=180.0
cnres.mpProjection="CylindricalEquidistant"
cnres.mpLimitMode="LatLon"
cnres.mpFillOn               = True
cnres.mpFillDrawOrder        = "PostDraw"
cnres.mpLandFillColor        = "Transparent"
cnres.mpOceanFillColor       = "Transparent"
cnres.mpInlandWaterFillColor = "Transparent"


contour = Ngl.contour_map(wks,psl,cnres)

Ngl.end()
