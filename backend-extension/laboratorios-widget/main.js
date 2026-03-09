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
                        display: flex;
                        flex-direction: column;
                        font-family: 'Roboto', sans-serif;
                        height: 100%; 
                    }

                    .search-container {
                        padding: 20px;
                        display: flex;
                        flex-direction: column;
                        flex-grow: 1;
                    }

                    .search-title {
                        font-size: 18px;
                        color: #444;
                        margin-bottom: 16px;
                        font-weight: 400;
                    }

                    .main-card {
                        background: #fff;
                        border: 1px solid #e0e0e0;
                        border-radius: 4px;
                        display: flex;
                        flex-direction: column;
                        flex-grow: 1; 
                        overflow: hidden;
                    }

                    .search-input-section {
                        display: flex;
                        justify-content: center;
                        padding: 30px 20px; 
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
                        border-radius: 25px;
                        font-size: 14px;
                        outline: none;
                        box-sizing: border-box;
                    }

                    .search-input:focus { border-color: #1976d2; }

                    .search-icon-btn {
                        position: absolute;
                        right: 15px;
                        top: 50%;
                        transform: translateY(-50%);
                        background: none;
                        border: none;
                        cursor: pointer;
                        color: #1976d2;
                        display: flex;
                    }

                    .results-section-header {
                        font-size: 14px;
                        font-weight: bold;
                        color: #333;
                        padding: 15px 20px;
                        border-top: 1px solid #e0e0e0; 
                        background-color: #fcfcfc;
                    }

                    #resultados-container {
                        flex-grow: 1;
                    }
                </style>
            `;

            this.shadowRoot.innerHTML = `
                ${SEARCH_STYLES}
                <div class="search-container">
                    <div class="search-title">Búsqueda de resultados</div>
                    
                    <div class="main-card">
                        <div class="search-input-section">
                            <div class="search-input-wrapper">
                                <input type="text" class="search-input" id="dniInput" placeholder="Ingrese número de documento del paciente" autocomplete="off">
                                <button class="search-icon-btn" id="searchBtn">
                                    <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
                                </button>
                            </div>
                        </div>

                        <div class="results-section-header">Resultados de la búsqueda</div>
                        
                        <div id="resultados-container">
                            </div>
                    </div>
                </div>
            `;

            const btn = this.shadowRoot.getElementById('searchBtn');
            const input = this.shadowRoot.getElementById('dniInput');

            btn.addEventListener('click', () => this.ejecutarBusqueda(input.value));
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.ejecutarBusqueda(input.value);
            });
        }

        async ejecutarBusqueda(dni) {
            if (!dni || dni.trim() === '') return;
            const contenedor = this.shadowRoot.getElementById('resultados-container');
            contenedor.innerHTML = `<div style="padding: 40px; text-align: center; color: #1976d2;">⏳ Buscando para el DNI ${dni}...</div>`;

            try {
                const response = await fetch(`${API_BASE_URL}/${dni.trim()}`);
                const data = await response.json();
                if (data.total_registros === 0) {
                    this.renderEmpty(dni);
                } else {
                    this.renderResultados(data.data, dni);
                }
            } catch (error) {
                this.renderError();
            }
        }

        renderResultados(laboratorios, dni) {
            const contenedor = this.shadowRoot.getElementById('resultados-container');
            const nombrePaciente = laboratorios[0]["Nombre del Paciente"] || "Paciente";

            const RESULTADOS_STYLES = `
                <style>
                    .paciente-header {
                        background-color: #e6f7ff; 
                        padding: 15px 20px;
                        display: flex;
                        align-items: center;
                        border-bottom: 1px solid #e0e0e0;
                    }
                    .icono-paciente { margin-right: 15px; color: #1890ff; display: flex; }
                    .item-estudio {
                        padding: 15px 20px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        border-bottom: 1px solid #f0f0f0;
                    }
                    .info-estudio { display: flex; align-items: center; }
                    .btn-descargar {
                        background-color: #1890ff;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 4px;
                        cursor: pointer;
                        display: flex;
                        align-items: center;
                        gap: 8px;
                        font-size: 13px;
                    }
                    .btn-descargar svg { fill: white; width: 16px; height: 16px; }
                </style>
            `;

            let htmlLista = '';
            laboratorios.forEach(lab => {
                const problema = lab["Problema Asociado"] ? lab["Problema Asociado"].split(' [')[0] : 'No especificado';
                htmlLista += `
                    <div class="item-estudio">
                        <div class="info-estudio">
                            <div style="margin-right:15px; color:#555;">
                                <svg width="24" height="24" fill="currentColor" viewBox="0 0 16 16"><path d="M14 4.5V14a2 2 0 0 1-2 2h-1v-1h1a1 1 0 0 0 1-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5zM1.6 11.85H0v3.999h.791v-1.342h.803q.43 0 .732-.173.305-.175.463-.474a1.4 1.4 0 0 0 .161-.677q0-.375-.158-.677a1.2 1.2 0 0 0-.46-.477q-.3-.18-.732-.179m.545 1.333a.8.8 0 0 1-.085.38.57.57 0 0 1-.238.241.8.8 0 0 1-.375.082H.788V12.48h.66q.327 0 .512.181.185.183.185.522m1.217-1.333v3.999h1.46q.602 0 .998-.237a1.45 1.45 0 0 0 .595-.689q.196-.45.196-1.084 0-.63-.196-1.075a1.43 1.43 0 0 0-.589-.68q-.396-.234-1.005-.234zm.791.645h.563q.371 0 .609.152a.9.9 0 0 1 .354.454q.118.302.118.753a2.3 2.3 0 0 1-.068.592 1.1 1.1 0 0 1-.196.422.8.8 0 0 1-.334.252 1.3 1.3 0 0 1-.483.082h-.563zm3.743 1.763v1.591h-.79V11.85h2.548v.653H7.896v1.117h1.606v.638z"/></svg>
                            </div>
                            <div>
                                <div style="font-weight: bold;">${lab["Nombre del Estudio"]}</div>
                                <div style="font-size: 13px;">Problema: ${problema}</div>
                            </div>
                        </div>
                        <button class="btn-descargar">
                            <svg viewBox="0 0 16 16"><path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5"/><path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708z"/></svg>
                            Descargar
                        </button>
                    </div>
                `;
            });

            contenedor.innerHTML = `
                ${RESULTADOS_STYLES}
                <div class="paciente-header">
                    <div class="icono-paciente">
                        <svg width="24" height="24" fill="currentColor" viewBox="0 0 16 16"><path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/><path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zm12 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1v-1c0-1-1-4-6-4s-6 3-6 4v1a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1z"/></svg>
                    </div>
                    <div>
                        <div style="font-weight: bold;">${nombrePaciente}</div>
                        <div style="font-size: 13px;">ID: ${dni}</div>
                    </div>
                </div>
                <div class="lista-estudios">${htmlLista}</div>
            `;
        }

        renderEmpty(dni) {
            this.shadowRoot.getElementById('resultados-container').innerHTML = `
                <div style="text-align: center; padding: 40px; color: #666;">No se encontraron resultados para: <strong>${dni}</strong>.</div>
            `;
        }

        renderError() {
            this.shadowRoot.getElementById('resultados-container').innerHTML = `
                <div style="text-align: center; padding: 20px; color: red;">Error de conexión.</div>
            `;
        }
    }
    customElements.define('laboratorios-widget', LaboratoriosWidget);
})(window.customElements);