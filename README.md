# OrgTask
Organizador de tareas basado en [org-mode](https://orgmode.org/). 
Interfaz basada en texto TUI escrita con la librería [textual](https://textual.textualize.io/)

versión 0.2.0
* DONE se modificó orgparse
la versión de orgparse se modificó para añadir ligeros cambios
en caso de que los marcadores de sdc (schedule, deadline, closed) no estén en la misma línea, se reescribe el arreglo que contiene a todas las líneas del nodo (OrgTask)

* DONE versión mínima
se ha hecho la versión mínima para mostrar en detalle las tareas conviertiéndolas en objetos, y mostrándo los atributos en una interfaz sencilla de lista detallada


* TODO detailed_list 
- mejorar los detalles que se muestran en detailed_list, el formato no es el adecuado para las fechas ni para las propiedades

* TODO OrgTask methods, org_core
- la siguiente pantalla incluirá ingreso de datos -> new_task
- editar entrada: en la lista detallada, posibilitar la edición de entradas -> edit_task 
