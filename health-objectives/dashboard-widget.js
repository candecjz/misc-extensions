(function (customElements) {

    const PYTHON_DASHBOARD_URL = "http://localhost:5000/dashboard";

    class DashboardWidget extends HTMLElement {
        constructor() {
            super();
            this.attachShadow({ mode: 'open' });
        }

        connectedCallback() {
            this.render();
        }

       
        getToken() {
            if (window.__HSI_DEV_TOKEN__) {
                return window.__HSI_DEV_TOKEN__;
            }

            const candidates = ['token', 'access_token', 'id_token', 'currentUser'];
            for (const key of candidates) {
                let item = localStorage.getItem(key) || sessionStorage.getItem(key);
                if (item) {
                    if (item.startsWith('"')) item = item.slice(1, -1);
                    if (item.startsWith('eyJ')) return item;
                    try {
                        const json = JSON.parse(item);
                        const subToken = json.token || json.accessToken;
                        if (subToken && subToken.startsWith('eyJ')) return subToken;
                    } catch (e) { }
                }

                return null;

            }

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
                        /* Altura fija para ver bien el contenido */
                        min-height: 850px; 
                        margin-top: 15px;
                    }
                    .dashboard-frame {
                        width: 100%;
                        height: 100%;
                        min-height: 850px;
                        border: none;
                        border-radius: 4px;
                        background-color: transparent; /* Transparente para integrarse mejor */
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