import maya.cmds as cmds

import random

import xml.dom.minidom


doc = xml.dom.minidom.parse("/Users/manish/Downloads/map.osm")



all_ways = doc.getElementsByTagName("way")

buildings = []

for el in all_ways:
	for ch in el.childNodes:
    
		if ch.attributes:

			if 'k' in ch.attributes.keys() and 'building' ==  ch.attributes['k'].value:
				buildings.append(el)
    
				break


nodes = doc.getElementsByTagName("node")
id_to_tuple = {}
for node in nodes:
	id_val = node.attributes['id'].value
	if 'lon' in node.attributes.keys():
		(lon, lat) = (node.attributes['lon'].value, node.attributes['lat'].value)
		id_to_tuple[id_val] = (lon, lat)
		

all_buildings = []

for b in buildings:
	lst = []
	nds = b.getElementsByTagName('nd')
	for ch in nds:
		if ch.tagName == 'nd':
			node_id = ch.attributes['ref'].value
			lst.append(id_to_tuple[node_id])
	all_buildings.append(lst)


print(all_buildings[0])

all_buildings = sorted(all_buildings)

sz = len(all_buildings)

start_lon = float(all_buildings[sz/2][0][0])
start_lat = float(all_buildings[sz/2][0][1])


print(all_buildings[0])


def get_xy(lon, lat):
    lon = float(lon)
    lat = float(lat)
    mul = 111.321 * 1000 # meters
    diff_lon = lon - start_lon
    diff_lat = lat - start_lat
    return (diff_lon * mul, diff_lat*mul)
     
buildings_xy = []

for lst in all_buildings:
    tmp = [] 
    for i in lst:
        tmp.append(get_xy(i[0], i[1]))
    buildings_xy.append(tmp)

print(buildings_xy[0])



# Polygons ready, now use it below

cubeList  = cmds.ls('myCube*')
if len(cubeList) > 0:
    cmds.delete(cubeList)
   
   

all_poly = []

for lst in buildings_xy:
    tmp = []
    for i in lst:
        (x,z) = i
        x/=100
        z/=100
        y = 0
        tmp.append((x,y,z))
    
    res = cmds.polyCreateFacet( p=tmp, name='buildingpoly#')
    
    all_poly.append(res)
    thickness = random.uniform(0.1, 0.2)
    cmds.polyExtrudeFacet(res[0], kft=1, thickness=thickness)
    





