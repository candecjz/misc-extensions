(function (customElements) {

    const STYLES = `
  <style>
    .link-button {
      display: inline-block;
      padding: 12px 28px;
      margin: 8px;
      font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 15px;
      font-weight: 400;
      text-align: center;
      text-decoration: none;
      color: #ffffff;
      background-color: #0078D7;
      border: 2px solid #0078D7;
      border-radius: 0;
      cursor: pointer;
      transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out;
    }
    .link-button:hover {
      background-color: #ffffff;
      color: #0078D7;
    }
  </style>`;

    class TicketButtonWidget extends HTMLElement {
        constructor() {
            super();
            this.attachShadow({ mode: 'open' });
        }

        connectedCallback() {
            this.shadowRoot.innerHTML = `
                ${STYLES}
                <a href="#" class="link-button">Ingresar a Soporte</a>
            `;

            this.shadowRoot.querySelector('.link-button').addEventListener('click', (e) => {
                e.preventDefault();

                
                fetch('/api/account/info')
                    .then(response => {
                        if (!response.ok) throw new Error("Sin sesión");
                        return response.json();
                    })
                    .then(data => {
                        const jsonStr = JSON.stringify(data);
                        
                        const utf8Str = unescape(encodeURIComponent(jsonStr));
                        const base64Payload = window.btoa(utf8Str);
                        
                        const safePayload = encodeURIComponent(base64Payload);
                        const ssoUrl = `http://128.201.239.37:8083/sso-redirect?token=${safePayload}`;
                        
                        window.open(ssoUrl, '_blank', 'noopener,noreferrer');
                    })
                    .catch(err => {
                        alert("No pudimos detectar tu sesión en HSI. Por favor, volvé a iniciar sesión.");
                    });
            });
        }
    }

    customElements.define('ticket-button-widget', TicketButtonWidget);

})(window.customElements);