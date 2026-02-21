import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../../../environments/environment';

export interface DashboardOverview {
  users: {
    total: number;
    new: number;
    active: number;
  };
  documents: {
    total: number;
    new: number;
  };
  topics: {
    total: number;
    views: number;
  };
  support: {
    total: number;
    verified: number;
  };
  chat: {
    total: number;
    new: number;
  };
  period: string;
}

export interface AdminUser {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: string;
  createdAt: string;
  lastLogin: string | null;
}

export interface AdminTopic {
  id: string;
  title: string;
  slug: string;
  category: string;
  published: boolean;
  views: number;
  createdAt: string;
  lastUpdated: string;
}

export interface AdminOrganization {
  id: string;
  name: string;
  type: string;
  verificationStatus: string;
  lastVerifiedAt: string | null;
  isAcceptingReferrals: boolean;
  createdAt: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    total: number;
    page: number;
    limit: number;
    totalPages: number;
  };
}

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private apiUrl = `${environment.apiUrl}/admin`;

  constructor(private http: HttpClient) {}

  // Dashboard
  getDashboardOverview(period: string = '7d'): Observable<DashboardOverview> {
    return this.http.get<DashboardOverview>(`${this.apiUrl}/dashboard/overview?period=${period}`);
  }

  // Users
  getUsers(page: number = 1, limit: number = 20, filters?: any): Observable<any> {
    let url = `${this.apiUrl}/users?page=${page}&limit=${limit}`;
    if (filters?.role) url += `&role=${filters.role}`;
    if (filters?.search) url += `&search=${encodeURIComponent(filters.search)}`;
    
    return this.http.get<any>(url);
  }

  getUserDetail(userId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/users/${userId}`);
  }

  updateUserRole(userId: string, role: string): Observable<any> {
    return this.http.patch(`${this.apiUrl}/users/${userId}/role`, { role });
  }

  // Topics
  getTopics(page: number = 1, limit: number = 20, filters?: any): Observable<PaginatedResponse<AdminTopic>> {
    let url = `${this.apiUrl}/topics?page=${page}&limit=${limit}`;
    if (filters?.category) url += `&category=${filters.category}`;
    if (filters?.published !== undefined) url += `&published=${filters.published}`;
    
    return this.http.get<any>(url).pipe(
      map((response: any) => ({
        data: response.topics,
        pagination: response.pagination
      }))
    );
  }

  createTopic(topic: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/topics`, topic);
  }

  updateTopic(topicId: string, topic: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/topics/${topicId}`, topic);
  }

  deleteTopic(topicId: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/topics/${topicId}`);
  }

  // Support Organizations
  getOrganizations(page: number = 1, limit: number = 20, filters?: any): Observable<PaginatedResponse<AdminOrganization>> {
    let url = `${this.apiUrl}/support?page=${page}&limit=${limit}`;
    if (filters?.type) url += `&type=${filters.type}`;
    if (filters?.verificationStatus) url += `&verificationStatus=${filters.verificationStatus}`;
    
    return this.http.get<any>(url).pipe(
      map((response: any) => ({
        data: response.organizations,
        pagination: response.pagination
      }))
    );
  }

  createOrganization(org: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/support`, org);
  }

  updateOrganization(orgId: string, org: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/support/${orgId}`, org);
  }

  verifyOrganization(orgId: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/support/${orgId}/verify`, {});
  }

  deleteOrganization(orgId: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/support/${orgId}`);
  }

  // Audit Logs
  getAuditLogs(page: number = 1, limit: number = 50, filters?: any): Observable<any> {
    let url = `${this.apiUrl}/audit-logs?page=${page}&limit=${limit}`;
    if (filters?.adminId) url += `&adminId=${filters.adminId}`;
    if (filters?.action) url += `&action=${encodeURIComponent(filters.action)}`;
    
    return this.http.get(url);
  }
}
