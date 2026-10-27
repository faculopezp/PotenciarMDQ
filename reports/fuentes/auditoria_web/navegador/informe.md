# Auditoría con navegador

## https://catalogo.datos.gba.gob.ar/dataset

- DOM: `dataset__dom.html`
- `{"tag": "input", "name": "q", "id": null, "type": "text", "value": "", "text": "", "onclick": "", "opciones": null}`
- `{"tag": "button", "name": null, "id": null, "type": "submit", "value": "search", "text": "", "onclick": "", "opciones": null}`
- `{"tag": "select", "name": "sort", "id": "field-order-by", "type": "select-one", "value": "metadata_modified desc", "text": "Última modificación\nAscendente (A - Z)\nDescendente (Z - A)", "onclick": "", "opciones": [["metadata_modified desc", "Última modificación"], ["title_string asc", "Ascendente (A - Z)"], ["title_string desc", "Descendente (Z - A)"]]}`
- `{"tag": "button", "name": null, "id": null, "type": "submit", "value": "", "text": "", "onclick": "", "opciones": null}`
### Menú «TMDA»: ✗ Locator.click: Timeout 5000ms exceeded.
Call log:
  - waiting for get_by_text("TMDA", exact=True).first

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

### Consulta de prueba (0226)
- Acciones: ninguna
- DOM: `consulta_0226__dom.html`

## Pedidos de red

- [dataset] GET https://catalogo.datos.gba.gob.ar/dataset → 200 `text/html; charset=utf-8` (document) · guardado `dataset___dataset`
- [dataset] GET https://www.google-analytics.com/analytics.js → 200 `text/javascript` (script) · guardado `dataset___analytics.js`
- [dataset] GET https://catalogo.datos.gba.gob.ar/fanstatic/base/:version:2019-12-02T16:58:12/:bundle:plugins/jquery.inherit.min.js;plugins/jquery.proxy-all.min.js;plugins/jquery.url-helpers.min.js;plugins/jquery.date-helpers.min.js;plugins/jquery.slug.min.js;plugins/jquery.slug-preview.min.js;plugins/jquery.truncator.min.js;plugins/jquery.masonry.min.js;plugins/jquery.form-warning.min.js;sandbox.min.js;module.min.js;pubsub.min.js;client.min.js;notify.min.js;i18n.min.js;main.min.js;modules/select-switch.min.js;modules/slug-preview.min.js;modules/basic-form.min.js;modules/confirm-action.min.js;modules/api-info.min.js;modules/autocomplete.min.js;modules/custom-fields.min.js;modules/data-viewer.min.js;modules/table-selectable-rows.min.js;modules/resource-form.min.js;modules/resource-upload-field.min.js;modules/resource-reorder.min.js;modules/resource-view-reorder.min.js;modules/follow.min.js;modules/activity-stream.min.js;modules/dashboard.min.js;modules/resource-view-embed.min.js;view-filters.min.js;modules/resource-view-filters-form.min.js;modules/resource-view-filters.min.js;modules/table-toggle-more.min.js;modules/dataset-visibility.min.js;modules/media-grid.min.js;modules/image-upload.min.js → 200 `application/javascript` (script) · guardado `dataset___fanstatic_base__version_2019-12-02T16_58_12__bundle_plugins_jquery.inherit.min.js_plugins_jquery.proxy-all.min.js_plugins_jquery.url-helpers`
- [dataset] GET https://catalogo.datos.gba.gob.ar/fanstatic/ckanext-googleanalytics/:version:2019-12-02T16:58:24/googleanalytics_event_tracking.js → 200 `application/javascript` (script) · guardado `dataset___fanstatic_ckanext-googleanalytics__version_2019-12-02T16_58_24_googleanalytics_event_tracking.js`
- [dataset] GET https://catalogo.datos.gba.gob.ar/fanstatic/gobar_js/:version:2019-12-02T17:16:31/:bundle:background_ie.js;console_message.js;header.js;replace_svg.js;forms/custom_popup.js;libs/BootstrapMenu.js;libs/bootstrap_scripts.js;libs/clamp.js;search/filters.js;search/groups.js → 200 `application/javascript` (script) · guardado `dataset___fanstatic_gobar_js__version_2019-12-02T17_16_31__bundle_background_ie.js_console_message.js_header.js_replace_svg.js_forms_custom_popup.js_l`
- [dataset] GET https://catalogo.datos.gba.gob.ar/fanstatic/vendor/:version:2019-12-02T16:58:12/jquery.min.js → 200 `application/javascript` (script) · guardado `dataset___fanstatic_vendor__version_2019-12-02T16_58_12_jquery.min.js`
- [dataset] GET https://catalogo.datos.gba.gob.ar/fanstatic/vendor/:version:2019-12-02T16:58:12/:bundle:bootstrap/js/bootstrap.min.js;jed.min.js;moment-with-locales.js;select2/select2.min.js → 200 `application/javascript` (script) · guardado `dataset___fanstatic_vendor__version_2019-12-02T16_58_12__bundle_bootstrap_js_bootstrap.min.js_jed.min.js_moment-with-locales.js_select2_select2.min.js`
- [dataset] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-01-184914.247043adminpub-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `dataset___uploads_group_2024-08-01-184914.247043adminpub-nn-01.svg`
- [dataset] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-01-185625.422619agricultura-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `dataset___uploads_group_2024-08-01-185625.422619agricultura-nn-01.svg`
- [dataset] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-01-191228.901293demografia-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `dataset___uploads_group_2024-08-01-191228.901293demografia-nn-01.svg`
- [dataset] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-02-131818.178601economia-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `dataset___uploads_group_2024-08-02-131818.178601economia-nn-01.svg`
- [dataset] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-02-131844.893245educacion-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `dataset___uploads_group_2024-08-02-131844.893245educacion-nn-01.svg`
- [dataset] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-02-131903.697006genero-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `dataset___uploads_group_2024-08-02-131903.697006genero-nn-01.svg`
- [dataset] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-02-131949.745468industria-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `dataset___uploads_group_2024-08-02-131949.745468industria-nn-01.svg`
- [dataset] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-02-132115.264054ambiente-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `dataset___uploads_group_2024-08-02-132115.264054ambiente-nn-01.svg`
- [dataset] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-02-132136.828658movilidad-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `dataset___uploads_group_2024-08-02-132136.828658movilidad-nn-01.svg`
- [dataset] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-02-132155.782494salud-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `dataset___uploads_group_2024-08-02-132155.782494salud-nn-01.svg`
- [dataset] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-02-132224.737631justicia-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `dataset___uploads_group_2024-08-02-132224.737631justicia-nn-01.svg`
- [dataset] GET https://catalogo.datos.gba.gob.ar/api/i18n/es → 200 `application/json;charset=utf-8` (xhr) · guardado `dataset___api_i18n_es`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/fanstatic/vendor/:version:2019-12-02T16:58:12/jquery.min.js → 200 `application/javascript` (script) · guardado `consulta_0226___fanstatic_vendor__version_2019-12-02T16_58_12_jquery.min.js`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/fanstatic/vendor/:version:2019-12-02T16:58:12/:bundle:bootstrap/js/bootstrap.min.js;jed.min.js;moment-with-locales.js;select2/select2.min.js → 200 `application/javascript` (script) · guardado `consulta_0226___fanstatic_vendor__version_2019-12-02T16_58_12__bundle_bootstrap_js_bootstrap.min.js_jed.min.js_moment-with-locales.js_select2_select2.`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/fanstatic/base/:version:2019-12-02T16:58:12/:bundle:plugins/jquery.inherit.min.js;plugins/jquery.proxy-all.min.js;plugins/jquery.url-helpers.min.js;plugins/jquery.date-helpers.min.js;plugins/jquery.slug.min.js;plugins/jquery.slug-preview.min.js;plugins/jquery.truncator.min.js;plugins/jquery.masonry.min.js;plugins/jquery.form-warning.min.js;sandbox.min.js;module.min.js;pubsub.min.js;client.min.js;notify.min.js;i18n.min.js;main.min.js;modules/select-switch.min.js;modules/slug-preview.min.js;modules/basic-form.min.js;modules/confirm-action.min.js;modules/api-info.min.js;modules/autocomplete.min.js;modules/custom-fields.min.js;modules/data-viewer.min.js;modules/table-selectable-rows.min.js;modules/resource-form.min.js;modules/resource-upload-field.min.js;modules/resource-reorder.min.js;modules/resource-view-reorder.min.js;modules/follow.min.js;modules/activity-stream.min.js;modules/dashboard.min.js;modules/resource-view-embed.min.js;view-filters.min.js;modules/resource-view-filters-form.min.js;modules/resource-view-filters.min.js;modules/table-toggle-more.min.js;modules/dataset-visibility.min.js;modules/media-grid.min.js;modules/image-upload.min.js → 200 `application/javascript` (script) · guardado `consulta_0226___fanstatic_base__version_2019-12-02T16_58_12__bundle_plugins_jquery.inherit.min.js_plugins_jquery.proxy-all.min.js_plugins_jquery.url-h`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/fanstatic/ckanext-googleanalytics/:version:2019-12-02T16:58:24/googleanalytics_event_tracking.js → 200 `application/javascript` (script) · guardado `consulta_0226___fanstatic_ckanext-googleanalytics__version_2019-12-02T16_58_24_googleanalytics_event_tracking.js`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/fanstatic/gobar_js/:version:2019-12-02T17:16:31/:bundle:background_ie.js;console_message.js;header.js;replace_svg.js;forms/custom_popup.js;libs/BootstrapMenu.js;libs/bootstrap_scripts.js;libs/clamp.js;search/filters.js;search/groups.js → 200 `application/javascript` (script) · guardado `consulta_0226___fanstatic_gobar_js__version_2019-12-02T17_16_31__bundle_background_ie.js_console_message.js_header.js_replace_svg.js_forms_custom_popu`
- [consulta_0226] GET https://www.google-analytics.com/analytics.js → 200 `text/javascript` (script) · guardado `consulta_0226___analytics.js`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/dataset → 200 `text/html; charset=utf-8` (document) · guardado `consulta_0226___dataset`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-01-184914.247043adminpub-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `consulta_0226___uploads_group_2024-08-01-184914.247043adminpub-nn-01.svg`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-01-185625.422619agricultura-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `consulta_0226___uploads_group_2024-08-01-185625.422619agricultura-nn-01.svg`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-01-191228.901293demografia-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `consulta_0226___uploads_group_2024-08-01-191228.901293demografia-nn-01.svg`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-02-131818.178601economia-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `consulta_0226___uploads_group_2024-08-02-131818.178601economia-nn-01.svg`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-02-131844.893245educacion-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `consulta_0226___uploads_group_2024-08-02-131844.893245educacion-nn-01.svg`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-02-131903.697006genero-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `consulta_0226___uploads_group_2024-08-02-131903.697006genero-nn-01.svg`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-02-131949.745468industria-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `consulta_0226___uploads_group_2024-08-02-131949.745468industria-nn-01.svg`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-02-132115.264054ambiente-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `consulta_0226___uploads_group_2024-08-02-132115.264054ambiente-nn-01.svg`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-02-132136.828658movilidad-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `consulta_0226___uploads_group_2024-08-02-132136.828658movilidad-nn-01.svg`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-02-132155.782494salud-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `consulta_0226___uploads_group_2024-08-02-132155.782494salud-nn-01.svg`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/uploads/group/2024-08-02-132224.737631justicia-nn-01.svg → 200 `image/svg+xml` (xhr) · guardado `consulta_0226___uploads_group_2024-08-02-132224.737631justicia-nn-01.svg`
- [consulta_0226] GET https://catalogo.datos.gba.gob.ar/api/i18n/es → 200 `application/json;charset=utf-8` (xhr) · guardado `consulta_0226___api_i18n_es`
