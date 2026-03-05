(function (customElements) {
    const API_BASE_URL = "http://localhost:8000/api/laboratorios";

    class LaboratoriosWidget extends HTMLElement {
        constructor() {
            super();
            this.attachShadow({ mode: 'open' });
        }

        connectedCallback() {
            this.renderSearch();
        }

        renderSearch() {
            const SEARCH_STYLES = `
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap');
                    
                    :host {
                        display: block;
                        font-family: 'Roboto', sans-serif;
                    }
                    .search-container {
                        padding: 20px;
                    }
                    .search-title {
                        font-size: 18px;
                        color: #444;
                        margin-bottom: 16px;
                        font-weight: 400;
                    }
                    .search-card {
                        background: #fff;
                        border: 1px solid #e0e0e0;
                        border-radius: 4px;
                        padding: 50px 20px;
                        display: flex;
                        justify-content: center;
                    }
                    .search-input-wrapper {
                        position: relative;
                        width: 100%;
                        max-width: 450px;
                    }
                    .search-input {
                        width: 100%;
                        padding: 12px 45px 12px 20px;
                        border: 1px solid #ccc;
                        border-radius: 25px; /* Bordes redondeados tipo píldora */
                        font-size: 14px;
                        outline: none;
                        box-sizing: border-box;
                        color: #333;
                    }
                    .search-input::placeholder {
                        color: #aaa;
                    }
                    .search-input:focus {
                        border-color: #1976d2;
                    }
                    .search-icon-btn {
                        position: absolute;
                        right: 15px;
                        top: 50%;
                        transform: translateY(-50%);
                        background: none;
                        border: none;
                        cursor: pointer;
                        color: #1976d2;
                        padding: 0;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }
                    .search-icon-btn svg {
                        width: 18px;
                        height: 18px;
                        fill: currentColor;
                    }
                </style>
            `;

            this.shadowRoot.innerHTML = `
                ${SEARCH_STYLES}
                <div class="search-container">
                    <div class="search-title">Búsqueda de resultados</div>
                    <div class="search-card">
                        <div class="search-input-wrapper">
                            <input type="text" class="search-input" id="dniInput" placeholder="Ingrese número de documento del paciente" autocomplete="off">
                            <button class="search-icon-btn" id="searchBtn">
                                <!-- Ícono de lupa SVG -->
                                <svg viewBox="0 0 24 24">
                                    <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
                                </svg>
                            </button>
                        </div>
                    </div>

                    <!-- 🔴 ESTE ES EL CONTENEDOR DONDE SE INYECTARÁN LOS RESULTADOS (Sin borrar el buscador) 🔴 -->
                    <div id="resultados-container"></div>
                </div>
            `;

            // eventos al botón 
            const btn = this.shadowRoot.getElementById('searchBtn');
            const input = this.shadowRoot.getElementById('dniInput');

            btn.addEventListener('click', () => this.ejecutarBusqueda(input.value));
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.ejecutarBusqueda(input.value);
            });
        }

        // busqueda
        async ejecutarBusqueda(dni) {
            if (!dni || dni.trim() === '') return;

            // ¡IMPORTANTE! Solo actualizamos el div de resultados, no todo el shadowRoot
            const contenedor = this.shadowRoot.getElementById('resultados-container');
            contenedor.innerHTML = `
                <div style="font-family: sans-serif; padding: 40px; text-align: center;">
                    <div style="color: #1976d2; font-size: 16px;">⏳ Buscando resultados para el DNI ${dni}...</div>
                </div>
            `;

            try {
                const response = await fetch(`${API_BASE_URL}/${dni.trim()}`);
                const data = await response.json();

                if (data.total_registros === 0) {
                    this.renderEmpty(dni);
                } else {
                    this.renderResultados(data.data, dni);
                }
            } catch (error) {
                console.error("Error obteniendo laboratorios:", error);
                this.renderError();
            }
        }

        // RESULTADOS
        renderResultados(laboratorios, dni) {
            const contenedor = this.shadowRoot.getElementById('resultados-container');
            
            const nombrePaciente = laboratorios[0]["Nombre del Paciente"] || "Paciente";

            const RESULTADOS_STYLES = `
                <style>
               
                    .resultados-wrapper {
                        margin-top: 30px;
                        font-family: 'Roboto', sans-serif;
                    }

                    .titulo-resultados {
                        /* TAREA: Cambiar tamaño de fuente y color */
                        font-weight: bold;
                        margin-bottom: 15px;
                    }

                    .paciente-header {
                        /* TAREA: Agregar fondo celeste claro (#e6f7ff), bordes, padding */
                        border: 1px solid black; 
                        padding: 10px;
                        display: flex;
                        align-items: center;
                    }

                    .icono-paciente {
                        /* TAREA: Darle estilo al ícono de usuario */
                        margin-right: 15px;
                        font-size: 24px;
                    }

                    .lista-estudios {
                        /* TAREA: Manejar el contenedor de la lista si es necesario */
                        margin-top: 10px;
                    }

                    .item-estudio {
                        /* TAREA: Flexbox para separar textos del botón de descarga, padding, hover */
                        border: 1px dashed gray; 
                        padding: 10px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 5px;
                    }

                    .info-estudio {
                        display: flex;
                        align-items: center;
                    }

                    .icono-pdf {
                        /* TAREA: Estilo para el icono de documento */
                        margin-right: 15px;
                        font-size: 24px;
                    }

                    .btn-descargar {
                        /* TAREA: Hacer que parezca un botón primario azul (fondo azul, texto blanco, sin borde, padding) */
                        background: transparent;
                        border: 1px solid black;
                        cursor: pointer;
                        padding: 5px 10px;
                    }
                </style>
            `;

            let htmlLista = '';
            laboratorios.forEach(lab => {
                const problemaInfo = lab["Problema Asociado"] ? lab["Problema Asociado"].split(' [')[0] : 'No especificado';

                htmlLista += `
                    <div class="item-estudio">
                        <div class="info-estudio">
                            <div class="icono-pdf">📄</div>
                            <div>
                                <div style="font-weight: bold;">${lab["Nombre del Estudio"]}</div>
                                <div style="font-size: 13px;">Problema: ${problemaInfo}</div>
                            </div>
                        </div>
                        <button class="btn-descargar">📥 Descargar</button>
                    </div>
                `;
            });

            contenedor.innerHTML = `
                ${RESULTADOS_STYLES}
                <div class="resultados-wrapper">
                    
                    <div class="titulo-resultados">Resultados de la búsqueda</div>
                    
                    <!-- ENCABEZADO CELESTE DEL PACIENTE -->
                    <div class="paciente-header">
                        <div class="icono-paciente">👤</div>
                        <div>
                            <div style="font-weight: bold;">${nombrePaciente}</div>
                            <div style="font-size: 13px;">ID: ${dni}</div>
                        </div>
                    </div>

                    <!-- LISTA DE ESTUDIOS -->
                    <div class="lista-estudios">
                        ${htmlLista}
                    </div>

                </div>
            `;
        }

        renderEmpty(dni) {
            const contenedor = this.shadowRoot.getElementById('resultados-container');
            contenedor.innerHTML = `
                <div style="text-align: center; padding: 40px; color: #666; font-family: sans-serif; margin-top: 20px;">
                    No se encontraron resultados para el DNI: <strong>${dni}</strong>.
                </div>
            `;
        }

        renderError() {
            const contenedor = this.shadowRoot.getElementById('resultados-container');
            contenedor.innerHTML = `
                <div style="text-align: center; padding: 20px; color: red; font-family: sans-serif; margin-top: 20px;">
                    Error de conexión. Asegúrate de que el backend esté corriendo.
                </div>
            `;
        }
    }

    customElements.define('laboratorios-widget', LaboratoriosWidget);

})(window.customElements);