(function (customElements) {

 
  const PYTHON_SITE_URL = "http://localhost:8000/dashboard"; // URL del dashboard de FastAPI

  const STYLES = `
  <style>
    .link-button {
      display: inline-block;
      padding: 12px 28px;
      margin: 8px;
      font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 15px;
      font-weight: 600;
      text-align: center;
      text-decoration: none;
      color: #ffffff;
      background-color: #0078D7;
      border: 2px solid #0078D7;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.2s ease-in-out;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .link-button:hover {
      background-color: #005a9e;
      border-color: #005a9e;
      transform: translateY(-1px);
      box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    /* Estilos de carga y error eliminados, ya que no hacemos validación previa */
  </style>`;

 
  const obtenerTokenHSI = () => {
    const token = localStorage.getItem('token') ||
      sessionStorage.getItem('token') ||
      localStorage.getItem('access_token'); // Nombres comunes
    return token ? token.replace(/"/g, '') : null;
  };

  const createTemplate = (label) => {
    const template = document.createElement('template');
    template.innerHTML = `
      ${STYLES}
      <button type="button" class="link-button">
        ${label}
      </button>
    `;
    return template;
  };

  class LinkButtonWidget extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
      // Renderizamos con el texto de tu extensión
      this.render({ label: "💊 Objetivos Sanitarios" });
    }

    render(params) {
      const { label } = params;
      this.shadowRoot.innerHTML = '';

      const template = createTemplate(label);
      this.shadowRoot.appendChild(template.content.cloneNode(true));

      // Agregamos el Listener del Click
      const btn = this.shadowRoot.querySelector('.link-button');
      btn.addEventListener('click', (e) => this.handleClick(e, btn));
    }

   
    handleClick(e, btn) {
      e.preventDefault(); 

      const token = obtenerTokenHSI();

      if (!token) {
        alert("⚠️ Error: No se detectó una sesión activa en HSI.");
        return;
      }

      const urlDestino = `${PYTHON_SITE_URL}?t=${encodeURIComponent(token)}`;
      
      window.open(urlDestino, '_blank');
    }
  }

  customElements.define('link-button-widget', LinkButtonWidget);

})(window.customElements);