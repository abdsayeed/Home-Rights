import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface SupportOrg {
  name: string;
  type: string;
  phone: string;
  distance: string;
  color: string;
}

@Component({
  selector: 'app-support-finder',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="support-container">
      <div class="support-header fade-up">
        <h1 class="serif">Find Local <span class="highlight">Support</span></h1>
        <p>100+ UK housing organisations indexed and ready to help</p>
      </div>

      <div class="filters-section fade-up" style="animation-delay: 0.1s">
        <div class="filter-group">
          <div class="filter-box">
            <span class="filter-icon">📍</span>
            <input type="text" placeholder="London, UK" />
          </div>
          <div class="filter-box">
            <span class="filter-icon">⚖</span>
            <select>
              <option>All Issues</option>
              <option>Eviction</option>
              <option>Deposits</option>
              <option>Repairs</option>
              <option>Rent</option>
            </select>
          </div>
        </div>
      </div>

      <div class="results-section">
        <div *ngFor="let org of organizations; let i = index" 
             class="org-card fade-up"
             [style.animation-delay]="(i * 0.1 + 0.2) + 's'">
          <div class="org-icon" [style.background]="org.color + '18'" [style.border-color]="org.color + '30'">
            <span>◉</span>
          </div>
          <div class="org-info">
            <h3>{{ org.name }}</h3>
            <p>{{ org.type }} · {{ org.phone }}</p>
          </div>
          <div class="org-distance" [style.color]="org.color">
            {{ org.distance }}
          </div>
        </div>
      </div>

      <div class="info-banner fade-up" style="animation-delay: 0.8s">
        <div class="banner-content">
          <h3 class="serif">Need immediate help?</h3>
          <p>If you're facing homelessness or an emergency housing situation, contact Shelter's emergency helpline.</p>
          <div class="emergency-contact">
            <span class="phone-icon">📞</span>
            <span class="phone-number">0808 800 4444</span>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .support-container {
      min-height: 100vh;
      background: var(--bg);
      padding: 60px 48px;
      max-width: 1000px;
      margin: 0 auto;
    }

    .support-header {
      text-align: center;
      margin-bottom: 48px;
    }

    .support-header h1 {
      font-size: 48px;
      font-weight: 400;
      letter-spacing: -1.2px;
      color: var(--ink);
      margin-bottom: 12px;
      line-height: 1.1;
    }

    .highlight {
      color: var(--red);
      font-style: italic;
    }

    .support-header p {
      font-size: 18px;
      color: var(--ink3);
      font-weight: 300;
    }

    .filters-section {
      margin-bottom: 40px;
    }

    .filter-group {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }

    .filter-box {
      background: #fff;
      border: 1.5px solid var(--border);
      border-radius: var(--r);
      padding: 14px 18px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: var(--shadow-sm);
      transition: all 0.2s;
    }

    .filter-box:focus-within {
      border-color: var(--teal);
      box-shadow: 0 0 0 3px rgba(0, 168, 138, 0.1);
    }

    .filter-icon {
      font-size: 18px;
      opacity: 0.7;
    }

    .filter-box input,
    .filter-box select {
      flex: 1;
      border: none;
      outline: none;
      font-size: 14px;
      color: var(--ink);
      background: transparent;
    }

    .filter-box input::placeholder {
      color: var(--ink3);
    }

    .results-section {
      margin-bottom: 56px;
    }

    .org-card {
      background: #fff;
      border: 1px solid var(--border);
      border-radius: var(--r);
      padding: 20px 24px;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 16px;
      transition: all 0.25s;
      box-shadow: var(--shadow-sm);
    }

    .org-card:hover {
      box-shadow: var(--shadow-md);
      transform: translateY(-2px);
    }

    .org-icon {
      width: 48px;
      height: 48px;
      border-radius: var(--r-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      border: 1px solid;
      flex-shrink: 0;
    }

    .org-info {
      flex: 1;
    }

    .org-info h3 {
      font-size: 16px;
      font-weight: 600;
      color: var(--ink);
      margin-bottom: 4px;
    }

    .org-info p {
      font-size: 13px;
      color: var(--ink3);
    }

    .org-distance {
      font-size: 14px;
      font-weight: 700;
      flex-shrink: 0;
    }

    .info-banner {
      background: linear-gradient(135deg, var(--red-lt), #fff5f5);
      border: 1px solid #f5b5b0;
      border-radius: var(--r);
      padding: 40px;
      text-align: center;
    }

    .banner-content h3 {
      font-size: 28px;
      font-weight: 400;
      letter-spacing: -0.7px;
      color: var(--ink);
      margin-bottom: 12px;
    }

    .banner-content p {
      font-size: 15px;
      color: var(--ink2);
      margin-bottom: 24px;
      max-width: 500px;
      margin-left: auto;
      margin-right: auto;
      line-height: 1.6;
    }

    .emergency-contact {
      display: inline-flex;
      align-items: center;
      gap: 12px;
      background: #fff;
      padding: 14px 28px;
      border-radius: var(--r-full);
      box-shadow: var(--shadow-md);
      border: 1px solid var(--border);
    }

    .phone-icon {
      font-size: 24px;
    }

    .phone-number {
      font-size: 20px;
      font-weight: 700;
      color: var(--red);
      font-family: 'Courier New', monospace;
    }

    @media (max-width: 768px) {
      .support-container {
        padding: 40px 24px;
      }

      .support-header h1 {
        font-size: 36px;
      }

      .filter-group {
        grid-template-columns: 1fr;
      }

      .info-banner {
        padding: 32px 24px;
      }

      .emergency-contact {
        flex-direction: column;
        gap: 8px;
      }
    }
  `]
})
export class SupportFinderComponent {
  organizations: SupportOrg[] = [
    { name: 'Shelter England', type: 'Housing Charity', phone: '0808 800 4444', distance: '0.3mi', color: '#00a88a' },
    { name: 'Citizens Advice', type: 'Legal Aid', phone: '0800 144 8848', distance: '0.7mi', color: '#7c6af0' },
    { name: 'Crisis UK', type: 'Homelessness', phone: '0800 038 4444', distance: '1.2mi', color: '#e8840a' },
    { name: 'Law Centres Network', type: 'Legal Support', phone: '020 3637 1330', distance: '1.5mi', color: '#3b7dd8' },
    { name: 'Housing Ombudsman', type: 'Dispute Resolution', phone: '0300 111 3000', distance: '2.1mi', color: '#d93025' },
  ];
}
