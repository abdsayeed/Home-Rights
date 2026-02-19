import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/chat',
    pathMatch: 'full'
  },
  {
    path: 'auth',
    loadChildren: () => import('./features/auth/auth.routes').then(m => m.AUTH_ROUTES)
  },
  {
    path: 'chat',
    loadComponent: () => import('./features/chat/chat.component').then(m => m.ChatComponent),
    canActivate: [authGuard]
  },
  {
    path: 'topics',
    loadChildren: () => import('./features/topics/topics.routes').then(m => m.TOPICS_ROUTES),
    canActivate: [authGuard]
  },
  {
    path: 'documents',
    loadComponent: () => import('./features/document-upload/upload.component').then(m => m.UploadComponent),
    canActivate: [authGuard]
  },
  {
    path: 'support',
    loadComponent: () => import('./features/support/support-finder.component').then(m => m.SupportFinderComponent),
    canActivate: [authGuard]
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent),
    canActivate: [authGuard]
  },
  {
    path: '**',
    redirectTo: '/chat'
  }
];
