import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { AdminService, AdminUser } from '../../core/services/admin.service';

@Component({
  selector: 'app-admin-users',
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
        <div class="admin-users">
          <div class="page-header">
            <h1>User Management</h1>
          </div>

          <div class="filters">
            <input 
              type="text" 
              placeholder="Search by name or email..." 
              [(ngModel)]="searchTerm"
              (input)="onSearch()"
              class="search-input">
            
            <select [(ngModel)]="roleFilter" (change)="onFilterChange()" class="filter-select">
              <option value="">All Roles</option>
              <option value="user">User</option>
              <option value="super_admin">Super Admin</option>
              <option value="content_admin">Content Admin</option>
              <option value="support_admin">Support Admin</option>
            </select>
          </div>

          @if (loading()) {
            <div class="loading">Loading users...</div>
          } @else {
            <div class="table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Registered</th>
                    <th>Last Login</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  @for (user of users(); track user.id) {
                    <tr>
                      <td>{{ user.firstName }} {{ user.lastName }}</td>
                      <td>{{ user.email }}</td>
                      <td>
                        <span class="role-badge" [class]="'role-' + user.role">
                          {{ user.role }}
                        </span>
                      </td>
                      <td>{{ formatDate(user.createdAt) }}</td>
                      <td>{{ user.lastLogin ? formatDate(user.lastLogin) : 'Never' }}</td>
                      <td>
                        <button class="btn-small" (click)="viewUser(user)">View</button>
                        <button class="btn-small" (click)="changeRole(user)">Change Role</button>
                      </td>
                    </tr>
                  }
                </tbody>
              </table>
            </div>

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

          @if (selectedUser()) {
            <div class="modal-overlay" (click)="closeModal()">
              <div class="modal" (click)="$event.stopPropagation()">
                <h2>Change User Role</h2>
                <p>User: {{ selectedUser()!.firstName }} {{ selectedUser()!.lastName }}</p>
                <p>Current Role: {{ selectedUser()!.role }}</p>
                
                <select [(ngModel)]="newRole" class="role-select">
                  <option value="user">User</option>
                  <option value="super_admin">Super Admin</option>
                  <option value="content_admin">Content Admin</option>
                  <option value="support_admin">Support Admin</option>
                  <option value="read_only">Read Only</option>
                </select>

                <div class="modal-actions">
                  <button class="btn-secondary" (click)="closeModal()">Cancel</button>
                  <button class="btn-primary" (click)="confirmRoleChange()">Update Role</button>
                </div>
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

    .admin-users {
      max-width: 1400px;
      margin: 0 auto;
    }

    .page-header h1 {
      margin: 0 0 2rem 0;
      font-size: 2rem;
      color: #1a1a1a;
    }

    .filters {
      display: flex;
      gap: 1rem;
      margin-bottom: 2rem;
    }

    .search-input {
      flex: 1;
      padding: 0.75rem;
      border: 1px solid #ddd;
      border-radius: 4px;
      font-size: 1rem;
    }

    .filter-select {
      padding: 0.75rem;
      border: 1px solid #ddd;
      border-radius: 4px;
      font-size: 1rem;
      min-width: 200px;
    }

    .table-container {
      background: white;
      border-radius: 8px;
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
    }

    .data-table td {
      padding: 1rem;
      border-bottom: 1px solid #e5e7eb;
    }

    .data-table tr:hover {
      background: #f9fafb;
    }

    .role-badge {
      padding: 0.25rem 0.75rem;
      border-radius: 12px;
      font-size: 0.875rem;
      font-weight: 600;
    }

    .role-user {
      background: #dbeafe;
      color: #1e40af;
    }

    .role-super_admin {
      background: #fce7f3;
      color: #9f1239;
    }

    .role-content_admin {
      background: #dcfce7;
      color: #166534;
    }

    .role-support_admin {
      background: #fef3c7;
      color: #92400e;
    }

    .btn-small {
      padding: 0.375rem 0.75rem;
      margin-right: 0.5rem;
      border: 1px solid #ddd;
      background: white;
      border-radius: 4px;
      cursor: pointer;
      font-size: 0.875rem;
    }

    .btn-small:hover {
      background: #f5f5f5;
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
      border-radius: 4px;
      cursor: pointer;
    }

    .pagination button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
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
      border-radius: 8px;
      max-width: 500px;
      width: 90%;
    }

    .modal h2 {
      margin-top: 0;
    }

    .role-select {
      width: 100%;
      padding: 0.75rem;
      border: 1px solid #ddd;
      border-radius: 4px;
      margin: 1rem 0;
    }

    .modal-actions {
      display: flex;
      gap: 1rem;
      justify-content: flex-end;
      margin-top: 1.5rem;
    }

    .btn-primary, .btn-secondary {
      padding: 0.75rem 1.5rem;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-weight: 600;
    }

    .btn-primary {
      background: #2563eb;
      color: white;
    }

    .btn-secondary {
      background: #e5e7eb;
      color: #374151;
    }

    .loading {
      text-align: center;
      padding: 3rem;
      color: #666;
    }
  `]
})
export class AdminUsersComponent implements OnInit {
  users = signal<AdminUser[]>([]);
  loading = signal(true);
  currentPage = signal(1);
  totalPages = signal(1);
  searchTerm = '';
  roleFilter = '';
  selectedUser = signal<AdminUser | null>(null);
  newRole = '';

  constructor(private adminService: AdminService) {}

  ngOnInit() {
    this.loadUsers();
  }

  loadUsers() {
    this.loading.set(true);
    const filters: any = {};
    if (this.searchTerm) filters.search = this.searchTerm;
    if (this.roleFilter) filters.role = this.roleFilter;

    this.adminService.getUsers(this.currentPage(), 20, filters).subscribe({
      next: (response: any) => {
        this.users.set(response.users);
        this.totalPages.set(response.pagination.totalPages);
        this.loading.set(false);
      },
      error: (error) => {
        console.error('Failed to load users:', error);
        this.loading.set(false);
      }
    });
  }

  onSearch() {
    this.currentPage.set(1);
    this.loadUsers();
  }

  onFilterChange() {
    this.currentPage.set(1);
    this.loadUsers();
  }

  goToPage(page: number) {
    this.currentPage.set(page);
    this.loadUsers();
  }

  viewUser(user: AdminUser) {
    // Navigate to user detail or show modal
    console.log('View user:', user);
  }

  changeRole(user: AdminUser) {
    this.selectedUser.set(user);
    this.newRole = user.role;
  }

  closeModal() {
    this.selectedUser.set(null);
  }

  confirmRoleChange() {
    const user = this.selectedUser();
    if (!user) return;

    this.adminService.updateUserRole(user.id, this.newRole).subscribe({
      next: () => {
        this.closeModal();
        this.loadUsers();
      },
      error: (error) => {
        console.error('Failed to update role:', error);
        alert('Failed to update user role');
      }
    });
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString();
  }
}
