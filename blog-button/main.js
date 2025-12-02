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
    .link-button:active {
      background-color: #e6e6e6;
      color: #0078D7;
    }
  </style>`;

    /**
     * Creates the HTML template for the link button.
     * @param {string} href - The URL the button will link to.
     * @param {string} label - The text displayed on the button.
     * @returns {HTMLTemplateElement} The template element.
     */
    const createTemplate = (href, label) => {
        const template = document.createElement('template');
        template.innerHTML = `
      ${STYLES}
      <a href="${href}" class="link-button" target="_blank" rel="noopener noreferrer">
        ${label}
      </a>
    `;
        return template;
    };

    /**
     * Defines the LinkButtonWidget custom element.
     */
    class LinkButtonWidget extends HTMLElement {
        constructor() {
            super();
            this.attachShadow({ mode: 'open' });
        }

        /**
         * Called when the element is added to the document's DOM.
         * This is a reliable lifecycle callback for initial setup.
         */
        connectedCallback() {
            const hardcodedParams = {
                href: "https://blog-hsi.nubecenter.com.ar/",
                label: "Acceder al blog"
            };

            this.render(hardcodedParams);
        }

        /**
         * Renders the component based on the provided parameters.
         * @param {object} params - The parameters for the component.
         */
        render(params) {
            const { href, label } = params;

            this.shadowRoot.innerHTML = '';

            const template = createTemplate(href, label);
            this.shadowRoot.appendChild(template.content.cloneNode(true));
        }
    }

    // Define the new custom element so it can be used in HTML.
    customElements.define('link-button-widget', LinkButtonWidget);

})(window.customElements);