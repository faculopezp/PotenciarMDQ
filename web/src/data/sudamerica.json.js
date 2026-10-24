// Data loader: países de Sudamérica (GeoJSON) desde world-atlas (node_modules, sin CDN).
import {readFileSync} from "node:fs";
import {createRequire} from "node:module";
import {feature} from "topojson-client";

const require = createRequire(import.meta.url);
const world = JSON.parse(readFileSync(require.resolve("world-atlas/countries-50m.json"), "utf8"));
// ISO 3166-1 numérico: AR, UY, CL, BR, PY, BO, PE
const ids = new Set(["032", "858", "152", "076", "600", "068", "604"]);
const paises = feature(world, world.objects.countries);
paises.features = paises.features.filter((f) => ids.has(String(f.id).padStart(3, "0")));
process.stdout.write(JSON.stringify(paises));
