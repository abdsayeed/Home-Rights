import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SupportService, SupportOrganization } from '../../core/services/support.service';

@Component({
  selector: 'app-support-finder',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="support-container">
      <div class="support-header fade-up">
        <h1 class="serif">Find Local <span class="highlight">Support</span></h1>
        <p>{{ totalOrgs() }}+ UK housing organisations indexed and ready to help</p>
      </div>

      <div class="emergency-banner fade-up" style="animation-delay: 0.05s">
        <div class="emergency-content">
          <span class="emergency-icon">🚨</span>
          <div class="emergency-text">
            <strong>Emergency Helpline:</strong> Shelter 0808 800 4444 (24/7)
          </div>
        </div>
      </div>

      <div class="filters-section fade-up" style="animation-delay: 0.1s">
        <div class="filter-group">
          <div class="filter-box">
            <span class="filter-icon">📍</span>
            <input 
              type="text" 
              placeholder="Enter postcode (e.g., SW1A 1AA)" 
              [(ngModel)]="postcode"
              (keyup.enter)="onSearch()" />
            <button class="search-btn" (click)="onSearch()">Search</button>
          </div>
          <div class="filter-box">
            <span class="filter-icon">⚖</span>
            <select [(ngModel)]="selectedType" (change)="onFilterChange()">
              <option value="">All Types</option>
              <option value="council">Local Council</option>
              <option value="charity">Charity</option>
              <option value="legal_aid">Legal Aid</option>
              <option value="advice_center">Advice Center</option>
            </select>
          </div>
        </div>
        
        @if (searchLocation()) {
          <div class="location-info">
            📍 Showing results near: <strong>{{ searchLocation() }}</strong>
          </div>
        }
      </div>

      @if (loading()) {
        <div class="loading">Searching for organizations...</div>
      } @else if (organizations().length === 0) {
        <div class="no-results">
          <p>No organizations found. Try a different postcode or expand your search.</p>
        </div>
      } @else {
        <div class="results-section">
          @for (org of organizations(); track org.id; let i = $index) {
            <div class="org-card fade-up" [style.animation-delay]="(i * 0.05 + 0.2) + 's'">
              <div class="org-icon" [style.background]="getTypeColor(org.type) + '18'" [style.border-color]="getTypeColor(org.type) + '30'">
                <span>{{ getTypeIcon(org.type) }}</span>
              </div>
              <div class="org-info">
                <div class="org-header">
                  <h3>{{ org.name }}</h3>
                  @if (org.verificationStatus === 'verified') {
                    <span class="verified-badge">✓ Verified</span>
                  }
                </div>
                <p class="org-type">{{ formatType(org.type) }}</p>
                <p class="org-description">{{ org.description }}</p>
                
                @if (org.address) {
                  <div class="org-address">
                    📍 {{ org.address }}
                  </div>
                }
                
                <div class="org-contact">
                  @if (org.contact.phone) {
                    <a [href]="'tel:' + org.contact.phone" class="contact-link" (click)="trackReferral(org.id, 'phone')">
                      📞 {{ org.contact.phone }}
                    </a>
                  }
                  @if (org.contact.website) {
                    <a [href]="org.contact.website" target="_blank" class="contact-link" (click)="trackReferral(org.id, 'website')">
                      🌐 Website
                    </a>
                  }
                </div>
                
                @if (org.openingHours && hasOpeningHours(org.openingHours)) {
                  <div class="opening-hours">
                    <span class="hours-label">Hours:</span>
                    <span>{{ formatOpeningHours(org.openingHours) }}</span>
                  </div>
                }
              </div>
              @if (org.distanceKm !== undefined) {
                <div class="org-distance" [style.color]="getTypeColor(org.type)">
                  {{ org.distanceKm }} km
                </div>
              }
            </div>
          }
        </div>

        @if (totalPages() > 1) {
          <div class="pagination">
            <button 
              [disabled]="currentPage() === 1" 
              (click)="goToPage(currentPage() - 1)"
              class="btn-pagination">
              ← Previous
            </button>
            <span class="page-info">Page {{ currentPage() }} of {{ totalPages() }}</span>
            <button 
              [disabled]="currentPage() === totalPages()" 
              (click)="goToPage(currentPage() + 1)"
              class="btn-pagination">
              Next →
            </button>
          </div>
        }
      }

      <div class="info-banner fade-up" style="animation-delay: 0.8s">
        <div class="banner-content">
          <h3 class="serif">Organization not listed?</h3>
          <p>Help us expand our database by submitting your organization's details.</p>
          <button class="btn-teal">Submit Organization</button>
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
      margin-bottom: 24px;
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

    .emergency-banner {
      background: linear-gradient(135deg, #fee2e2, #fef2f2);
      border: 2px solid #fca5a5;
      border-radius: var(--r);
      padding: 16px 24px;
      margin-bottom: 32px;
    }

    .emergency-content {
      display: flex;
      align-items: center;
      gap: 12px;
      justify-content: center;
    }

    .emergency-icon {
      font-size: 24px;
    }

    .emergency-text {
      font-size: 15px;
      color: var(--ink);
    }

    .emergency-text strong {
      color: var(--red);
      font-weight: 700;
    }

    .filters-section {
      margin-bottom: 32px;
    }

    .filter-group {
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 16px;
      margin-bottom: 16px;
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

    .search-btn {
      padding: 8px 16px;
      background: var(--teal);
      color: white;
      border: none;
      border-radius: var(--r-sm);
      cursor: pointer;
      font-size: 14px;
      font-weight: 600;
      transition: all 0.2s;
    }

    .search-btn:hover {
      background: #008f75;
    }

    .location-info {
      text-align: center;
      font-size: 14px;
      color: var(--ink2);
      padding: 8px;
    }

    .results-section {
      margin-bottom: 40px;
    }

    .org-card {
      background: #fff;
      border: 1px solid var(--border);
      border-radius: var(--r);
      padding: 24px;
      margin-bottom: 16px;
      display: flex;
      align-items: flex-start;
      gap: 20px;
      transition: all 0.25s;
      box-shadow: var(--shadow-sm);
    }

    .org-card:hover {
      box-shadow: var(--shadow-md);
      transform: translateY(-2px);
    }

    .org-icon {
      width: 56px;
      height: 56px;
      border-radius: var(--r-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      border: 1px solid;
      flex-shrink: 0;
    }

    .org-info {
      flex: 1;
    }

    .org-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 4px;
    }

    .org-info h3 {
      font-size: 18px;
      font-weight: 600;
      color: var(--ink);
    }

    .verified-badge {
      padding: 2px 8px;
      background: #dcfce7;
      color: #166534;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 600;
    }

    .org-type {
      font-size: 13px;
      color: var(--ink3);
      margin-bottom: 8px;
    }

    .org-description {
      font-size: 14px;
      color: var(--ink2);
      line-height: 1.5;
      margin-bottom: 12px;
    }

    .org-address {
      font-size: 13px;
      color: var(--ink3);
      margin-bottom: 12px;
      padding: 8px 12px;
      background: var(--bg);
      border-radius: var(--r-sm);
    }

    .org-contact {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 8px;
    }

    .contact-link {
      font-size: 13px;
      color: var(--teal);
      text-decoration: none;
      padding: 4px 12px;
      background: var(--teal-lt);
      border-radius: 12px;
      transition: all 0.2s;
    }

    .contact-link:hover {
      background: var(--teal);
      color: white;
    }

    .opening-hours {
      font-size: 12px;
      color: var(--ink3);
      margin-top: 8px;
    }

    .hours-label {
      font-weight: 600;
      margin-right: 4px;
    }

    .org-distance {
      font-size: 16px;
      font-weight: 700;
      flex-shrink: 0;
      padding: 8px 12px;
      background: var(--bg);
      border-radius: var(--r-sm);
    }

    .pagination {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 20px;
      margin-bottom: 40px;
    }

    .btn-pagination {
      padding: 10px 20px;
      border: 1.5px solid var(--border);
      background: white;
      border-radius: var(--r);
      cursor: pointer;
      font-size: 14px;
      font-weight: 500;
      transition: all 0.2s;
    }

    .btn-pagination:hover:not(:disabled) {
      background: var(--teal);
      color: white;
      border-color: var(--teal);
    }

    .btn-pagination:disabled {
      opacity: 0.4;
      cursor: not-allowed;
    }

    .page-info {
      font-size: 14px;
      color: var(--ink2);
    }

    .loading, .no-results {
      text-align: center;
      padding: 60px 20px;
      color: var(--ink3);
      font-size: 16px;
    }

    .info-banner {
      background: linear-gradient(135deg, var(--teal-lt), #e6f3fd);
      border: 1px solid var(--teal-mid);
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

      .org-card {
        flex-direction: column;
      }

      .org-distance {
        align-self: flex-start;
      }
    }
  `]
})
export class SupportFinderComponent implements OnInit {
  organizations = signal<SupportOrganization[]>([]);
  loading = signal(false);
  currentPage = signal(1);
  totalPages = signal(1);
  totalOrgs = signal(100);
  postcode = '';
  selectedType = '';
  searchLocation = signal('');

  constructor(private supportService: SupportService) {}

  ngOnInit() {
    this.loadOrganizations();
  }

  loadOrganizations() {
    this.loading.set(true);
    
    const params: any = {
      page: this.currentPage(),
      limit: 20
    };
    
    if (this.postcode) {
      params.postcode = this.postcode;
      this.searchLocation.set(this.postcode);
    }
    if (this.selectedType) params.service_type = this.selectedType;
    
    this.supportService.findSupport(params).subscribe({
      next: (response: any) => {
        this.organizations.set(response.organizations || []);
        if (response.pagination) {
          this.totalPages.set(response.pagination.totalPages);
          this.totalOrgs.set(response.pagination.total);
        }
        this.loading.set(false);
      },
      error: (error) => {
        console.error('Failed to load organizations:', error);
        this.loading.set(false);
      }
    });
  }

  onSearch() {
    this.currentPage.set(1);
    this.loadOrganizations();
  }

  onFilterChange() {
    this.currentPage.set(1);
    this.loadOrganizations();
  }

  goToPage(page: number) {
    this.currentPage.set(page);
    this.loadOrganizations();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  trackReferral(orgId: string, type: string) {
    this.supportService.trackReferral(orgId, type).subscribe();
  }

  getTypeIcon(type: string): string {
    const icons: any = {
      'council': '🏛️',
      'charity': '❤️',
      'legal_aid': '⚖️',
      'advice_center': '💡'
    };
    return icons[type] || '◉';
  }

  getTypeColor(type: string): string {
    const colors: any = {
      'council': '#3b7dd8',
      'charity': '#d93025',
      'legal_aid': '#7c6af0',
      'advice_center': '#00a88a'
    };
    return colors[type] || '#666';
  }

  formatType(type: string): string {
    return type.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  }

  formatOpeningHours(hours: any): string {
    if (!hours || Object.keys(hours).length === 0) return 'Contact for hours';
    const today = new Date().toLocaleDateString('en-US', { weekday: 'short' }).toLowerCase();
    const todayHours = hours[today];
    if (todayHours) {
      return `Today: ${todayHours.open} - ${todayHours.close}`;
    }
    return 'See website for hours';
  }

  hasOpeningHours(hours: any): boolean {
    return hours && Object.keys(hours).length > 0;
  }
}
