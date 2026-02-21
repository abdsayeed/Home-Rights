import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AdminService, DashboardOverview } from '../../core/services/admin.service';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="admin-container">
      <!-- Admin Sidebar -->
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
          <a routerLink="/admin/audit-logs" routerLinkActive="active" class="nav-item">
            <span class="nav-icon">📋</span>
            <span class="nav-label">Audit Logs</span>
          </a>
        </nav>
        
        <div class="sidebar-footer">
          <a routerLink="/dashboard" class="back-link">
            <span>←</span> Back to App
          </a>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="admin-main">
        <div class="admin-dashboard">
          <div class="dashboard-header">
            <h1>Dashboard Overview</h1>
            <div class="period-selector">
              <button 
                *ngFor="let p of periods" 
                [class.active]="period() === p.value"
                (click)="setPeriod(p.value)">
                {{ p.label }}
              </button>
            </div>
          </div>

          @if (loading()) {
            <div class="loading">
              <div class="spinner"></div>
              <p>Loading dashboard...</p>
            </div>
          } @else if (error()) {
            <div class="error-state">
              <div class="error-icon">⚠️</div>
              <h3>Failed to load dashboard</h3>
              <p>{{ error() }}</p>
              <button (click)="loadDashboard()" class="btn-primary">Retry</button>
            </div>
          } @else if (overview()) {
            <div class="kpi-grid">
              <div class="kpi-card">
                <div class="kpi-icon">👥</div>
                <div class="kpi-content">
                  <h3>Total Users</h3>
                  <div class="kpi-value">{{ overview()!.users.total }}</div>
                  <div class="kpi-meta">
                    <span class="badge success">+{{ overview()!.users.new }} new</span>
                    <span>{{ overview()!.users.active }} active</span>
                  </div>
                </div>
              </div>

              <div class="kpi-card">
                <div class="kpi-icon">📄</div>
                <div class="kpi-content">
                  <h3>Documents</h3>
                  <div class="kpi-value">{{ overview()!.documents.total }}</div>
                  <div class="kpi-meta">
                    <span class="badge success">+{{ overview()!.documents.new }} new</span>
                  </div>
                </div>
              </div>

              <div class="kpi-card">
                <div class="kpi-icon">📚</div>
                <div class="kpi-content">
                  <h3>Topics</h3>
                  <div class="kpi-value">{{ overview()!.topics.total }}</div>
                  <div class="kpi-meta">
                    <span>{{ overview()!.topics.views }} views</span>
                  </div>
                </div>
              </div>

              <div class="kpi-card">
                <div class="kpi-icon">🏢</div>
                <div class="kpi-content">
                  <h3>Support Orgs</h3>
                  <div class="kpi-value">{{ overview()!.support.total }}</div>
                  <div class="kpi-meta">
                    <span class="badge success">{{ overview()!.support.verified }} verified</span>
                  </div>
                </div>
              </div>

              <div class="kpi-card">
                <div class="kpi-icon">💬</div>
                <div class="kpi-content">
                  <h3>Chat Messages</h3>
                  <div class="kpi-value">{{ overview()!.chat.total }}</div>
                  <div class="kpi-meta">
                    <span class="badge success">+{{ overview()!.chat.new }} new</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="quick-actions">
              <h2>Quick Actions</h2>
              <div class="action-grid">
                <a routerLink="/admin/users" class="action-card">
                  <span class="action-icon">👥</span>
                  <span class="action-label">Manage Users</span>
                  <span class="action-count">{{ overview()!.users.total }}</span>
                </a>
                <a routerLink="/admin/topics" class="action-card">
                  <span class="action-icon">📚</span>
                  <span class="action-label">Manage Topics</span>
                  <span class="action-count">{{ overview()!.topics.total }}</span>
                </a>
                <a routerLink="/admin/support" class="action-card">
                  <span class="action-icon">🏢</span>
                  <span class="action-label">Manage Organizations</span>
                  <span class="action-count">{{ overview()!.support.total }}</span>
                </a>
                <a routerLink="/admin/audit-logs" class="action-card">
                  <span class="action-icon">📋</span>
                  <span class="action-label">View Audit Logs</span>
                  <span class="action-count">Recent</span>
                </a>
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

    .admin-dashboard {
      max-width: 1400px;
      margin: 0 auto;
    }

    .dashboard-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2rem;
    }

    .dashboard-header h1 {
      margin: 0;
      font-size: 2rem;
      color: #1a1a1a;
    }

    .period-selector {
      display: flex;
      gap: 0.5rem;
      background: white;
      padding: 0.25rem;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .period-selector button {
      padding: 0.5rem 1rem;
      border: none;
      background: transparent;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s;
      font-weight: 500;
      color: #6b7280;
    }

    .period-selector button:hover {
      background: #f3f4f6;
      color: #1f2937;
    }

    .period-selector button.active {
      background: #7c3aed;
      color: white;
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
      padding: 4rem;
      background: white;
      border-radius: 12px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .error-icon {
      font-size: 3rem;
      margin-bottom: 1rem;
    }

    .error-state h3 {
      margin: 0 0 0.5rem 0;
      color: #dc2626;
    }

    .error-state p {
      color: #6b7280;
      margin-bottom: 1.5rem;
    }

    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1.5rem;
      margin-bottom: 3rem;
    }

    .kpi-card {
      background: white;
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      display: flex;
      gap: 1rem;
      transition: all 0.2s;
    }

    .kpi-card:hover {
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      transform: translateY(-2px);
    }

    .kpi-icon {
      font-size: 2.5rem;
    }

    .kpi-content {
      flex: 1;
    }

    .kpi-content h3 {
      margin: 0 0 0.5rem 0;
      font-size: 0.875rem;
      color: #666;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .kpi-value {
      font-size: 2rem;
      font-weight: 700;
      color: #1a1a1a;
      margin-bottom: 0.5rem;
    }

    .kpi-meta {
      display: flex;
      gap: 0.75rem;
      font-size: 0.875rem;
      color: #666;
      flex-wrap: wrap;
    }

    .badge {
      padding: 0.25rem 0.5rem;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 600;
    }

    .badge.success {
      background: #dcfce7;
      color: #166534;
    }

    .quick-actions {
      background: white;
      border-radius: 12px;
      padding: 2rem;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .quick-actions h2 {
      margin: 0 0 1.5rem 0;
      font-size: 1.5rem;
      color: #1a1a1a;
    }

    .action-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
    }

    .action-card {
      background: #f9fafb;
      border: 2px solid #e5e7eb;
      border-radius: 12px;
      padding: 1.5rem;
      text-align: center;
      text-decoration: none;
      color: #1a1a1a;
      transition: all 0.2s;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 0.75rem;
    }

    .action-card:hover {
      border-color: #7c3aed;
      transform: translateY(-2px);
      box-shadow: 0 4px 6px rgba(124, 58, 237, 0.1);
    }

    .action-icon {
      font-size: 2rem;
    }

    .action-label {
      font-weight: 600;
      font-size: 0.95rem;
    }

    .action-count {
      font-size: 0.875rem;
      color: #6b7280;
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

      .dashboard-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
      }
    }
  `]
})
export class AdminDashboardComponent implements OnInit {
  overview = signal<DashboardOverview | null>(null);
  loading = signal(true);
  error = signal<string | null>(null);
  period = signal('7d');

  periods = [
    { value: '7d', label: '7 Days' },
    { value: '30d', label: '30 Days' },
    { value: '90d', label: '90 Days' }
  ];

  constructor(private adminService: AdminService) {}

  ngOnInit() {
    this.loadDashboard();
  }

  setPeriod(period: string) {
    this.period.set(period);
    this.loadDashboard();
  }

  loadDashboard() {
    this.loading.set(true);
    this.error.set(null);
    
    this.adminService.getDashboardOverview(this.period()).subscribe({
      next: (data) => {
        this.overview.set(data);
        this.loading.set(false);
      },
      error: (err) => {
        console.error('Failed to load dashboard:', err);
        this.error.set(err.error?.error || 'Failed to load dashboard data. Please try again.');
        this.loading.set(false);
      }
    });
  }
}
