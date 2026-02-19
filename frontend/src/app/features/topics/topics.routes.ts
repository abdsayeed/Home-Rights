import { Routes } from '@angular/router';

export const TOPICS_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./topics-list.component').then(m => m.TopicsListComponent)
  }
];
