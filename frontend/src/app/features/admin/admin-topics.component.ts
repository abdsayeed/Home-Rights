import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { AdminService, AdminTopic } from '../../core/services/admin.service';

@Component({
  selector: 'app-admin-topics',
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
        <div class="admin-topics">
          <div class="page-header">
            <h1>Topics Management</h1>
            <button class="btn-primary" (click)="openCreateModal()">
              <span>+</span> Create Topic
            </button>
          </div>

          <div class="filters">
            <select [(ngModel)]="categoryFilter" (change)="onFilterChange()" class="filter-select">
              <option value="">All Categories</option>
              <option value="eviction">Eviction</option>
              <option value="deposits">Deposits</option>
              <option value="repairs">Repairs</option>
              <option value="rent">Rent</option>
              <option value="rights">Rights</option>
            </select>
            
            <select [(ngModel)]="publishedFilter" (change)="onFilterChange()" class="filter-select">
              <option value="">All Status</option>
              <option value="true">Published</option>
              <option value="false">Draft</option>
            </select>
          </div>

          @if (loading()) {
            <div class="loading">
              <div class="spinner"></div>
              <p>Loading topics...</p>
            </div>
          } @else if (error()) {
            <div class="error-state">
              <p>{{ error() }}</p>
              <button (click)="loadTopics()" class="btn-primary">Retry</button>
            </div>
          } @else {
            <div class="table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Title</th>
                    <th>Category</th>
                    <th>Status</th>
                    <th>Views</th>
                    <th>Last Updated</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  @for (topic of topics(); track topic.id) {
                    <tr>
                      <td>
                        <div class="topic-title">{{ topic.title }}</div>
                        <div class="topic-slug">/{{ topic.slug }}</div>
                      </td>
                      <td>
                        <span class="category-badge">{{ topic.category }}</span>
                      </td>
                      <td>
                        <span class="status-badge" [class.published]="topic.published" [class.draft]="!topic.published">
                          {{ topic.published ? 'Published' : 'Draft' }}
                        </span>
                      </td>
                      <td>{{ topic.views }}</td>
                      <td>{{ formatDate(topic.lastUpdated) }}</td>
                      <td>
                        <button class="btn-small" (click)="editTopic(topic)">Edit</button>
                        <button class="btn-small btn-danger" (click)="deleteTopic(topic)">Delete</button>
                      </td>
                    </tr>
                  } @empty {
                    <tr>
                      <td colspan="6" class="empty-state">No topics found</td>
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
                <h2>{{ editingTopic() ? 'Edit Topic' : 'Create Topic' }}</h2>
                
                <form (ngSubmit)="saveTopic()">
                  <div class="form-group">
                    <label>Title *</label>
                    <input type="text" [(ngModel)]="formData.title" name="title" required class="form-input">
                  </div>

                  <div class="form-group">
                    <label>Slug *</label>
                    <input type="text" [(ngModel)]="formData.slug" name="slug" required class="form-input">
                    <small>URL-friendly version (e.g., section-21-notice)</small>
                  </div>

                  <div class="form-row">
                    <div class="form-group">
                      <label>Category *</label>
                      <select [(ngModel)]="formData.category" name="category" required class="form-input">
                        <option value="eviction">Eviction</option>
                        <option value="deposits">Deposits</option>
                        <option value="repairs">Repairs</option>
                        <option value="rent">Rent</option>
                        <option value="rights">Rights</option>
                      </select>
                    </div>

                    <div class="form-group">
                      <label>Status</label>
                      <select [(ngModel)]="formData.published" name="published" class="form-input">
                        <option [ngValue]="false">Draft</option>
                        <option [ngValue]="true">Published</option>
                      </select>
                    </div>
                  </div>

                  <div class="form-group">
                    <label>Summary *</label>
                    <textarea [(ngModel)]="formData.summary" name="summary" required rows="3" class="form-input"></textarea>
                  </div>

                  <div class="form-group">
                    <label>Body Content *</label>
                    <textarea [(ngModel)]="formData.body" name="body" required rows="10" class="form-input"></textarea>
                  </div>

                  <div class="form-group">
                    <label>Tags (comma-separated)</label>
                    <input type="text" [(ngModel)]="tagsInput" name="tags" class="form-input" placeholder="eviction, section 21, notice">
                  </div>

                  <div class="modal-actions">
                    <button type="button" class="btn-secondary" (click)="closeModal()">Cancel</button>
                    <button type="submit" class="btn-primary" [disabled]="saving()">
                      {{ saving() ? 'Saving...' : 'Save Topic' }}
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

    .admin-topics {
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

    .topic-title {
      font-weight: 600;
      color: #1a1a1a;
      margin-bottom: 0.25rem;
    }

    .topic-slug {
      font-size: 0.875rem;
      color: #6b7280;
      font-family: monospace;
    }

    .category-badge {
      padding: 0.25rem 0.75rem;
      border-radius: 12px;
      font-size: 0.875rem;
      font-weight: 600;
      background: #e0e7ff;
      color: #3730a3;
      text-transform: capitalize;
    }

    .status-badge {
      padding: 0.25rem 0.75rem;
      border-radius: 12px;
      font-size: 0.875rem;
      font-weight: 600;
    }

    .status-badge.published {
      background: #dcfce7;
      color: #166534;
    }

    .status-badge.draft {
      background: #fef3c7;
      color: #92400e;
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

    .form-group small {
      display: block;
      margin-top: 0.25rem;
      color: #6b7280;
      font-size: 0.875rem;
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
      min-height: 100px;
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
export class AdminTopicsComponent implements OnInit {
  topics = signal<AdminTopic[]>([]);
  loading = signal(true);
  error = signal<string | null>(null);
  currentPage = signal(1);
  totalPages = signal(1);
  categoryFilter = '';
  publishedFilter = '';
  
  showModal = signal(false);
  editingTopic = signal<AdminTopic | null>(null);
  saving = signal(false);
  
  formData: any = {
    title: '',
    slug: '',
    category: 'eviction',
    summary: '',
    body: '',
    published: false
  };
  tagsInput = '';

  constructor(private adminService: AdminService) {}

  ngOnInit() {
    this.loadTopics();
  }

  loadTopics() {
    this.loading.set(true);
    this.error.set(null);
    
    const filters: any = {};
    if (this.categoryFilter) filters.category = this.categoryFilter;
    if (this.publishedFilter) filters.published = this.publishedFilter;

    this.adminService.getTopics(this.currentPage(), 20, filters).subscribe({
      next: (response: any) => {
        this.topics.set(response.data);
        this.totalPages.set(response.pagination.totalPages);
        this.loading.set(false);
      },
      error: (err) => {
        console.error('Failed to load topics:', err);
        this.error.set('Failed to load topics. Please try again.');
        this.loading.set(false);
      }
    });
  }

  onFilterChange() {
    this.currentPage.set(1);
    this.loadTopics();
  }

  goToPage(page: number) {
    this.currentPage.set(page);
    this.loadTopics();
  }

  openCreateModal() {
    this.editingTopic.set(null);
    this.formData = {
      title: '',
      slug: '',
      category: 'eviction',
      summary: '',
      body: '',
      published: false
    };
    this.tagsInput = '';
    this.showModal.set(true);
  }

  editTopic(topic: AdminTopic) {
    this.editingTopic.set(topic);
    this.formData = {
      title: topic.title,
      slug: topic.slug,
      category: topic.category,
      summary: '', // Would need to fetch full topic details
      body: '',
      published: topic.published
    };
    this.tagsInput = '';
    this.showModal.set(true);
  }

  closeModal() {
    this.showModal.set(false);
    this.editingTopic.set(null);
  }

  saveTopic() {
    this.saving.set(true);
    
    const topicData = {
      ...this.formData,
      tags: this.tagsInput.split(',').map(t => t.trim()).filter(t => t)
    };

    const request = this.editingTopic()
      ? this.adminService.updateTopic(this.editingTopic()!.id, topicData)
      : this.adminService.createTopic(topicData);

    request.subscribe({
      next: () => {
        this.saving.set(false);
        this.closeModal();
        this.loadTopics();
      },
      error: (err) => {
        console.error('Failed to save topic:', err);
        alert('Failed to save topic: ' + (err.error?.error || 'Unknown error'));
        this.saving.set(false);
      }
    });
  }

  deleteTopic(topic: AdminTopic) {
    if (!confirm(`Are you sure you want to delete "${topic.title}"?`)) {
      return;
    }

    this.adminService.deleteTopic(topic.id).subscribe({
      next: () => {
        this.loadTopics();
      },
      error: (err) => {
        console.error('Failed to delete topic:', err);
        alert('Failed to delete topic');
      }
    });
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString();
  }
}
