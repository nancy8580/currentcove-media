import {geoDistance} from 'd3-geo';
const N=[-123.393,-48.877],R=6371;
const P={Ducie:[-124.783,-24.667],MotuNui:[-109.45,-27.2],Maher:[-126.367,-72.967]};
for(const k in P)console.log(k,Math.round(geoDistance(N,P[k])*R));
