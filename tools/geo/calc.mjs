import {geoDistance, geoInterpolate, geoRotation, geoArea} from 'd3-geo';
import * as topo from 'topojson-client'; import fs from 'fs';
const DEL=[77.1,28.56], NYC=[-73.78,40.64], R=6371;
console.log('gc km', Math.round(geoDistance(DEL,NYC)*R));
const ip=geoInterpolate(DEL,NYC); let mx=0; for(let i=0;i<=200;i++){mx=Math.max(mx,ip(i/200)[1])} console.log('max lat', mx.toFixed(1));
// rhumb line distance (loxodrome) going west
const rad=x=>x*Math.PI/180; const p1=rad(DEL[1]),p2=rad(NYC[1]); let dl=rad(NYC[0]-DEL[0]); // -150.88 deg westward
const dpsi=Math.log(Math.tan(Math.PI/4+p2/2)/Math.tan(Math.PI/4+p1/2)); const dp=p2-p1; const q=Math.abs(dpsi)>1e-12?dp/dpsi:Math.cos(p1);
console.log('rhumb km', Math.round(Math.sqrt(dp*dp+q*q*dl*dl)*R));
const w=JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-110m.json')); const c=topo.feature(w,w.objects.countries);
const g=c.features.find(f=>f.properties.name==='Greenland'), africa=c.features.filter(f=>['Algeria','Dem. Rep. Congo','Sudan','Libya','Chad','Niger','Angola','Mali','South Africa','Ethiopia','Egypt','Nigeria','Tanzania','Mauritania','Namibia','Mozambique','Zambia','Somalia','Central African Rep.','S. Sudan','Botswana','Madagascar','Kenya','Cameroon','Morocco','Zimbabwe','Gabon','Congo','Côte d\'Ivoire','Burkina Faso','Guinea','Ghana','Uganda','Senegal','Tunisia','Malawi','Eritrea','Benin','Liberia','Sierra Leone','Togo','Guinea-Bissau','Lesotho','Eq. Guinea','Burundi','Rwanda','Djibouti','eSwatini','Gambia','W. Sahara'].includes(f.properties.name));
const A=africa.reduce((s,f)=>s+geoArea(f),0)*R*R, G=geoArea(g)*R*R; console.log('africa',Math.round(A/1e6),'M km2 greenland',(G/1e6).toFixed(2),'ratio',(A/G).toFixed(1));
