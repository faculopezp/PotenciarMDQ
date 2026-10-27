# Auditoría con navegador

## https://ondat.c3t-utn.ar/?p=1308

- DOM: `raiz__dom.html`
- `{"tag": "input", "name": "s", "id": "s", "type": "text", "value": "", "text": "", "onclick": "", "opciones": null}`
- `{"tag": "input", "name": null, "id": "searchsubmit", "type": "submit", "value": "Buscar", "text": "", "onclick": "", "opciones": null}`
- `{"tag": "select", "name": "cat", "id": "cat", "type": "select-one", "value": "-1", "text": "Elegir la categoría\nEstadisticas\nFlota/Parque/Vehículos\nInfr", "onclick": "", "opciones": [["-1", "Elegir la categoría"], ["4", "Estadisticas"], ["104", "Flota/Parque/Vehículos"], ["102", "Infraestructura"], ["118", "Aérea"], ["119", "Ferroviaria"], ["117", "Vial"], ["103", "Medio ambiente"], ["89", "Transporte de Cargas y Logística"], ["97", "Aéreo"], ["115", "Automotor"], ["92", "Ferroviario"], ["259", "Intermodalidad"], ["90", "Marítimo y Fluvial"], ["93", "Transporte de Pasajeros"], ["166", "Interurbano"], ["96", "Aéreo"], ["98", "Automotor"], ["101", "Ferroviario"], ["286", "Intermodalidad"], ["95", "Urbano"], ["99", "Automotor"], ["100", "Ferroviario"], ["116", "Subte"], ["263", "Intermodalidad"], ["260", "Transporte internacional"]]}`
### Menú «TMDA»
- URL: https://ondat.c3t-utn.ar/?tag=tmda
- DOM: `menu_TMDA__dom.html`
- `{"tag": "input", "name": "s", "id": "s", "type": "text", "value": "", "text": "", "onclick": "", "opciones": null}`
- `{"tag": "input", "name": null, "id": "searchsubmit", "type": "submit", "value": "Buscar", "text": "", "onclick": "", "opciones": null}`
- `{"tag": "select", "name": "cat", "id": "cat", "type": "select-one", "value": "-1", "text": "Elegir la categoría\nEstadisticas\nFlota/Parque/Vehículos\nInfr", "onclick": "", "opciones": [["-1", "Elegir la categoría"], ["4", "Estadisticas"], ["104", "Flota/Parque/Vehículos"], ["102", "Infraestructura"], ["118", "Aérea"], ["119", "Ferroviaria"], ["117", "Vial"], ["103", "Medio ambiente"], ["89", "Transporte de Cargas y Logística"], ["97", "Aéreo"], ["115", "Automotor"], ["92", "Ferroviario"], ["259", "Intermodalidad"], ["90", "Marítimo y Fluvial"], ["93", "Transporte de Pasajeros"], ["166", "Interurbano"], ["96", "Aéreo"], ["98", "Automotor"], ["101", "Ferroviario"], ["286", "Intermodalidad"], ["95", "Urbano"], ["99", "Automotor"], ["100", "Ferroviario"], ["116", "Subte"], ["263", "Intermodalidad"], ["260", "Transporte internacional"]]}`
### Menú «Temporales»: ✗ Locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_text("Temporales", exact=True).first

### Menú «Interanuales»: ✗ Locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_text("Interanuales", exact=True).first

### Menú «SEGMENTACIÓN»: ✗ Locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_text("SEGMENTACIÓN", exact=True).first

### Menú «CLASIFICACIÓN»: ✗ Locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_text("CLASIFICACIÓN", exact=True).first

### Consulta de prueba: ✗ ElementHandle.inner_text: Execution context was destroyed, most likely because of a navigation
Call log:
  - waiting for locator(":scope")


## Pedidos de red

- [raiz] GET https://ondat.c3t-utn.ar/?p=1308 → 200 `text/html; charset=UTF-8` (document) · guardado `raiz___`
- [raiz] GET https://ondat.c3t-utn.ar/wp-content/themes/rt_novus_wp/js/rokbox/rokbox.js → 200 `text/javascript` (script) · guardado `raiz___wp-content_themes_rt_novus_wp_js_rokbox_rokbox.js`
- [raiz] GET https://ondat.c3t-utn.ar/wp-content/themes/rt_novus_wp/js/mootools.js → 200 `text/javascript` (script) · guardado `raiz___wp-content_themes_rt_novus_wp_js_mootools.js`
- [raiz] GET https://ondat.c3t-utn.ar/wp-content/themes/rt_novus_wp/js/rokbox/themes/light/rokbox-config.js → 200 `text/javascript` (script) · guardado `raiz___wp-content_themes_rt_novus_wp_js_rokbox_themes_light_rokbox-config.js`
- [raiz] GET https://ondat.c3t-utn.ar/wp-content/plugins/jquery-vertical-accordion-menu/js/jquery.hoverIntent.minified.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `raiz___wp-content_plugins_jquery-vertical-accordion-menu_js_jquery.hoverIntent.minified.js`
- [raiz] GET https://ondat.c3t-utn.ar/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.3.2 → 200 `text/javascript` (script) · guardado `raiz___wp-includes_js_jquery_jquery-migrate.min.js`
- [raiz] GET https://ondat.c3t-utn.ar/wp-content/plugins/jquery-mega-menu/js/jquery.dcmegamenu.1.3.4.min.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `raiz___wp-content_plugins_jquery-mega-menu_js_jquery.dcmegamenu.1.3.4.min.js`
- [raiz] GET https://ondat.c3t-utn.ar/wp-content/plugins/jquery-vertical-accordion-menu/js/jquery.dcjqaccordion.2.9.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `raiz___wp-content_plugins_jquery-vertical-accordion-menu_js_jquery.dcjqaccordion.2.9.js`
- [raiz] GET https://ondat.c3t-utn.ar/wp-includes/js/comment-reply.min.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `raiz___wp-includes_js_comment-reply.min.js`
- [raiz] GET https://ondat.c3t-utn.ar/wp-content/plugins/jquery-vertical-accordion-menu/js/jquery.cookie.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `raiz___wp-content_plugins_jquery-vertical-accordion-menu_js_jquery.cookie.js`
- [raiz] GET https://ondat.c3t-utn.ar/wp-includes/js/jquery/jquery.min.js?ver=3.6.0 → 200 `text/javascript` (script) · guardado `raiz___wp-includes_js_jquery_jquery.min.js`
- [raiz] GET https://ondat.c3t-utn.ar/wp-content/plugins/contact-form-7/includes/js/jquery.form.min.js?ver=3.32.0-2013.04.03 → 200 `text/javascript` (script) · guardado `raiz___wp-content_plugins_contact-form-7_includes_js_jquery.form.min.js`
- [raiz] GET https://ondat.c3t-utn.ar/wp-content/plugins/contact-form-7/includes/js/scripts.js?ver=3.4 → 200 `text/javascript` (script) · guardado `raiz___wp-content_plugins_contact-form-7_includes_js_scripts.js`
- [raiz] GET https://ondat.c3t-utn.ar/wp-content/plugins/theme-my-login/assets/scripts/theme-my-login.min.js?ver=7.1.4 → 200 `text/javascript` (script) · guardado `raiz___wp-content_plugins_theme-my-login_assets_scripts_theme-my-login.min.js`
- [raiz] GET https://www.google-analytics.com/analytics.js → 200 `text/javascript` (script) · guardado `raiz___analytics.js`
- [raiz] GET https://ondat.c3t-utn.ar/wp-includes/js/wp-emoji-release.min.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `raiz___wp-includes_js_wp-emoji-release.min.js`
- [raiz] POST https://www.google-analytics.com/j/collect?v=1&_v=j102&a=1825177865&t=pageview&_s=1&dl=https%3A%2F%2Fondat.c3t-utn.ar%2F%3Fp%3D1308&ul=en-us&dt=Tr%C3%A1nsito%20Medio%20Diario%20Anual%20(TMDA)%20en%20rutas%20nacionales%20%7C%20ONDaT&sr=1280x720&vp=1280x720&_u=IEBAAEABAAAAACAAI~&jid=2079604391&gjid=2049109258&cid=81062252.1793064397&tid=UA-56136044-1&_gid=1592739676.1793064397&_r=1&_slc=1&z=2013484211 → 200 `text/plain` (xhr) · guardado `raiz___j_collect`
- [raiz] GET https://www.googletagmanager.com/gtag/js?id=G-PPFCQ2KBZ9&cx=c&_slc=1 → 200 `application/javascript; charset=UTF-8` (script) · guardado `raiz___gtag_js`
- [raiz] POST https://www.google-analytics.com/g/collect?v=2&tid=G-PPFCQ2KBZ9&gtm=45je6an1v9106943316za20gxf1&_p=1793064397178&gcd=13l3l3l3l2l1&npa=0&dma=0&_eu=ABAI&cid=81062252.1793064397&frm=0&ngs=1&pscdl=noapi&rcb=11&sr=1280x720&uaa=x86&uab=64&uafvl=Not%253AA-Brand%3B8.0.0.0%7CChromium%3B156.0.8078.4%7CHeadlessChrome%3B156.0.8078.4&uam=&uamb=0&uap=Linux&uapv=&uaw=0&ul=en-us&_s=1&tag_exp=115938466~115938469~118897920~118897930~120213116~120385423~120469145~120469153~121246026~121246034&dl=https%3A%2F%2Fondat.c3t-utn.ar%2F%3Fp%3D1308&dt=Tr%C3%A1nsito%20Medio%20Diario%20Anual%20(TMDA)%20en%20rutas%20nacionales%20%7C%20ONDaT&sid=1793064397&sct=1&seg=0&en=page_view&_fv=1&_ss=1&_ee=1&tfd=483 → 204 `text/plain` (fetch)
- [menu_TMDA] GET https://ondat.c3t-utn.ar/wp-content/themes/rt_novus_wp/js/mootools.js → 200 `text/javascript` (script) · guardado `menu_TMDA___wp-content_themes_rt_novus_wp_js_mootools.js`
- [menu_TMDA] GET https://ondat.c3t-utn.ar/wp-content/themes/rt_novus_wp/js/rokbox/rokbox.js → 200 `text/javascript` (script) · guardado `menu_TMDA___wp-content_themes_rt_novus_wp_js_rokbox_rokbox.js`
- [menu_TMDA] GET https://ondat.c3t-utn.ar/wp-content/themes/rt_novus_wp/js/rokbox/themes/light/rokbox-config.js → 200 `text/javascript` (script) · guardado `menu_TMDA___wp-content_themes_rt_novus_wp_js_rokbox_themes_light_rokbox-config.js`
- [menu_TMDA] GET https://ondat.c3t-utn.ar/wp-includes/js/jquery/jquery.min.js?ver=3.6.0 → 200 `text/javascript` (script) · guardado `menu_TMDA___wp-includes_js_jquery_jquery.min.js`
- [menu_TMDA] GET https://ondat.c3t-utn.ar/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.3.2 → 200 `text/javascript` (script) · guardado `menu_TMDA___wp-includes_js_jquery_jquery-migrate.min.js`
- [menu_TMDA] GET https://ondat.c3t-utn.ar/wp-content/plugins/jquery-vertical-accordion-menu/js/jquery.hoverIntent.minified.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `menu_TMDA___wp-content_plugins_jquery-vertical-accordion-menu_js_jquery.hoverIntent.minified.js`
- [menu_TMDA] GET https://ondat.c3t-utn.ar/wp-content/plugins/jquery-vertical-accordion-menu/js/jquery.cookie.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `menu_TMDA___wp-content_plugins_jquery-vertical-accordion-menu_js_jquery.cookie.js`
- [menu_TMDA] GET https://ondat.c3t-utn.ar/wp-content/plugins/jquery-vertical-accordion-menu/js/jquery.dcjqaccordion.2.9.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `menu_TMDA___wp-content_plugins_jquery-vertical-accordion-menu_js_jquery.dcjqaccordion.2.9.js`
- [menu_TMDA] GET https://ondat.c3t-utn.ar/wp-content/plugins/jquery-mega-menu/js/jquery.dcmegamenu.1.3.4.min.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `menu_TMDA___wp-content_plugins_jquery-mega-menu_js_jquery.dcmegamenu.1.3.4.min.js`
- [menu_TMDA] GET https://www.google-analytics.com/analytics.js → 200 `text/javascript` (script) · guardado `menu_TMDA___analytics.js`
- [menu_TMDA] GET https://ondat.c3t-utn.ar/wp-includes/js/wp-emoji-release.min.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `menu_TMDA___wp-includes_js_wp-emoji-release.min.js`
- [menu_TMDA] GET https://ondat.c3t-utn.ar/?tag=tmda → 200 `text/html; charset=UTF-8` (document) · guardado `menu_TMDA___`
- [menu_TMDA] GET https://ondat.c3t-utn.ar/wp-content/plugins/contact-form-7/includes/js/jquery.form.min.js?ver=3.32.0-2013.04.03 → 200 `text/javascript` (script) · guardado `menu_TMDA___wp-content_plugins_contact-form-7_includes_js_jquery.form.min.js`
- [menu_TMDA] GET https://ondat.c3t-utn.ar/wp-content/plugins/contact-form-7/includes/js/scripts.js?ver=3.4 → 200 `text/javascript` (script) · guardado `menu_TMDA___wp-content_plugins_contact-form-7_includes_js_scripts.js`
- [menu_TMDA] GET https://ondat.c3t-utn.ar/wp-content/plugins/theme-my-login/assets/scripts/theme-my-login.min.js?ver=7.1.4 → 200 `text/javascript` (script) · guardado `menu_TMDA___wp-content_plugins_theme-my-login_assets_scripts_theme-my-login.min.js`
- [menu_TMDA] POST https://www.google-analytics.com/j/collect?v=1&_v=j102&a=1282015641&t=pageview&_s=1&dl=https%3A%2F%2Fondat.c3t-utn.ar%2F%3Ftag%3Dtmda&ul=en-us&dt=TMDA%20%7C%20ONDaT&sr=1280x720&vp=1280x720&_u=AACAAEABAAAAACAAI~&jid=&gjid=&cid=81062252.1793064397&tid=UA-56136044-1&_gid=1592739676.1793064397&_slc=1&z=829661234 → 200 `text/plain` (xhr) · guardado `menu_TMDA___j_collect`
- [menu_TMDA] GET https://www.googletagmanager.com/gtag/js?id=G-PPFCQ2KBZ9&cx=c&_slc=1 → 200 `application/javascript; charset=UTF-8` (script) · guardado `menu_TMDA___gtag_js`
- [menu_Temporales] POST https://www.google-analytics.com/g/collect?v=2&tid=G-PPFCQ2KBZ9&gtm=45je6an1v9106943316za20gxf1&_p=1793064400014&gcd=13l3l3l3l2l1&npa=0&dma=0&_eu=ABAIAAQ&cid=81062252.1793064397&frm=0&ngs=1&pscdl=noapi&rcb=10&sr=1280x720&uaa=x86&uab=64&uafvl=Not%253AA-Brand%3B8.0.0.0%7CChromium%3B156.0.8078.4%7CHeadlessChrome%3B156.0.8078.4&uam=&uamb=0&uap=Linux&uapv=&uaw=0&ul=en-us&tag_exp=115616986~115938466~115938469~118897920~118897930~119860443~120213116~120385423~120420416~120469145~120469153~121246026~121246034&dl=https%3A%2F%2Fondat.c3t-utn.ar%2F%3Ftag%3Dtmda&dt=TMDA%20%7C%20ONDaT&sid=1793064397&sct=1&seg=1&_s=1&tfd=5138 → 204 `text/plain` (fetch) · POST `en=page_view&_ee=1
en=page_view&_ee=1&_et=1
en=page_view&_ee=1`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/themes/rt_novus_wp/js/mootools.js → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_themes_rt_novus_wp_js_mootools.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/themes/rt_novus_wp/js/rokbox/rokbox.js → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_themes_rt_novus_wp_js_rokbox_rokbox.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/themes/rt_novus_wp/js/rokbox/themes/light/rokbox-config.js → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_themes_rt_novus_wp_js_rokbox_themes_light_rokbox-config.js`
- [consulta_0226] GET https://www.google-analytics.com/analytics.js → 200 `text/javascript` (script) · guardado `consulta_0226___analytics.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-includes/js/wp-emoji-release.min.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-includes_js_wp-emoji-release.min.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-includes/js/jquery/jquery.min.js?ver=3.6.0 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-includes_js_jquery_jquery.min.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.3.2 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-includes_js_jquery_jquery-migrate.min.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/plugins/jquery-vertical-accordion-menu/js/jquery.hoverIntent.minified.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_plugins_jquery-vertical-accordion-menu_js_jquery.hoverIntent.minified.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/plugins/jquery-vertical-accordion-menu/js/jquery.cookie.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_plugins_jquery-vertical-accordion-menu_js_jquery.cookie.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/plugins/jquery-vertical-accordion-menu/js/jquery.dcjqaccordion.2.9.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_plugins_jquery-vertical-accordion-menu_js_jquery.dcjqaccordion.2.9.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/plugins/jquery-mega-menu/js/jquery.dcmegamenu.1.3.4.min.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_plugins_jquery-mega-menu_js_jquery.dcmegamenu.1.3.4.min.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/?p=1308 → 200 `text/html; charset=UTF-8` (document) · guardado `consulta_0226___`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-includes/js/comment-reply.min.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-includes_js_comment-reply.min.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/plugins/contact-form-7/includes/js/jquery.form.min.js?ver=3.32.0-2013.04.03 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_plugins_contact-form-7_includes_js_jquery.form.min.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/plugins/contact-form-7/includes/js/scripts.js?ver=3.4 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_plugins_contact-form-7_includes_js_scripts.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/plugins/theme-my-login/assets/scripts/theme-my-login.min.js?ver=7.1.4 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_plugins_theme-my-login_assets_scripts_theme-my-login.min.js`
- [consulta_0226] POST https://www.google-analytics.com/j/collect?v=1&_v=j102&a=1908680916&t=pageview&_s=1&dl=https%3A%2F%2Fondat.c3t-utn.ar%2F%3Fp%3D1308&ul=en-us&dt=Tr%C3%A1nsito%20Medio%20Diario%20Anual%20(TMDA)%20en%20rutas%20nacionales%20%7C%20ONDaT&sr=1280x720&vp=1280x720&_u=AACAAEABAAAAACAAI~&jid=&gjid=&cid=81062252.1793064397&tid=UA-56136044-1&_gid=1592739676.1793064397&_slc=1&z=520898459 → 200 `text/plain` (xhr) · guardado `consulta_0226___j_collect`
- [consulta_0226] GET https://www.googletagmanager.com/gtag/js?id=G-PPFCQ2KBZ9&cx=c&_slc=1 → 200 `application/javascript; charset=UTF-8` (script) · guardado `consulta_0226___gtag_js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/themes/rt_novus_wp/js/mootools.js → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_themes_rt_novus_wp_js_mootools.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/themes/rt_novus_wp/js/rokbox/rokbox.js → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_themes_rt_novus_wp_js_rokbox_rokbox.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/themes/rt_novus_wp/js/rokbox/themes/light/rokbox-config.js → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_themes_rt_novus_wp_js_rokbox_themes_light_rokbox-config.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-includes/js/jquery/jquery.min.js?ver=3.6.0 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-includes_js_jquery_jquery.min.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.3.2 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-includes_js_jquery_jquery-migrate.min.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/plugins/jquery-vertical-accordion-menu/js/jquery.hoverIntent.minified.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_plugins_jquery-vertical-accordion-menu_js_jquery.hoverIntent.minified.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/plugins/jquery-vertical-accordion-menu/js/jquery.cookie.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_plugins_jquery-vertical-accordion-menu_js_jquery.cookie.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/plugins/jquery-vertical-accordion-menu/js/jquery.dcjqaccordion.2.9.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_plugins_jquery-vertical-accordion-menu_js_jquery.dcjqaccordion.2.9.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/plugins/jquery-mega-menu/js/jquery.dcmegamenu.1.3.4.min.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_plugins_jquery-mega-menu_js_jquery.dcmegamenu.1.3.4.min.js`
- [consulta_0226] GET https://www.google-analytics.com/analytics.js → 200 `text/javascript` (script) · guardado `consulta_0226___analytics.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-includes/js/wp-emoji-release.min.js?ver=5.9.19 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-includes_js_wp-emoji-release.min.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/?s= → 200 `text/html; charset=UTF-8` (document) · guardado `consulta_0226___`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/plugins/contact-form-7/includes/js/jquery.form.min.js?ver=3.32.0-2013.04.03 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_plugins_contact-form-7_includes_js_jquery.form.min.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/plugins/contact-form-7/includes/js/scripts.js?ver=3.4 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_plugins_contact-form-7_includes_js_scripts.js`
- [consulta_0226] GET https://ondat.c3t-utn.ar/wp-content/plugins/theme-my-login/assets/scripts/theme-my-login.min.js?ver=7.1.4 → 200 `text/javascript` (script) · guardado `consulta_0226___wp-content_plugins_theme-my-login_assets_scripts_theme-my-login.min.js`
- [consulta_0226] POST https://www.google-analytics.com/j/collect?v=1&_v=j102&a=625719066&t=pageview&_s=1&dl=https%3A%2F%2Fondat.c3t-utn.ar%2F%3Fs%3D&ul=en-us&dt=Resultados%20para%20%22%22%20%7C%20ONDaT&sr=1280x720&vp=1280x720&_u=AACAAEABAAAAACAAI~&jid=&gjid=&cid=81062252.1793064397&tid=UA-56136044-1&_gid=1592739676.1793064397&_slc=1&z=1847424522 → 200 `text/plain` (xhr) · guardado `consulta_0226___j_collect`
- [consulta_0226] GET https://www.googletagmanager.com/gtag/js?id=G-PPFCQ2KBZ9&cx=c&_slc=1 → 200 `application/javascript; charset=UTF-8` (script) · guardado `consulta_0226___gtag_js`
