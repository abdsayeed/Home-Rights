import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const adminGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  const user = authService.currentUser();
  const isAdmin = user?.role === 'super_admin' || 
                  user?.role === 'content_admin' || 
                  user?.role === 'support_admin' || 
                  user?.role === 'read_only';

  if (!isAdmin) {
    router.navigate(['/dashboard']);
    return false;
  }

  return true;
};
