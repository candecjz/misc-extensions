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
            if (window.__HSI_DEV_TOKEN__) {
                return window.__HSI_DEV_TOKEN__;
            }

            const candidates = ['token', 'access_token', 'id_token', 'currentUser'];
            
       
            for (const key of candidates) {
                let item = localStorage.getItem(key) || sessionStorage.getItem(key);
                
                if (item) {
                    
                    if (item.startsWith('"')) item = item.slice(1, -1);
                    
                    // Si es token directo
                    if (item.startsWith('eyJ')) return item;
                    
                    // Si es objeto JSON
                    try {
                        const json = JSON.parse(item);
                        const subToken = json.token || json.accessToken || json.id_token;
                        if (subToken && subToken.startsWith('eyJ')) return subToken;
                    } catch (e) { }
                }
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
            const token = this.getToken() || "";

            this.shadowRoot.innerHTML = `
                <style>
                    :host {
                        display: block;
                        width: 100%;
                        padding: 30px 0; 
                        box-sizing: border-box;
                        display: flex;
                    }
                    .dashboard-frame {
                        width: 100%;
                        min-height: 500px;
                        height: calc(100vh - 140px); 
                        max-width: 1300px;
                        min-height: 500px;
                        border: none;
                        border-radius: 8px;
                        background-color: transparent;
                    }

                    @media (max-width: 768px) {
                        :host {
                            padding: 15px; 
                        }
                        .dashboard-frame {
                            width: 95%;
                            height: calc(100vh - 100px);
                        }
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