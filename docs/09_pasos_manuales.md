# Pasos manuales (lo que no se puede automatizar)

Todo lo demás corre solo: GitHub Actions baja los datos los días 5 y 20 de cada mes, reconstruye la BD,
commitea los JSON de la web y Vercel publica.

## Una sola vez (≈ 15 min)

1. **Dar acceso al repo a Claude** (para que pueda pushear el código).
   - Ir a <https://claude.ai/connect-github> → instalar/configurar la app de Claude en GitHub →
     en "Repository access" agregar `faculopezp/PotenciarMDQ`.
2. **Permitir que el workflow escriba en el repo.**
   - GitHub → repo → *Settings* → *Actions* → *General* → *Workflow permissions* →
     "Read and write permissions" → *Save*.
3. **Correr la primera actualización a mano.**
   - GitHub → *Actions* → `actualizar-datos` → *Run workflow*.
   - Al terminar: abrir el run → *Artifacts* → bajar `potenciar-mdq-N` → mirar `reports/probe.md`
     (qué fuentes respondieron) y `reports/qa/anac_movimientos.md` (calidad).
4. **Verificar Vercel.**
   - El push del workflow dispara un deploy. Abrir <https://potenciar-mdq.vercel.app>.
   - Si el build falla: Vercel → proyecto → *Deployments* → último → *Build Logs*.
   - No hace falta tocar *Settings*: el `vercel.json` del repo define install, build y salida.

## Cada mes (≈ 10 min, opcional pero recomendado)

1. Abrir el último run de `actualizar-datos` → artefacto → `reports/qa/anac_movimientos.md`.
2. Revisar 3 secciones:
   - "Aeronaves sin clasificar": si aparece un avión comercial nuevo, agregar regex en `config/aeronaves.yaml`.
   - "Columnas sin mapear" (si el run falló): agregar el alias en `src/potenciar_mdq/standardize/columns.py`.
   - "Códigos sin coordenadas": solo importa si es un destino regular de MDQ.
3. Cargar 1 mes testigo en `config/reconciliacion.csv` con el total oficial de pasajeros de MDQ del
   informe mensual de ANAC → la sección "Reconciliación" del QA muestra la diferencia (objetivo ≤ 2 %).

## Cuando haga falta

| Situación | Qué hacer |
|---|---|
| Un hito nuevo (ruta, aerolínea, obra) | Agregarlo en `config/hitos.yaml` con link a la fuente |
| Cambiar aeropuertos pares | `config/mdq.yaml` → `pares` (código ANAC = `local_code` de OurAirports) |
| El portal de ANAC no responde | Nada: el pipeline usa el espejo de respaldo solo (2023+) |
| Correr todo local | `make setup && make all && make web-dev` |
