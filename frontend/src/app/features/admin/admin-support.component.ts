import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { AdminService, AdminOrganization } from '../../core/services/admin.service';

@Component({
  selector: 'app-admin-support',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  template: `
    <div class="admin-container">
      <aside class="admin-sidebar">
        <div class="sidebar-header">
          <div class="admin-badge">
            <span class="badge-icon">⚙️</span>
            <span class="badge-text">Admin Panel</span>
          </div>
        </div>
        
        <nav class="sidebar-nav">
          <a routerLink="/admin" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}" class="nav-item">
            <span class="nav-icon">📊</span>
            <span class="nav-label">Dashboard</span>
          </a>
          <a routerLink="/admin/users" routerLinkActive="active" class="nav-item">
            <span class="nav-icon">👥</span>
            <span class="nav-label">Users</span>
          </a>
          <a routerLink="/admin/topics" routerLinkActive="active" class="nav-item">
            <span class="nav-icon">📚</span>
            <span class="nav-label">Topics</span>
          </a>
          <a routerLink="/admin/support" routerLinkActive="active" class="nav-item">
            <span class="nav-icon">🏢</span>
            <span class="nav-label">Organizations</span>
          </a>
        </nav>
        
        <div class="sidebar-footer">
          <a routerLink="/dashboard" class="back-link">
            <span>←</span> Back to App
          </a>
        </div>
      </aside>

      <main class="admin-main">
        <div class="admin-support">
          <div class="page-header">
            <h1>Organizations Management</h1>
            <button class="btn-primary" (click)="openCreateModal()">
              <span>+</span> Add Organization
            </button>
          </div>

          <div class="filters">
            <select [(ngModel)]="typeFilter" (change)="onFilterChange()" class="filter-select">
              <option value="">All Types</option>
              <option value="charity">Charity</option>
              <option value="advice_center">Advice Center</option>
              <option value="legal_aid">Legal Aid</option>
              <option value="council">Council</option>
            </select>
            
            <select [(ngModel)]="verificationFilter" (change)="onFilterChange()" class="filter-select">
              <option value="">All Verification Status</option>
              <option value="verified">Verified</option>
              <option value="unverified">Unverified</option>
              <option value="pending">Pending</option>
            </select>
          </div>

          @if (loading()) {
            <div class="loading">
              <div class="spinner"></div>
              <p>Loading organizations...</p>
            </div>
          } @else if (error()) {
            <div class="error-state">
              <p>{{ error() }}</p>
              <button (click)="loadOrganizations()" class="btn-primary">Retry</button>
            </div>
          } @else {
            <div class="table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Verification</th>
                    <th>Last Verified</th>
                    <th>Accepting Referrals</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  @for (org of organizations(); track org.id) {
                    <tr>
                      <td>
                        <div class="org-name">{{ org.name }}</div>
                      </td>
                      <td>
                        <span class="type-badge">{{ formatType(org.type) }}</span>
                      </td>
                      <td>
                        <span class="verification-badge" [class]="'status-' + org.verificationStatus">
                          {{ formatStatus(org.verificationStatus) }}
                        </span>
                      </td>
                      <td>{{ org.lastVerifiedAt ? formatDate(org.lastVerifiedAt) : 'Never' }}</td>
                      <td>
                        <span class="referral-badge" [class.accepting]="org.isAcceptingReferrals" [class.not-accepting]="!org.isAcceptingReferrals">
                          {{ org.isAcceptingReferrals ? 'Yes' : 'No' }}
                        </span>
                      </td>
                      <td>
                        <button class="btn-small" (click)="editOrganization(org)">Edit</button>
                        @if (org.verificationStatus !== 'verified') {
                          <button class="btn-small btn-success" (click)="verifyOrganization(org)">Verify</button>
                        }
                        <button class="btn-small btn-danger" (click)="deleteOrganization(org)">Delete</button>
                      </td>
                    </tr>
                  } @empty {
                    <tr>
                      <td colspan="6" class="empty-state">No organizations found</td>
                    </tr>
                  }
                </tbody>
              </table>
            </div>

            @if (totalPages() > 1) {
              <div class="pagination">
                <button 
                  [disabled]="currentPage() === 1" 
                  (click)="goToPage(currentPage() - 1)">
                  Previous
                </button>
                <span>Page {{ currentPage() }} of {{ totalPages() }}</span>
                <button 
                  [disabled]="currentPage() === totalPages()" 
                  (click)="goToPage(currentPage() + 1)">
                  Next
                </button>
              </div>
            }
          }

          <!-- Create/Edit Modal -->
          @if (showModal()) {
            <div class="modal-overlay" (click)="closeModal()">
              <div class="modal modal-large" (click)="$event.stopPropagation()">
                <h2>{{ editingOrg() ? 'Edit Organization' : 'Add Organization' }}</h2>
                
                <form (ngSubmit)="saveOrganization()">
                  <div class="form-group">
                    <label>Organization Name *</label>
                    <input type="text" [(ngModel)]="formData.name" name="name" required class="form-input">
                  </div>

                  <div class="form-row">
                    <div class="form-group">
                      <label>Type *</label>
                      <select [(ngModel)]="formData.type" name="type" required class="form-input">
                        <option value="charity">Charity</option>
                        <option value="advice_center">Advice Center</option>
                        <option value="legal_aid">Legal Aid</option>
                        <option value="council">Council</option>
                      </select>
                    </div>

                    <div class="form-group">
                      <label>Accepting Referrals</label>
                      <select [(ngModel)]="formData.isAcceptingReferrals" name="isAcceptingReferrals" class="form-input">
                        <option [ngValue]="true">Yes</option>
                        <option [ngValue]="false">No</option>
                      </select>
                    </div>
                  </div>

                  <div class="form-group">
                    <label>Description</label>
                    <textarea [(ngModel)]="formData.description" name="description" rows="3" class="form-input"></textarea>
                  </div>

                  <div class="form-group">
                    <label>Services (comma-separated)</label>
                    <input type="text" [(ngModel)]="servicesInput" name="services" class="form-input" placeholder="Emergency housing, Legal advice">
                  </div>

                  <div class="form-group">
                    <label>Phone</label>
                    <input type="tel" [(ngModel)]="formData.contact.phone" name="phone" class="form-input">
                  </div>

                  <div class="form-group">
                    <label>Email</label>
                    <input type="email" [(ngModel)]="formData.contact.email" name="email" class="form-input">
                  </div>

                  <div class="form-group">
                    <label>Website</label>
                    <input type="url" [(ngModel)]="formData.contact.website" name="website" class="form-input">
                  </div>

                  <div class="form-group">
                    <label>Address</label>
                    <textarea [(ngModel)]="formData.address" name="address" rows="2" class="form-input"></textarea>
                  </div>

                  <div class="modal-actions">
                    <button type="button" class="btn-secondary" (click)="closeModal()">Cancel</button>
                    <button type="submit" class="btn-primary" [disabled]="saving()">
                      {{ saving() ? 'Saving...' : 'Save Organization' }}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          }
        </div>
      </main>
    </div>
  `,
  styles: [`
    .admin-container {
      display: flex;
      min-height: calc(100vh - 64px);
      background: #f8f9fa;
    }

    .admin-sidebar {
      width: 260px;
      background: white;
      border-right: 1px solid #e5e7eb;
      display: flex;
      flex-direction: column;
      position: fixed;
      height: calc(100vh - 64px);
      overflow-y: auto;
    }

    .sidebar-header {
      padding: 1.5rem;
      border-bottom: 1px solid #e5e7eb;
    }

    .admin-badge {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.75rem;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 8px;
      color: white;
    }

    .badge-icon {
      font-size: 1.5rem;
    }

    .badge-text {
      font-weight: 600;
      font-size: 0.95rem;
    }

    .sidebar-nav {
      flex: 1;
      padding: 1rem;
    }

    .nav-item {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.75rem 1rem;
      border-radius: 8px;
      text-decoration: none;
      color: #4b5563;
      transition: all 0.2s;
      margin-bottom: 0.25rem;
    }

    .nav-item:hover {
      background: #f3f4f6;
      color: #1f2937;
    }

    .nav-item.active {
      background: #ede9fe;
      color: #7c3aed;
      font-weight: 600;
    }

    .nav-icon {
      font-size: 1.25rem;
    }

    .nav-label {
      font-size: 0.95rem;
    }

    .sidebar-footer {
      padding: 1rem;
      border-top: 1px solid #e5e7eb;
    }

    .back-link {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.75rem 1rem;
      border-radius: 8px;
      text-decoration: none;
      color: #6b7280;
      font-size: 0.9rem;
      transition: all 0.2s;
    }

    .back-link:hover {
      background: #f3f4f6;
      color: #1f2937;
    }

    .admin-main {
      flex: 1;
      margin-left: 260px;
      padding: 2rem;
    }

    .admin-support {
      max-width: 1400px;
      margin: 0 auto;
    }

    .page-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2rem;
    }

    .page-header h1 {
      margin: 0;
      font-size: 2rem;
      color: #1a1a1a;
    }

    .filters {
      display: flex;
      gap: 1rem;
      margin-bottom: 2rem;
    }

    .filter-select {
      padding: 0.75rem;
      border: 1px solid #ddd;
      border-radius: 8px;
      font-size: 0.95rem;
      background: white;
      min-width: 200px;
    }

    .table-container {
      background: white;
      border-radius: 12px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      overflow-x: auto;
    }

    .data-table {
      width: 100%;
      border-collapse: collapse;
    }

    .data-table th {
      background: #f9fafb;
      padding: 1rem;
      text-align: left;
      font-weight: 600;
      color: #374151;
      border-bottom: 2px solid #e5e7eb;
      font-size: 0.875rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .data-table td {
      padding: 1rem;
      border-bottom: 1px solid #e5e7eb;
    }

    .data-table tr:hover {
      background: #f9fafb;
    }

    .org-name {
      font-weight: 600;
      color: #1a1a1a;
    }

    .type-badge {
      padding: 0.25rem 0.75rem;
      border-radius: 12px;
      font-size: 0.875rem;
      font-weight: 600;
      background: #dbeafe;
      color: #1e40af;
      text-transform: capitalize;
    }

    .verification-badge {
      padding: 0.25rem 0.75rem;
      border-radius: 12px;
      font-size: 0.875rem;
      font-weight: 600;
    }

    .verification-badge.status-verified {
      background: #dcfce7;
      color: #166534;
    }

    .verification-badge.status-unverified {
      background: #fef3c7;
      color: #92400e;
    }

    .verification-badge.status-pending {
      background: #e0e7ff;
      color: #3730a3;
    }

    .referral-badge {
      padding: 0.25rem 0.75rem;
      border-radius: 12px;
      font-size: 0.875rem;
      font-weight: 600;
    }

    .referral-badge.accepting {
      background: #dcfce7;
      color: #166534;
    }

    .referral-badge.not-accepting {
      background: #fee2e2;
      color: #991b1b;
    }

    .btn-small {
      padding: 0.375rem 0.75rem;
      margin-right: 0.5rem;
      border: 1px solid #ddd;
      background: white;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.875rem;
      transition: all 0.2s;
    }

    .btn-small:hover {
      background: #f5f5f5;
    }

    .btn-small.btn-success {
      color: #16a34a;
      border-color: #bbf7d0;
    }

    .btn-small.btn-success:hover {
      background: #dcfce7;
    }

    .btn-small.btn-danger {
      color: #dc2626;
      border-color: #fecaca;
    }

    .btn-small.btn-danger:hover {
      background: #fee2e2;
    }

    .btn-primary {
      padding: 0.75rem 1.5rem;
      border: none;
      background: #7c3aed;
      color: white;
      border-radius: 8px;
      cursor: pointer;
      font-weight: 600;
      font-size: 0.95rem;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .btn-primary:hover {
      background: #6d28d9;
    }

    .btn-primary:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .btn-secondary {
      padding: 0.75rem 1.5rem;
      border: 1px solid #ddd;
      background: white;
      color: #374151;
      border-radius: 8px;
      cursor: pointer;
      font-weight: 600;
    }

    .pagination {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 1rem;
      margin-top: 2rem;
    }

    .pagination button {
      padding: 0.5rem 1rem;
      border: 1px solid #ddd;
      background: white;
      border-radius: 6px;
      cursor: pointer;
    }

    .pagination button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .loading {
      text-align: center;
      padding: 4rem;
      color: #666;
    }

    .spinner {
      width: 40px;
      height: 40px;
      border: 4px solid #f3f4f6;
      border-top-color: #7c3aed;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 1rem;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    .error-state {
      text-align: center;
      padding: 3rem;
      background: white;
      border-radius: 12px;
    }

    .empty-state {
      text-align: center;
      padding: 3rem;
      color: #6b7280;
    }

    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0,0,0,0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }

    .modal {
      background: white;
      padding: 2rem;
      border-radius: 12px;
      max-width: 600px;
      width: 90%;
      max-height: 90vh;
      overflow-y: auto;
    }

    .modal-large {
      max-width: 900px;
    }

    .modal h2 {
      margin-top: 0;
      margin-bottom: 1.5rem;
    }

    .form-group {
      margin-bottom: 1.5rem;
    }

    .form-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
    }

    .form-group label {
      display: block;
      margin-bottom: 0.5rem;
      font-weight: 600;
      color: #374151;
      font-size: 0.95rem;
    }

    .form-input {
      width: 100%;
      padding: 0.75rem;
      border: 1px solid #ddd;
      border-radius: 8px;
      font-size: 0.95rem;
      font-family: inherit;
    }

    .form-input:focus {
      outline: none;
      border-color: #7c3aed;
      box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
    }

    textarea.form-input {
      resize: vertical;
      min-height: 80px;
    }

    .modal-actions {
      display: flex;
      gap: 1rem;
      justify-content: flex-end;
      margin-top: 2rem;
      padding-top: 1.5rem;
      border-top: 1px solid #e5e7eb;
    }

    @media (max-width: 1024px) {
      .admin-sidebar {
        width: 200px;
      }

      .admin-main {
        margin-left: 200px;
      }
    }

    @media (max-width: 768px) {
      .admin-sidebar {
        display: none;
      }

      .admin-main {
        margin-left: 0;
        padding: 1rem;
      }

      .page-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
      }

      .form-row {
        grid-template-columns: 1fr;
      }
    }
  `]
})
export class AdminSupportComponent implements OnInit {
  organizations = signal<AdminOrganization[]>([]);
  loading = signal(true);
  error = signal<string | null>(null);
  currentPage = signal(1);
  totalPages = signal(1);
  typeFilter = '';
  verificationFilter = '';
  
  showModal = signal(false);
  editingOrg = signal<AdminOrganization | null>(null);
  saving = signal(false);
  
  formData: any = {
    name: '',
    type: 'charity',
    description: '',
    contact: {
      phone: '',
      email: '',
      website: ''
    },
    address: '',
    isAcceptingReferrals: true
  };
  servicesInput = '';

  constructor(private adminService: AdminService) {}

  ngOnInit() {
    this.loadOrganizations();
  }

  loadOrganizations() {
    this.loading.set(true);
    this.error.set(null);
    
    const filters: any = {};
    if (this.typeFilter) filters.type = this.typeFilter;
    if (this.verificationFilter) filters.verificationStatus = this.verificationFilter;

    this.adminService.getOrganizations(this.currentPage(), 20, filters).subscribe({
      next: (response: any) => {
        this.organizations.set(response.data);
        this.totalPages.set(response.pagination.totalPages);
        this.loading.set(false);
      },
      error: (err) => {
        console.error('Failed to load organizations:', err);
        this.error.set('Failed to load organizations. Please try again.');
        this.loading.set(false);
      }
    });
  }

  onFilterChange() {
    this.currentPage.set(1);
    this.loadOrganizations();
  }

  goToPage(page: number) {
    this.currentPage.set(page);
    this.loadOrganizations();
  }

  openCreateModal() {
    this.editingOrg.set(null);
    this.formData = {
      name: '',
      type: 'charity',
      description: '',
      contact: {
        phone: '',
        email: '',
        website: ''
      },
      address: '',
      isAcceptingReferrals: true
    };
    this.servicesInput = '';
    this.showModal.set(true);
  }

  editOrganization(org: AdminOrganization) {
    this.editingOrg.set(org);
    this.formData = {
      name: org.name,
      type: org.type,
      description: '',
      contact: {
        phone: '',
        email: '',
        website: ''
      },
      address: '',
      isAcceptingReferrals: org.isAcceptingReferrals
    };
    this.servicesInput = '';
    this.showModal.set(true);
  }

  closeModal() {
    this.showModal.set(false);
    this.editingOrg.set(null);
  }

  saveOrganization() {
    this.saving.set(true);
    
    const orgData = {
      ...this.formData,
      services: this.servicesInput.split(',').map(s => s.trim()).filter(s => s)
    };

    const request = this.editingOrg()
      ? this.adminService.updateOrganization(this.editingOrg()!.id, orgData)
      : this.adminService.createOrganization(orgData);

    request.subscribe({
      next: () => {
        this.saving.set(false);
        this.closeModal();
        this.loadOrganizations();
      },
      error: (err) => {
        console.error('Failed to save organization:', err);
        alert('Failed to save organization: ' + (err.error?.error || 'Unknown error'));
        this.saving.set(false);
      }
    });
  }

  verifyOrganization(org: AdminOrganization) {
    if (!confirm(`Verify "${org.name}"?`)) {
      return;
    }

    this.adminService.verifyOrganization(org.id).subscribe({
      next: () => {
        this.loadOrganizations();
      },
      error: (err) => {
        console.error('Failed to verify organization:', err);
        alert('Failed to verify organization');
      }
    });
  }

  deleteOrganization(org: AdminOrganization) {
    if (!confirm(`Are you sure you want to delete "${org.name}"?`)) {
      return;
    }

    this.adminService.deleteOrganization(org.id).subscribe({
      next: () => {
        this.loadOrganizations();
      },
      error: (err) => {
        console.error('Failed to delete organization:', err);
        alert('Failed to delete organization');
      }
    });
  }

  formatType(type: string): string {
    return type.replace('_', ' ');
  }

  formatStatus(status: string): string {
    return status.charAt(0).toUpperCase() + status.slice(1);
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString();
  }
}
