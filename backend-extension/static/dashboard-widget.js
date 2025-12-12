(function (customElements) {

const PYTHON_DASHBOARD_URL = "https://extension-hsi.nubecenter.com.ar/dashboard";

    class DashboardWidget extends HTMLElement {
        constructor() {
            super();
            this.attachShadow({ mode: 'open' });
        }

        connectedCallback() {
            this.render();
        }

        getToken() {
            // 1. Prioridad: Window Global
            if (window.__HSI_DEV_TOKEN__) {
                return window.__HSI_DEV_TOKEN__;
            }

            const candidates = ['token', 'access_token', 'id_token', 'currentUser'];
            
            // 2. Bucle corregido
            for (const key of candidates) {
                let item = localStorage.getItem(key) || sessionStorage.getItem(key);
                
                if (item) {
                    // Limpiar comillas si es string
                    if (item.startsWith('"')) item = item.slice(1, -1);
                    
                    // Si es token directo
                    if (item.startsWith('eyJ')) return item;
                    
                    // Si es objeto JSON
                    try {
                        const json = JSON.parse(item);
                        // Buscamos propiedades comunes
                        const subToken = json.token || json.accessToken || json.id_token;
                        if (subToken && subToken.startsWith('eyJ')) return subToken;
                    } catch (e) { }
                }
                // ELIMINADO EL return null DE AQUÍ
            }
            // (El bucle termina sin encontrar nada en storage)

            // 3. Cookies
            if (document.cookie) {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.includes('eyJ')) {
                        const parts = cookie.split('=');
                        if (parts.length === 2 && parts[1].startsWith('eyJ')) {
                            return parts[1];
                        }
                    }
                }
            }

            // Si llegamos aquí y no encontramos nada, entonces devolvemos null
            return null;
        }

        render() {
            // Obtenemos el token o usamos una cadena vacía
            const token = this.getToken() || "";

            this.shadowRoot.innerHTML = `
                <style>
                    :host {
                        display: block;
                        width: 100%;
                        min-height: 850px; 
                        margin-top: 15px;
                    }
                    .dashboard-frame {
                        width: 100%;
                        height: 100%;
                        min-height: 850px;
                        border: none;
                        border-radius: 4px;
                        background-color: transparent;
                    }
                </style>
            `;

            const iframe = document.createElement('iframe');
            iframe.className = 'dashboard-frame';
            iframe.src = `${PYTHON_DASHBOARD_URL}?t=${encodeURIComponent(token)}`;
            
            this.shadowRoot.appendChild(iframe);
        }
    }

    customElements.define('dashboard-widget', DashboardWidget);

})(window.customElements);