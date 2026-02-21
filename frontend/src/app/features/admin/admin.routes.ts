import { Routes } from '@angular/router';
import { authGuard } from '../../core/guards/auth.guard';
import { adminGuard } from '../../core/guards/admin.guard';

export const adminRoutes: Routes = [
  {
    path: '',
    canActivate: [authGuard, adminGuard],
    children: [
      {
        path: '',
        loadComponent: () => import('./admin-dashboard.component').then(m => m.AdminDashboardComponent)
      },
      {
        path: 'users',
        loadComponent: () => import('./admin-users.component').then(m => m.AdminUsersComponent)
      },
      {
        path: 'topics',
        loadComponent: () => import('./admin-topics.component').then(m => m.AdminTopicsComponent)
      },
      {
        path: 'support',
        loadComponent: () => import('./admin-support.component').then(m => m.AdminSupportComponent)
      }
    ]
  }
];
