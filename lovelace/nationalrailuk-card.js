/**
 * National Rail UK Departure Board Card
 * 
 * A simple table card for displaying train departures from National Rail sensors.
 * 
 * @version 1.0.0
 * @author darrenparkinson
 * @inspiration ChevronTango/nationalrail-status-card
 */

class NationalRailUKCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._hass = null;
    this._config = null;
    this._lastUpdate = 0;
  }

  setConfig(config) {
    this._validateConfig(config);

    this._config = {
      title: config.title || 'Train Departures',
      entity: config.entity,
      max_rows: config.max_rows || 10,
      limit: config.limit || 10,
      show_delayed: config.show_delayed !== false,
      show_cancelled: config.show_cancelled !== false,
      show_platform: config.show_platform || false,
      show_operator: config.show_operator || false,
      refresh_interval: config.refresh_interval || 30,
      ...config
    };

    if (config.limit && !config.max_rows) {
      this._config.max_rows = config.limit;
    }

    this.render();
  }

  static getStubConfig() {
    return {
      entity: 'sensor.train_schedule_wat_all',
      title: 'Train Departures'
    };
  }

  render() {
    if (!this.shadowRoot) return;
    
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          font-family: var(--ha-card-font-family, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif);
        }
        
        .card {
          background: var(--ha-card-background, #fff);
          border-radius: 12px;
          padding: 16px;
          margin: 8px;
        }
        
        .header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 16px;
          font-size: 16px;
          font-weight: 500;
          color: var(--primary-text-color, #212121);
        }
        
        .title {
          margin: 0;
          font-size: 18px;
          font-weight: 600;
        }
        
        .status {
          font-size: 12px;
          padding: 4px 8px;
          border-radius: 12px;
          background: var(--primary-color, #03a9f4);
          color: white;
        }
        
        .status.available {
          background: #4caf50;
        }
        
        .status.unavailable {
          background: #f44336;
        }
        
        .table {
          width: 100%;
          border-collapse: collapse;
          font-size: 14px;
        }
        
        .table th {
          text-align: left;
          padding: 8px 12px;
          border-bottom: 2px solid var(--divider-color, #e0e0e0);
          font-weight: 600;
          color: var(--primary-text-color, #212121);
        }
        
        .table td {
          padding: 8px 12px;
          border-bottom: 1px solid var(--divider-color, #e0e0e0);
          color: var(--primary-text-color, #212121);
        }
        
        .table tr:hover {
          background-color: var(--divider-color, #f5f5f5);
        }
        
        .time {
          font-weight: 600;
          font-family: monospace;
        }
        
        .destination {
          max-width: 200px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
        
        .status-cell {
          text-align: center;
        }
        
        .status-on-time {
          color: #4caf50;
          font-weight: 600;
        }
        
        .status-delayed {
          color: #ff9800;
          font-weight: 600;
        }
        
        .status-cancelled {
          color: #f44336;
          font-weight: 600;
        }
        
        .no-trains {
          text-align: center;
          padding: 20px;
          color: var(--secondary-text-color, #757575);
          font-style: italic;
        }
        
        .error {
          text-align: center;
          padding: 20px;
          color: #f44336;
        }
        
        .loading {
          text-align: center;
          padding: 20px;
          color: var(--secondary-text-color, #757575);
        }
      </style>
      
      <ha-card>
        <div class="card">
          <div class="header">
            <div class="title">${this._config ? this._config.title : 'Train Departures'}</div>
            <div class="status" id="status">Loading...</div>
          </div>
          <div id="content">
            <div class="loading">Loading departures...</div>
          </div>
        </div>
      </ha-card>
    `;
  }

  set hass(hass) {
    if (this._hass === hass) return;
    this._hass = hass;
    this.updateContent();
  }

  updateContent() {
    if (!this._hass || !this._config) return;
    
    const entity = this._hass.states[this._config.entity];
    const statusElement = this.shadowRoot.getElementById('status');
    const contentElement = this.shadowRoot.getElementById('content');

    if (!statusElement || !contentElement) return;

    if (!entity) {
      statusElement.textContent = 'Entity not found';
      statusElement.className = 'status unavailable';
      contentElement.innerHTML = '<div class="error">Entity not found</div>';
      return;
    }

    if (entity.state === 'unavailable') {
      statusElement.textContent = 'Unavailable';
      statusElement.className = 'status unavailable';
      contentElement.innerHTML = '<div class="error">Sensor unavailable</div>';
      return;
    }

    statusElement.textContent = entity.state;
    statusElement.className = 'status available';

    const trains = entity.attributes.trains || [];
    
    if (trains.length === 0) {
      contentElement.innerHTML = '<div class="no-trains">No trains available</div>';
      return;
    }

    let filteredTrains = trains.filter(train => {
      if (!this._config.show_cancelled && train.isCancelled) return false;
      if (!this._config.show_delayed && this.isDelayed(train)) return false;
      return true;
    });

    filteredTrains.sort((a, b) => {
      const timeA = this.parseTime(a.std);
      const timeB = this.parseTime(b.std);
      return timeA - timeB;
    });

    filteredTrains = filteredTrains.slice(0, this._config.max_rows);

    const tableHTML = this.generateTable(filteredTrains);
    contentElement.innerHTML = tableHTML;
  }

  _validateConfig(config) {
    if (!config.entity) {
      throw new Error('Entity is required');
    }
    
    if (config.max_rows && (config.max_rows < 1 || config.max_rows > 50)) {
      throw new Error('max_rows must be between 1 and 50');
    }
    
    if (config.limit && (config.limit < 1 || config.limit > 50)) {
      throw new Error('limit must be between 1 and 50');
    }
  }

  generateTable(trains) {
    if (trains.length === 0) {
      return '<div class="no-trains">No trains match your filters</div>';
    }

    let tableHTML = `
      <table class="table">
        <thead>
          <tr>
            <th>Time</th>
            <th>Destination</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
    `;

    trains.forEach(train => {
      const scheduledTime = train.std || 'N/A';
      const destination = this.getDestination(train);
      const status = this.getStatus(train);

      tableHTML += `
        <tr>
          <td class="time">${scheduledTime}</td>
          <td class="destination" title="${destination}">${destination}</td>
          <td class="status-cell ${status.class}">${status.text}</td>
        </tr>
      `;
    });

    tableHTML += '</tbody></table>';
    return tableHTML;
  }

  getDestination(train) {
    if (train.destination && train.destination.length > 0) {
      return train.destination[0].locationName || 'Unknown';
    }
    return 'Unknown';
  }

  getStatus(train) {
    if (train.isCancelled) {
      return { text: 'Cancelled', class: 'status-cancelled' };
    }
    
    if (this.isDelayed(train)) {
      const scheduled = this.parseTime(train.std);
      const expected = this.parseTime(train.etd);
      const delay = expected - scheduled;
      
      if (delay > 0) {
        return { text: `+${delay}min`, class: 'status-delayed' };
      }
    }
    
    return { text: 'On time', class: 'status-on-time' };
  }

  isDelayed(train) {
    if (!train.std || !train.etd) return false;
    if (train.std === train.etd) return false;
    
    const scheduled = this.parseTime(train.std);
    const expected = this.parseTime(train.etd);
    
    return expected !== scheduled;
  }

  parseTime(timeStr) {
    if (!timeStr || timeStr === 'N/A') return 0;
    
    const parts = timeStr.split(':');
    if (parts.length === 2) {
      return parseInt(parts[0]) * 60 + parseInt(parts[1]);
    }
    
    return 0;
  }

  getCardSize() {
    return 3;
  }
}

customElements.define('nationalrailuk-card', NationalRailUKCard); 