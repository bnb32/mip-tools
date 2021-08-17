import os, numpy
import Ngl, Nio
import sys
import re

#
# Create some dummy data for the contour plot.
#

model=sys.argv[1]
variable=sys.argv[2]
directory=sys.argv[3]

files = [f for f in os.listdir(directory) if re.match(model+'_'+variable+r'_[0-9]*\.nc', f)]
files=sorted(files)

var={}

tmp = Nio.open_file(directory+'/'+files[0])
lat  = tmp.variables["lat"][:]
lon  = tmp.variables["lon"][:]


for i in range(len(files)):
    tmp = Nio.open_file(directory+'/'+files[i])
    var[i]=tmp.variables[variable][0,:,:]
 
wks_type = "png"
wks = Ngl.open_wks(wks_type,directory+'/'+model+'_'+variable+'_monthly')

cnres                 = Ngl.Resources()

# Contour resources
cnres.cnFillOn        = True
cnres.nglDraw=False
cnres.nglFrame=False
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

plot = []
for i in range(len(files)):
    plot.append(Ngl.contour_map(wks,var[i],cnres))

panelres=Ngl.Resources()
panelres.nglPanelYWhiteSpacePercent = 6.
panelres.nglPanelXWhiteSpacePercent = 4.
panelres.nglPanelLabelBar                 = True 
panelres.nglPanelLabelBarWidthF           = 0.700 
panelres.nglPanelTop                      = 1.0
panelres.nglPanelFigureStrings            = ["A","B","C","D","E","F","G","H","I","J","K","L"]
panelres.nglPanelFigureStringsJust        = "BottomRight"
panelres.nglPaperMargin=0.0
panelres.nglPaperHeight=14.0
panelres.nglPaperWidth=12.5

Ngl.panel(wks,plot[0:len(files)],[4,3],panelres)

#contour = Ngl.contour_map(wks,psl,cnres)

Ngl.end()
